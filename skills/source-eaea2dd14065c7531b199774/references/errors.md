# Errors reference

## Error filters

Apply in both proactive and reactive modes before scoring or surfacing any error. A candidate failing either filter is skipped — do not include it in fixable or vendor buckets.

- **No stack trace** — skip. Without frames pointing to specific code there's no path to a root cause fix.
- **Pure third-party** — skip. If every stack frame is from a third-party domain, the store owner can't action it. Note the service name internally but don't surface it as a finding.

---

## Third-party handling

**In reactive diagnosis** — if the origin is third-party, name the specific service and be explicit: the fix path is contacting the vendor, not a code change. Don't imply a fix the operator can't ship.

**Third-party CWV contributors** — scripts like analytics pixels, email capture tools, and loyalty widgets can't be edited directly, but their impact can be mitigated: load with `async`/`defer`, reserve space in CSS to prevent layout shift, or contact the vendor for a lighter embed.

**Infrastructure-level fixes** — SSR changes, CDN configuration, server response time. Flag these specifically as requiring backend/DevOps access, distinct from theme or code changes.

---

## Root cause over symptom suppression

Never wrap code in try/catch to silence an error or add null checks that hide the real issue. A fix must address why the error happens. If the root cause can't be determined from available data, say so — don't ship a suppression.

---

## Cookie-consent observability check

If an error fires on a consent-related endpoint (OneTrust, Cookiebot, TrustArc) and impacted sessions are very short with no further navigation, this is likely an observability gap — the consent platform may be removing Noibu's script and ending the recording early. Flag as a data limitation, not user impact. Name the specific platform when identifiable.

---

## Stack-frame classification

Check `platform_overrides` in `$HOME/.tech-diagnosis-config.json` first — if `merchant_paths` and `vendor_paths` are set, use those. If not, read the built-in platform reference file:
- Shopify → `references/platforms/shopify.md`
- Magento → `references/platforms/magento.md`
- WooCommerce → `references/platforms/woocommerce.md`
- BigCommerce → `references/platforms/bigcommerce.md`
- Headless, custom, or other → `references/platforms/generic.md`

To customise paths, ask Claude to update `platform_overrides` in the config file — no JSON editing required.

When reading frames, identify:
- Whether the frame is in merchant-owned code (fixable), platform code (not fixable), or vendor code (share with vendor)
- The function or operation running when the error fired
- Monitoring/recording wrappers (Sentry, rrweb) affect data collection, not user experience — flag but don't treat as user-impacting

Use View Source (not Inspect) to verify whether a script or element is in the initial HTML response. The Elements panel shows the post-JS DOM and will mislead on load-order questions.

---

## Technical details fields

Rendered only when the operator explicitly asks or the Technical details chip is selected in the share widget. Render exactly these fields in order, omitting any with no data. No placeholder text, no commentary between fields.

- **Issue ID** — plain identifier (e.g. `#445`)
- **Issue type** — one descriptive line (e.g. "HTTP 422 Unprocessable Entity", "JavaScript TypeError")
- **Error message** — exact, in code style
- **Error signature** — when available
- **Pattern** — short prose description Noibu provides for occurrence context
- **Stack trace** — top 3-5 frames, first-party vs third-party labeled
- **HTTP debug data** — request headers, response headers, request payload, response body. Only when the API populates them. May contain sensitive data.
- **Browser impact** — horizontal bar chart, % of occurrences, top 5 with long-tail indicator
- **OS impact** — same format
- **Browser version impact** — only when one version concentrates ≥30% of occurrences
- **OS version impact** — only when one version concentrates ≥30% of occurrences
- **File/line** — only when source enrichment ran
