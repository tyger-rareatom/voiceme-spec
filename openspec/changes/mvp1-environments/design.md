# Design: mvp1-environments

## Decisions

- **Two environments, not three (2026-07-07).** Staging + production; local dev stays
  docker-compose (Postgres+pgvector, mocked vendors) and is documented in a README, not spec'd.
  A third pre-prod environment is rejected at MVP-1 traffic: it doubles idle vendor/infra cost
  against the ~$0-idle economics and adds no gate staging can't run.
- **Separate GCP projects per environment.** Project boundary = IAM isolation, per-environment
  billing visibility (clean cost attribution for the margin dashboard), separate quotas, and
  blast-radius containment — parity with the platform's "isolation by construction" principle.
  Same Terraform modules, different tfvars.
- **Staging in the same region (`europe-west3`).** The Frankfurt decision's whole value is zero
  transatlantic vendor hops; a different-region staging would validate a latency profile we
  don't ship. Rejected: cheaper/other-region staging.
- **Real vendors in staging, separate keys.** Vendor latency and EU-endpoint pinning must be
  continuously exercised — mocked vendors in staging are rejected (they'd pass a probe that
  proves nothing). Exception: Stripe test mode (real charges are the thing to mock).
- **Seed tenants = demo tenants.** AcmePay and TelcoOne live permanently in staging as both
  demo material and isolation-suite fixtures. No production data in staging — with
  consent-governed audio (NDPR/POPIA) this is a compliance requirement, not hygiene.

## Promotion pipeline

merge → CI (unit + parity check) → auto-deploy staging → gates (isolation suite ·
synthetic-call SLO probe · metering smoke) → manual/auto promote → production.
Break-glass bypass exists, is audited, and pages.

## Synthetic call probe

- A LiveKit client (Python, reuses the agents SDK) joins a staging room against a seed tenant,
  plays canned caller audio, and measures per-segment latency from telemetry.
- Doubles as the repeatable home for the two open hosting spikes: the Joburg→Frankfurt media
  probe (run the client from a SA vantage point) and the Deepgram Nigerian-accented-English WER
  check (canned audio corpus swap).
- Probe traffic is tagged synthetic end-to-end: excluded from billing aggregates but visible in
  observability (isolation approach: probe runs as seed tenants, so tenant scoping is exercised,
  not bypassed).

## Hot-path note

No live-call-path changes. The probe *measures* the hot path; gates run pre-promotion, adding
zero per-turn latency.

## Tenant isolation

Environments hold no cross-environment data paths (separate projects/credentials). Within
staging, seed tenants exercise the standard tenant-scoped repository layer.
