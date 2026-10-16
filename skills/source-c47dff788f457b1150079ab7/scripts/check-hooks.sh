#!/usr/bin/env bash
# Exercise hooks/hooks.json's SessionStart command. In CI only the Droid
# harness runs it, through Droid, so for every other vendor this is the only check
# that it resolves the root; installer/test/session-start-hook.test.js checks what the scripts print.
#
# Run from the repo root:
#   .claude/skills/add-marketplace/scripts/check-hooks.sh
#   .claude/skills/add-marketplace/scripts/check-hooks.sh KIMI_PLUGIN_ROOT ...
#   .claude/skills/add-marketplace/scripts/check-hooks.sh none
#
# Each named variable is checked on its own, from an empty directory, so only
# a token the command really uses resolves. Pass the new vendor's variable when
# adding a route; a FAIL means its manifest must point at hooks/session-start.
#
# Pass `none` for a config-only or package vendor: neither reads hooks.json, so
# it has no token to check. Naming a variable that does not exist
# would report a FAIL that reads like a regression.
set -uo pipefail

repo=$PWD
[ -r "$repo/hooks/hooks.json" ] || { echo "run me from the repo root" >&2; exit 2; }

cmd=$(node -p 'JSON.parse(require("fs").readFileSync("hooks/hooks.json","utf8")).hooks.SessionStart[0].hooks[0].command')
status=0

# Every plugin-root variable a vendor sets, so each check starts from nothing.
clear_env=(env -u CLAUDE_PLUGIN_ROOT -u CURSOR_PLUGIN_ROOT -u KIMI_PLUGIN_ROOT -u PLUGIN_ROOT -u DROID_PLUGIN_ROOT)

check_resolves() {
  local var=$1 out rc
  out=$(cd "$(mktemp -d)" && "${clear_env[@]}" "$var=$repo" bash -c "$cmd" 2>&1) && rc=0 || rc=$?
  if [ "$rc" -eq 0 ] && [ -n "$out" ]; then
    echo "ok   \$$var resolves the plugin root"
  else
    echo "FAIL \$$var does not resolve — the hook prints nothing and that route loses its mandate"
    printf '%s\n' "${out:-<no output>}" | sed 's/^/       /'
    status=1
  fi
}

check_resolves CLAUDE_PLUGIN_ROOT

for var in ${1+"$@"}; do
  # `none` is an answer, not a variable: this vendor has no plugin root and the
  # hook is not supposed to grow a token for it.
  if [ "$var" = none ]; then
    echo "n/a  this vendor has no plugin-root variable - paths resolve against the project root"
    continue
  fi
  check_resolves "$var"
done

# Droid fills in ${DROID_PLUGIN_ROOT} too, and its Skill tool rejects `postman:<skill>`.
out=$(cd "$(mktemp -d)" && "${clear_env[@]}" CLAUDE_PLUGIN_ROOT="$repo" DROID_PLUGIN_ROOT="$repo" bash -c "$cmd" 2>&1) && rc=0 || rc=$?
if [ "$rc" -eq 0 ] && [ -n "$out" ] && ! grep -q 'postman:' <<<"$out"; then
  echo "ok   \$DROID_PLUGIN_ROOT -> the mandate with bare skill names"
else
  echo "FAIL \$DROID_PLUGIN_ROOT -> exit $rc; Droid needs the mandate with no \`postman:\` prefix"
  status=1
fi

# With no root variable set the hook must fail loudly rather than
# cat "/hooks/session-start-context.md" and leave no trace.
out=$(cd "$(mktemp -d)" && "${clear_env[@]}" bash -c "$cmd" 2>&1) && rc=0 || rc=$?
if [ "$rc" -ne 0 ] && [ -n "$out" ]; then
  echo "ok   no root variable -> exit $rc with a message"
else
  echo "FAIL no root variable -> exit $rc, output: ${out:-<none>} (want non-zero + a message)"
  status=1
fi

exit $status
