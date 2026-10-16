# Product Analysis — Query Workflow

Four-step workflow for full analysis. Field names are role-based — already confirmed during setup.

---

## Step 1 — Broad overview (fire all four in one turn)

| Query | Tool | Group by | Measures | Limit | Order |
|---|---|---|---|---|---|
| Products by views | Session search | Viewed product titles | Sessions, CVR, revenue/session | 20 | Sessions ↓ |
| Product ATC opportunities | Page visits | URL (filter: CONTAINS '/products/') | Page views, ATC_LIFT_OPPORTUNITY, add-to-cart rate | 10 | ATC_LIFT_OPPORTUNITY ↓ |
| Collections by conversion | Session search | Viewed collection titles | Sessions, CVR, revenue/session | 15 | Sessions ↓ |
| Product types by conversion | Session search | Viewed product types | Sessions, CVR, revenue/session | 10 | Sessions ↓ |

> **Product ATC opportunities:** `ATC_LIFT_OPPORTUNITY` is a pre-computed score combining traffic volume and ATC rate gap — higher = more opportunity. Use this ranking directly to identify low-ATC product candidates.

> **Products by purchase is not in Step 1.** Only run it in Step 3 if the data suggests cart abandonment (a product with good ATC rates but weak purchase completion).

---

## Step 2 — Cross-reference in post-processing

- **ATC opportunity** = use the `ATC_LIFT_OPPORTUNITY` ranking directly. Cross-check the top URLs against products-by-views to confirm they are high-traffic products.
- **Collection CVR benchmark** = compare collections against others in the same price tier, not the site-wide average. Two game-focused collections are valid benchmarks for each other; a premium hardware collection is not a valid benchmark for a accessories collection. Only flag low CVR when a same-tier benchmark exists.
- **Viewed-only %** = sessions with no funnel progression ÷ total view sessions. Flag products where 80%+ viewed-only, but check site-wide average first — high viewed-only is normal for low-intent browsing.
- **Site-wide CVR benchmark** = total purchases ÷ total sessions. Use only as context — never to flag high-ticket products, collections, or types as underperforming. Price data is not in Noibu session data; infer price tier from product/collection names.

---

## Step 3 — Pick 2–4 signals to dig into

| If you see this… | Follow-up |
|---|---|
| High ATC_LIFT_OPPORTUNITY product in top-20 views | Page deep-dive: scroll depth, time on page, click engagement, errors |
| Product with good ATC rate but weak purchase completion suspected | Run "Products by purchase" now (session search, purchased product titles, sessions + median cart value, limit 20, sessions ↓) — then funnel depth breakdown for that product |
| Collection CVR well below a comparable benchmark collection | Country breakdown: near-zero CVR across LATAM/non-primary = localization/checkout gap |
| Collection CVR below others in same category | Product mix drill-down within that collection |
| Product type significantly over/under | Break down by product title within the type |
| High-purchase product absent from views top | Journey path analysis — likely reached via search/direct links |
| Collections with non-English names at very low CVR | Check checkout/shipping availability in those markets |

---

## Step 4 — Deeper follow-up queries

Run only the follow-ups the signals call for. Apply traffic thresholds now:
- >500K sessions/month: threshold ~0.1–0.2% of total
- 50K–500K: ~0.3–0.5%
- <50K: very low or skip

**Product page deep-dive** (high ATC_LIFT_OPPORTUNITY)
- Use page visits tool. Filter URLs CONTAINS the product's SKU code or slug fragment (limit 15).
- Measures: page views, ATC_LIFT_OPPORTUNITY, add-to-cart rate, median duration, median max scroll depth ratio, median clicked selector count, total visual error count. Order by ATC_LIFT_OPPORTUNITY ↓.
- Use URL CONTAINS (not exact URL) — product pages appear under `/products/`, `/collections/[name]/products/`, `/es/products/`, etc.
- Scroll depth: <0.20 = users not reaching ATC button; 0.20–0.40 with low clicks = content/pricing concern; high errors on one URL variant = possible JS error blocking ATC.
- Compare ATC rate across URL variants — a rate that's low on one variant but normal on others points to a URL-specific issue (broken localised page, collection-scoped page with missing ATC).

**Funnel depth breakdown** (strong ATC, weak purchase)
- Session search tool. Filter to sessions where target product title was viewed. Group by funnel depth field. Measure session count. Order ↓.
- Depth values: null = viewed only, 1 = ATC, 2 = checkout started, 3 = payment submitted, 4 = completed.
- Lead with "Viewed only %" = null sessions ÷ total.
- Note: depth-4 outnumbering depth-2/3 is normal (Apple Pay, Shop Pay skip checkout pages — not a data error).

**Country breakdown** (collection CVR well below benchmark)
- Session search tool. Filter to sessions where collection title was viewed. Group by country code (limit 20). Measure sessions, CVR, revenue/session. Order ↓.
- Near-zero CVR across multiple LATAM/non-English markets = ops/localization gap, not a merchandising problem.

**Product mix within a collection** (collection underperforms, country breakdown is clean)
- Session search tool. Filter to collection title viewed. Group by viewed product titles (array join, limit 25). Measure sessions, CVR. Order ↓.

**Journey paths** (high views, high bounce)
- User journey tool. Anchor on product slug fragment, loose mode. Both directions, max depth 6.
