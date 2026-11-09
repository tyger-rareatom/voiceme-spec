# Proposal: mvp1-outcome-billing

## Status
**Phase: MVP 1 — Blocked by:** `mvp1-usage-metering`, `mvp1-billing-subscription`,
`mvp1-tenant-config-store`, `mvp1-observability`. **Uses** `mvp1-caller-verification` (caller
reference for repeat-contact matching) and `mvp1-workflow-engine` (resolution windows, pilot
evaluation). **Feeds** `mvp2-action-packs`, whose per-pack resolution criteria emit into the same
resolution event defined here. **Replaces** the minute-tier pricing card in `project.md` §7.

## Why
The minute-tier card (Starter $2–5k / Growth $10–20k / Scale $30–60k with included minutes) prices a
three-minute call at about $3.00–4.50 on Growth. A human-handled contact at a Nigerian lender or
fintech costs an estimated $0.23–0.57 (founders' pitch model: $300–500 per agent per month; assumed
40–60 calls per agent per day). The card therefore charges 5–20x the cost of the alternative, which is
why the customer ROI case fails and why the founder-board Offers lens conditioned funding on repricing.

Buyers pay for compliance, verified answers and resolved calls, not for minutes. Minute pricing also
rewards slow calls and exposes VoiceMe's cost structure. The fix is a three-part structure:
- a **platform fee** priced by compliance and deployment level, which carries most of the margin;
- a **per-resolution fee**, the value metric, priced between 2x VoiceMe's cost per resolved call and
  the buyer's cost per human contact;
- **modules** priced on value, with third-party costs passed through;

plus a **paid pilot with a containment guarantee**. Outcome pricing only works if "resolved" is
defined, measured and auditable, so this change defines it.

## What Changes
- Add a versioned **pricing catalogue** held as data (plans, platform fees, fair-use minute pools,
  overage, resolution price, modules, pilot terms, currencies). Contracts pin a catalogue version.
- Define a **resolved conversation** and a provisional → final **resolution lifecycle** with a
  repeat-contact window.
- Emit **resolution events** (final, idempotent, one per conversation at most) to metering and billing.
- Add **resolution audit and disputes** visible to the tenant.
- Add **pilot billing**: fixed fee, containment target, automatic credit note when missed, credit
  toward the first contract year when converted.
- Add **currency handling**: USD list prices; per-tenant invoice currency; FX rate locked per quarter
  with its source recorded.
- Add a **margin guardrail** on the internal margin dashboard.

## User-visible impact
- Tenants see each billed resolution with the transcript and the reason it counted.
- Tenants can dispute a resolution within the billing period.
- Pilots show progress against the containment target and settle automatically.

## Rollback
Per-tenant `billing_model` flag in the tenant config store (`outcome` | `legacy_minutes`). Resolution
events are recorded from day one but only billed when the flag is `outcome`. Catalogue versions are
append-only, so a bad version is superseded, never edited.

## Out of scope
- Final list prices: the catalogue holds them as data. Initial values come from the pricing work
  (`founder/pricing.md`) and change without a code release.
- Action-pack module pricing logic beyond a catalogue line item (`mvp2-action-packs`).
