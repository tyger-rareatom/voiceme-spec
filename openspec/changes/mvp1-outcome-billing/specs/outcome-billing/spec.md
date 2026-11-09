## ADDED Requirements

### Requirement: Versioned pricing catalogue
The system SHALL hold plans, platform fees, fair-use minute pools, overage rates, resolution prices,
modules, pilot terms and currencies as a versioned, effective-dated catalogue, SHALL pin each tenant
contract to one catalogue version, and SHALL NOT hardcode any price in application code.

#### Scenario: Price change does not move existing contracts
- GIVEN AcmePay's contract is pinned to catalogue version 3
- WHEN catalogue version 4 raises the resolution price
- THEN AcmePay is billed at version 3 prices until its contract is renewed on version 4

#### Scenario: Catalogue versions are append-only
- GIVEN catalogue version 3 is published
- WHEN anyone attempts to edit a price in version 3
- THEN the edit is rejected and a new version must be created

### Requirement: Resolved conversation definition
The system SHALL classify a conversation as provisionally resolved only when all of these hold: the
caller confirmed the answer or ended the conversation without asking for a human; no escalation,
failure path, complaint case or follow-up commitment was opened; and the conversation was not
greeting-only, abandoned within the tenant's minimum duration, or synthetic.

#### Scenario: Escalated call is not resolved
- GIVEN a caller asks for a human and is handed to the tenant's team
- WHEN the conversation ends
- THEN it is classified as not resolved and no resolution fee accrues

#### Scenario: Synthetic probe is never billed
- GIVEN a synthetic-call probe from the staging promotion gate
- WHEN it completes
- THEN it is excluded from resolution classification

### Requirement: Repeat-contact window
The system SHALL hold each provisional resolution for a repeat-contact window (default 72 hours,
tenant-configurable between 24 and 168 hours) and SHALL finalise it only if the same caller reference
has not contacted the tenant about the same matter within the window.

#### Scenario: Caller comes back about the same transfer
- GIVEN a provisional resolution for a transfer-status question at 10:00 on Monday
- WHEN the same caller asks about the same transfer at 09:00 on Tuesday
- THEN the Monday resolution is voided and only the later conversation can resolve

#### Scenario: Anonymous caller
- GIVEN a session at assurance level L0 with no caller reference
- WHEN it ends without explicit spoken confirmation that the question was answered
- THEN it is not finalised as resolved, because a repeat contact cannot be checked

### Requirement: Resolution events
The system SHALL emit exactly one final resolution event per resolved conversation, carrying tenant,
conversation, catalogue version, resolution reason and the evidence that satisfied the definition, and
SHALL deliver it to metering and billing idempotently.

#### Scenario: Duplicate delivery is billed once
- GIVEN a final resolution event is delivered twice
- WHEN billing processes it
- THEN the tenant is charged once

#### Scenario: Resolution events never cross tenants
- GIVEN resolution events for AcmePay and TelcoOne
- WHEN TelcoOne's invoice is built
- THEN no AcmePay event, conversation or amount appears on it

### Requirement: Resolution audit and disputes
The system SHALL show tenants every billed resolution with its transcript link and reason, and SHALL let
a tenant admin dispute a resolution until the billing period closes, holding the disputed amount off the
invoice until the dispute is decided.

#### Scenario: Tenant disputes a resolution
- GIVEN a billed resolution the tenant believes was wrong
- WHEN the admin disputes it before period close
- THEN the amount is held off the invoice and the dispute is queued with the evidence

### Requirement: Fair-use minutes and overage
The system SHALL include a fair-use pool of conversation minutes in each plan for unresolved, escalated
and resolved conversations alike, and SHALL bill minutes above the pool at the catalogue overage rate
under the tenant's overage policy.

#### Scenario: Pool exceeded
- GIVEN a tenant has used its monthly minute pool
- WHEN further conversations take place
- THEN the extra minutes are billed at the catalogue overage rate, or blocked if the tenant chose block

### Requirement: Pilot billing with containment guarantee
The system SHALL support a pilot contract with a fixed fee, a duration, an agreed containment target
(share of AI-handled conversations finalised as resolved) and a measurement window, SHALL issue a
credit note for the pilot fee automatically if the target is missed, and SHALL credit the pilot fee
against the first contract year when the tenant converts.

#### Scenario: Target missed
- GIVEN a 90-day pilot with a 40% containment target
- WHEN the pilot ends at 33% containment
- THEN a credit note for the pilot fee is issued and recorded with the measured rate

#### Scenario: Pilot converts
- GIVEN a pilot that met its target
- WHEN the tenant signs an annual contract
- THEN the pilot fee is credited against the first year's invoices

### Requirement: Currency and FX
The system SHALL keep list prices in USD, invoice each tenant in its contract currency, and, for
non-USD invoices, convert at an FX rate locked for the quarter with the rate and its source recorded on
every invoice.

#### Scenario: Naira invoice
- GIVEN a Nigerian tenant invoiced in naira
- WHEN a monthly invoice is issued
- THEN the invoice shows the USD amount, the locked quarterly rate, its source and the naira total

### Requirement: Margin guardrail
The system SHALL compute, per tenant and month, revenue per final resolution against VoiceMe's cost per
resolved conversation, and SHALL alert when revenue falls below twice that cost.

#### Scenario: Long calls erode margin
- GIVEN a tenant whose average resolved call grows from 3 to 7 minutes
- WHEN the monthly margin is computed
- THEN an alert fires if revenue per resolution is below twice the cost per resolved conversation
