# Tasks: mvp1-outcome-billing

## 1. Catalogue
- [ ] 1.1 Catalogue schema (plans, fees, pools, overage, resolution price, modules, pilot terms, currencies)
- [ ] 1.2 Append-only versioning with effective dates; contract pins a version
- [ ] 1.3 Load initial catalogue from the agreed price list

## 2. Resolution lifecycle
- [ ] 2.1 Session-end classifier (definition checks from recorded signals)
- [ ] 2.2 Provisional record + repeat-contact window timer on the workflow engine
- [ ] 2.3 Same-matter matching (caller reference + intent or pack subject)
- [ ] 2.4 L0 rule: finalise only on explicit confirmation
- [ ] 2.5 Final resolution event on the metering spool (idempotent by conversation id)

## 3. Billing
- [ ] 3.1 Resolution and minute lines to the tenant's `billing_provider`
- [ ] 3.2 Fair-use pool and overage policy (bill or block)
- [ ] 3.3 Disputes: hold, queue with evidence, decide, release
- [ ] 3.4 Pilot settlement template (credit note or conversion credit)
- [ ] 3.5 Currency: contract currency, quarterly FX lock, rate source on invoice

## 4. Visibility
- [ ] 4.1 Tenant resolution audit view (transcript link, reason)
- [ ] 4.2 Pilot progress view against the containment target
- [ ] 4.3 Margin guardrail on the internal dashboard (revenue per resolution vs 2x cost)

## 5. Tests
- [ ] 5.1 Cross-tenant denial test (resolution records, disputes, invoice lines)
- [ ] 5.2 Escalated, synthetic, greeting-only and abandoned calls never resolve
- [ ] 5.3 Repeat contact inside the window voids the earlier resolution
- [ ] 5.4 Duplicate event delivery bills once
- [ ] 5.5 Catalogue edit rejected; contract keeps its pinned version
- [ ] 5.6 Pilot miss issues a credit note; pilot conversion credits year 1
- [ ] 5.7 Classification and window-expiry lag instrumentation
