---
name: ui-theme-designer-design-tokens
description: "TRIGGER: questions about the SAP Design System and SAP Fiori design tokens — which themes exist, what value a theme parameter (e.g. sapButton_Background, sapHighlightColor) has in a given theme, how parameters inherit/extend across the theme chain, which parameters a specific UI component (UI5 control, UI5 Web Component, Fundamental Styles component) consumes. SKIP: how-to questions about UI theme designer as a product (creating, publishing, transporting themes — use ui-theme-designer-help)."
allowed-tools: Bash(npm ci) Read Glob Grep WebFetch
---

# Design Tokens

_With `$THIS` being the folder that contains this SKILL.md:_

## Prerequisite

`$THIS/node_modules/` exists and is not older than 7 days; if not: `cd $THIS && npm ci`

## Context

Design Tokens are defined in LESS files of the theming-base-content, and consumed in LESS and CSS files of different frameworks (= UI technologies). In `$THIS/node_modules/` you find the following:

- **UI5:** (with `$LIBRARY` being e.g. `sap.ui.core`, and `$THEME` being e.g. `sap_horizon`)
   - `$THIS/node_modules/@openui5/$LIBRARY/src/${LIBRARY/./\//}/**/themes/base` contains the `baseTheme` of the different libraries
   - `$THIS/node_modules/@openui5/themelib_$THEME/src/${LIBRARY/./\//}/themes/` contains the `$THEME` of the different libraries
- **UI5 Web Components:** (with `$THEME` being e.g. `sap_horizon`, and `$COMPONENT` being e.g. `Button`)
   - `$THIS/node_modules/@ui5/*/src/themes/$COMPONENT.css` contains theme-independent component skeleton CSS, using parameters from theming-base-content as CSS custom properties, as well as CSS custom properties defined in `base/` (see below)
   - `$THIS/node_modules/@ui5/*/src/themes/base/$COMPONENT-parameters.css` contains CSS custom property definitions for components; never report those UI5 Web Components-specific internal CSS custom properties.
   - `$THIS/node_modules/@ui5/*/src/themes/$THEME/$COMPONENT-parameters.css` contains theme-dependent values for the custom property definitions from `base/` (see above)
- **Fundamental Styles:**
   - `$THIS/node_modules/fundamental-styles/dist/*.css` contains theme-independent component skeleton CSS, using parameters from theming-base-content as CSS custom properties, as well as CSS custom properties defined in `theming/` (see below)
   - `$THIS/node_modules/fundamental-styles/dist/theming/$THEME.css` contains theme-dependent values for the custom property definitions used in `dist/*.css` (see above); never report those Fundamental Styles-specific internal CSS custom properties
   - `$THIS/node_modules/@fundamental-styles/common-css/dist/*.css` theme-independent helper CSS, using parameters from theming-base-content as CSS custom properties
- **Base:** (with `$LIBRARY` being e.g. `baseLib`, and `$THEME` being e.g. `sap_horizon`)
   - `$THIS/node_modules/@sap-theming/theming-base-content/content` is a theme repository as described in https://raw.githubusercontent.com/SAP-docs/btp-ui-theme-designer/main/docs/cf/About-Themes/overview-of-sap-theming-content-91ebfe2.md, containing `Base/`; used by all frameworks
   - `$THIS/node_modules/@sap-theming/theming-base-content/content/Base/.theming` contains metadata about the `Base` framework
   - `$THIS/node_modules/@sap-theming/theming-base-content/content/Base/$LIBRARY/.theming` contains metadata about libraries
   - `$THIS/node_modules/@sap-theming/theming-base-content/content/Base/$LIBRARY/$THEME/.theming` contains metadata about themes
   - Metadata includes
      - `sEntity`: "Framework", "Library" or "Theme"
      - `sType` (for themes): "STANDARD" (= single theme) or "SET" (= no CSS, just references to different themes of `sType=STANDARD`)
      - `aFiles`: LESS source files
      - `aBuildFiles`: CSS files built from `aFiles`
      - `*sBase{Library,Theme,File}Id`: ID of the most important library/theme/file
      - `oExtends`: the `$FRAMEWORK[.$LIBRARY[.$THEME[.$FILE]]]` "object path" of the parent entity
      - `sSourcePathPattern`: pattern to resolve object paths to file paths
      - (optional) `bIgnore=true`: entity is ignored from theming
   - Alongside the LESS sources and `.theming` metadata, a theme dir under `.../baseLib/$THEME/` also ships **fully-resolved** parameter values built from the LESS chain — use these for resolved-value lookups instead of evaluating LESS:
      - `css_variables.css` — resolved values as CSS custom properties (e.g. `--sapBrandColor: #0070f2;`); **widest theme coverage**, the preferred resolved-value source
      - `less_variables.less` — the same resolved values as LESS variables (e.g. `@sapBrandColor: #0070f2;`)
      - `variables.json` — the same resolved values as JSON (e.g. `"sapBrandColor": "#0070f2"`)
      - `design-tokens.json` — a token's `type`, `description`, and derivation graph **only**; its color `value` fields are HSLA references (e.g. `hsla({Main._sapBrandColorH}, …)`), **not** final values — not a resolved-value source

## Procedure

1. Determine the SAP theme the users question targets, present the available theme IDs from `$THIS/node_modules/@sap-theming/theming-base-content/content/Base/baseLib` as select options if unclear, default to `sap_horizon`
2. Determine the framework the user's question targets. Present the frameworks from "Context" as select options if unclear, applying these defaults:
   1. **framework stated:** use that
   2. **component stated, no framework:**
      1. search _UI5 Web Components_ for a CSS file for the component; if found use _UI5 Web Components_ as primary source
      2. additionally search _Base_ for parameters matching `sap$COMPONENT_*`: report any such parameters not already referenced in _UI5 Web Components_ as supplementary, labelled "defined in theming-base-content, not yet referenced in UI5 Web Components CSS"
   3. **no component, no framework:** use _Base_
3. Read the `.theming` file of the framework the users question targets, determine `sBaseLibraryId` and `sSourcePathPattern`
4. Read the `.theming` file of the theme of the `sBaseLibrary` of the framework the users question targets, based on `sSourcePathPattern` of the frameworks `.theming` file
5. While there is an `oExtends`:
   1. Read the `.theming` file of the theme referenced by `oExtends`; if you haven't encountered the framework (the first section of the Object Path) before, read the framework `.theming` first to determine its `sSourcePathPattern`
   2. Merge the `.theming` JSON with what you already have from the theme `.theming` files: if a key already exists, leave it untouched; add key+value if the key does not yet exist
6. If the question only needs the **resolved value** of one or more parameters in the theme (e.g. "what value does `sapButton_Background` have in `sap_horizon`?"), read the theme's flat, pre-resolved artifact from `$THIS/node_modules/@sap-theming/theming-base-content/content/Base/baseLib/<theme>/` and take the value directly — prefer `css_variables.css` (`--sapButton_Background: #fff;`, widest theme coverage), or equivalently `less_variables.less` (`@sapButton_Background: #fff;`) or `variables.json` (`"sapButton_Background": "#fff"`). Do **not** read `design-tokens.json` for values (its color `value` fields are HSLA references such as `hsla({Main._sapBrandColorH}, …)`, not final values). The LESS traversal in steps 7–8 is not needed for a plain value lookup.
7. Otherwise, when inheritance or annotation semantics are needed, build the merged LESS: read the `${sBaseFileId}.less` file (`sBaseFileId` comes from the merged `.theming` files) of the theme of the `sBaseLibrary` of the framework the users question targets, then for each LESS `@import` statement, recursively:
   1. Read the referenced LESS file
   2. Replace the `@import` statement with the read content
8. In the merged LESS file, map the lines `// [<Annotation> <required: Value> <optional: More Values>]` that precede parameter definitions to that parameter:
   1. If a parameter is defined multiple times, merge those annotations
   2. If an annotation already exists: append the value to the existing annotation values
   3. If an annotation has values for which it also has "anti-values" (the same value but starting with a `!`, e.g. "Protected" and "!Protected"), remove both values from the values list
   4. If an annotation values list is empty, remove the annotation
9. If the user targets "UI5 Web Components", for each relevant component look up the three CSS sources:
   1. the theme-independent skeleton at `@ui5/*/src/themes/<Component>.css`, merged with
   2. the always-used base parameters at `@ui5/*/src/themes/base/<Component>-parameters.css`, then with
   3. the theme-specific delta at `@ui5/*/src/themes/<theme>/<Component>-parameters.css`
10. If the user targets "Fundamental Styles", scan `fundamental-styles/dist/*.css` for the relevant component; theme-specific values come from the CSS custom properties in `theming-base-content/content/Base/baseLib/<theme>/css_variables.css` (standard `sap*` parameters), merged with `fundamental-styles/dist/theming/<theme>.css` (Fundamental Styles-specific tokens not present in theming-base-content, e.g. `sapMenu_*`, `sapNavigation_*`)
11. Answer the users question based on the information collected
