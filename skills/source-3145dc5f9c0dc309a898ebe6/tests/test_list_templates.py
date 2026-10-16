"""
Tests for scripts/list_templates.py
"""
import json
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from scripts import list_templates as lt


SAMPLE_TEMPLATES = [
    {"name": "jira-issue-panel-ui-kit", "description": "Jira issue panel using UI Kit"},
    {"name": "jira-dashboard-gadget", "description": "Jira dashboard gadget"},
    {"name": "jira-service-management-portal-footer", "description": "JSM portal footer"},
    {"name": "confluence-macro-ui-kit", "description": "Confluence macro using UI Kit"},
    {"name": "bitbucket-pipeline-extension", "description": "Bitbucket pipeline extension"},
    {"name": "compass-component-page", "description": "Compass component page"},
    {"name": "rovo-agent", "description": "Rovo agent"},
    {"name": "automation-rule", "description": "Automation rule"},
    {"name": "dashboards-overview-gadget", "description": "Dashboards gadget"},
    {"name": "teamwork-graph-extension", "description": "Teamwork Graph extension"},
    {"name": "custom-app", "description": "Generic custom app"},
]


class TestFetchTemplates(unittest.TestCase):

    @patch("scripts.list_templates.urllib.request.urlopen")
    def test_fetch_templates_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(SAMPLE_TEMPLATES).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = lt.fetch_templates()
        self.assertEqual(len(result), len(SAMPLE_TEMPLATES))
        self.assertEqual(result[0]["name"], "jira-issue-panel-ui-kit")

    @patch("scripts.list_templates.urllib.request.urlopen")
    def test_fetch_templates_network_error(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Network error")
        with self.assertRaises(SystemExit) as cm:
            lt.fetch_templates()
        self.assertEqual(cm.exception.code, 1)


class TestCategorizeTemplates(unittest.TestCase):

    def test_jira_templates_categorized(self):
        categories = lt.categorize_templates(SAMPLE_TEMPLATES)
        self.assertIn("Jira", categories)
        self.assertIn("jira-issue-panel-ui-kit", categories["Jira"])
        self.assertIn("jira-dashboard-gadget", categories["Jira"])

    def test_jsm_templates_separate_from_jira(self):
        categories = lt.categorize_templates(SAMPLE_TEMPLATES)
        self.assertIn("Jira Service Management", categories)
        self.assertIn("jira-service-management-portal-footer", categories["Jira Service Management"])
        self.assertNotIn("jira-service-management-portal-footer", categories.get("Jira", []))

    def test_confluence_templates_categorized(self):
        categories = lt.categorize_templates(SAMPLE_TEMPLATES)
        self.assertIn("Confluence", categories)
        self.assertIn("confluence-macro-ui-kit", categories["Confluence"])

    def test_bitbucket_templates_categorized(self):
        categories = lt.categorize_templates(SAMPLE_TEMPLATES)
        self.assertIn("Bitbucket", categories)
        self.assertIn("bitbucket-pipeline-extension", categories["Bitbucket"])

    def test_rovo_templates_categorized(self):
        categories = lt.categorize_templates(SAMPLE_TEMPLATES)
        self.assertIn("Rovo", categories)
        self.assertIn("rovo-agent", categories["Rovo"])

    def test_other_category_for_unrecognized(self):
        categories = lt.categorize_templates(SAMPLE_TEMPLATES)
        self.assertIn("Other", categories)
        self.assertIn("custom-app", categories["Other"])

    def test_empty_categories_excluded(self):
        # Only Jira templates — no Confluence category should appear
        jira_only = [{"name": "jira-issue-panel-ui-kit", "description": ""}]
        categories = lt.categorize_templates(jira_only)
        self.assertNotIn("Confluence", categories)

    def test_categories_are_sorted(self):
        categories = lt.categorize_templates(SAMPLE_TEMPLATES)
        for category, templates in categories.items():
            self.assertEqual(templates, sorted(templates),
                             f"Templates in '{category}' are not sorted")


class TestValidateTemplate(unittest.TestCase):

    def test_valid_template(self):
        captured = StringIO()
        with patch("sys.stdout", captured):
            result = lt.validate_template("jira-issue-panel-ui-kit", SAMPLE_TEMPLATES)
        self.assertTrue(result)

    def test_invalid_template(self):
        captured = StringIO()
        with patch("sys.stdout", captured):
            result = lt.validate_template("nonexistent-template", SAMPLE_TEMPLATES)
        self.assertFalse(result)

    def test_invalid_template_suggests_similar(self):
        captured = StringIO()
        with patch("sys.stdout", captured):
            lt.validate_template("jira-panel", SAMPLE_TEMPLATES)
        output = captured.getvalue()
        # Should suggest jira templates since "jira" matches
        self.assertIn("jira", output.lower())

    def test_invalid_template_suggests_product_match(self):
        captured = StringIO()
        with patch("sys.stdout", captured):
            lt.validate_template("confluence-nonexistent", SAMPLE_TEMPLATES)
        output = captured.getvalue()
        self.assertIn("confluence", output.lower())


class TestListTemplates(unittest.TestCase):

    @patch("scripts.list_templates.fetch_templates", return_value=SAMPLE_TEMPLATES)
    def test_list_templates_text_format(self, mock_fetch):
        output = lt.list_templates(format="text")
        self.assertIn("FORGE TEMPLATES", output)
        self.assertIn("jira-issue-panel-ui-kit", output)
        self.assertIn("confluence-macro-ui-kit", output)

    @patch("scripts.list_templates.fetch_templates", return_value=SAMPLE_TEMPLATES)
    def test_list_templates_json_format(self, mock_fetch):
        output = lt.list_templates(format="json")
        parsed = json.loads(output)
        self.assertIn("templates", parsed)
        self.assertIn("count", parsed)
        self.assertEqual(parsed["count"], len(SAMPLE_TEMPLATES))
        self.assertEqual(parsed["templates"], sorted(t["name"] for t in SAMPLE_TEMPLATES))

    @patch("scripts.list_templates.fetch_templates", return_value=SAMPLE_TEMPLATES)
    def test_list_templates_includes_source_url(self, mock_fetch):
        output = lt.list_templates(format="text")
        self.assertIn(lt.TEMPLATE_REGISTRY_URL, output)


if __name__ == "__main__":
    unittest.main()
