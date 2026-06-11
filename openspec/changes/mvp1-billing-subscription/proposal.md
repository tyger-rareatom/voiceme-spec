# Proposal: mvp1-billing-subscription

## Why
Recurring subscription + metered overage is the business model.

## What Changes
Stripe subscriptions (3 tiers, operative enterprise pricing), entitlement enforcement, overage billing
fed by the metering plane.

## User-visible impact
Tenants subscribe to a tier and are billed monthly, with overage where configured.

## Rollback
Billing in test mode; enforcement flag-gated.
