# Copyright (c) 2026 DataRobot, Inc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Print the current user's effective DataRobot workload scaling limits.

Reads DATAROBOT_ENDPOINT (must include /api/v2) and DATAROBOT_API_TOKEN from
the environment.  Limits are set by the org admin; a value of 0 means
unlimited.

Usage:
    python check_limits.py [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, cast

import httpx


def fetch_limits(base: str, headers: dict[str, str]) -> dict[str, Any]:
    """GET /account/info/, return the limits block plus user/org ids for context."""
    r = httpx.get(f"{base}/account/info/", headers=headers, timeout=15)
    r.raise_for_status()
    data = cast(dict[str, Any], r.json())
    return {
        "uid": data.get("uid"),
        "email": data.get("email"),
        "orgId": data.get("orgId"),
        "tenantId": data.get("tenantId"),
        "limits": data.get("limits") or {},
    }


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = p.parse_args()

    base = os.environ.get("DATAROBOT_ENDPOINT", "").rstrip("/")
    token = os.environ.get("DATAROBOT_API_TOKEN", "")
    if not base or not token:
        print(
            "DATAROBOT_ENDPOINT and DATAROBOT_API_TOKEN must be set.", file=sys.stderr
        )
        return 1
    headers = {"Authorization": f"Bearer {token}"}

    info = fetch_limits(base, headers)
    if args.json:
        print(json.dumps(info, indent=2, default=str))
        return 0

    limits = info["limits"]
    mcw = limits.get("maxConcurrentWorkloads")
    mwr = limits.get("maxWorkloadReplicas")

    def fmt(val: Any) -> str:
        if val is None:
            return "not set"
        if val == 0:
            return "unlimited (0)"
        return str(val)

    print(f"User:      {info.get('email')} ({info.get('uid')})")
    print(f"Org ID:    {info.get('orgId')}")
    print(f"Tenant:    {info.get('tenantId')}")
    print()
    print(f"  maxConcurrentWorkloads: {fmt(mcw)}")
    print(f"  maxWorkloadReplicas:    {fmt(mwr)}")
    print()
    print(
        "These are the effective limits as resolved server-side. "
        "Limits are admin-set; users cannot change them. "
        "Exceeding either returns HTTP 403 from POST /workloads/ create or "
        "PATCH /workloads/{id}/settings/ scale. "
        "The org-level and per-user-in-org endpoints exist in the spec but "
        "require Admin API access — `/account/info/` (above) is the only path "
        "a regular user has."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
