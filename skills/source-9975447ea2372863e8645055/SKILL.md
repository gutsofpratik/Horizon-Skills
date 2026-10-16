---
name: user-role
description: Use when the user wants to manage database users, roles, passwords, or access privileges in Milvus.
---

## Prerequisites

1. CLI installed, logged in, and cluster context set (see setup skill).

## Commands Reference

### Users

#### Create a User

```bash
zilliz user create --user <username> --password <password>
```

*Create a new database user.*

#### List Users

```bash
zilliz user list
```

*List all database users.*

#### Describe a User

```bash
zilliz user describe --user <username>
```

*Get details of a user.*

#### Drop a User

```bash
zilliz user drop --user <username-to-drop>
```

*Drop a database user.*

#### Update Password

```bash
zilliz user update-password \
  --user <username> \
  --password <current-password> \
  --new-password <new-password>
```

*Update user password.*

#### Grant a Role to a User

```bash
zilliz user grant-role --user <username> --role <role-name-to-grant>
```

*Grant a role to a user.*

#### Revoke a Role from a User

```bash
zilliz user revoke-role --user <username> --role <role-name-to-revoke>
```

*Revoke a role from a user.*

### Roles

#### Create a Role

```bash
zilliz role create --role <role-name>
```

*Create a new role.*

#### List Roles

```bash
zilliz role list
```

*List all roles.*

#### Describe a Role

```bash
zilliz role describe --role <role-name>
```

*Get details and privileges of a role.*

#### Drop a Role

```bash
zilliz role drop --role <role-name-to-drop>
```

*Drop a role.*

#### Grant a Privilege

```bash
zilliz role grant-privilege \
  --role <role-name> \
  --object-type <Global|Collection|Database> \
  --object-name <object-name> \
  --privilege <privilege-name>
# Optional: --database <database-name>
```

*Grant a privilege to a role.*

#### Revoke a Privilege

```bash
zilliz role revoke-privilege \
  --role <role-name> \
  --object-type <Global|Collection|Database> \
  --object-name <object-name> \
  --privilege <privilege-name>
# Optional: --database <database-name>
```

*Revoke a privilege from a role.*

## Common Privileges

Common privileges by object type:

- **Collection**: `Search`, `Query`, `Insert`, `Delete`, `CreateIndex`, `DropCollection`
- **Global**: `CreateCollection`, `All`
- **Database**: `ListCollections`

## Guidance

- User and role management is only available on **Dedicated** clusters.
- Built-in roles: `admin` (full access), `public` (no privileges by default -- must be granted explicitly).
- When setting up RBAC, suggest a workflow: create role, grant privileges, create user, assign role.
- Before dropping a user or role, confirm with the user.
- Use `*` as object-name to grant privilege on all objects of that type.
- These commands are **Milvus database RBAC**, scoped to one cluster. They do
  not control who can create, modify, or delete cloud resources -- that is
  cloud-level RBAC over organizations and projects, managed with `zilliz acl`
  (see the acl skill). Granting a Milvus role never grants cloud permissions,
  and vice versa.
