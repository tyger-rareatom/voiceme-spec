# Design: mvp2-complaint-cases

## Approach
- **Detection** comes from the same structured output the LLM already returns per turn (an intent
  field), plus explicit phrases and action-pack dispute events. No separate classifier call on the turn.
- **Confirmation** is a normal spoken turn; the case opens only on a "yes".
- **Template `complaint_case_v1`** on `mvp1-workflow-engine`: `opened → acknowledged → assigned →
  in_progress → resolved → closed`, with `escalated` and `breached` set by timers.
- **Deadline:** period read from the tenant's jurisdiction profile (`complaint_reporting_days`, per
  category where defined) at case open; the profile version is stored on the case so later profile
  changes do not move existing deadlines.
- **Reference numbers:** tenant-prefixed, sequential per tenant, generated in the same transaction as
  the case.
- **Classification:** the tenant's taxonomy (product, category, severity) lives in tenant config; the
  model proposes values at turn end; the owning team can correct them.
- **Routing:** cases go to the tenant CRM as tickets through the existing connector, with the case
  workflow kept in VoiceMe as the clock of record.
- **Duplicates:** open cases for the caller reference are loaded at session setup (shared with the
  follow-through lookup); matter similarity is checked within those cases only.
- **Priority routing:** fraud and vulnerability signals trigger the existing human escalation path at
  top priority.
- **Evidence:** every state change writes to the `mvp2-compliance-evidence` store.

## Tenant isolation
Cases, reference sequences, taxonomies, and evidence are tenant-scoped. Cross-tenant denial test covers
cases and reference lookups (a TelcoOne reference number never resolves an AcmePay case).

## Hot-path sequence note
Intent comes from the existing turn output; confirmation is one extra spoken turn only on complaints;
case creation is written at turn end via the outbox. **Expected impact on the ≤ 1.5 s p50 turn budget:
none per turn.** Instrument detection, confirmation rate, and outbox lag.

## Metering
Acknowledgement and closure messages are metered by the engine.

## Vendor interfaces wrapped
Existing CRM connector and `notification_channel`; no new vendors.
