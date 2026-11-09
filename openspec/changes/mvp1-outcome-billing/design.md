# Design: mvp1-outcome-billing

## Pricing structure the catalogue encodes
| Layer | What it charges for | Notes |
|---|---|---|
| Platform fee | Compliance and deployment level: Standard, Regulated, Sovereign | Carries most of the margin; annual contract, billed quarterly in advance |
| Per-resolution fee | Each final resolved conversation | Price between 2x cost per resolved call and the buyer's cost per human contact |
| Fair-use minutes | Minute pool per plan; overage per minute | Covers unresolved and escalated time; overage near cost |
| Modules | Action packs, operator caller checks, phone and WhatsApp channels, specialist languages, onboarding | Third-party costs passed through with a margin |
| Pilot | Fixed fee, containment target, credit-back | Board condition for a guarantee the margin can carry |

Initial list prices are data, set from `founder/pricing.md` (VoiceMe founder pack) and changed by
publishing a new catalogue version.

### Initial catalogue (version 1, 9 November 2026)
| Item | Price | Basis |
|---|---|---|
| Standard platform fee | $1,000 / month | Hypothesis; not yet tested with buyers |
| Regulated platform fee | $3,500 / month | Simulated buyer panel: acceptable range $1,520–5,003, indifference point $3,505 |
| Action-pack module | $1,500 / month (Regulated only) | Brings the Regulated + Actions price to $5,000, top of the range; to be tested |
| Resolution fee | $0.45 per final resolution | Between 2x cost per resolved call ($0.28–0.56) and estimated human cost per contact ($0.23–0.57) |
| Sovereign platform fee | Not priced | Waits for the in-country speech-processing cost |
| Design-partner pilot | No platform fee; $0.45 per resolution with a $1,500 monthly minimum; 90 days; minimums credited back if the containment target is missed | Board condition (guarantee) and panel requests ("no platform fee until the resolution share is proven") |

These are starting values to be confirmed in the Gate 2 discovery calls. The CFO model at these prices
puts break-even at 18 paying tenants, or 12 with the action-pack module and a 5 Standard : 7
Regulated mix.

## Resolution lifecycle
```
conversation end
  → classify (definition checks)            → not_resolved (terminal)
  → provisional_resolved
      → repeat contact, same caller + matter → voided (terminal)
      → window expires                       → final_resolved → resolution event
```
- **Classification** runs at session end, off the turn path, from signals already recorded: caller
  confirmation intent, hand-off and failure-path events, complaint and commitment events, duration,
  synthetic tag.
- **Window timers** run on `mvp1-workflow-engine` (durable, idempotent). The window length is
  read from tenant config at session end and stored on the record.
- **Same matter**: same caller reference (tenant-scoped hash from `mvp1-caller-verification`) and the
  same top-level intent or pack (for action packs, the same subject, such as the transfer reference).
- **L0 sessions** have no caller reference, so they finalise only on explicit spoken confirmation.
- **Action packs** (`mvp2-action-packs`) add pack-specific criteria; they feed this lifecycle rather
  than emitting a separate billing event.

## Billing integration
- Final resolution events and minute usage flow through the existing metering spool to the collector,
  then to the tenant's `billing_provider` (Stripe for USD; Paystack or Flutterwave for African
  currencies, per the open gap in `mvp1-billing-subscription`).
- Disputes hold line items in a `disputed` state; the invoice builder excludes them until decided.
- Pilot settlement is a workflow template: at pilot end, compute containment over the measurement
  window and issue either a credit note or a conversion credit.

## Currency
List prices in USD. A tenant's contract currency is set at signing. For non-USD invoices the quarterly
FX rate and its source are stored on the catalogue-quarter record. Whether USD invoicing of Nigerian
customers is permitted is a counsel question; the design supports either answer.

## Tenant isolation
Catalogue versions are global; contracts, resolution records, disputes, pilot records and invoices are
tenant-scoped through the repository layer. Cross-tenant denial tests cover resolution records,
disputes and invoice lines.

## Hot-path sequence note
Classification and window timers run after the session ends. **Expected impact on the ≤ 1.5 s p50
turn budget: none.** Instrument classification lag and window-expiry lag.

## Metering
Resolution events are a new lossless event class on the existing spool (at-least-once, idempotent by
conversation id). Minute usage is unchanged.

## Vendor interfaces wrapped
`billing_provider` (Stripe, Paystack or Flutterwave). No vendor SDK in classification or catalogue
code.
