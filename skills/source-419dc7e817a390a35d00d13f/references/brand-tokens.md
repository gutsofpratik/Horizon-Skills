# Brand Token Resolution

Resolve brand tokens automatically — the user never fills in a config file manually. Work
through the decision tree below, then resolve every token in the schema before rendering.

## A — Check for an Uploaded Brand Template

Look for any of the following in the current conversation:

| File type | What to extract |
|---|---|
| **HTML / CSS file** | Parse all `color`, `background`, `font-family`, and `border` declarations. Identify the dominant background, primary accent, heading font, and body font. Extract any `--variable` tokens if a design system is present. |
| **PDF report or one-pager** | Visually analyse the document. Identify background color(s), the dominant accent/highlight color, heading and body typefaces, logo presence, and footer text. |
| **Image (PNG / JPG / SVG)** | Extract the 3–5 most visually prominent colors using the image content. Identify any visible text to infer font style (serif vs sans-serif, bold vs light). Note logo or wordmark if present. |
| **PowerPoint / PPTX** | Read slide backgrounds, title font, body font, accent colors from shapes and highlights. |
| **CSS / design token file** | Map token names to the brand token schema below directly. |

Once extracted, map findings to the Brand Token Schema. If the user has dropped **multiple**
files, treat the most recent one as authoritative for branding, unless the user specifies
otherwise.

## B — No Template Provided → Apply Chronograph Defaults

If no brand template is present in the conversation, apply the following defaults silently —
do not ask the user to provide branding.

```
firm_name:             Chronograph
website:               www.chronograph.pe
confidentiality_label: CONFIDENTIAL

colors:
  bg_primary:       #101C1D   ← Near Black 1 (page background)
  bg_secondary:     #1A2627   ← Near Black 2 (card / panel background)
  bg_header:        #1B4147   ← Deep Teal (header strip)
  accent_primary:   #57E5EE   ← Bright Teal (headlines, KPI values, eyebrows)
  accent_secondary: #11A8B2   ← Regular Teal (bars, borders, left-rule accents)
  accent_negative:  #F95532   ← Accent Red (EBITDA bars, negative deltas)
  accent_positive:  #4ecb8a   ← Green (positive deltas)
  text_primary:     #FFFFFF   ← White (body text)
  text_muted:       #D9E8E8   ← Light teal tint (footnotes, commentary)
  table_header_bg:  #1B4147   ← Deep Teal (table header row)

fonts:
  heading:         Ubuntu
  heading_weight:  700
  body:            Open Sans
  body_weight:     300
  google_fonts_url: https://fonts.googleapis.com/css2?family=Ubuntu:wght@700&family=Open+Sans:wght@300;300i&display=swap

logo:
  url:      (none — render firm name as text)
  position: top-left

theme: dark
```

## C — Brand Token Schema

Whether tokens are extracted from a template (A) or defaults are applied (B), resolve all
of the following before proceeding. Every downstream panel references these names.

| Token | Role | Fallback if undetectable |
|---|---|---|
| `firm_name` | Firm name in header and footer | Infer from logo text or filename; else `"Your Firm"` |
| `website` | Footer URL | `""` (omit from footer) |
| `confidentiality_label` | Footer suffix | `"CONFIDENTIAL"` |
| `bg_primary` | Page / root background | Chronograph default |
| `bg_secondary` | Card / panel background | Darken `bg_primary` by 5% |
| `bg_header` | Header strip background | Darken `bg_primary` by 15% |
| `accent_primary` | Headlines, KPI values, eyebrow labels | Dominant bright color from template |
| `accent_secondary` | Bars, borders, left-rule accents | Mute `accent_primary` by 30% |
| `accent_negative` | Negative values, downward deltas | `#F95532` |
| `accent_positive` | Positive deltas | `#4ecb8a` |
| `text_primary` | Main body text | `#FFFFFF` on dark; `#1A1A1A` on light |
| `text_muted` | Footnotes, commentary | Tint `text_primary` toward `bg_primary` by 20% |
| `table_header_bg` | Table header row | `bg_header` |
| `font_heading` | Heading / KPI / eyebrow font | Detected from template; else `Ubuntu` |
| `font_heading_weight` | Heading weight | `700` |
| `font_body` | Body / table / footnote font | Detected from template; else `Open Sans` |
| `font_body_weight` | Body weight | `300` |
| `google_fonts_url` | Font load URL | Build from detected font names |
| `logo_url` | Logo image src | `""` — fall back to firm name as text |
| `logo_position` | Header logo placement | `top-left` |
| `theme` | `dark` or `light` | `dark` if `bg_primary` luminance < 0.2; else `light` |

## D — Theme Handling

**Dark theme** (luminance of `bg_primary` < 0.2):
Use the token values as resolved. Default contrast pairings apply (white text on dark
backgrounds). Minimum contrast ratio: 4.5:1 for body text, 3:1 for large text (≥ 18px bold).

**Light theme** (luminance of `bg_primary` ≥ 0.2):
- Swap `text_primary` to a near-black (e.g. `#1A1A1A`) if not already dark
- Ensure `accent_primary` provides ≥ 3:1 contrast against `bg_primary`
- Table header: use the firm's dark brand color (e.g. deep navy / dark green) rather than
  a light value

## E — Confirm with the User (optional, brief)

After resolving tokens, output a **single short line** — not a table, not a list — before
generating the report:

> *"Using [firm_name] branding — [accent_primary] accent on [bg_primary] background,
> [font_heading] / [font_body] fonts."*

If brand detection produced low-confidence results (e.g. only a logo image was provided with
no color context), ask one focused question:

> *"I've picked up [X] and [Y] from your file — is that the right color scheme,
> or would you like to adjust anything?"*

Do not ask if defaults were applied — just proceed.
