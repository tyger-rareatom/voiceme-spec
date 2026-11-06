# Design: mvp2-follow-through

## Approach
- **Commitment source:** the runtime emits `commitment.created` when the caller accepts an offer. The
  offers already specified in `mvp1-failover-baseline` and `mvp2-action-packs` call one shared
  `offer_follow_up()` function in the runtime, so every offer path produces the same event. Those specs
  are not archived yet, so this change wires them through the shared function rather than adding
  `MODIFIED` deltas.
- **Template `follow_through_v1`** on `mvp1-workflow-engine`: `scheduled → notified → in_progress →
  kept | kept_late | attempted | broken | cancelled`. Pre-breach escalation is a timer at
  `due − lead_time`.
- **Scheduling** combines tenant hours (agent configuration), caller preference, and the jurisdiction
  profile's contact rules (`mvp2-compliance-evidence`; until it is available, tenant hours only).
- **Human callbacks** go to the tenant CRM through the existing connector (queue item or task with due
  time) or to a VoiceMe callback queue view for tenants without a CRM.
- **Status watches** poll through the `mvp2-action-packs` connector at a bounded interval, or accept a
  tenant webhook. Watches are read-only and use the caller's subject binding.
- **Duplicate closure:** an inbound call from a caller with an open commitment surfaces it to the agent
  at session setup; the agent confirms and closes it.
- **WhatsApp adapter:** a new `notification_channel` implementation using an approved WhatsApp Business
  message template (outside the 24-hour window, only pre-approved templates may be sent).

## Tenant isolation
Commitments, queues, and watches are tenant-scoped. Cross-tenant denial test covers commitments and
status watches.

## Hot-path sequence note
Open-commitment lookup runs once at session setup with tenant config (indexed by caller reference).
**Expected impact on the ≤ 1.5 s p50 turn budget: none per turn;** session setup adds one indexed read.
Instrument the lookup and outbox lag.

## Metering
Messages are metered by the engine; status-watch polls are metered as connector calls.

## Vendor interfaces wrapped
`notification_channel` (new WhatsApp implementation), existing CRM and action connectors.

## Out of scope
Automated outbound voice callbacks: Phase 4 `outbound-voice` adds an outbound-voice adapter to this
template, behind its own consent and compliance controls.
