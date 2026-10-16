---
name: remove
description: Delete the saved LinqAlpha default-source preference from Claude's memory. Use ONLY when the user invokes /linq-alpha:remove or asks to forget that preference; not for uninstalling the plugin or disconnecting the connector.
---

Remove the LinqAlpha default-source preference that `/linq-alpha:setup` may
have saved on this surface.

1. **Claude chat** — search memory for entries that set LinqAlpha as the default
   source for financial data. Inspect each candidate before deleting it:
   - If the entry contains the `/linq-alpha:setup` provenance marker and clearly
     expresses the LinqAlpha default-source preference, delete it.
   - If the entry expresses a similar default-source preference but does not
     contain the marker, show its full contents to the user and ask for
     confirmation. Delete it only after the user clearly agrees.
   - Do not rely on an exact sentence match: Claude Memory may rephrase text
     when saving it.
   Tell the user to verify the result under **Settings → Memory**.
2. If no such preference exists on this surface, say so plainly and stop.
3. Confirm exactly what was removed and where the user can verify the result.

Notes:

- This does not disconnect the LinqAlpha connector and does not uninstall the
  plugin; both are managed under **Settings → Plugins**.
- Do not remove anything from memory beyond the preference described above.
