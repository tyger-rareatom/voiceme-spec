# Design: mvp1-tenant-config-store

## Approach
- Config store in the control plane; cached for hot-path reads; changes take effect on next session.
- Defaults are explicit and safe (cascaded audio, pgvector RAG).
