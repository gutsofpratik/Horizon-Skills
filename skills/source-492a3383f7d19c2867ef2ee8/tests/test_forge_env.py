"""Tests for scripts/forge_env.py"""
import unittest

from scripts.forge_env import forge_env


class TestForgeEnv(unittest.TestCase):

    def test_stamps_skill_name(self):
        env = forge_env("forge-connector", base={})
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SKILL_NAME"], "forge-connector")

    def test_preserves_base_environment(self):
        env = forge_env("forge-connector", base={"PATH": "/usr/bin"})
        self.assertEqual(env["PATH"], "/usr/bin")
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SKILL_NAME"], "forge-connector")

    def test_defaults_to_current_process_environment(self):
        import os
        env = forge_env("forge-connector")
        self.assertIn("ATL_FORGE_ATTRIBUTION_SKILL_NAME", env)
        self.assertNotIn("ATL_FORGE_ATTRIBUTION_SKILL_NAME", os.environ)

    def test_extra_keys_are_upper_cased_and_prefixed(self):
        env = forge_env("forge-connector", extra={"session_id": "abc123"}, base={})
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SESSION_ID"], "abc123")

    def test_multiple_wildcard_extras_are_all_stamped(self):
        env = forge_env(
            "forge-connector",
            extra={"run_id": "r1", "session_id": "s1"},
            base={},
        )
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_RUN_ID"], "r1")
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SESSION_ID"], "s1")
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SKILL_NAME"], "forge-connector")

    def test_ambient_wildcard_vars_pass_through(self):
        # Wildcard vars the agent host already set must reach the CLI untouched.
        env = forge_env(
            "forge-connector",
            base={"ATL_FORGE_ATTRIBUTION_RUN_ID": "host-run-42", "PATH": "/usr/bin"},
        )
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_RUN_ID"], "host-run-42")
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SKILL_NAME"], "forge-connector")

    def test_invalid_extra_value_is_dropped(self):
        env = forge_env("forge-connector", extra={"run_id": "bad value!"}, base={})
        self.assertNotIn("ATL_FORGE_ATTRIBUTION_RUN_ID", env)
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SKILL_NAME"], "forge-connector")

    def test_over_length_value_is_dropped(self):
        env = forge_env("x" * 129, base={})
        self.assertNotIn("ATL_FORGE_ATTRIBUTION_SKILL_NAME", env)

    def test_invalid_charset_value_is_dropped(self):
        env = forge_env("bad name!", base={})
        self.assertNotIn("ATL_FORGE_ATTRIBUTION_SKILL_NAME", env)


if __name__ == "__main__":
    unittest.main()
