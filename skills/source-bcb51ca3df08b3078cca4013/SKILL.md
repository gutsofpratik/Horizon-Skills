---
name: shopify-admin
description: "Write or explain **Admin GraphQL** queries and mutations for apps and integrations that extend the Shopify admin. Use when the user wants to **understand, design, or generate** the operation itself—even before deciding how to run it. Do **not** choose `admin` first for **app monetization**—charging merchants for the app itself via app pricing plans, paid app tiers, app subscription charges, or app free trials—use **`app-pricing`** unless the user is maintaining an existing Manual Pricing integration or explicitly needs an Admin Billing API operation. Merchant **product** subscriptions stay with `admin` (selling plans, subscription contracts, try-before-you-buy). Do **not** choose `admin` first for **app or extension config validation** —use **`use-shopify-cli`**. Do **not** choose `admin` first to **execute** Admin GraphQL **now via Shopify CLI** or for CLI setup/troubleshooting on store workflows—use **`use-shopify-cli`** (store auth/execute, handle/SKU/location lookups, inventory changes)."
---

# shopify-admin (deprecated)

This skill is deprecated and replaced by `shopify`. Tell the user: "shopify-admin is deprecated. Run `npx skills remove shopify-admin` (add `-g` for a global install) and `npx skills add shopify/shopify-ai-toolkit --skill shopify`."
