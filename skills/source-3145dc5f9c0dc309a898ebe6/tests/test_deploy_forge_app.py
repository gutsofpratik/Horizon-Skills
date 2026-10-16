"""
Tests for scripts/deploy_forge_app.py
"""
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from scripts import deploy_forge_app as dfa


class TestCheckNode(unittest.TestCase):

    @patch("scripts.deploy_forge_app.run_command")
    def test_returns_true_when_node_present(self, mock_run):
        mock_run.return_value = MagicMock(stdout="v22.0.0\n")
        self.assertTrue(dfa.check_node())

    @patch("scripts.deploy_forge_app.run_command")
    def test_returns_false_when_node_missing(self, mock_run):
        mock_run.side_effect = Exception("node not found")
        self.assertFalse(dfa.check_node())


class TestCheckForgeCli(unittest.TestCase):

    @patch("scripts.deploy_forge_app.run_command")
    def test_returns_true_when_forge_present(self, mock_run):
        mock_run.return_value = MagicMock(stdout="10.0.0\nsome other line\n")
        self.assertTrue(dfa.check_forge_cli())

    @patch("scripts.deploy_forge_app.run_command")
    def test_returns_false_when_forge_missing(self, mock_run):
        mock_run.side_effect = Exception("forge not found")
        self.assertFalse(dfa.check_forge_cli())


class TestCheckForgeLogin(unittest.TestCase):

    @patch("scripts.deploy_forge_app.run_command")
    def test_returns_true_when_logged_in(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Logged in as user@example.com\n")
        self.assertTrue(dfa.check_forge_login())

    @patch("scripts.deploy_forge_app.run_command")
    def test_returns_false_when_not_logged_in(self, mock_run):
        mock_run.side_effect = Exception("not logged in")
        self.assertFalse(dfa.check_forge_login())

    @patch("scripts.deploy_forge_app.run_command")
    def test_returns_false_when_output_has_no_email(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Some output without email\n")
        self.assertFalse(dfa.check_forge_login())


class TestCheckAppRegistered(unittest.TestCase):

    def test_returns_true_when_app_id_present(self):
        manifest_content = "app:\n  id: ari:cloud:ecosystem::app/abc-123\n"
        with patch("builtins.open", mock_open(read_data=manifest_content)), \
             patch("scripts.deploy_forge_app.Path.exists", return_value=True):
            result = dfa.check_app_registered("/fake/app")
        self.assertTrue(result)

    def test_returns_false_when_manifest_missing(self):
        with patch("scripts.deploy_forge_app.Path.exists", return_value=False):
            result = dfa.check_app_registered("/fake/app")
        self.assertFalse(result)

    def test_returns_false_when_placeholder_id(self):
        manifest_content = "app:\n  id: will-be-generated\n"
        with patch("builtins.open", mock_open(read_data=manifest_content)), \
             patch("scripts.deploy_forge_app.Path.exists", return_value=True):
            result = dfa.check_app_registered("/fake/app")
        self.assertFalse(result)


class TestDetectRequiredProducts(unittest.TestCase):

    def _run_detect(self, manifest_content):
        with patch("builtins.open", mock_open(read_data=manifest_content)), \
             patch("scripts.deploy_forge_app.Path.exists", return_value=True):
            return dfa.detect_required_products("/fake/app")

    def test_detects_jira_from_scope(self):
        manifest = "permissions:\n  scopes:\n    - read:jira-work\n"
        products = self._run_detect(manifest)
        self.assertIn("jira", products)

    def test_detects_confluence_from_scope(self):
        manifest = "permissions:\n  scopes:\n    - read:confluence-content\n"
        products = self._run_detect(manifest)
        self.assertIn("confluence", products)

    def test_detects_both_products(self):
        manifest = (
            "permissions:\n  scopes:\n"
            "    - read:jira-work\n"
            "    - write:confluence-content\n"
        )
        products = self._run_detect(manifest)
        self.assertIn("jira", products)
        self.assertIn("confluence", products)

    def test_detects_jira_from_module_key(self):
        manifest = "modules:\n  jira:issuePanel:\n    - key: my-panel\n"
        products = self._run_detect(manifest)
        self.assertIn("jira", products)

    def test_detects_confluence_from_module_key(self):
        manifest = "modules:\n  confluence:spacePage:\n    - key: my-macro\n"
        products = self._run_detect(manifest)
        self.assertIn("confluence", products)

    def test_returns_empty_set_when_manifest_missing(self):
        with patch("scripts.deploy_forge_app.Path.exists", return_value=False):
            products = dfa.detect_required_products("/fake/app")
        self.assertEqual(products, set())

    def test_returns_empty_set_for_no_product_scopes(self):
        manifest = "permissions:\n  scopes:\n    - storage:app\n"
        products = self._run_detect(manifest)
        self.assertEqual(products, set())


class TestDeployApp(unittest.TestCase):

    @patch("scripts.deploy_forge_app.run_command")
    def test_deploy_runs_correct_command(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        dfa.deploy_app("/fake/app", environment="development")
        cmd = mock_run.call_args[0][0]
        self.assertIn("forge deploy", cmd)
        self.assertIn("--non-interactive", cmd)
        self.assertIn("development", cmd)

    @patch("scripts.deploy_forge_app.run_command")
    def test_deploy_uses_specified_environment(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        dfa.deploy_app("/fake/app", environment="staging")
        cmd = mock_run.call_args[0][0]
        self.assertIn("staging", cmd)


class TestInstallApp(unittest.TestCase):

    @patch("scripts.deploy_forge_app.run_command")
    def test_install_runs_correct_command(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        dfa.install_app("/fake/app", "mysite.atlassian.net", product="jira")
        cmd = mock_run.call_args[0][0]
        self.assertIn("forge install", cmd)
        self.assertIn("--non-interactive", cmd)
        self.assertIn("mysite.atlassian.net", cmd)
        self.assertIn("jira", cmd)

    @patch("scripts.deploy_forge_app.run_command")
    def test_install_uses_specified_product(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        dfa.install_app("/fake/app", "mysite.atlassian.net", product="confluence")
        cmd = mock_run.call_args[0][0]
        self.assertIn("confluence", cmd)


class TestRunCommand(unittest.TestCase):

    @patch("scripts.deploy_forge_app.subprocess.run")
    def test_returns_result_on_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        result = dfa.run_command("echo hello")
        self.assertEqual(result.stdout, "ok")

    @patch("scripts.deploy_forge_app.subprocess.run")
    def test_raises_on_failure(self, mock_run):
        import subprocess
        mock_run.side_effect = subprocess.CalledProcessError(1, "bad-cmd")
        with self.assertRaises(subprocess.CalledProcessError):
            dfa.run_command("bad-cmd")

    @patch("scripts.deploy_forge_app.subprocess.run")
    def test_stamps_skill_name_env_var(self, mock_run):
        """Every command run by the deploy script carries the attribution env var."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        dfa.run_command("forge deploy")
        env = mock_run.call_args[1].get("env")
        self.assertIsNotNone(env)
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SKILL_NAME"], "forge-app-builder")


if __name__ == "__main__":
    unittest.main()
