# Design: mvp1-tenant-provisioning

## Approach
- Control-plane service (FastAPI). Postgres with a `tenants` table and a **tenant-scoped repository
  layer** that requires `tenant_id` on every query; unscoped queries forbidden by lint/review.
- Subdomain provisioning via wildcard DNS + per-tenant routing.
- Auth via OIDC-compatible provider; sessions carry `tenant_id` + role claims.

## Tenant-isolation note
Isolation is enforced at the repository layer by construction (required parameter), backed by a
cross-tenant test suite that must prove inaccessibility — not by per-endpoint permission checks alone.
