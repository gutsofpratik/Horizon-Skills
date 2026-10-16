# restate-brief hook

Optional. Ships inside the skill so one copy step installs everything, but a
hook is not loaded from a skill directory: it has to be registered in
`settings.json` before it does anything.

    cp restate-brief.py ~/.claude/hooks/
    chmod +x ~/.claude/hooks/restate-brief.py
    # then merge settings-snippet.json into ~/.claude/settings.json

Check it works before wiring it up. The first command prints the brief, the
second prints nothing:

    echo '{"prompt":"bau mir ein script das alte logs aufraeumt"}' | python3 ~/.claude/hooks/restate-brief.py
    echo '{"prompt":"was steht in zeile 12"}' | python3 ~/.claude/hooks/restate-brief.py

Why this is a hook and not part of the skill's own behaviour: a skill is
selected, so it fires some of the time. A restatement before multi-step work
should fire every time the condition holds, and only then.

The payload field name varies between Claude Code versions; the script tries
four common variants and exits zero on anything it cannot parse, because a hook
that blocks a turn is worse than one that does nothing.
