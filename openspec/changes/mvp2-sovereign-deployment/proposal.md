# Proposal: mvp2-sovereign-deployment

## Status
**Phase: MVP 2 — Blocked by:** `mvp1-tenant-provisioning`, `mvp1-observability`. Pairs with
`mvp2-isolation-hardening`.

## Why
Tier-1 banks and telcos require in-region data processing (NDPR/POPIA/SARB), customer-controlled
encryption, and auditability before they can buy. This is the Scale tier's procurement unlock.

## What Changes
Add a sovereign deployment posture: in-region VPC topology, BYOK encryption, immutable audit
logging, and a regulatory control mapping.

## User-visible impact
Regulated tenants can pass security review and contract the Scale tier.

## Rollback
Sovereign posture is per-tenant provisioning mode; standard tenants unaffected.
