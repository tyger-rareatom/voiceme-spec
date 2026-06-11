# Proposal: mvp1-rag-retrieval

## Why
Grounded answers require tenant-scoped retrieval in the live-call hot path.

## What Changes
Add a retrieval API returning top-k chunks for a query, scoped by tenant, behind the `rag_backend`
interface (pgvector first).

## User-visible impact
The agent answers from the tenant's own content only; admits when it doesn't know.

## Rollback
Additive; retrieval can be bypassed per tenant via flag for debugging.
