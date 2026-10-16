#!/usr/bin/env python3
"""Resolve exact assets from the shared catalog without modifying the package."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ROLES = ("master", "example", "preview")
FORMATS = {"docx": "host-document", "xlsx": "host-spreadsheet", "pptx": "host-presentation"}


def contained_path(root, relative):
    if not isinstance(relative, str) or "\\" in relative:
        raise ValueError("Invalid catalog path")
    parts = PurePosixPath(relative)
    if parts.is_absolute() or any(p in ("", ".", "..") for p in relative.split("/")):
        raise ValueError(f"Unsafe catalog path: {relative}")
    path = (root / relative).resolve(strict=True)
    if not path.is_file() or root.resolve() not in path.parents:
        raise ValueError(f"Catalog path escapes skill or is not a file: {relative}")
    return path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_catalog(root=ROOT, expected_catalog_sha256=None):
    data = contained_path(root, "assets/catalog.json").read_bytes()
    sha256 = digest(data)
    if expected_catalog_sha256 is not None and sha256 != expected_catalog_sha256:
        raise ValueError("Selected catalog revision is unavailable (catalog checksum mismatch)")
    catalog = json.loads(data)
    if catalog.get("schema_version") != 1 or not isinstance(catalog.get("templates"), list):
        raise ValueError("Unsupported template catalog schema")
    if not isinstance(catalog.get("library_revision"), str) or catalog.get("adaptation_skill") != "govtribe-document-editing":
        raise ValueError("Invalid catalog identity or adaptation skill")
    source_catalog_sha256 = catalog.get("source_catalog_sha256")
    if not isinstance(source_catalog_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", source_catalog_sha256):
        raise ValueError("Invalid source catalog provenance")
    seen = set()
    for template in catalog["templates"]:
        template_id = template.get("id", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", template_id) or template_id in seen:
            raise ValueError(f"Invalid or duplicate template ID: {template_id}")
        seen.add(template_id)
        if template.get("format") not in FORMATS or template.get("format_skill") != FORMATS[template["format"]]:
            raise ValueError(f"Invalid format mapping: {template_id}")
        for field in ("display_name", "domain_skill", "completion_reference"):
            if not isinstance(template.get(field), str) or not template[field]:
                raise ValueError(f"Missing {field}: {template_id}")
        if template["completion_reference"] != f"references/{template_id}.md":
            raise ValueError(f"Invalid completion reference: {template_id}")
        for role in ROLES:
            asset = template.get(role, {})
            if not isinstance(asset, dict) or not isinstance(asset.get("path"), str):
                raise ValueError(f"Missing {role}: {template_id}")
            if not asset["path"].startswith(f"assets/{template_id}/"):
                raise ValueError(f"Unexpected {role} directory: {template_id}")
            if not re.fullmatch(r"[0-9a-f]{64}", asset.get("sha256", "")) or type(asset.get("bytes")) is not int or asset["bytes"] <= 0:
                raise ValueError(f"Invalid {role} integrity metadata: {template_id}")
            if not re.fullmatch(r"[0-9a-f]{64}", asset.get("source_sha256", "")) or type(asset.get("source_bytes")) is not int or asset["source_bytes"] <= 0:
                raise ValueError(f"Invalid {role} source provenance: {template_id}")
            suffix = PurePosixPath(asset["path"]).suffix
            if suffix != (".png" if role == "preview" else "." + template["format"]):
                raise ValueError(f"Invalid {role} extension: {template_id}")
        if template["master"]["path"] == template["example"]["path"]:
            raise ValueError(f"Master and example must be distinct: {template_id}")
    return catalog, sha256


def resolve(template_id, root=ROOT, expected_catalog_sha256=None, expected_master_sha256=None):
    catalog, catalog_sha256 = load_catalog(root, expected_catalog_sha256)
    template = next((t for t in catalog["templates"] if t["id"] == template_id), None)
    if template is None:
        raise ValueError(f"Unknown template ID: {template_id}")
    if expected_master_sha256 is not None and template["master"]["sha256"] != expected_master_sha256:
        raise ValueError("Selected master revision is unavailable (master checksum mismatch)")
    result = dict(template, library_revision=catalog["library_revision"], catalog_sha256=catalog_sha256,
                  adaptation_skill=catalog["adaptation_skill"],
                  source_catalog_sha256=catalog["source_catalog_sha256"])
    result["completion_reference_path"] = str(contained_path(root, template["completion_reference"]))
    for role in ROLES:
        asset = template[role]
        path = contained_path(root, asset["path"])
        data = path.read_bytes()
        if len(data) != asset["bytes"] or digest(data) != asset["sha256"]:
            raise ValueError(f"Asset checksum mismatch: {asset['path']}")
        result[role] = dict(asset, absolute_path=str(path))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template_id", nargs="?")
    parser.add_argument("--verify-all", action="store_true")
    parser.add_argument("--expected-catalog-sha256")
    parser.add_argument("--expected-master-sha256")
    args = parser.parse_args()
    if bool(args.template_id) == args.verify_all or (args.verify_all and args.expected_master_sha256):
        parser.error("Select one template ID or --verify-all; expected master applies to one template")
    try:
        if args.verify_all:
            catalog, _ = load_catalog(expected_catalog_sha256=args.expected_catalog_sha256)
            result = [resolve(t["id"], expected_catalog_sha256=args.expected_catalog_sha256) for t in catalog["templates"]]
        else:
            result = resolve(args.template_id, expected_catalog_sha256=args.expected_catalog_sha256,
                             expected_master_sha256=args.expected_master_sha256)
        print(json.dumps({"ok": True, "result": result}, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
