---
name: acl
description: Use when the user wants to manage Zilliz Cloud access control -- custom org or project roles and their policies, granting or revoking a role for an organization member, or binding roles to a SCIM user group. This is cloud-level RBAC over organizations, projects, and clusters -- for database users and privileges inside Milvus see the user-role skill.
---

## Prerequisites

1. CLI installed and logged in (see setup skill).
2. No cluster context required -- these are control-plane operations.
3. The `/v2/roles`, `/v2/members`, and `/v2/groups` routes must be enabled
   for the caller's endpoint. They are still rolling out: a 404 from any
   `zilliz acl` command means the API is not live there yet.

## Commands Reference

`zilliz acl` is a three-level tree -- `acl role`, `acl member`, and `acl group`. It is deliberately absent from `zilliz --help` and shell completion while the routes roll out, but every command below runs today and every `--help` under it works.

### Roles

```bash
# One project's roles: the pre-defined project roles plus that project's
# custom roles. --project-id is required; it is prompted for when omitted.
zilliz acl role list --project-id <project-id>
# Optional: --page <n>, --page-size <n>, --all

# Org roles (--project-id is rejected here: org roles have no project boundary)
zilliz acl role list --type org

zilliz acl role describe <role-id>
# Optional: --project-id <project-id>

zilliz acl role principals <role-id> --all
# Optional: --project-id <project-id>, --page <n>, --page-size <n>
# Lists the members, groups, and API keys the role is bound to.

zilliz acl role delete <role-id>
# Optional: --project-id <project-id>
# Confirms first; pass -y to skip.
```

`--project-id` on `describe`, `principals`, and `delete` is the project boundary
of a *pre-defined* project role, which carries none of its own. A custom role is
addressed by ID alone.

### Create and update a role

```bash
zilliz acl role create --name <role-name> --project-id <project-id> \
  --policy project_member:view \
  --policy 'serving_cluster:view,modify=in01-a,in01-b'
# Optional: --description <text>, --policies-file <path>

zilliz acl role update <role-id> --description <text>
# Optional:
#   --name <role-name>
#   --project-id <project-id>
#   --policy <shorthand>
#   --policies-file <path>
#   -y
```

Only **project** roles can be created; the API has no org-role create path.
`update` replaces the policy wholesale -- it never merges -- and prompts before
shrinking the statement count unless `-y` is passed.

### Writing a policy

Three ways to supply the policy on `role create` and `role update`:

1. **Shorthand** (`--policy`, repeatable), validated locally before the request:

   ```
   RESOURCE:ACTION[,ACTION...][=SELECTION[,SELECTION...]][@cluster=CLUSTER_ID]
   ```

   ```bash
   --policy project_member:view
   --policy 'serving_cluster:view,modify=in01-a,in01-b'
   --policy 'serving_cluster_data:read=mydb/*@cluster=in01-abc'
   --policy 'volume_data:read,write=*'
   ```

   `SELECTION` picks which instances the statement covers; `*` means all, and
   data resources also accept the `db/collection` form. `@cluster=` is an
   optional trailing marker, so an `@` inside a selection value is left alone.

2. **JSON file** (`--policies-file <path>`, `-` reads stdin), taking the
   `policies` array exactly as the API defines it. Mutually exclusive with
   `--policy`:

   ```json
   [
     { "resourceType": "serving_cluster", "privileges": ["view"], "resources": ["in01-a"] },
     { "resourceType": "project_member",  "privileges": ["view"] }
   ]
   ```

3. **Interactive builder**: with neither flag on a terminal, `role create`
   walks through resource, actions, and selection, then prints the equivalent
   `--policy` flags so the run can be scripted next time. Off a terminal with
   neither flag the command errors instead.

### Members

```bash
zilliz acl member roles <email|user-id>
zilliz acl member grant <email|user-id> --role <role-id|role-name>
zilliz acl member revoke <email|user-id> --role <role-id|role-name>
# Optional on grant/revoke: --project-id <project-id>; revoke also takes -y
```

The member argument takes an email or a `usr-` user ID. An email costs one
extra lookup to resolve; a user ID goes straight through.

### Groups

```bash
zilliz acl group list
# Optional: --name <text>, --page <n>, --page-size <n>, --all

zilliz acl group members <group-id>
# Optional: --page <n>, --page-size <n>, --all

zilliz acl group roles <group-id>
zilliz acl group grant <group-id> --role <role-id|role-name>
zilliz acl group revoke <group-id> --role <role-id|role-name>
# Optional on grant/revoke: --project-id <project-id>; revoke also takes -y
```

Groups come from SCIM provisioning; this command tree reads them and manages
their role bindings, it does not create them.

### Project scoping

`--project-id` is prompted for only where the API genuinely requires it, and the
answer is used for that invocation alone -- it is never written to
`~/.zilliz/config`.

| Command | Behavior when `--project-id` is absent |
|---|---|
| `role create` | prompts on a terminal; errors otherwise |
| `role list --type project` | prompts on a terminal; errors otherwise |
| `role list --type org` | not applicable -- the flag is rejected outright |
| `member/group grant`, `member/group revoke` | prompts only when the role is a *pre-defined* project role, which carries no boundary of its own |
| the same, given a `--role` *name* | prompts on a terminal when no org role matches the name, since the project-role listing it falls back to requires a project |
| `role update`, `role principals` | proceeds without a project |

### Action catalog

Every `RESOURCE:ACTION` pair `--policy` accepts. A **selectable** resource
takes `=SELECTION` on every action except `create`, which must never carry
one; a resource that is not selectable takes no selection at all.

A resource can appear at both levels with different actions -- read the
Level column before composing a statement.

| Resource | Level | Selectable | Actions |
|---|---|---|---|
| `org_member` | org | no | `view`, `create`, `modify`, `delete` |
| `group` | org | no | `view`, `create`, `modify`, `delete` |
| `api_key` | org | no | `view`, `create`, `modify`, `delete` |
| `org_role` | org | no | `view`, `grant` |
| `project_role` | org | no | `view`, `create`, `modify`, `delete`, `grant` |
| `project` | org | no | `view`, `create` |
| `billing` | org | no | `view`, `manage` |
| `authentication` | org | no | `view`, `manage` |
| `org_control_ops` | org | no | `view`, `modify`, `delete` |
| `recovery` | org | no | `view`, `manage` |
| `project_member` | project | no | `view`, `create`, `modify`, `delete` |
| `project_role` | project | no | `view`, `create`, `modify`, `delete`, `grant` |
| `project` | project | no | `view`, `modify`, `delete` |
| `security` | project | no | `view`, `manage` |
| `backup` | project | no | `view`, `manage` |
| `observability` | project | no | `view`, `manage` |
| `serving_cluster` | project | yes | `create`, `view`, `modify`, `delete` |
| `on_demand_cluster` | project | yes | `create`, `view`, `modify`, `delete` |
| `volume` | project | yes | `create`, `view`, `modify`, `delete`, `usage` |
| `storage_integration` | project | yes | `create`, `view`, `modify`, `delete`, `usage` |
| `model_provider_integration` | project | yes | `create`, `view`, `modify`, `delete`, `usage` |
| `kms_integration` | project | yes | `create`, `view`, `modify`, `delete`, `usage` |
| `datadog_integration` | project | yes | `create`, `view`, `modify`, `delete`, `usage` |
| `serving_cluster_data` | project | yes | `read`, `write`, `all` |
| `on_demand_compute_data` | project | no | `read`, `write`, `all` |
| `volume_data` | project | yes | `read`, `write`, `all` |

## Guidance

- **This is cloud-level RBAC, not Milvus RBAC.** `zilliz acl` governs who can
  act on organizations, projects, clusters, and volumes in Zilliz Cloud. For
  database users, roles, and privileges *inside* a Milvus cluster (`Search`,
  `Insert`, `CreateCollection`, ...) use the `user-role` skill instead. The two
  are separate systems and neither grants the other.
- **Grant and revoke are not idempotent.** Re-granting an existing binding and
  revoking an absent one are both rejected by the backend. Check
  `acl member roles <member>` or `acl role principals <role-id>` first rather
  than retrying a failed call.
- **`--role` takes an ID or an exact name.** A name is matched against the org
  roles first and then inside one project, so granting a *project* role by name
  needs `--project-id` off a terminal. An ambiguous name lists the candidates
  instead of guessing -- pass the role ID to resolve it. Prefer IDs in scripts.
- **Org roles are read-only here.** The backend defines no `org_role`
  create / modify / delete actions, so `role create` is project-only and
  updating or deleting an org role always fails. `role list --type org` and
  `role describe` work normally.
- **A resource can exist at both levels with different actions.** `project_role`
  and `project` appear once as an org-level resource and once as a project-level
  one. Read the Level column before composing a statement; a level mismatch is
  reported as an unknown resource for that level.
- **Selection rules are enforced locally before the request.** An action on a
  selectable resource needs `=SELECTION` -- except `create`, which must never
  carry one. `serving_cluster:create,view=in01-a` is valid: the selection binds
  to `view` only.
- **`role update` replaces the policy wholesale.** To add one statement, read
  the current policy with `role describe` and resend the full set, including the
  statements being kept.
- **Deleting a role cascades to its bindings.** Confirm the blast radius with
  `role principals <role-id>` before deleting, and tell the user who loses
  access.
- The action catalog above is a snapshot of what the backend seeds. It drives
  local validation, so when the server rejects a policy this client accepted,
  surface the server's message verbatim -- it is the authority, not the table.
- A 404 from any `zilliz acl` command means the ACL routes are not enabled on
  that endpoint yet. This is a rollout state, not a permissions problem: tell
  the user to contact support rather than retrying or changing the command.
