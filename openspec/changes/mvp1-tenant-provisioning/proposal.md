# Proposal: mvp1-tenant-provisioning

## Why
Every other capability depends on a tenant existing and being isolated. This is the root change.

## What Changes
Add self-serve sign-up, auth, branded subdomain provisioning, and a tenant-scoped data model with
role-based access (admin/member).

## User-visible impact
A business can create an account and receive an isolated, branded workspace.

## Rollback
Feature-flag sign-up closed; existing tenants unaffected (additive schema only).
