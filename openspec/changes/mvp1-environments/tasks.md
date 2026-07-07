# Tasks: mvp1-environments

## 1. Infrastructure

- [ ] 1.1 Terraform modules for the full topology, parameterized by environment tfvars (region fixed `europe-west3`)
- [ ] 1.2 Provision staging + production GCP projects (IAM, budgets + budget alerts, Secret Manager per project)
- [ ] 1.3 Per-environment vendor keys (Deepgram/Cartesia/Vertex/LiveKit staging-scoped; Stripe test mode in staging)
- [ ] 1.4 Environment parity check in CI (declared component list vs deployed topology, both envs)

## 2. Staging fixtures

- [ ] 2.1 Seed-tenant provisioning script (AcmePay, TelcoOne: distinct docs, configs, credentials), idempotent on reset
- [ ] 2.2 Synthetic call probe: LiveKit scripted caller + canned audio corpus + per-segment latency assertion vs SLO
- [ ] 2.3 Tag + exclude synthetic traffic from billing aggregates while keeping it in observability (test: probe call → no billable usage, visible telemetry)
- [ ] 2.4 Collector-outage chaos gate: kill metering collector in staging, run probe (turn latency unchanged), restore, assert spooled usage events reconcile with calls (zero loss)

## 3. Promotion pipeline

- [ ] 3.1 Deploy-to-staging on merge; promotion job gated on isolation suite + probe SLO + metering smoke test
- [ ] 3.2 Metering smoke test (staging call completes → usage record exists with tenant/backend/metrics)
- [ ] 3.3 Break-glass bypass path (authz-restricted, audited, alerting)
- [ ] 3.4 Cross-environment isolation test (staging credentials denied against production resources)

## 4. Production durability

- [ ] 4.1 Postgres PITR configuration + stated RPO/RTO, restore drill documented
- [ ] 4.2 Widget CDN channels: staging tracks latest, production pinned with explicit promote/rollback
- [ ] 4.3 Staging data-governance guard (block prod-datastore restore/copy into staging, log attempts)
