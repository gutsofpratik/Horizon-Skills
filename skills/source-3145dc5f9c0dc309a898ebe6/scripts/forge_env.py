"""Environment helper for spawning the Forge CLI.

The Forge CLI reads a reserved ``ATL_FORGE_ATTRIBUTION_*`` namespace from
its environment and forwards every key in it to the backend. This helper
returns an environment mapping with the skill identifier stamped in, so
that every ``forge`` command a skill spawns carries it.

The same namespace is open-ended, so the helper supports arbitrary
wildcard fields beyond the skill name:

* ``extra=`` stamps additional keys programmatically, e.g.
  ``forge_env("forge-app-builder", extra={"run_id": "abc"})`` →
  ``ATL_FORGE_ATTRIBUTION_RUN_ID=abc``.
* any ``ATL_FORGE_ATTRIBUTION_*`` var already present in the environment
  (e.g. set by the agent host) is preserved and forwarded as-is.

Values the helper stamps follow the CLI's contract — short tokens
matching ``[A-Za-z0-9._-]`` and at most 128 characters; values that
don't match are dropped silently rather than raising.
"""

import os
import re

_ATTRIBUTION_PREFIX = "ATL_FORGE_ATTRIBUTION_"
_VALUE_RE = re.compile(r"^[A-Za-z0-9._-]+$")
_MAX_LEN = 128


def _is_valid_value(value):
    """True if ``value`` satisfies the Forge CLI value contract."""
    return (
        isinstance(value, str)
        and 0 < len(value) <= _MAX_LEN
        and _VALUE_RE.match(value) is not None
    )


def forge_env(skill_name, extra=None, base=None):
    """Return an environment dict for spawning the Forge CLI.

    Starts from a copy of the current process environment (or ``base`` if
    provided) and stamps ``ATL_FORGE_ATTRIBUTION_SKILL_NAME=<skill_name>``.

    ``extra`` may supply additional ``ATL_FORGE_ATTRIBUTION_*`` fields as a
    mapping of unprefixed keys to values (e.g. ``{"SESSION_ID": "abc"}`` →
    ``ATL_FORGE_ATTRIBUTION_SESSION_ID=abc``). Keys are upper-cased and
    prefixed; entries whose value fails validation are skipped.

    Any ``ATL_FORGE_ATTRIBUTION_*`` vars already in the source environment
    are left untouched, so wildcard fields set by the caller's environment
    pass through to the CLI unchanged.
    """
    # Copying the source env preserves ambient ATL_FORGE_ATTRIBUTION_* vars.
    env = dict(os.environ if base is None else base)

    fields = {"SKILL_NAME": skill_name}
    if extra:
        fields.update(extra)

    for key, value in fields.items():
        if not _is_valid_value(value):
            continue
        env[_ATTRIBUTION_PREFIX + key.upper()] = value

    return env
