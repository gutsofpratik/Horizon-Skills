#!/usr/bin/env python3
"""Check a prompt against the mechanically detectable anti-patterns.

This covers only what a regex can see. Altitude, whether a constraint carries its
reason, whether examples anchor creative work: those need judgment and stay with
the model. Run this first anyway, because the grading ladder says code before
LLM, and every finding here is one the model no longer has to spend attention on.

Usage:
    python scripts/lint_prompt.py myprompt.md
    python scripts/lint_prompt.py myprompt.md --class 1
    cat myprompt.md | python scripts/lint_prompt.py -
    python scripts/lint_prompt.py myprompt.md --json
"""
import argparse
import json
import re
import sys

# (id, severity, regex, message, applies_to_classes)
CHECKS = [
    ("reasoning-reproduction", "error",
     r"(?i)\b(think step by step|show your (reasoning|thinking|work)|explain your reasoning|"
     r"<thinking>|in thinking tags|walk me through your thought)",
     "Instructs the model to reproduce its reasoning. On internal-reasoning models "
     "this adds nothing and current models can decline it as a reasoning-extraction "
     "request. If the OUTPUT needs a reasoning "
     "artifact, frame it as an output artifact instead.", {"1"}),

    ("missing-cot", "warn",
     None,  # handled separately
     "No chain-of-thought guidance found. Class 2 and 3 models need it explicitly "
     "for multi-step work.", {"2", "3"}),

    ("prefill", "error",
     r"(?i)(prefill|pre-fill|assistant.{0,20}turn.{0,20}(start|begin)s? with|"
     r"begin your response with the following text)",
     "Looks like a prefill technique. Unsupported on Claude 4.6 and later, returns "
     "400. Use structured outputs, a strict tool schema, or instruct the format.",
     None),

    ("prompt-text-json", "warn",
     r"(?i)(respond only (in|with) (valid )?json|output only json|"
     r"return (a |valid )?json (object|array)|no (other )?text.{0,15}json)",
     "Enforces JSON through prompt text. If the API offers structured outputs or a "
     "strict tool schema, use that instead; it is a grammar constraint, not a "
     "request.", None),

    ("vague-quality", "warn",
     r"(?i)\b(be (accurate|helpful|professional|engaging|thorough|concise)|"
     r"high[- ]quality|make it good|do your best|as best you can)\b",
     "Vague quality word with no measurable criterion, or a constraint restating a "
     "model default. Replace with a checkable success criterion.", None),

    ("filler-role", "warn",
     r"(?i)("
     r"\b(world[- ]class|expert[- ]level|you are the best|renowned|highly skilled|"
     r"master(ful)? (of|at)|10x |rockstar|top[- ]tier|elite)\b"
     r"|\b(weltklasse|erstklassig|herausragend)\b"
     r"|\b(you are an? )?(senior|principal|staff|lead) (developer|engineer|"
     r"architect|designer|writer)\b"
     r"|\bdu bist (ein )?(senior|erfahrener|langjaehriger)\b"
     r"|(you|du) (have|hast) (already |schon )?(built|gebaut|geschrieben|shipped)\b"
     r"|\b(years of experience|jahrelange erfahrung|von null bis produktion)\b"
     r"|\bmehrere \w+([- ]\w+)* (apps|projekte|anwendungen|systeme)\b"
     r")",
     "Padding in the role: asserts experience, seniority, or excellence rather "
     "than domain. Cut the clause and check whether the output would change; if "
     "not, it was flattery aimed at the model.",
     None),

    ("undated-model", "warn",
     r"(?i)("
     # current Claude naming: tier before number
     r"\bclaude[- ](opus|sonnet|haiku|fable|mythos)[- ]?[\d.]+"
     # legacy Claude naming: number before tier, e.g. claude-3-5-sonnet,
     # claude-3-opus. These are exactly what turns up in revise mode, where an
     # old prompt arrives carrying an old model id.
     r"|\bclaude[- ]\d(?:[-.]\d)*[- ](opus|sonnet|haiku|instant)"
     # oldest Claude ids carry no tier at all: claude-2.1, claude-instant-1.2
     r"|\bclaude-(instant-)?\d+(\.\d+)*\b"
     r"|\bgpt-\d[\w.-]*|\bgpt-4o\b"
     r"|\bgemini[- ][\d.]+|\bo[1-9]\b|\bllama[- ]?[\d.]+|\bqwen[\d.-]*"
     r")",
     "Hardcoded model name. In a reusable template, add a date or describe the "
     "capability instead, or the prompt silently rots.", None),

    ("negation-heavy", "warn",
     None,  # handled separately
     "Heavy use of prohibitions. Negations are unreliable on smaller models; show "
     "the target instead of forbidding the miss.", None),

    ("no-placeholders", "warn",
     None,  # handled separately
     "No {{VARIABLE}} placeholders found. If this template takes variable input, "
     "the input needs to be marked as such.", None),
]

# The permitted value rarely sits directly after the verb; a field name or two
# usually stands between them ("return product null, severity low").
SENTINEL_ALLOW_RE = re.compile(
    r"(?i)\b(return|use|set|output|leave|emit|default to)\b"
    r"(?:\s+[\w,`\"'/]+){0,4}?\s+[`\"']?(null|none|nil|n/a)\b")
SENTINEL_FORBID_RE = re.compile(
    r"(?i)(never|do not|don't|must not)\s+(?:\w+\s+){0,4}"
    r"(null|none|nil|empty|unset|blank)"
    r"|(?:a\s+)?(null|empty|unset|blank)\s+(?:\w+\s+){0,3}"
    r"(breaks|fails|is invalid|is rejected|crashes)")

NEGATION_RE = re.compile(r"(?i)\b(don't|do not|never|avoid|no |must not|should not|refrain)\b")
COT_RE = re.compile(r"(?i)(step by step|first.{0,40}then|work through|before (you )?answer)")
PLACEHOLDER_RE = re.compile(r"\{\{[A-Za-z0-9_]+\}\}")
CODEBLOCK_RE = re.compile(r"```.*?```", re.S)
# A file can waive checks it discusses rather than commits:
#   <!-- lint-disable: prefill, vague-quality -->
# and a single line can waive everything with a trailing "lint-ignore".
DISABLE_RE = re.compile(r"lint-disable:\s*([a-z0-9,\s-]+)", re.I)
# The capture runs up to the closing "-->" and swallows its first hyphen, so the
# last id in a list arrives as "filler-role -". Normalise before comparing.
CHECK_ID_RE = re.compile(r"[a-z][a-z0-9-]*[a-z0-9]", re.I)


# Checks that fire on a *mention* of a pattern, not on its use. Reference
# documentation about prompting necessarily names prefill, thinking-tag
# instructions and model versions; linting prose about an anti-pattern as if it
# were the anti-pattern is a category error.
DOC_EXEMPT = {"prefill", "reasoning-reproduction", "sentinel-conflict",
              "no-placeholders", "prompt-text-json", "filler-role"}

# "undated-model" stays live even in docs mode: its whole point is the staleness
# reminder, and reference documentation is the first thing to go stale. Instead
# of exempting the file, honour what the message actually asks for. A file that
# records when its model names were current has complied.
DATED_RE = re.compile(
    r"(?i)(as of|stand:|current as of|dated)\s+\w*\s*20\d\d"
    r"|\b20\d\d-\d\d-\d\d\b"
    r"|\b(january|february|march|april|may|june|july|august|september|october|"
    r"november|december|januar|februar|maerz|mai|juni|juli|oktober|dezember)\s+20\d\d\b")


def lint(text, target_class=None, docs=False, scan_code=None):
    """scan_code: True scans fenced blocks, False strips them.

    Default follows the mode. A prompt handed over for review is nearly always
    pasted inside a fence, so in normal mode the fenced block IS the object
    under test and stripping it lints the prose around the prompt instead of the
    prompt. In docs mode the opposite holds: fenced blocks there are quoted
    examples of the very patterns being explained.
    """
    if scan_code is None:
        scan_code = not docs
    findings = []
    disabled = set(DOC_EXEMPT) if docs else set()
    if DATED_RE.search(text):
        disabled.add("undated-model")
    for m in DISABLE_RE.finditer(text):
        for chunk in m.group(1).split(","):
            found = CHECK_ID_RE.search(chunk)
            if found:
                disabled.add(found.group(0).lower())
    scannable = text if scan_code else CODEBLOCK_RE.sub("", text)
    lines = scannable.splitlines()

    for cid, sev, pattern, msg, classes in CHECKS:
        if cid in disabled:
            continue
        if classes and target_class and target_class not in classes:
            continue
        if pattern is None:
            continue
        rx = re.compile(pattern)
        for i, line in enumerate(lines, 1):
            if "lint-ignore" in line:
                continue
            m = rx.search(line)
            if m:
                findings.append({"check": cid, "severity": sev, "line": i,
                                 "match": m.group(0)[:60], "message": msg})

    words = max(len(scannable.split()), 1)
    negations = len(NEGATION_RE.findall(scannable))
    if "negation-heavy" not in disabled and negations / words > 0.02 and negations >= 5:
        findings.append({"check": "negation-heavy", "severity": "warn", "line": 0,
                         "match": f"{negations} prohibitions in {words} words",
                         "message": dict((c[0], c[3]) for c in CHECKS)["negation-heavy"]})

    # An agentic build prompt is parameterless by design; its variable part lives
    # in the repo it operates on. Flagging it teaches the reader to invent
    # placeholders with nothing to fill them.
    agentic = bool(re.search(
        r"(?i)(<phases>|acceptance.criteri|akzeptanzkriterien|checkpoint.polic|"
        r"end your turn|beende den zug|one feature per session|"
        r"ein feature pro session)", text))
    if "sentinel-conflict" not in disabled:
        allow = SENTINEL_ALLOW_RE.search(scannable)
        forbid = SENTINEL_FORBID_RE.search(scannable)
        if allow and forbid:
            findings.append({
                "check": "sentinel-conflict", "severity": "error", "line": 0,
                "match": f"{allow.group(0)[:40]} / {forbid.group(0)[:40]}",
                "message": "The prompt both permits a sentinel value and calls it "
                           "an error. The model will pick one of the two per run. "
                           "Name a distinct sentinel and say which consumer "
                           "expects it."})

    if ("no-placeholders" not in disabled and not agentic
            and not PLACEHOLDER_RE.search(text) and words > 80):
        findings.append({"check": "no-placeholders", "severity": "warn", "line": 0,
                         "match": "none found",
                         "message": dict((c[0], c[3]) for c in CHECKS)["no-placeholders"]})

    if ("missing-cot" not in disabled and target_class in {"2", "3"}
            and not COT_RE.search(scannable)):
        findings.append({"check": "missing-cot", "severity": "warn", "line": 0,
                         "match": "none found",
                         "message": dict((c[0], c[3]) for c in CHECKS)["missing-cot"]})

    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="prompt file, or - for stdin")
    ap.add_argument("--class", dest="cls", choices=["1", "2", "3"],
                    help="target model class; enables class-specific checks")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--skip-code", action="store_true",
                    help="strip fenced blocks before scanning; the default in "
                         "--docs mode and rarely right otherwise")
    ap.add_argument("--scan-code", action="store_true",
                    help="scan fenced blocks even in --docs mode")
    ap.add_argument("--docs", action="store_true",
                    help="the file is documentation about prompting, not a prompt; "
                         "skips the checks that fire on merely naming a pattern")
    args = ap.parse_args()

    text = sys.stdin.read() if args.path == "-" else open(args.path).read()
    scan_code = None
    if args.scan_code:
        scan_code = True
    elif args.skip_code:
        scan_code = False
    findings = lint(text, args.cls, docs=args.docs, scan_code=scan_code)

    if args.json:
        print(json.dumps(findings, indent=2))
    elif not findings:
        print("clean: no mechanical anti-patterns found")
        print("Altitude, reasons behind constraints, and example choice still need review.")
    else:
        errors = sum(1 for f in findings if f["severity"] == "error")
        for f in findings:
            loc = f"line {f['line']}" if f["line"] else "whole file"
            print(f"[{f['severity']}] {f['check']} ({loc}): {f['match']}")
            print(f"    {f['message']}\n")
        print(f"{len(findings)} finding(s), {errors} error(s)")

    return 1 if any(f["severity"] == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
