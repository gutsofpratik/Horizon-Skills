#!/usr/bin/env bash
# Lint every prose file the skill ships, each in the mode that fits it:
# instructions normally, documentation with --docs. Exits non-zero if any fail.
#
# The claim "the skill passes its own linter" is only worth making if the set is
# the whole skill, so this covers SKILL.md, references/, commands/ and hooks/.
# evals/evals.json is data, not prose; it is validated as JSON instead.
set -u
cd "$(dirname "$0")/.." || exit 1
fail=0

lint() {  # $1 = file, $2 = optional --docs
  if ! python3 scripts/lint_prompt.py "$1" ${2:-} > /dev/null; then
    echo "  findings: $1 ${2:-}"
    fail=1
  fi
}

# Instructions: linted as prompts, because that is what they are.
lint SKILL.md
for f in commands/*.md; do [ -e "$f" ] && lint "$f"; done

# Documentation about prompting: --docs, since six checks fire on merely naming
# a pattern. undated-model stays live in both modes and is satisfied by a date.
for f in references/*.md; do [ -e "$f" ] && lint "$f" --docs; done
for f in hooks/*.md; do [ -e "$f" ] && lint "$f" --docs; done

# Data files: structural validation, not linting.
for f in evals/evals.json hooks/settings-snippet.json; do
  [ -e "$f" ] || continue
  python3 -c "import json,sys;json.load(open('$f'))" || { echo "  $f is not valid JSON"; fail=1; }
done

if [ "$fail" -eq 0 ]; then
  echo "all skill files clean"
else
  echo "run the listed files individually for detail"
fi
exit "$fail"
