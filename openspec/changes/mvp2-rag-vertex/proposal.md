# Proposal: mvp2-rag-vertex

## Status
**Phase: MVP 2 — Blocked by:** `mvp1-rag-retrieval`, `mvp1-tenant-config-store`.

> **Re-scope pending (exploration decision):** the Scale/sovereign backend is now **AlloyDB AI
> (ScaNN)**, not Vertex AI RAG Engine — one Postgres lineage (pgvector → AlloyDB → AlloyDB Omni) that
> makes tier upgrades lift-and-shift and fills the sovereign-region hole. Rename to
> `mvp2-rag-alloydb` and update the `rag-backend` / `rag-migration` spec deltas (which still name
> Vertex) when formalized. Rationale in `design.md`. Vertex retained only as "considered, rejected
> (adds an engine family + sovereign hole)."

## Why
Scale-tier tenants need Vertex AI RAG Engine: its fixed node-hour cost amortizes at 100k+ min/month
volume, and it provides the in-region data-residency posture sovereign procurement requires.

## What Changes
Add Vertex AI RAG Engine as a second `rag_backend`, plus an idempotent tier-upgrade migration
(pgvector → Vertex) with a retrieval-parity evaluation.

## User-visible impact
Scale tenants get the residency-compliant RAG backend; upgrades migrate content without quality loss.

## Rollback
Per-tenant `rag_backend` flag back to pgvector; migration is non-destructive (source retained until
parity passes).
