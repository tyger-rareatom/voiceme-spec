# Proposal: mvp1-tenant-config-store

## Why
The Tenant Config Router needs a control-plane source of truth for per-tenant flags (`tier`,
`language`, `audio_backend`, `rag_backend`, entitlements).

## What Changes
Add a tenant config store with a hot-path read API, consumed by the router at session setup.

## User-visible impact
Internal; enables per-tenant backend routing.

## Rollback
Explicit safe defaults applied if config missing.
