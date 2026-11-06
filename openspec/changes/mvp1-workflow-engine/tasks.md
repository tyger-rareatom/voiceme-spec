# Tasks: mvp1-workflow-engine

## 1. Events
- [ ] 1.1 Workflow event schema (`enquiry.unanswered`, `commitment.created`, `complaint.detected`, extensible)
- [ ] 1.2 `workflow_outbox` table written in the same transaction as session/turn records
- [ ] 1.3 Outbox relay → NATS JetStream

## 2. Workflow service
- [ ] 2.1 Instance, step, and timer tables (tenant-scoped)
- [ ] 2.2 Idempotent instance creation keyed by source event
- [ ] 2.3 Timer workers (`SKIP LOCKED`), retries with backoff
- [ ] 2.4 Template interface + versioning; tenant parameters from the config store

## 3. Notification adapters
- [ ] 3.1 `notification_channel` interface + stub
- [ ] 3.2 Email adapter (send + inbound reply webhook)
- [ ] 3.3 SMS adapter (reuse wrapped SMS vendor)
- [ ] 3.4 Idempotency keys on every send

## 4. Metering and visibility
- [ ] 4.1 Usage event per message + conformance test (un-metered adapter rejected)
- [ ] 4.2 Per-tenant monthly notification cap + policy
- [ ] 4.3 Overdue alerts + per-tenant open/overdue/completed view

## 5. Tests
- [ ] 5.1 Cross-tenant denial test (instances, recipients, messages)
- [ ] 5.2 Duplicate-event test (one instance)
- [ ] 5.3 Restart-before-timer test (fires once)
- [ ] 5.4 Provider-timeout retry test (message delivered once)
- [ ] 5.5 Workflow-service-down test: turn latency unchanged, events delivered after recovery
