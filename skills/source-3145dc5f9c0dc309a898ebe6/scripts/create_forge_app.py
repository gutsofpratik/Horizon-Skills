#!/usr/bin/env python3
"""
Automated Forge App Creation Script
Wraps 'forge create' command with non-interactive mode and better error handling.

Run from the skill directory: python -m scripts.create_forge_app
"""

import subprocess
import sys
import argparse
import os
import re
import json

# Relative imports — scripts/ is a package; run as python -m scripts.create_forge_app from skill dir
from . import list_templates as list_templates_module
from .forge_env import forge_env

# Environment for every Forge CLI invocation this script spawns.
_FORGE_ENV = forge_env("forge-app-builder")

def validate_prerequisites():
    """Check if Forge CLI and Node.js are available"""
    try:
        subprocess.run(['forge', '--version'], capture_output=True, check=True, env=_FORGE_ENV)
        subprocess.run(['node', '-v'], capture_output=True, check=True, env=_FORGE_ENV)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def validate_template(template_name):
    """
    Validate that a template name is valid by checking against the official registry
    Returns (is_valid, suggestions) tuple
    """
    try:
        templates = list_templates_module.fetch_templates()
        template_names = [t['name'] for t in templates]
        
        if template_name in template_names:
            return True, None
        
        # Find similar templates for suggestion
        words = template_name.lower().replace('-', ' ').split()
        suggestions = []
        for valid_template in template_names:
            valid_words = valid_template.lower().replace('-', ' ').split()
            if any(word in valid_words for word in words):
                suggestions.append(valid_template)
        
        return False, suggestions[:5] if suggestions else template_names[:5]
        
    except Exception as e:
        print(f"⚠️  Could not validate template: {e}")
        return True, None  # Assume valid if validation fails

def discover_dev_spaces():
    """
    Discover available developer spaces via the Forge CLI.
    Returns a list of {'id': str, 'name': str} dictionaries.
    """
    try:
        result = subprocess.run(
            ['forge', 'developer-spaces', 'list', '--json'],
            capture_output=True, text=True, timeout=30, env=_FORGE_ENV,
        )
        if result.returncode != 0:
            print(f"⚠️  forge developer-spaces list failed: {result.stderr.strip()}")
            return []

        raw = json.loads(result.stdout)
        spaces = raw if isinstance(raw, list) else raw.get("data", raw.get("spaces", []))
        return [
            {"id": entry.get("id") or entry.get("developerSpaceId"), "name": entry.get("name", "")}
            for entry in spaces
            if entry.get("id") or entry.get("developerSpaceId")
        ]
    except Exception as e:
        print(f"⚠️  Could not discover developer spaces: {e}")
        return []

def create_app(template, app_name, output_dir=None, dev_space_id=None):
    """
    Create a Forge app using 'forge create'
    
    Args:
        template: Template name (e.g., 'jira-issue-panel-ui-kit')
        app_name: Name for the new app
        output_dir: Parent directory where the app folder will be created.
                    The script cd's into this directory before running forge create
                    so the app folder is created as a subdirectory.
        dev_space_id: Developer space ID to use (required)
    
    Returns:
        True if successful, False otherwise
    """
    
    if not validate_prerequisites():
        print("❌ Prerequisites missing. Ensure Forge CLI and a currently supported Node.js version are installed.")
        print("   Install: npm install -g @forge/cli")
        return False
    
    # Validate template
    is_valid, suggestions = validate_template(template)
    if not is_valid:
        print(f"❌ Template '{template}' is not recognized.")
        print(f"\n📋 Did you mean one of these?")
        for suggestion in suggestions:
            print(f"   - {suggestion}")
        print(f"\n💡 To see all available templates, run:")
        print(f"   python -m scripts.list_templates --list")
        return False
    
    if not dev_space_id:
        print("❌ Developer space ID is required. Please use --dev-space-id flag.")
        return False

    # Resolve the working directory for forge create.
    # We cd into output_dir (the parent) and let forge create the app subfolder,
    # instead of using forge's --directory flag which treats the path as the
    # full output path and fails if it already exists.
    cwd = os.path.abspath(output_dir) if output_dir else os.getcwd()

    if not os.path.isdir(cwd):
        print(f"❌ Parent directory does not exist: {cwd}")
        return False

    app_path = os.path.join(cwd, app_name)
    if os.path.exists(app_path):
        print(f"❌ Directory already exists: {app_path}")
        print(f"   Choose a different app name or remove the existing folder.")
        return False

    # Build command — no --directory flag; we run from the parent dir instead
    cmd = ['forge', 'create', '--template', template, app_name]
    
    if dev_space_id:
        cmd.extend(['--developer-space-id', dev_space_id])
        cmd.append('--accept-terms')
    
    try:
        print(f"\n📦 Creating Forge app: {app_name}")
        print(f"📋 Template: {template}")
        print(f"📂 Location: {cwd}")
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=_FORGE_ENV)

        if result.returncode != 0:
            stderr = result.stderr.strip()
            stdout = result.stdout.strip()
            print(f"❌ Failed to create app (exit code {result.returncode})")
            if stdout:
                print(f"\n--- stdout ---\n{stdout}")
            if stderr:
                print(f"\n--- stderr ---\n{stderr}")
            return False
        
        print(f"✅ App created successfully at: {app_path}")
        print(f"📝 Next steps:")
        print(f"   1. cd {app_path}")
        print(f"   2. npm install")
        print(f"   3. Customize the code")
        print(f"   4. Deploy with: forge deploy --non-interactive -e development")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create app: {e}")
        if e.stdout:
            print(f"\n--- stdout ---\n{e.stdout}")
        if e.stderr:
            print(f"\n--- stderr ---\n{e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Automated Forge app creation with developer space selection'
    )
    parser.add_argument('--template', required=True, help='Forge template (e.g., jira-issue-panel-ui-kit)')
    parser.add_argument('--name', required=True, help='App name')
    parser.add_argument('--directory', help='Output directory (defaults to current directory)')
    parser.add_argument('--dev-space-id', help='Developer space ID (if not provided, will prompt for selection)')
    
    args = parser.parse_args()
    
    # Step 1: Get developer space ID (either from arg or by discovery + prompt)
    dev_space_id = args.dev_space_id
    
    if not dev_space_id:
        # Step 1a: Discover developer spaces
        print("🔍 Step 1: Discovering your Developer Spaces...\n")
        dev_spaces = discover_dev_spaces()
        
        if not dev_spaces:
            print("\n❌ Could not discover any developer spaces.")
            print("\n📋 Please create a developer space at:")
            print("   https://developer.atlassian.com/console/")
            print("\nThen run this script again, or use 'forge create' interactively:")
            print(f"   ATL_FORGE_ATTRIBUTION_SKILL_NAME=forge-app-builder forge create --template {args.template} {args.name}")
            sys.exit(1)
        
        # Step 1b: Ask user which dev space to use
        print(f"✅ Found {len(dev_spaces)} developer space(s):\n")
        for i, space in enumerate(dev_spaces, 1):
            print(f"  {i}. {space['name']}")
            print(f"     ID: {space['id']}\n")
        
        if len(dev_spaces) == 1:
            choice = input(f"Use '{dev_spaces[0]['name']}'? [Y/n]: ").strip().lower()
            if choice in ['', 'y', 'yes']:
                dev_space_id = dev_spaces[0]['id']
                print(f"✅ Selected: {dev_spaces[0]['name']}\n")
            else:
                print("❌ Cancelled by user")
                sys.exit(1)
        else:
            while True:
                try:
                    choice = input(f"Select a Developer Space (1-{len(dev_spaces)}): ").strip()
                    idx = int(choice) - 1
                    if 0 <= idx < len(dev_spaces):
                        dev_space_id = dev_spaces[idx]['id']
                        print(f"✅ Selected: {dev_spaces[idx]['name']}\n")
                        break
                    else:
                        print(f"❌ Please enter a number between 1 and {len(dev_spaces)}")
                except ValueError:
                    print("❌ Please enter a valid number")
                except KeyboardInterrupt:
                    print("\n❌ Cancelled by user")
                    sys.exit(1)
    
    # Step 2: Create the app with the selected developer space
    print(f"📦 Step 2: Creating Forge app with selected developer space...\n")
    success = create_app(args.template, args.name, args.directory, dev_space_id)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
