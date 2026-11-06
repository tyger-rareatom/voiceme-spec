# Design: mvp1-workflow-engine

## Approach
Pattern: **event-driven architecture** with a **transactional outbox** and a **durable workflow state
machine**.

- **Outbox:** the session runtime writes `workflow_outbox` rows in the same Postgres transaction as the
  session or turn record that caused them. A relay publishes rows to NATS JetStream and marks them sent.
  The write path follows the non-blocking persistence rule: it happens at turn end through the existing
  async spool, never inside the audio loop.
- **Workflow service** (Go, same class as the metering collector): consumes JetStream, creates or
  advances `workflow_instances` keyed by `(tenant_id, template, source_event_id)` for idempotency.
  Steps and timers live in Postgres (`workflow_steps`, `workflow_timers`); workers claim due timers with
  `SELECT … FOR UPDATE SKIP LOCKED`.
- **Templates:** code-defined state machines, versioned. Tenant parameters live in the tenant config
  store. A running instance keeps the template version it started with.
- **Notification adapters** (`notification_channel`): `send(tenant, recipient_ref, template_id,
  vars, idempotency_key) -> Result`. MVP 1 implementations: email (send + inbound reply webhook) and SMS
  (reuses the SMS vendor already wrapped for `mvp1-caller-verification` OTP). Recipients are references
  resolved at send time, so raw contact details are not copied into workflow state.

## Build vs buy
| Option | Pros | Cons | Decision |
|---|---|---|---|
| Postgres state + JetStream (this design) | Fits the stack; no new cluster; cheap at idle | Timers, retries, idempotency built in-house | **Chosen for MVP 1–2** |
| Temporal | Proven durable execution and timers | Extra cluster to run; heavy for fixed templates | Revisit for tenant-authored workflows (Phase 5) |

## Tenant isolation
All workflow tables carry `tenant_id` and go through the tenant-scoped repository layer. Cross-tenant
denial test covers instances, recipients, and messages.

## Hot-path sequence note
No change to the turn path: events are written at turn end via the async spool. **Expected impact on the
≤ 1.5 s p50 turn budget: none.** Instrument outbox lag (event written → consumed) and spool depth.

## Metering
Every message emits a usage event (channel, provider, segments or size). Notification caps read the
running count from the metering plane.

## Vendor interfaces wrapped
`notification_channel` (email provider, SMS vendor). No vendor SDK in workflow logic.
