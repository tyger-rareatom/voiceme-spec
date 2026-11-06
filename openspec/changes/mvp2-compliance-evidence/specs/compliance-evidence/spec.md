## ADDED Requirements

### Requirement: Jurisdiction profiles
The system SHALL assign each tenant one or more versioned jurisdiction profiles and SHALL apply, per
call, the profile's AI-disclosure wording, consent rules for the call's channel, and retention periods.
Profiles SHALL be data, not code, and each version SHALL record who approved it.

#### Scenario: Disclosure follows the profile
- GIVEN a tenant on the Nigeria profile version 3
- WHEN a call starts on the web widget
- THEN the agent speaks profile version 3's AI disclosure before the first answer
- AND the session record stores the profile version applied

#### Scenario: Unapproved profile cannot be activated
- GIVEN a profile version with no recorded approver
- WHEN a tenant admin tries to activate it
- THEN activation is refused

### Requirement: Answer provenance
The system SHALL record, for every agent turn, the retrieved chunk IDs with their document versions,
the tool results used, and the model that produced the answer, linked to the transcript turn.

#### Scenario: Answer traced to its source
- GIVEN a transcript turn in which the agent quoted a fee
- WHEN a compliance user opens that turn
- THEN they see the document name and version the fee came from

#### Scenario: Provenance never crosses tenants
- GIVEN provenance records for AcmePay and TelcoOne
- WHEN a TelcoOne user queries provenance
- THEN no AcmePay record, chunk, or document name is returned

### Requirement: Cross-border transfer register
The system SHALL produce, per tenant and period, a register of every vendor and processing region that
handled the tenant's audio, transcripts, documents, or embeddings, derived from metering events, and
SHALL flag any processing outside the countries the tenant's profile allows.

#### Scenario: Out-of-country processing is flagged
- GIVEN a tenant on the Nigeria profile whose calls are transcribed by an EU endpoint
- WHEN the monthly register is generated
- THEN the register lists the EU endpoint with call counts
- AND it marks the entry as a cross-border transfer

#### Scenario: Usage event without a region is rejected
- GIVEN a backend usage event missing the processing region
- WHEN it reaches the metering collector
- THEN it is accepted for billing and recorded as a register gap, and an alert fires

### Requirement: Append-only evidence store
The system SHALL store consent records, provenance records, profile applications, deletions, and
data-subject request events in a tenant-scoped append-only store that rejects updates and deletes except
retention-driven expiry, which is itself recorded.

#### Scenario: Evidence cannot be edited
- GIVEN an existing consent record
- WHEN any service attempts to modify it
- THEN the write is rejected and the attempt is recorded

### Requirement: Evidence reports
The system SHALL generate, on demand and on a schedule, per-tenant evidence reports covering consent
records, escalation and complaint handling times, the transfer register, retention deletions, and
data-subject requests, exportable as CSV and PDF.

#### Scenario: Compliance user exports a quarterly report
- GIVEN a tenant compliance user
- WHEN they request the report for last quarter
- THEN a CSV and a PDF are produced containing only that tenant's data for that quarter

### Requirement: Data-subject requests
The system SHALL let a caller request access to or deletion of their data during a call, log the
request, route it to the tenant's configured destination, and record its completion date.

#### Scenario: Caller asks to delete their data
- GIVEN a caller asks the agent to delete their recordings
- WHEN the request is captured
- THEN a request record is created and routed to the tenant
- AND the caller is told what happens next and in what period, per the tenant's profile
