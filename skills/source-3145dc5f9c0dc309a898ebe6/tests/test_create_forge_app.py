"""
Tests for scripts/create_forge_app.py
"""
import os
import subprocess
import unittest
from unittest.mock import patch, MagicMock, call

from scripts import create_forge_app as cfa


SAMPLE_TEMPLATES = [
    {"name": "jira-issue-panel-ui-kit", "description": "Jira issue panel"},
    {"name": "confluence-macro-ui-kit", "description": "Confluence macro"},
]


class TestValidatePrerequisites(unittest.TestCase):

    @patch("scripts.create_forge_app.subprocess.run")
    def test_returns_true_when_both_present(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(cfa.validate_prerequisites())

    @patch("scripts.create_forge_app.subprocess.run")
    def test_returns_false_when_forge_missing(self, mock_run):
        mock_run.side_effect = FileNotFoundError("forge not found")
        self.assertFalse(cfa.validate_prerequisites())

    @patch("scripts.create_forge_app.subprocess.run")
    def test_returns_false_when_command_fails(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "forge")
        self.assertFalse(cfa.validate_prerequisites())


class TestValidateTemplate(unittest.TestCase):

    @patch("scripts.create_forge_app.list_templates_module.fetch_templates",
           return_value=SAMPLE_TEMPLATES)
    def test_valid_template_returns_true(self, mock_fetch):
        is_valid, suggestions = cfa.validate_template("jira-issue-panel-ui-kit")
        self.assertTrue(is_valid)
        self.assertIsNone(suggestions)

    @patch("scripts.create_forge_app.list_templates_module.fetch_templates",
           return_value=SAMPLE_TEMPLATES)
    def test_invalid_template_returns_false_with_suggestions(self, mock_fetch):
        is_valid, suggestions = cfa.validate_template("jira-nonexistent")
        self.assertFalse(is_valid)
        self.assertIsNotNone(suggestions)

    @patch("scripts.create_forge_app.list_templates_module.fetch_templates",
           return_value=SAMPLE_TEMPLATES)
    def test_suggestions_contain_similar_templates(self, mock_fetch):
        is_valid, suggestions = cfa.validate_template("jira-panel")
        self.assertFalse(is_valid)
        # "jira" keyword matches "jira-issue-panel-ui-kit"
        self.assertTrue(any("jira" in s for s in suggestions))

    @patch("scripts.create_forge_app.list_templates_module.fetch_templates",
           side_effect=Exception("network error"))
    def test_assumes_valid_if_validation_fails(self, mock_fetch):
        # When we can't fetch templates, assume valid to avoid blocking the user
        is_valid, suggestions = cfa.validate_template("any-template")
        self.assertTrue(is_valid)


class TestDiscoverDevSpaces(unittest.TestCase):

    def _mock_cli(self, json_output, returncode=0, stderr=""):
        import json as _json
        return MagicMock(
            returncode=returncode,
            stdout=_json.dumps(json_output) if isinstance(json_output, (list, dict)) else json_output,
            stderr=stderr,
        )

    @patch("scripts.create_forge_app.subprocess.run")
    def test_returns_spaces_list(self, mock_run):
        mock_run.return_value = self._mock_cli([{"id": "abc", "name": "My Space"}])
        result = cfa.discover_dev_spaces()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "abc")

    @patch("scripts.create_forge_app.subprocess.run")
    def test_returns_empty_list_when_no_spaces(self, mock_run):
        mock_run.return_value = self._mock_cli([])
        result = cfa.discover_dev_spaces()
        self.assertEqual(result, [])

    @patch("scripts.create_forge_app.subprocess.run")
    def test_returns_empty_list_on_cli_failure(self, mock_run):
        mock_run.return_value = self._mock_cli("", returncode=1, stderr="not logged in")
        result = cfa.discover_dev_spaces()
        self.assertEqual(result, [])

    @patch("scripts.create_forge_app.subprocess.run",
           side_effect=Exception("error"))
    def test_returns_empty_list_on_exception(self, mock_run):
        result = cfa.discover_dev_spaces()
        self.assertEqual(result, [])


class TestCreateApp(unittest.TestCase):

    @patch("scripts.create_forge_app.subprocess.run")
    @patch("scripts.create_forge_app.validate_template", return_value=(True, None))
    @patch("scripts.create_forge_app.validate_prerequisites", return_value=True)
    def test_creates_app_successfully(self, mock_prereqs, mock_validate, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        with patch("scripts.create_forge_app.os.path.isdir", return_value=True), \
             patch("scripts.create_forge_app.os.path.exists", return_value=False):
            result = cfa.create_app(
                template="jira-issue-panel-ui-kit",
                app_name="my-app",
                output_dir="/tmp",
                dev_space_id="abc-123"
            )

        self.assertTrue(result)
        # Verify forge create was called with correct args
        call_args = mock_run.call_args[0][0]
        self.assertIn("forge", call_args)
        self.assertIn("create", call_args)
        self.assertIn("--template", call_args)
        self.assertIn("jira-issue-panel-ui-kit", call_args)
        self.assertIn("my-app", call_args)
        self.assertIn("--developer-space-id", call_args)
        self.assertIn("abc-123", call_args)

    @patch("scripts.create_forge_app.validate_prerequisites", return_value=False)
    def test_returns_false_when_prerequisites_missing(self, mock_prereqs):
        result = cfa.create_app("jira-issue-panel-ui-kit", "my-app", dev_space_id="abc")
        self.assertFalse(result)

    @patch("scripts.create_forge_app.validate_template", return_value=(False, ["jira-issue-panel-ui-kit"]))
    @patch("scripts.create_forge_app.validate_prerequisites", return_value=True)
    def test_returns_false_for_invalid_template(self, mock_prereqs, mock_validate):
        result = cfa.create_app("bad-template", "my-app", dev_space_id="abc")
        self.assertFalse(result)

    @patch("scripts.create_forge_app.validate_template", return_value=(True, None))
    @patch("scripts.create_forge_app.validate_prerequisites", return_value=True)
    def test_returns_false_without_dev_space_id(self, mock_prereqs, mock_validate):
        result = cfa.create_app("jira-issue-panel-ui-kit", "my-app", dev_space_id=None)
        self.assertFalse(result)

    @patch("scripts.create_forge_app.validate_template", return_value=(True, None))
    @patch("scripts.create_forge_app.validate_prerequisites", return_value=True)
    def test_returns_false_when_output_dir_missing(self, mock_prereqs, mock_validate):
        with patch("scripts.create_forge_app.os.path.isdir", return_value=False):
            result = cfa.create_app(
                "jira-issue-panel-ui-kit", "my-app",
                output_dir="/nonexistent",
                dev_space_id="abc"
            )
        self.assertFalse(result)

    @patch("scripts.create_forge_app.validate_template", return_value=(True, None))
    @patch("scripts.create_forge_app.validate_prerequisites", return_value=True)
    def test_returns_false_when_app_dir_already_exists(self, mock_prereqs, mock_validate):
        with patch("scripts.create_forge_app.os.path.isdir", return_value=True), \
             patch("scripts.create_forge_app.os.path.exists", return_value=True):
            result = cfa.create_app(
                "jira-issue-panel-ui-kit", "my-app",
                output_dir="/tmp",
                dev_space_id="abc"
            )
        self.assertFalse(result)

    @patch("scripts.create_forge_app.subprocess.run")
    @patch("scripts.create_forge_app.validate_template", return_value=(True, None))
    @patch("scripts.create_forge_app.validate_prerequisites", return_value=True)
    def test_returns_false_on_forge_create_failure(self, mock_prereqs, mock_validate, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="forge error")

        with patch("scripts.create_forge_app.os.path.isdir", return_value=True), \
             patch("scripts.create_forge_app.os.path.exists", return_value=False):
            result = cfa.create_app(
                "jira-issue-panel-ui-kit", "my-app",
                output_dir="/tmp",
                dev_space_id="abc"
            )
        self.assertFalse(result)

    @patch("scripts.create_forge_app.subprocess.run")
    @patch("scripts.create_forge_app.validate_template", return_value=(True, None))
    @patch("scripts.create_forge_app.validate_prerequisites", return_value=True)
    def test_runs_from_parent_directory(self, mock_prereqs, mock_validate, mock_run):
        """forge create should be run from the parent directory, not the app directory."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        with patch("scripts.create_forge_app.os.path.isdir", return_value=True), \
             patch("scripts.create_forge_app.os.path.exists", return_value=False), \
             patch("scripts.create_forge_app.os.path.abspath", return_value="/parent"):
            cfa.create_app(
                "jira-issue-panel-ui-kit", "my-app",
                output_dir="/parent",
                dev_space_id="abc"
            )

        call_kwargs = mock_run.call_args[1]
        self.assertEqual(call_kwargs.get("cwd"), "/parent")

    @patch("scripts.create_forge_app.subprocess.run")
    @patch("scripts.create_forge_app.validate_template", return_value=(True, None))
    @patch("scripts.create_forge_app.validate_prerequisites", return_value=True)
    def test_stamps_skill_name_env_var(self, mock_prereqs, mock_validate, mock_run):
        """forge create must carry the skill-name attribution env var."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        with patch("scripts.create_forge_app.os.path.isdir", return_value=True), \
             patch("scripts.create_forge_app.os.path.exists", return_value=False):
            cfa.create_app(
                "jira-issue-panel-ui-kit", "my-app",
                output_dir="/tmp", dev_space_id="abc-123",
            )

        env = mock_run.call_args[1].get("env")
        self.assertIsNotNone(env)
        self.assertEqual(env["ATL_FORGE_ATTRIBUTION_SKILL_NAME"], "forge-app-builder")


if __name__ == "__main__":
    unittest.main()
