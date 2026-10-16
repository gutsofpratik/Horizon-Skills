---
name: rill-rillyaml
description: Detailed instructions and examples for developing the rill.yaml file
---

# Instructions for developing `rill.yaml`

## Introduction

`rill.yaml` is a required configuration file located at the root of every Rill project. It defines project-wide settings, similar to `package.json` in Node.js or `dbt_project.yml` in dbt.

## Core Concepts

### Project metadata

There are no required properties in `rill.yaml`, but it is common to configure:

- `display_name`: Human-readable name shown in the UI
- `description`: Brief description of the project's purpose
- `compiler`: Deprecated property that is commonly found in old projects

### Default OLAP connector

The `olap_connector` property sets the default OLAP database for the project. Models output to this connector by default, and metrics views query from it unless explicitly overridden.

Common values are `duckdb` or `clickhouse`. If not specified, Rill initializes a managed DuckDB database and uses it as the default OLAP connector. 

### Default AI connector

The `ai_connector` property selects the connector powering AI features (developer agent, AI charts, chat). Point it to an AI connector defined in the project, such as `openai`, `claude`, or `gemini`. Defaults to Rill's built-in AI service.

### Mock users for security testing

The `mock_users` property defines test users for validating security policies during local development. Each mock user can have:

- `email` (required): The user's email address
- `name`: Display name
- `admin`: Boolean indicating admin privileges
- `groups`: List of group memberships
- Custom attributes for use in security policy expressions

When mock users are defined and security policies exist, a "View as" dropdown appears in the dashboard preview.

### Environment variables

The `env` property sets default values for non-sensitive variables. These can be referenced in resource files using templating syntax (`{{ .env.<variable> }}`). Sensitive secrets should go in `.env` instead.

### Resource type defaults

Project-wide defaults can be set for resource types using plural keys:

- `models`: Default settings for all models (e.g., refresh schedules)
- `metrics_views`: Default settings for all metrics views (e.g., `first_day_of_week`)
- `explores`: Default settings for explore dashboards (e.g., `time_ranges`, `time_zones`)
- `canvases`: Default settings for canvas dashboards

Individual resources can override these defaults.

### Path management

- `ignore_paths`: List of paths to exclude from parsing (use leading `/`)
- `public_paths`: List of paths to expose over HTTP (defaults to `['./public']`)

### Environment overrides

The `dev` and `prod` properties allow environment-specific configuration overrides.

## Minimal Example

A minimal `rill.yaml` for a new project:

```yaml
display_name: My Analytics Project
```

## Complete Example

A comprehensive `rill.yaml` demonstrating common configurations:

```yaml
display_name: Sales Analytics
description: Sales performance dashboards with partner access controls

olap_connector: duckdb

# Use a project-defined Claude connector to power AI features
ai_connector: claude

# Non-sensitive environment variables
env:
  default_lookback: P30D
  data_bucket: gs://my-company-data

# Mock users for testing security policies locally
mock_users:
  - email: admin@mycompany.com
    name: Admin User
    admin: true
  - email: partner@external.com
    groups:
      - partners
  - email: viewer@mycompany.com
    tenant_id: xyz

# Project-wide defaults for models
models:
  refresh:
    cron: 0 0 * * *

# Project-wide defaults for metrics views
metrics_views:
  smallest_time_grain: day

# Project-wide defaults for explore dashboards
explores:
  defaults:
    time_range: P3M
  time_zones:
    - UTC
    - America/New_York
    - Europe/London
  time_ranges:
    - PT24H
    - P7D
    - P30D
    - P3M
    - P12M

# Exclude non-Rill files from parsing
ignore_paths:
  - /docs
```

## Reference documentation

Here is a full JSON schema for the `rill.yaml` syntax:

```
$schema: http://json-schema.org/draft-07/schema#
allOf:
    - properties:
        ai_connector:
            description: Specifies the default AI connector for the project. Defaults to Rill's internal AI connector if not set.
            type: string
        ai_instructions:
            description: Extra instructions for LLM/AI features. Used to guide natural language question answering and routing.
            type: string
        ai_prompts:
            description: Suggested prompts shown as starters in the project-wide AI chat, and on dashboards that have no `ai_prompts` of their own. Each entry is either a prompt string or an object with `label` and `prompt`. At most 8 distinct entries.
            items:
                oneOf:
                    - description: The prompt. A short label is derived from its first words.
                      type: string
                    - additionalProperties: false
                      description: A prompt with an explicit label.
                      properties:
                        label:
                            description: Short label shown on the prompt's button (at most 40 characters). Derived from the prompt if omitted.
                            type: string
                        prompt:
                            description: The full question sent to the AI when the user picks the prompt.
                            type: string
                      required:
                        - prompt
                      type: object
            type: array
        compiler:
            description: Specifies the parser version to use for compiling resources
            type: string
        description:
            description: A brief description of the project
            type: string
        display_name:
            description: The display name of the project, shown in the upper-left corner of the UI
            type: string
        features:
            description: Optional feature flags. Can be specified as a map of feature names to booleans.
            type: object
      title: Properties
      type: object
    - description: |
        Rill allows you to specify the default OLAP engine to use in your project via `rill.yaml`.
        :::info Curious about OLAP Engines?
        Please see our reference documentation on [OLAP Engines](/developers/build/connectors/olap).
        :::
      properties:
        olap_connector:
            description: Specifies the default OLAP engine for the project. Defaults to duckdb if not set.
            examples:
                - olap_connector: clickhouse
            type: string
      title: Configuring the default OLAP Engine
      type: object
    - description: |
        In `rill.yaml`, project-wide defaults can be specified for a resource type within a project. Unless otherwise specified, _individual resources will inherit any defaults_ that have been specified in `rill.yaml`. For available properties that can be configured, please refer to the YAML specification for each individual resource type - [model](models.md), [metrics_view](metrics-views.md), and [explore](explore-dashboards.md)

        :::note Use plurals when specifying project-wide defaults
        In your `rill.yaml`, the top-level property for the resource type needs to be **plural**, such as `models`, `metrics_views`, and `explores`.
        :::

        :::info Hierarchy of inheritance and property overrides
        As a general rule of thumb, properties that have been specified at a more _granular_ level will supersede or override higher-level properties that have been inherited. Therefore, in order of inheritance, Rill will prioritize properties in the following order:
        1. Individual [models](models.md)/[metrics_views](metrics-views.md)/[explore](explore-dashboards.md) object-level properties (e.g. `models.yaml` or `explore-dashboards.yaml`)
        2. [Environment](/developers/build/models/templating) level properties (e.g. a specific property that has been set for `dev`)
        3. [Project-wide defaults](#project-wide-defaults) for a specific property and resource type
        :::
      properties:
        canvases:
            description: Defines project-wide default settings for canvases. Unless overridden, individual canvases will inherit these defaults.
            examples:
                - canvases:
                    defaults:
                        time_range: P7D
                    time_ranges:
                        - PT24H
                        - P7D
                    time_zones:
                        - UTC
                  explores:
                    defaults:
                        time_range: P24M
                    time_ranges:
                        - PT24H
                        - P6M
                    time_zones:
                        - UTC
                  metrics_views:
                    first_day_of_week: 1
                    smallest_time_grain: month
                  models:
                    refresh:
                        cron: 0 * * * *
            type: object
        explores:
            description: Defines project-wide default settings for explores. Unless overridden, individual explores will inherit these defaults.
            type: object
        metrics_views:
            description: Defines project-wide default settings for metrics_views. Unless overridden, individual metrics_views will inherit these defaults.
            type: object
        models:
            description: Defines project-wide default settings for models. Unless overridden, individual models will inherit these defaults.
            type: object
      title: Project-wide defaults
      type: object
    - description: |
        Primarily useful for [templating](/developers/build/connectors/templating), variables can be set in the `rill.yaml` file directly. This allows variables to be set for your projects deployed to Rill Cloud while still being able to use different variable values locally if you prefer.
        :::info Overriding variables locally
        Variables also follow an order of precedence and can be overridden locally. By default, any variables defined will be inherited from `rill.yaml`. However, if you manually pass in a variable when starting Rill Developer locally via the CLI, this value will be used instead for the current instance of your running project:
        ```bash
        rill start --env numeric_var=100 --env string_var="different_value"
        ```
        :::
        :::tip Setting variables through `.env`
        Variables can also be set through your project's `<RILL_PROJECT_HOME>/.env` file (or using the `rill env set` CLI command), such as:
        ```bash
        variable=xyz
        ```
        Similar to how [connector credentials can be pushed / pulled](/developers/build/connectors/credentials#pulling-credentials-and-variables-from-a-deployed-project-on-rill-cloud) from local to cloud or vice versa, project variables set locally in Rill Developer can be pushed to Rill Cloud and/or pulled back to your local instance from your deployed project by using the `rill env push` and `rill env pull` commands respectively.
        :::
      properties:
        env:
            description: |
                A map of key-value pairs for setting variables on your project. It accepts both user-defined variables (for use with templating) and reserved `rill.*` keys that configure project-wide settings. The full set of reserved keys is listed below.
            examples:
                - env:
                    foo: bar
                    rill.interactive_sql_row_limit: 5000
            properties:
                rill.ai.completion_timeout_seconds:
                    description: 'Maximum duration of a full AI completion request (which may include multiple LLM calls and tool uses), in seconds. Default: 300.'
                    type: integer
                rill.ai.default_query_limit:
                    description: 'Default row limit applied to AI tool queries when no limit is specified. Default: 25.'
                    type: integer
                rill.ai.llm_timeout_seconds:
                    description: 'Maximum duration of a single LLM completion request, in seconds. Default: 180. Note: when using Rill''s hosted AI service (i.e. not a self-configured LLM), the admin server enforces a hard upper bound of 10 minutes, so values above that have no effect.'
                    type: integer
                rill.ai.max_query_limit:
                    description: 'Maximum row limit allowed for AI tool queries. Default: 250.'
                    type: integer
                rill.ai.max_time_range_days:
                    description: 'Maximum time range allowed for AI tool queries, in days. Set to 0 for no limit. Default: 0.'
                    type: integer
                rill.ai.require_time_range:
                    description: 'Require AI tool queries to include a time range filter; reject queries without one. Default: true.'
                    type: boolean
                rill.alerts.default_streaming_refresh_cron:
                    description: 'Default cron expression for refreshing alerts that depend on streaming refs (for example, external tables in Druid where new data may arrive at any time). Default: `0 0 * * *` (every 24 hours).'
                    type: string
                rill.alerts.fast_streaming_refresh_cron:
                    description: 'Cron expression for refreshing streaming alerts on always-on OLAP connectors. Default: `*/10 * * * *` (every 10 minutes).'
                    type: string
                rill.download_limit_bytes:
                    description: 'Limit on the size of an exported file, in bytes. Default: 134217728 (128 MB).'
                    type: integer
                rill.interactive_sql_row_limit:
                    description: 'Row limit for interactive SQL queries; does not apply to SQL exports. Default: 10000.'
                    type: integer
                rill.metrics.approximate_comparisons:
                    description: 'Rewrite metrics comparison queries to use an approximate, faster form. Approximate comparisons may not return data points for all values. Default: true.'
                    type: boolean
                rill.metrics.approximate_comparisons_cte:
                    description: 'Rewrite metrics comparison queries to use a CTE for the base query. Default: false.'
                    type: boolean
                rill.metrics.approximate_comparisons_two_phase_limit:
                    description: 'Row-limit threshold under which metrics comparison queries use a two-phase strategy (base values first, comparison values second). Default: 250.'
                    type: integer
                rill.metrics.druid_mvd_filtered_group_by:
                    description: 'Narrow unnested (multi-value) dimensions to the filtered values when grouping in Druid, so results contain only the filtered values rather than every value co-occurring in matching rows. Default: false.'
                    type: boolean
                rill.metrics.druid_mvd_filtered_search:
                    description: 'Extends rill.metrics.druid_mvd_filtered_group_by to dimension search (ILIKE filters) using MV_FILTER_REGEX, so search results contain only values matching the search text. Requires Druid 35.0.0 or newer. Default: false.'
                    type: boolean
                rill.metrics.exactify_druid_topn:
                    description: 'Split Druid TopN queries into two queries to improve measure accuracy, at the cost of performance. Default: false.'
                    type: boolean
                rill.metrics.timeseries_null_filling_implementation:
                    description: 'Null-filling implementation for timeseries queries. One of `none`, `new`, or `pushdown`. Default: `pushdown`.'
                    type: string
                rill.model.partitions_warn_on_failure:
                    description: 'When true, partition execution failures are surfaced as non-blocking warnings instead of errors. Default: true in `prod`, false otherwise.'
                    type: boolean
                rill.model.tests_warn_on_failure:
                    description: 'When true, model test failures are surfaced as non-blocking warnings instead of errors. Default: true in `prod`, false otherwise.'
                    type: boolean
                rill.model.timeout_override:
                    description: 'Timeout for model reconciliation in seconds, used in validation mode. Default: 0 (no override).'
                    type: integer
                rill.models.concurrent_execution_limit:
                    description: 'Maximum number of concurrent model executions. Default: 5.'
                    type: integer
                rill.models.default_materialize:
                    description: 'Materialize models as tables by default instead of views. Default: false.'
                    type: boolean
                rill.models.disable:
                    description: 'When true, model execution is disabled. Useful for stopping any ingestion in Rill temporarily. Default: false.'
                    type: boolean
                rill.models.materialize_delay_seconds:
                    description: 'Delay before materializing models, in seconds. Default: 0.'
                    type: integer
                rill.parser.skip_updates_if_parse_errors:
                    description: 'Short-circuit project parser reconciliation when parse errors exist. Default: false.'
                    type: boolean
                rill.strict_model_properties:
                    description: 'Return an error when a model contains unmapped properties. Default: false.'
                    type: boolean
                rill.strict_resolver_properties:
                    description: 'Return an error when a resolver contains properties not recognized by its implementation. Default: false.'
                    type: boolean
            type: object
      title: Setting variables
      type: object
    - description: |
        The public_paths and ignore_paths properties in the rill.yaml file provide control over which files and directories are processed or exposed by Rill. The public_paths property defines a list of file or directory paths to expose over HTTP. By default, it includes ['./public']. The ignore_paths property specifies a list of files or directories that Rill excludes during ingestion and parsing. This prevents unnecessary or incompatible content from affecting the project.
        :::tip
        Don't forget the leading `/` when specifying the path for `ignore_paths`. This path is relative to your project root.
        :::
      properties:
        ignore_paths:
            description: A list of file or directory paths to exclude from parsing. Useful for ignoring extraneous or non-Rill files in the project
            examples:
                - ignore_paths:
                    - /path/to/ignore
                    - /file_to_ignore.yaml
            items:
                type: string
            type: array
        public_paths:
            description: List of file or directory paths to expose over HTTP. Defaults to ['./public']
            items:
                type: string
            type: array
      title: Managing Paths in Rill
      type: object
    - description: |
        During development, it is always a good idea to check if your [access policies](/developers/build/metrics-view/security) are behaving the way you designed them to before pushing these changes into production. You can set mock users, which enables a drop-down in the dashboard preview to view as a specific user.
        :::info The View as selector is not visible in my dashboard, why?
        This feature is _only_ enabled when you have set a security policy on the dashboard. By default, the dashboard and its contents are viewable by every user.
        :::
      properties:
        mock_users:
            description: A list of mock users used to test dashboard security policies within the project
            examples:
                - mock_users:
                    - admin: true
                      email: john@yourcompany.com
                      name: John Doe
                    - email: jane@partnercompany.com
                      groups:
                        - partners
                    - email: anon@unknown.com
                    - custom_variable_1: Value_1
                      custom_variable_2: Value_2
                      email: embed@rilldata.com
                      name: embed
            items:
                properties:
                    admin:
                        description: Indicates whether the mock user has administrative privileges
                        type: boolean
                    email:
                        description: The email address of the mock user. This field is required
                        type: string
                    groups:
                        description: An array of group names that the mock user is a member of
                        items:
                            type: string
                        type: array
                    name:
                        description: The name of the mock user.
                        type: string
                required:
                    - email
                type: object
            type: array
      title: Testing access policies
      type: object
    - properties:
        dev:
            description: Overrides any properties in development environment.
            type: object
        prod:
            description: Overrides any properties in production environment.
            type: object
      title: Common Properties
      type: object
description: The `rill.yaml` file contains metadata about your project.
id: rill-yaml.schema.yaml
title: Project YAML
type: object
```