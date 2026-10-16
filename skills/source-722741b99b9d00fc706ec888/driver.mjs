#!/usr/bin/env node
/**
 * Smoke-drives vscode-extension-builder end to end:
 * scaffold -> npm install -> compile -> vsce package -> (optional) code install.
 *
 * Usage:
 *   node driver.mjs [--type command|theme|snippets] [--keep] [--install] [--uninstall-after]
 *
 * Exit code is non-zero if any stage fails. Prints a PASS/FAIL line per stage.
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..', '..');
const GENERATOR = path.join(REPO_ROOT, 'skills', 'vscode-extension-builder', 'scripts', 'create-extension.js');

function parseArgs(argv) {
	const out = { type: 'command', keep: false, install: false, uninstallAfter: false };
	for (const arg of argv) {
		if (arg === '--keep') out.keep = true;
		else if (arg === '--install') out.install = true;
		else if (arg === '--uninstall-after') out.uninstallAfter = true;
		else if (arg.startsWith('--type=')) out.type = arg.slice('--type='.length);
		else if (arg === '--type') out.type = 'NEXT';
		else if (out.type === 'NEXT') out.type = arg;
	}
	return out;
}

const args = parseArgs(process.argv.slice(2));
if (!['command', 'theme', 'snippets'].includes(args.type)) {
	console.error(`--type must be one of command | theme | snippets (got "${args.type}")`);
	process.exit(1);
}

const stamp = Date.now();
const name = `smoke-${args.type}-${stamp}`;
const outDir = path.join(fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'vscode-ext-smoke-')), name);

const results = [];
function stage(label, fn) {
	process.stdout.write(`\n=== ${label} ===\n`);
	const res = fn();
	const ok = res === true || (res && res.status === 0);
	results.push({ label, ok });
	process.stdout.write(`${ok ? 'PASS' : 'FAIL'}: ${label}\n`);
	if (!ok) {
		process.stdout.write(`\nSmoke test aborted at: ${label}\n`);
		summarizeAndExit();
	}
	return res;
}

function run(cmd, cmdArgs, opts = {}) {
	// Only npm/npx/code need a shell on Windows (they resolve to .cmd shims);
	// `node` must run without shell:true or paths containing spaces get
	// mis-tokenized by cmd.exe's argument passing.
	const needsShell = process.platform === 'win32' && cmd !== 'node';
	const res = spawnSync(cmd, cmdArgs, { stdio: 'inherit', shell: needsShell, ...opts });
	return res;
}

function summarizeAndExit() {
	process.stdout.write('\n--- Summary ---\n');
	for (const r of results) process.stdout.write(`${r.ok ? 'PASS' : 'FAIL'}  ${r.label}\n`);
	const failed = results.some((r) => !r.ok);
	if (!args.keep && fs.existsSync(outDir)) {
		fs.rmSync(outDir, { recursive: true, force: true });
	} else if (args.keep) {
		process.stdout.write(`\nKept output at: ${outDir}\n`);
	}
	process.exit(failed ? 1 : 0);
}

process.stdout.write(`Driving vscode-extension-builder (type=${args.type}) at: ${outDir}\n`);

stage('scaffold (create-extension.js)', () =>
	run('node', [
		GENERATOR,
		'--name', name,
		'--displayName', `Smoke ${args.type}`,
		'--description', 'Driver smoke test extension',
		'--publisher', 'local-dev',
		'--type', args.type,
		'--dir', outDir,
	])
);

const pkgJsonPath = path.join(outDir, 'package.json');
stage('scaffold output sanity (package.json exists)', () => fs.existsSync(pkgJsonPath));

if (args.type === 'command') {
	stage('npm install', () => run('npm', ['install'], { cwd: outDir }));
	stage('npm run compile', () => run('npm', ['run', 'compile'], { cwd: outDir }));
	stage('compiled output exists (out/extension.js)', () => fs.existsSync(path.join(outDir, 'out', 'extension.js')));
	stage('vsce package', () => run('npx', ['--yes', '@vscode/vsce', 'package', '--allow-missing-repository'], { cwd: outDir }));

	const vsix = fs.readdirSync(outDir).find((f) => f.endsWith('.vsix'));
	stage('vsix produced', () => Boolean(vsix));

	if (args.install && vsix) {
		const vsixPath = path.join(outDir, vsix);
		const codeCheck = run('code', ['--version']);
		if (codeCheck.status === 0) {
			stage('code --install-extension', () => run('code', ['--install-extension', vsixPath]));
			stage('extension appears in --list-extensions', () => {
				const res = spawnSync('code', ['--list-extensions'], { encoding: 'utf8', shell: process.platform === 'win32' });
				return res.stdout.toLowerCase().includes(`local-dev.${name}`.toLowerCase());
			});
			if (args.uninstallAfter) {
				stage('code --uninstall-extension (cleanup)', () => run('code', ['--uninstall-extension', `local-dev.${name}`]));
			}
		} else {
			process.stdout.write('code CLI not on PATH — skipping install stages.\n');
		}
	}
} else {
	// theme / snippets: no compile step, just confirm the type-specific asset landed.
	const assetDir = args.type === 'theme' ? 'themes' : 'snippets';
	stage(`${assetDir}/ asset dir exists`, () => fs.existsSync(path.join(outDir, assetDir)) && fs.readdirSync(path.join(outDir, assetDir)).length > 0);
}

summarizeAndExit();
