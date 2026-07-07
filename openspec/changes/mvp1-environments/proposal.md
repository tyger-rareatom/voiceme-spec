# Proposal: mvp1-environments

**Capability:** `deployment-environments` · **Phase:** MVP 1

## Why
Voice has properties that cannot be validated locally: real WebRTC media paths, real EU-pinned
vendor latency, the 1.5s p50 turn budget, and the isolation/metering release gates. Without a
spec'd staging + production topology, every GA deliverable (metering accuracy, isolation proof,
latency SLO) lacks a place to be proven before it reaches paying tenants.

## What Changes
Define two spec'd environments — **staging** and **production** — as separate GCP projects built
from the same Terraform modules in the same region (`europe-west3`), with per-environment vendor
keys and secrets, a gated promotion pipeline (isolation suite + synthetic-call SLO + metering
smoke test), staging data governance (no production data; AcmePay/TelcoOne seed tenants), and a
synthetic call probe as a first-class staging fixture. Local dev remains docker-compose and is
documented, not spec'd.

## User-visible impact
None directly (internal). Indirectly: underpins SLA claims, prevents un-gated regressions from
reaching tenant traffic, and gives the two open hosting spikes (Joburg→Frankfurt latency,
Deepgram Nigerian-English WER) a repeatable home.

## Rollback
Additive — environments are new infrastructure. Promotion gates are flag-relaxable in an
emergency (documented break-glass), and staging can be torn down and re-created from Terraform
at any time.

## Prerequisites
- `mvp1-tenant-provisioning` (seed tenants), `mvp1-usage-metering` (metering smoke test),
  `mvp1-observability` (probe metrics land somewhere). The promotion gate consumes the
  cross-tenant isolation suite from `mvp1-tenant-provisioning` task 1.6.
