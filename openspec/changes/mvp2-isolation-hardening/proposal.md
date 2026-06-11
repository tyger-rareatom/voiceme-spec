# Proposal: mvp2-isolation-hardening

## Status
**Phase: MVP 2 — Blocked by:** `mvp1-tenant-provisioning`. Pairs with `mvp2-sovereign-deployment`.

## Why
A bank's security review will ask how isolation is enforced on shared infrastructure — and whether
they can have dedicated infrastructure. Assertion is not enough; enforcement must be provable.

## What Changes
Add a dedicated-isolation provisioning tier (dedicated VPC/compute for sovereign tenants),
noisy-neighbour controls on shared infra, and an isolation-proof test suite as a release gate.

## User-visible impact
Sovereign tenants get contractually dedicated infrastructure; all tenants get provable isolation.

## Rollback
Dedicated mode is per-tenant provisioning; shared-infra controls are additive.
