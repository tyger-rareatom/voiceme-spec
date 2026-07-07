# Tasks: mvp1-usage-metering

## 1. Pipeline
- [ ] 1.1 Usage event schema (tenant, session, backend, metrics)
- [ ] 1.2 Collector service (Go) + durable store
- [ ] 1.3 Backend usage-callback integration (cascaded first)
- [ ] 1.4 Non-blocking emitter: in-process buffer + local durable spool, at-least-once delivery + idempotent collector ingestion
- [ ] 1.5 Spool-threshold admission policy hook (alert-only default, block-new-sessions behind flag)
- [ ] 1.6 Collector-outage test: turns unaffected during outage, zero event loss after recovery

## 2. Enforcement & visibility
- [ ] 2.1 Cap evaluation + overage policy hook
- [ ] 2.2 Margin dashboard (revenue vs vendor cost per tenant)
- [ ] 2.3 Reconciliation tests vs vendor invoices
