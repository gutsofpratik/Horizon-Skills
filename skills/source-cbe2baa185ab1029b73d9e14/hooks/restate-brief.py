#!/usr/bin/env python3
"""UserPromptSubmit hook: ask for a short restatement before multi-step work.

Why a hook and not a skill: a skill is selected, so it fires some of the time.
This has to fire every time the condition holds, and only then.

What it injects is deliberately small. The expensive artifact (a written prompt,
a feature list, a worker prompt) is worth it only when work spans sessions; for
everything else the whole value is three sentences that let the user catch a
misread brief before the work happens.

Install: see settings.json snippet next to this file.
"""
import json
import re
import sys

# Verbs that imply building something multi-step. Tuned to fire on real work and
# stay silent on questions, lookups, and single edits.
BUILD = re.compile(
    r"(?i)\b(bau|baue|build|implementier|implement|erstell|erstelle|create|"
    r"schreib mir|write me|setz.{0,5}auf|set up|refactor|migrier|migrate|"
    r"automatisier|automate|integrier|integrate|deploy)\w*\b")

# If any of these appear, the user already knows what they want in detail, or
# they are asking rather than commissioning. Staying quiet is the right default.
SKIP = re.compile(
    r"(?i)\b(was ist|what is|wieso|warum|why|wie funktioniert|how does|"
    r"erklär|explain|zeig mir|show me|lies|read|find|such|grep|"
    r"fix typo|rename|kommentier)\w*\b")

BRIEF = """Before starting, restate this briefly: the goal as you understand it,
the assumptions you are making that the request did not specify, and the
acceptance criteria you will hold yourself to. If an assumption would be
expensive to get wrong, ask instead of guessing. Then do the work.

Keep it short and follow whatever response style is already in force; this asks
for the content, not for a particular register or length. The restatement is not
a plan document and not a deliverable. If your turn ends with it and no tool
calls, nothing happened.

If the task spans more than one session, this is the case where written
artifacts earn their cost: use the prompt-engineer skill and split it into an
initializer and a worker."""

MIN_WORDS = 6      # shorter than this is usually a follow-up, not a commission
MAX_WORDS = 120    # longer than this and the user has already specified it


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)          # never block the turn on a hook failure

    # Field name differs between harness versions; try the likely ones.
    prompt = ""
    for key in ("prompt", "user_prompt", "userPrompt", "message"):
        if isinstance(payload.get(key), str):
            prompt = payload[key]
            break
    if not prompt:
        sys.exit(0)

    words = len(prompt.split())
    if words < MIN_WORDS or words > MAX_WORDS:
        sys.exit(0)
    if SKIP.search(prompt):
        sys.exit(0)
    if not BUILD.search(prompt):
        sys.exit(0)

    print(BRIEF)
    sys.exit(0)


if __name__ == "__main__":
    main()
