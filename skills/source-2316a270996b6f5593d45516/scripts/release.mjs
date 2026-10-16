#!/usr/bin/env node
// The deterministic half of the release-installer skill; SKILL.md says when to run each command.
// `check`, `smoke`, `watch` and `verify` exit 1 when a check fails, and every command exits 2 when it
// can't reach npm, GitHub or origin: an unanswered lookup is never read as "absent".
import { execFileSync, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const NAME = '@postman/postman-plugin',
    GALLERY = `https://pi.dev/packages/${NAME}`,
    // release.yml's own tag pattern and dist-tag allowlist, so a version passing here passes there.
    VERSION_PATTERN = /^[0-9]+\.[0-9]+\.[0-9]+(-([A-Za-z0-9-]+)[A-Za-z0-9.-]*)?$/,
    SEMVER = 'semver@7.8.5',
    // Everything the tarball ships or builds from; a change elsewhere reaches no user.
    SHIPPED = ['installer', 'skills', 'hooks/session-start-context.md', 'mcp.pi.json', 'README.md', 'LICENSE'],
    USAGE = 'usage: release.mjs status | suggest <rc|latest> [patch|minor|major] | check <version> [commit]' +
        ' | bump <version> | smoke <commit> [--minutes N] | watch <version> [--minutes N] [--new-run] | verify <version>',
    root = execFileSync('git', ['rev-parse', '--show-toplevel'], { encoding: 'utf8' }).trim();

function sh (command, args, options = {}) {
    const result = spawnSync(command, args, { cwd: root, encoding: 'utf8', ...options });

    return { code: result.status ?? 1, out: (result.stdout || '').trim(), err: (result.stderr || '').trim() };
}

const firstLine = (text) => text.split('\n')[0] || 'no output',
    tagOf = (version) => `${NAME}@${version}`;

function distTagOf (version) {
    const match = version.match(VERSION_PATTERN);

    if (!match) {
        return null;
    }

    const prerelease = match[2];

    if (!prerelease) {
        return 'latest';
    }

    if (/^(rc|next|[0-9]+)$/.test(prerelease)) {
        return 'next';
    }

    return /^(alpha|beta|canary)$/.test(prerelease) ? prerelease : null;
}

function distTags (online = false) {
    const { code, out, err } = sh('npm', ['view', NAME, 'dist-tags', '--json', ...(online ? ['--prefer-online'] : [])]);

    if (code !== 0 || !out) {
        throw new Error(`could not read ${NAME}'s dist-tags from npm: ${firstLine(err)}`);
    }

    return JSON.parse(out);
}

/** True when npm has the version, false when npm says it doesn't (E404); throws on any other answer. */
function onNpm (version, online = false) {
    const { code, out, err } = sh('npm', ['view', `${NAME}@${version}`, 'version', ...(online ? ['--prefer-online'] : [])]);

    if (code === 0) {
        return out === version;
    }

    if (/\bE404\b/.test(err)) {
        return false;
    }

    throw new Error(`could not ask npm about ${NAME}@${version}: ${firstLine(err)}`);
}

function onOrigin (tag) {
    const { code, out, err } = sh('git', ['ls-remote', '--tags', 'origin', `refs/tags/${tag}`]);

    if (code !== 0) {
        throw new Error(`could not list origin's tags: ${firstLine(err)}`);
    }

    return Boolean(out);
}

function fetchOrigin () {
    const { code, err } = sh('git', ['fetch', '--quiet', '--tags', 'origin']);

    if (code !== 0) {
        throw new Error(`could not fetch origin: ${firstLine(err)}`);
    }
}

function parse (version) {
    const match = version?.match(/^(\d+)\.(\d+)\.(\d+)(?:-rc\.(\d+))?$/);

    return match ? { major: +match[1], minor: +match[2], patch: +match[3], rc: match[4] === undefined ? null : +match[4] } : null;
}

const base = ({ major, minor, patch }) => `${major}.${minor}.${patch}`;

/** Compares the major.minor.patch of two versions. */
function compareBase (a, b) {
    const [x, y] = [parse(a), parse(b)];

    return x.major - y.major || x.minor - y.minor || x.patch - y.patch;
}

function increment (version, level) {
    const { major, minor, patch } = parse(version);

    return { major: `${major + 1}.0.0`, minor: `${major}.${minor + 1}.0`, patch: `${major}.${minor}.${patch + 1}` }[level];
}

/** True when `version` is newer than `than`, by the same semver release.yml runs. */
function newer (version, than) {
    const { code, err } = sh('npx', ['-y', SEMVER, '--include-prerelease', '--range', `>${than}`, version]);

    if (code !== 0 && err) {
        throw new Error(`could not run ${SEMVER}: ${firstLine(err)}`);
    }

    return code === 0;
}

function status () {
    fetchOrigin();

    const tags = distTags(),
        baseline = tagOf(tags.latest);

    // npm's latest is the baseline: a local tag that was never published says nothing about users.
    if (sh('git', ['rev-parse', '--quiet', '--verify', `refs/tags/${baseline}`]).code !== 0) {
        throw new Error(`npm's latest is ${tags.latest}, but origin has no tag ${baseline}`);
    }

    const changes = sh('git', ['log', '--oneline', '--no-merges', `${baseline}..origin/main`, '--', ...SHIPPED]).out;

    console.log(`npm dist-tags: ${JSON.stringify(tags)}`);
    console.log(`changes to shipped files on origin/main since ${baseline}:`);
    console.log(changes ? changes.replace(/^/gm, '  ') : '  none');
}

function suggest (kind, level) {
    if (!['rc', 'latest'].includes(kind) || (level && !['patch', 'minor', 'major'].includes(level))) {
        throw new Error('usage: suggest <rc|latest> [patch|minor|major]');
    }

    const { latest, next } = distTags();

    if (parse(latest)?.rc !== null) {
        throw new Error(`npm's latest is ${latest}, not a plain version`);
    }

    const line = parse(next),
        // An open rc line is one whose base is newer than latest; it continues until promoted.
        openLine = line && line.rc !== null && compareBase(base(line), latest) > 0 ? line : null;

    if (kind === 'latest') {
        console.log(openLine && !level ? base(openLine) : increment(latest, level || 'patch'));

        return;
    }

    if (openLine && !level) {
        console.log(`${base(openLine)}-rc.${openLine.rc + 1}`);

        return;
    }

    // A new line has to start above an open one, or its rc.0 is already taken.
    let start = increment(latest, level || 'patch');

    if (openLine && compareBase(start, base(openLine)) <= 0) {
        start = increment(base(openLine), level || 'patch');
    }

    console.log(`${start}-rc.0`);
}

/** The problems with `commit` as the release commit for `version`: it must carry the version in all three files. */
function commitProblems (version, commit) {
    const read = (file) => {
        const { code, out, err } = sh('git', ['show', `${commit}:${file}`]);

        if (code !== 0) {
            throw new Error(`could not read ${file} at ${commit}: ${firstLine(err)}`);
        }

        return JSON.parse(out);
    };

    const problems = [],
        declared = read('installer/package.json').version,
        headers = Object.values(read('mcp.pi.json').mcpServers).map((server) => server.headers);

    if (declared !== version) {
        problems.push(`${commit} carries installer/package.json ${declared}, not ${version}`);
    }

    const lock = read('installer/package-lock.json');

    if (lock.version !== version || lock.packages[''].version !== version) {
        problems.push(`${commit}'s installer/package-lock.json is not at ${version}; rerun bump`);
    }

    if (headers.some((entry) => entry['X-Plugin-Version'] !== version || entry['User-Agent'] !== `${entry['X-Source']}/${version}`)) {
        problems.push(`${commit}'s mcp.pi.json headers are not at ${version}; rerun bump`);
    }

    return problems;
}

function check (version, commit) {
    const distTag = distTagOf(version),
        tag = tagOf(version),
        problems = [];

    if (!distTag) {
        problems.push(`${version} is not <major>.<minor>.<patch>[-rc.N|-alpha.N|-beta.N|-canary.N]`);
    }
    else {
        if (onNpm(version)) {
            problems.push(`${NAME}@${version} is already on npm; versions are immutable`);
        }

        const current = distTags()[distTag];

        if (current && !newer(version, current)) {
            problems.push(`${version} would move the '${distTag}' dist-tag back from ${current}`);
        }

        if (commit) {
            problems.push(...commitProblems(version, commit));
        }
    }

    if (onOrigin(tag)) {
        problems.push(`${tag} is already on origin; never move a pushed tag, cut the next version`);
    }

    if (sh('gh', ['auth', 'status']).code !== 0) {
        problems.push('gh is not signed in; run `gh auth login`');
    }

    console.log(`tag: ${tag}\ndist-tag: ${distTag || 'none'}${commit ? `\ncommit: ${commit}` : ''}`);
    report(problems);
}

function bump (version) {
    if (!distTagOf(version)) {
        throw new Error(`${version} is not a version release.yml accepts`);
    }

    execFileSync('npm', ['version', version, '--no-git-tag-version', '--allow-same-version'], { cwd: path.join(root, 'installer'), stdio: 'ignore' });

    const file = path.join(root, 'mcp.pi.json'),
        config = JSON.parse(fs.readFileSync(file, 'utf8'));

    for (const server of Object.values(config.mcpServers)) {
        server.headers['X-Plugin-Version'] = version;
        server.headers['User-Agent'] = `${server.headers['X-Source']}/${version}`;
    }

    fs.writeFileSync(file, `${JSON.stringify(config, null, 2)}\n`);
    console.log(sh('git', ['status', '--short']).out);
}

const retryCommand = (tag) => `gh workflow run release.yml --ref ${tag} -f tag=${tag}`;

function verify (version) {
    const problems = [],
        distTag = distTagOf(version),
        tag = tagOf(version),
        release = sh('gh', ['release', 'view', tag, '--json', 'isPrerelease,url']),
        ran = sh('npx', ['-y', `${NAME}@${version}`, '--version']).out;

    if (!onNpm(version)) {
        problems.push(`${NAME}@${version} is not on npm`);
    }

    if (distTags()[distTag] !== version) {
        problems.push(`the '${distTag}' dist-tag does not point at ${version}`);
    }

    if (release.code !== 0) {
        problems.push(`${tag} has no GitHub release page; rerun: ${retryCommand(tag)}`);
    }
    else if (JSON.parse(release.out).isPrerelease !== (distTag !== 'latest')) {
        problems.push(`${tag}'s release page has the wrong pre-release flag`);
    }

    if (ran !== version) {
        problems.push(`npx ${NAME}@${version} --version printed "${ran}"`);
    }

    if (distTag === 'latest') {
        const listed = sh('curl', ['-s', '-o', '/dev/null', '-w', '%{http_code}', '-m', '15', GALLERY]).out;

        console.log(listed === '200' ?
            `Pi gallery: ${GALLERY}` :
            `Pi gallery: not listed yet (HTTP ${listed}); it indexes npm on its own schedule, so check again later`);
    }

    report(problems);
}

const sleep = (seconds) => new Promise((resolve) => setTimeout(resolve, seconds * 1000)),
    elapsed = (start) => `${Math.round((Date.now() - start) / 1000)}s`;

/** Polls `probe` every `seconds` until it returns a value, or returns null at `deadline`. */
async function until (deadline, seconds, probe) {
    for (;;) {
        const value = probe();

        if (value) {
            return value;
        }

        if (Date.now() + seconds * 1000 > deadline) {
            return null;
        }

        await sleep(seconds);
    }
}

/** The newest release.yml run on the tag's ref, which a tag push and a `--ref <tag>` retry both use. */
function runFor (tag, since) {
    const { code, out, err } = sh('gh', ['run', 'list', '--workflow', 'release.yml', '--branch', tag, '--limit', '5',
        '--json', 'databaseId,status,conclusion,url,createdAt']);

    if (code !== 0) {
        throw new Error(`could not list release.yml runs: ${firstLine(err)}`);
    }

    return JSON.parse(out || '[]').find((run) => !since || Date.parse(run.createdAt) >= since) ?? null;
}

function failedSteps (id) {
    const { code, out, err } = sh('gh', ['run', 'view', String(id), '--json', 'jobs', '--jq',
        '[.jobs[] | select(.conclusion == "failure") | "\\(.name): \\([.steps[] | select(.conclusion == "failure") | .name] | join(", "))"] | join("; ")']);

    if (code !== 0) {
        throw new Error(`could not read run ${id}: ${firstLine(err)}`);
    }

    return out || `no failed step reported; read \`gh run view ${id} --log-failed\``;
}

function watchOptions (args, usage = 'watch <version> [--minutes N] [--new-run]') {
    const options = { minutes: 30, newRun: false };

    for (let at = 0; at < args.length; at++) {
        if (args[at] === '--new-run') {
            options.newRun = true;
        }
        else if (args[at] === '--minutes') {
            options.minutes = Number(args[++at]);
        }
        else {
            options.minutes = NaN;
        }
    }

    if (!(Number.isFinite(options.minutes) && options.minutes > 0)) {
        throw new Error(`usage: ${usage}`);
    }

    return options;
}

/** The dispatched smoke run for `sha` created since `since`, by the run name the workflow gives it. */
function smokeRunFor (sha, since) {
    const { code, out, err } = sh('gh', ['run', 'list', '--workflow', 'installer-smoke.yml', '--event', 'workflow_dispatch',
        '--limit', '20', '--json', 'databaseId,displayTitle,createdAt']);

    if (code !== 0) {
        throw new Error(`could not list installer-smoke.yml runs: ${firstLine(err)}`);
    }

    return JSON.parse(out || '[]')
        .find((run) => run.displayTitle === `Installer smoke on ${sha}` && Date.parse(run.createdAt) >= since) ?? null;
}

function smokeRun (id) {
    const { code, out, err } = sh('gh', ['run', 'view', String(id), '--json', 'databaseId,status,conclusion,url']);

    if (code !== 0) {
        throw new Error(`could not read smoke run ${id}: ${firstLine(err)}`);
    }

    return JSON.parse(out);
}

/** Whether GitHub has `sha`; GitHub answers 422 "No commit found" for one it doesn't. */
function onGitHub (sha) {
    const { code, out, err } = sh('gh', ['api', `repos/{owner}/{repo}/commits/${sha}`, '--jq', '.sha']);

    if (code === 0) {
        return out === sha;
    }

    if (/No commit found|HTTP 404/.test(err)) {
        return false;
    }

    throw new Error(`could not look ${sha} up on GitHub: ${firstLine(err)}`);
}

/** Runs installer-smoke.yml, every agent on Linux and Windows, on the commit about to be tagged. */
async function smoke (commit, ...args) {
    const { minutes } = watchOptions(args, 'smoke <commit> [--minutes N]'),
        resolved = sh('git', ['rev-parse', '--verify', `${commit}^{commit}`]),
        start = Date.now(),
        deadline = start + minutes * 60 * 1000;

    if (resolved.code !== 0) {
        return report([`${commit} is not a commit here`]);
    }

    const sha = resolved.out;

    // The runner checks the commit out from GitHub, so a commit only on this machine can't be tested.
    if (!onGitHub(sha)) {
        return report([`${sha} is not on GitHub; push its branch first`]);
    }

    const dispatched = sh('gh', ['workflow', 'run', 'installer-smoke.yml', '--ref', 'main', '-f', `ref=${sha}`]);

    if (dispatched.code !== 0) {
        throw new Error(`could not dispatch installer-smoke.yml: ${firstLine(dispatched.err)}`);
    }

    // The run appears a few seconds after the dispatch, which the clocks may disagree about a little.
    const found = await until(deadline, 5, () => smokeRunFor(sha, start - 30 * 1000));

    if (!found) {
        return report([`timed out after ${minutes} minutes waiting for the dispatched smoke run`]);
    }

    const run = await until(deadline, 30, () => {
        const current = smokeRun(found.databaseId);

        return current.status === 'completed' ? current : null;
    });

    console.log(`smoke ${sha.slice(0, 7)}: ${run?.url ?? `run ${found.databaseId}`}`);

    if (!run) {
        return report([`timed out after ${minutes} minutes waiting for the smoke run to finish`]);
    }

    report(run.conclusion === 'success' ? [] : [`smoke run ${run.databaseId} ended ${run.conclusion}: ${failedSteps(run.databaseId)}`]);
}

/** Follows the tag's release.yml run, then waits until npm serves the version and npx can run it. */
async function watch (version, ...args) {
    const { minutes, newRun } = watchOptions(args),
        tag = tagOf(version),
        distTag = distTagOf(version),
        start = Date.now(),
        deadline = start + minutes * 60 * 1000,
        // A retry's run is the first one after the dispatch, which may precede the watch by a little.
        since = newRun ? start - 60 * 1000 : null,
        timedOut = (what) => report([`timed out after ${minutes} minutes waiting for ${what}`]);

    if (!distTag) {
        throw new Error(`${version} is not a version release.yml accepts`);
    }

    let run = await until(deadline, 10, () => runFor(tag, since));

    if (!run) {
        return timedOut(`a release.yml run for ${tag}; was the tag pushed?`);
    }

    console.log(`run ${run.databaseId}: ${run.url}`);

    let seen = '';

    run = await until(deadline, 15, () => {
        const current = runFor(tag, since);

        if (current && current.status !== seen) {
            seen = current.status;
            console.log(`run ${current.databaseId} ${current.status} (${elapsed(start)})`);
        }

        return current?.status === 'completed' ? current : null;
    });

    if (!run) {
        return timedOut('the run to finish');
    }

    if (run.conclusion !== 'success') {
        return report([`run ${run.databaseId} ended ${run.conclusion}: ${failedSteps(run.databaseId)}`]);
    }

    // The registry, the dist-tag and the tarball CDN each lag on their own; a failed lookup here
    // is lag too, so it is retried until the deadline rather than ending the watch.
    const live = await until(deadline, 15, () => {
        try {
            return onNpm(version, true) && distTags(true)[distTag] === version &&
                sh('npx', ['-y', '--prefer-online', `${NAME}@${version}`, '--version']).out === version;
        }
        catch {
            return false;
        }
    });

    if (!live) {
        return timedOut(`npm to serve ${NAME}@${version} on '${distTag}'`);
    }

    console.log(`live: ${NAME}@${version} on '${distTag}', ${elapsed(start)} after the watch began`);
    report([]);
}

function report (problems) {
    for (const problem of problems) {
        console.log(`FAIL ${problem}`);
    }

    console.log(problems.length ? `${problems.length} problem(s)` : 'ok');
    process.exitCode = problems.length ? 1 : 0;
}

const [command, ...args] = process.argv.slice(2),
    commands = { status, suggest, check, bump, smoke, watch, verify };

if (!commands[command] || (command !== 'status' && !args[0])) {
    console.error(USAGE);
    process.exit(2);
}

try {
    await commands[command](...args);
}
catch (error) {
    console.error(error.message);
    process.exit(2);
}
