# Proposal: mvp3-gpu-ops

## Status
**Phase: MVP 3 — Blocked by:** `mvp1-observability`, `mvp1-usage-metering`. Build alongside
`mvp3-audio-nvidia`. **This is a dedicated platform workstream — not absorbable by the MVP team.**

## Why
Self-hosted NIM at production quality requires real GPU operations: deployment, concurrency-aware
autoscaling, MLOps (versioned models, rollback), and cost telemetry. Without this, the NVIDIA path
is a demo, not a tier.

## What Changes
Stand up the GPU serving substrate and its operations: NIM orchestration, autoscaling on call
concurrency, model lifecycle management, GPU cost telemetry into the margin dashboard, and the
self-host inflection routing input.

## User-visible impact
Internal; underpins NVIDIA-backend reliability, SLA, and unit economics.

## Rollback
GPU substrate is independent; tear-down reverts affected tenants to managed backends.
