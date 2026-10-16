## Dependency Validation

Run in `<target_dir>` when dependency validation is required — e.g. [pre-coding checklist](pre-coding-checklist.md) step 10 or [pre-deployment checklist](pre-deployment-checklist.md) step 4.

Respect the [Dependency check session rule](../SKILL.md#dependency-check-session-rule) in `SKILL.md` before starting (skip if already passed for the same `<target_dir>`).

---

### Flow

1. **Check** — `dr dependency check`
   - On zero exit: set `<dependency_check_passed>` = true and `<dependency_check_target_dir>` = `<target_dir>`. Done.
2. **Fix** (if step 1 failed — missing dependencies, wrong versions, or both):
   - `dr dependency install --yes`
   - On non-zero exit: hard stop — return full output from all commands run so far.
3. **Re-check** — `dr dependency check`
   - On zero exit: set `<dependency_check_passed>` = true and `<dependency_check_target_dir>` = `<target_dir>`. Done.
   - On non-zero exit: hard stop — return full output from all commands run.
