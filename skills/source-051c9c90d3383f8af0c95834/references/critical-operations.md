# Critical Operations Reference

This file contains **verified procedures** for critical account and cluster operations.

**IMPORTANT**: Always use this reference for these operations. Do NOT rely on general knowledge or assumptions.

---

## Table of Contents

1. [Account Deletion](#account-deletion)
2. [Organization Deletion](#organization-deletion)
3. [Cluster Deletion](#cluster-deletion)
4. [Recycle Bin & Recovery](#recycle-bin--recovery)
5. [Billing & Subscription Management](#billing--subscription-management)

---

## Account Deletion

### Self-Service Flow (Console)

Users can delete their own account through the Console:

1. Log in to [Zilliz Cloud Console](https://cloud.zilliz.com/login)
2. Click profile icon (upper-right) → **Account Settings**
3. Click **Close Account** button
4. Provide reason for leaving (optional feedback)
5. Enter email address → Click **Send Verification Code** → Enter code
6. Tick confirmation boxes → Click **Next**
7. Account deletion email notification will be sent when complete

### Important Notes

| Item | Detail |
|------|--------|
| Post-closure access | Cannot log in with that account |
| Data retention | All data permanently deleted after **30 days** |
| Reopen within 30 days | Create ticket at [Support Portal](https://support.zilliz.com/hc/en-us/) |

### Pre-Closure Checklist (If Organization Owner)

Before closing account, the owner must:

1. **Delete all project clusters** in the organization
2. **Ensure all bills are paid**
3. **Refund any advance pay funds**
4. **Cancel third-party marketplace subscriptions** (AWS/GCP/Azure)
5. Go to **Settings → System Settings → Delete Organization** and follow prompts

### When to Escalate to Support

- Cannot access account to self-delete
- Organization has multiple owners
- Billing disputes need resolution first
- Data export needed before deletion

**Support Portal**: https://support.zilliz.com

---

## Organization Deletion

### Self-Service Flow (Console)

1. Ensure you are the **Organization Owner**
2. Complete pre-deletion requirements:
   - Delete all clusters in all projects
   - Settle all outstanding bills
   - Cancel marketplace subscriptions
3. Go to **Settings → System Settings → Delete Organization**
4. Follow confirmation prompts

### Requirements

| Requirement | Why |
|-------------|-----|
| All clusters deleted | Cannot delete org with active resources |
| All bills paid | Prevent billing issues |
| Owner role | Only owners can delete |

---

## Cluster Deletion

### Method 1: Console UI

1. Navigate to **Cluster Details** page
2. Click **Drop cluster**
3. Confirm the action

### Method 2: REST API (V2)

```bash
curl --request POST \
     --url "https://api.cloud.zilliz.com/v2/clusters/${CLUSTER_ID}/drop" \
     --header "Authorization: Bearer ${API_KEY}" \
     --header "Accept: application/json" \
     --header "Content-Type: application/json"
```

### Behavior

| Cluster Type | Recycle Bin | Recovery Period |
|--------------|-------------|-----------------|
| **Paid clusters** | Yes | 30 days |
| **Free clusters** | No | Immediate permanent deletion |

---

## Recycle Bin & Recovery

### Retention Period

**30 days** for all deleted clusters (except Free tier).

### What Goes to Recycle Bin

| Deletion Type | Goes to Recycle Bin |
|---------------|---------------------|
| Manual deletion | Yes |
| Auto-deletion (billing overdue) | Yes |
| Trial expiration | Yes |
| Free cluster deletion | **No** (permanent) |

### Recovery Process

1. Go to **Recycle Bin** in Console
2. Select the cluster to restore
3. Click **Restore**
4. Cluster will be restored to original state

### After 30 Days

- Cluster is **permanently deleted**
- **No recovery possible**
- All data is lost

---

## Billing & Subscription Management

### AWS Marketplace Subscription

1. Subscribe via AWS Marketplace
2. Link Zilliz account using company email
3. Click **Link Organization** to associate

### Cancel Subscription

1. Go to AWS Console → AWS Marketplace → Manage subscriptions
2. Find Zilliz Cloud subscription
3. Cancel subscription
4. **Important**: Cancel in marketplace **before** deleting Zilliz account

### Billing Issues

| Issue | Action |
|-------|--------|
| Incorrect charges | Open ticket at Support Portal |
| Need invoice | Download from Console → Billing |
| Volume discount inquiry | Contact Sales |

---

## Quick Reference: Escalation Paths

| Need | Contact |
|------|---------|
| Account/billing issues | [Support Portal](https://support.zilliz.com) |
| Cannot self-delete | [Support Portal](https://support.zilliz.com) |
| Data export before deletion | [Support Portal](https://support.zilliz.com) |
| Volume discounts, contracts | [Sales](https://zilliz.com/contact-sales) |
