# Design: mvp2-sovereign-deployment

## Approach
- Per-tenant provisioning mode: sovereign tenants get in-region VPC topology (see isolation-hardening
  for dedicated compute), regional storage, and regional model endpoints where applicable.
- BYOK via cloud KMS with customer-managed keys; key-revocation path tested.
- Audit log: append-only store, tamper-evident, exportable for regulator review.
- Deliverable includes an NDPR/POPIA/SARB control mapping document (procurement artifact).

## Honest constraint
Vendor calls that cannot be made in-region (e.g., a managed LLM with no regional endpoint) must be
explicitly surfaced in the control mapping — full in-VPC inference arrives with MVP 3's NVIDIA path.
