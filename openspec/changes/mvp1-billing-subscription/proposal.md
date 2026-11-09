# Proposal: mvp1-billing-subscription

## Why
Recurring platform fees plus metered usage are the business model. The pricing structure is defined in
`project.md` §7 and encoded as a versioned catalogue by `mvp1-outcome-billing`.

## What Changes
Subscriptions per plan (Standard, Regulated, Sovereign) with prices read from the pricing catalogue,
entitlement enforcement, and usage billing (resolutions, minutes over the fair-use pool, modules) fed by
the metering plane, through a `billing_provider` interface.

## User-visible impact
Tenants subscribe to a plan and are billed monthly or quarterly for the platform fee, plus usage.

## Rollback
Billing in test mode; enforcement flag-gated.
