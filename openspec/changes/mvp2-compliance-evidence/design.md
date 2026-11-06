# Design: mvp2-compliance-evidence

## Approach
- **Jurisdiction profiles** are versioned documents in the control plane (schema-validated YAML/JSON):
  `country`, `disclosure_text` per language, `consent` rules per channel, `retention` per data class,
  `allowed_processing_countries`, `complaint_reporting_days`, `dsr_response_days`, `approved_by`,
  `approved_at`. First profiles: NG (NDPA (Nigeria Data Protection Act)), ZA (POPIA (Protection of
  Personal Information Act)), KE (Kenya Data Protection Act). Profile **contents are counsel-owned**;
  engineering owns the schema and enforcement.
- **Provenance** is written by the session runtime at turn end through the non-blocking event path
  (same class as metering: lossless spool, at-least-once). Retrieval already returns chunk IDs; this
  change adds `document_version` to chunks at ingestion and to retrieval results.
- **Transfer register** is a derived view over metering events. This change adds a mandatory
  `processing_region` field to the usage event schema (extend `mvp1-usage-metering` conformance).
- **Evidence store:** standard tenants get a tenant-partitioned append-only table (insert-only role,
  hash-chained rows for tamper evidence). Sovereign tenants write to the `mvp2-sovereign-deployment`
  audit log in-region.
- **Reports:** a scheduled job in the control plane builds per-tenant reports from the evidence store,
  provenance, metering, and CRM escalation timestamps. Output: CSV + PDF.
- **Data-subject requests:** an agent intent (`dsr_access`, `dsr_delete`) creates a request record and a
  CRM ticket through the existing connector; completion is recorded when the tenant closes it.

## Tenant isolation
All records carry `tenant_id` and go through the tenant-scoped repository layer. Reports are built per
tenant only. Cross-tenant denial test covers provenance, register, evidence store, and reports.

## Hot-path sequence note
Disclosure is spoken during the greeting (adds its spoken length to the first turn only). Provenance
writes are async at turn end. **Expected impact on the ≤ 1.5 s p50 turn budget: none after the first
turn.** Instrument disclosure duration and provenance spool depth.

## Metering
No new billable usage. The `processing_region` field is added to every usage event; events without it
are accepted for billing but recorded as register gaps (billing integrity comes first).

## Vendor interfaces wrapped
None new. PDF rendering sits behind an internal report-renderer interface.

## Relationship to other changes
- Extends `mvp2-sovereign-deployment` task 3.1 (control mapping) from a one-off document to a generated
  report.
- Feeds Phase 5 `compliance-certifications` with continuous evidence.
