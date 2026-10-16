#!/usr/bin/env python3
"""Run the eval cases in evals.json and check the outputs against expectations.

What this can and cannot do, stated up front because the distinction matters:

CAN check whether the skill, once applied, produces the right *kind* of answer.
Each case is graded in two layers, following the grading ladder in
references/evaluation.md: regex assertions for what a regex is the right
instrument for, and a rubric graded by a second model for everything that needs
judgment. Keyword matching on a judgment question measures agreement with the
author's vocabulary rather than quality, which is why the split exists.

CANNOT check triggering. Whether a skill activates on a given phrasing is a
property of the harness that loads it, not of the model. There is no API call
that reproduces it. Cases marked "triggering": true are printed as a manual
checklist instead of being run, and they are the more important half.

Usage:
    export ANTHROPIC_API_KEY=...
    python evals/run_evals.py                       # run automatable cases
    python evals/run_evals.py --manual              # print the manual checklist
    python evals/run_evals.py --model claude-opus-5-5
    python evals/run_evals.py --case 2
    python evals/run_evals.py --dry-run             # show prompts, call nothing
"""
import argparse
import json
import os
import signal
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
SKILL = ROOT.parent / "SKILL.md"
API = "https://api.anthropic.com/v1/messages"


def load_skill():
    text = SKILL.read_text()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    return text.strip()


class StopError(Exception):
    """The model stopped for a reason other than finishing its answer."""


# On models where thinking always runs, max_tokens covers thinking plus the
# answer. A budget sized for the answer alone truncates it, and the truncated
# text then fails the rubric for a reason that has nothing to do with the skill.
GEN_MAX_TOKENS = 16000
GRADE_MAX_TOKENS = 8000


def call(model, system, prompt, max_tokens=GEN_MAX_TOKENS):
    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(API, data=body, headers={
        "content-type": "application/json",
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01",
    })
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    stop = data.get("stop_reason")
    text = "".join(b.get("text", "") for b in data.get("content", []))
    # A refusal arrives as HTTP 200 with little or no text. Grading it would
    # report a bad answer and send you tuning a prompt that was never the problem.
    if stop == "refusal":
        category = (data.get("stop_details") or {}).get("category", "unspecified")
        raise StopError(f"refusal ({category})")
    if stop == "max_tokens":
        raise StopError(f"truncated at max_tokens={max_tokens}; raise the budget")
    return text


GRADER_SYSTEM = """You grade one response against a rubric. You did not write the
response and you are not being asked to improve it.

For each rubric item, answer MET or NOT MET, then one sentence of evidence quoting
or pointing at the part of the response that decided it. Judge what the response
does, not the words it uses to do it: a response that delegates schema
enforcement to a tool definition has met an item about API-level enforcement
even if it never uses the phrase.

Output one line per item, in order, formatted exactly:
<n>. MET|NOT MET - <evidence>
Then a final line: VERDICT: <met count>/<total>
Nothing else."""


def check_structural(case, output):
    """Regex assertions only, for things a regex is the right instrument for."""
    problems = []
    low = output.lower()
    for pattern in case.get("must_contain", []):
        if not re.search(pattern, low, re.I):
            problems.append(f"missing: {pattern}")
    for pattern in case.get("must_not_contain", []):
        m = re.search(pattern, low, re.I)
        if m:
            problems.append(f"present but should not be: {pattern} ({m.group(0)[:40]})")
    return problems


def grade_rubric(model, case, output):
    """Judgment items, graded by a model. Returns (met, total, lines)."""
    rubric = case.get("rubric") or []
    if not rubric:
        return 0, 0, []
    items = "\n".join(f"{i}. {r}" for i, r in enumerate(rubric, 1))
    prompt = (f"RUBRIC:\n{items}\n\n"
              f"REQUEST THE RESPONSE WAS ANSWERING:\n{case['prompt']}\n\n"
              f"RESPONSE:\n{output}")
    verdict = call(model, GRADER_SYSTEM, prompt, max_tokens=GRADE_MAX_TOKENS)
    met = len(re.findall(r"^\s*\d+\.\s*MET\b", verdict, re.M | re.I))
    return met, len(rubric), verdict.strip().splitlines()


SELF_TEST = [
    # (rubric verdict text, expected met count)
    ("1. MET - uses a tool definition\n2. NOT MET - no review flag\nVERDICT: 1/2", 1),
    ("1. NOT MET - rewrites the prompt first\n2. NOT MET - no baseline\nVERDICT: 0/2", 0),
    ("1. met - lowercase still counts\n2. MET - fine\nVERDICT: 2/2", 2),
]


def self_test():
    """Exercise the parsing and structural checks without touching the API."""
    ok = True
    for text, expected in SELF_TEST:
        got = len(re.findall(r"^\s*\d+\.\s*MET\b", text, re.M | re.I))
        status = "ok" if got == expected else "FAIL"
        if got != expected:
            ok = False
        print(f"  rubric parse: expected {expected}, got {got}  {status}")

    case = {"must_contain": [r"\{\{[a-z_]+\}\}"], "must_not_contain": ["respond only in valid json"]}
    checks = [
        ("uses {{ticket_text}} and a tool schema", 0),
        ("no placeholders anywhere", 1),
        ("uses {{x}} but says respond only in valid JSON", 1),
    ]
    for text, expected in checks:
        n = len(check_structural(case, text))
        status = "ok" if n == expected else "FAIL"
        if n != expected:
            ok = False
        print(f"  structural:   expected {expected} problem(s), got {n}  {status}")
    print("self-test passed" if ok else "self-test FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-sonnet-5-5",
                    help="model that produces the responses")
    ap.add_argument("--grader", default="claude-opus-5-5",
                    help="model that grades them; keep it different from --model, "
                         "because a model grading its own output is measuring itself")
    ap.add_argument("--case", type=int, help="run a single case by id")
    ap.add_argument("--manual", action="store_true", help="print the manual checklist only")
    ap.add_argument("--dry-run", action="store_true", help="print prompts, make no calls")
    ap.add_argument("--self-test", action="store_true",
                    help="check the grading logic offline, no API calls, no quota")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    spec = json.loads((ROOT / "evals.json").read_text())
    cases = spec["evals"]
    if args.case:
        cases = [c for c in cases if c["id"] == args.case]

    manual = [c for c in cases if c.get("triggering")]
    auto = [c for c in cases if not c.get("triggering")]

    if args.manual or not auto:
        print("Manual checklist: triggering cannot be tested through the API.")
        print("Open a fresh session with the skill installed, paste each prompt,")
        print("and record whether the skill loaded before anything else happened.\n")
        for c in manual:
            print(f"[{c['id']}] {c['prompt']}")
            print(f"     expect: {c['expected_output']}\n")
        if args.manual:
            return 0

    if args.dry_run:
        for c in auto:
            print(f"--- case {c['id']} ---\n{c['prompt']}\n")
        return 0

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        return 2

    system = load_skill()
    failed = 0
    for c in auto:
        try:
            try:
                out = call(args.model, system, c["prompt"])
            except StopError as e:
                print(f"[{c['id']}] STOPPED generating: {e}")
                failed += 1
                continue
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            detail = e.read()[:200].decode(errors="replace") if hasattr(e, "read") else str(e)
            print(f"[{c['id']}] ERROR generating: {detail}")
            failed += 1
            continue

        problems = check_structural(c, out)
        try:
            try:
                met, total, lines = grade_rubric(args.grader, c, out)
            except StopError as e:
                (ROOT / f"out_{c['id']}.txt").write_text(out)
                print(f"[{c['id']}] STOPPED grading: {e}. Response saved to "
                      f"evals/out_{c['id']}.txt")
                failed += 1
                continue
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            # A grader failure must not destroy the response we just paid for.
            (ROOT / f"out_{c['id']}.txt").write_text(out)
            print(f"[{c['id']}] ERROR grading: {e}. Response saved to "
                  f"evals/out_{c['id']}.txt; rerun grading with --case {c['id']}.")
            failed += 1
            continue
        ok = not problems and (total == 0 or met == total)
        print(f"[{c['id']}] {'PASS' if ok else 'FAIL'}  rubric {met}/{total}  {c['prompt'][:50]}...")
        for p in problems:
            print(f"      structural: {p}")
        for line in lines:
            if re.match(r"\s*\d+\.\s*NOT MET", line, re.I):
                print(f"      {line.strip()}")
        if not ok:
            failed += 1
            (ROOT / f"out_{c['id']}.txt").write_text(out + "\n\n---- rubric ----\n" + "\n".join(lines))
            print(f"      full output and rubric written to evals/out_{c['id']}.txt")

    print(f"\n{len(auto) - failed}/{len(auto)} automatable cases passed.")
    if manual:
        print(f"{len(manual)} triggering case(s) still need a manual run: --manual")
    return 1 if failed else 0


if __name__ == "__main__":
    # Piping into head sends SIGPIPE; die quietly rather than with a traceback.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
