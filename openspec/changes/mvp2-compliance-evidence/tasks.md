# Tasks: mvp2-compliance-evidence

## 1. Jurisdiction profiles
- [ ] 1.1 Profile schema + validator (including approver fields)
- [ ] 1.2 Profile store with versioning; tenant assignment in the portal
- [ ] 1.3 Apply disclosure and consent rules per call and channel; record profile version on the session
- [ ] 1.4 Draft NG, ZA, KE profiles for counsel review

## 2. Provenance
- [ ] 2.1 Add `document_version` to chunks at ingestion and to retrieval results
- [ ] 2.2 Turn-end provenance record (chunks, tool results, model) via the async event path
- [ ] 2.3 Transcript view links each turn to its sources

## 3. Transfer register
- [ ] 3.1 Add mandatory `processing_region` to the usage event schema + conformance check
- [ ] 3.2 Register view per tenant and period; flag countries outside the profile
- [ ] 3.3 Register-gap alert for events without a region

## 4. Evidence store
- [ ] 4.1 Tenant-partitioned append-only table, insert-only role, hash-chained rows
- [ ] 4.2 Route sovereign tenants to the `mvp2-sovereign-deployment` audit log
- [ ] 4.3 Retention-driven expiry with an expiry record

## 5. Reports and requests
- [ ] 5.1 Report builder (consent, handling times, register, deletions, data-subject requests)
- [ ] 5.2 CSV + PDF export; scheduled and on-demand runs
- [ ] 5.3 Data-subject request intents, record, CRM routing, completion tracking

## 6. Tests
- [ ] 6.1 Cross-tenant denial test for provenance, register, evidence store, reports
- [ ] 6.2 Append-only enforcement test (update/delete rejected)
- [ ] 6.3 Unapproved profile activation refused
- [ ] 6.4 Register flags out-of-country processing
- [ ] 6.5 Disclosure duration + provenance spool instrumentation
