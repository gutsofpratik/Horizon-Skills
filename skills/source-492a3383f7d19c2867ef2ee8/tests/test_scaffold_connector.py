"""Tests for scripts/scaffold_connector.py"""
import unittest
from unittest.mock import patch, MagicMock

from scripts import scaffold_connector as sc


class TestRunForgeCreate(unittest.TestCase):

    @patch("scripts.scaffold_connector.subprocess.run")
    def test_stamps_skill_name_env_var(self, mock_run):
        """forge create must carry the skill-name attribution env var."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        sc.run_forge_create("my-connector", "/parent", dev_space_id="abc")
        env = mock_run.call_args[1].get("env")
        self.assertIsNotNone(env)
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SKILL_NAME"], "forge-connector")

    @patch("scripts.scaffold_connector.subprocess.run")
    def test_passes_developer_space_id(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        sc.run_forge_create("my-connector", "/parent", dev_space_id="space-123")
        cmd = mock_run.call_args[0][0]
        self.assertIn("--developer-space-id", cmd)
        self.assertIn("space-123", cmd)


if __name__ == "__main__":
    unittest.main()
