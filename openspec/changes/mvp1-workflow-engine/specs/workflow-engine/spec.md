## ADDED Requirements

### Requirement: Lossless, non-blocking workflow events
The system SHALL write each workflow event in the same database transaction as the record that caused
it (transactional outbox), SHALL deliver it to the workflow service at least once, and SHALL NOT make any
caller turn wait on event delivery.

#### Scenario: Workflow service down during a call
- GIVEN the workflow service is unavailable
- WHEN a call emits an `enquiry.unanswered` event
- THEN the caller's turn latency is unaffected
- AND the event is delivered once the service recovers

#### Scenario: Duplicate delivery
- GIVEN the same event is delivered twice
- WHEN the workflow service processes it
- THEN exactly one workflow instance exists for that event

### Requirement: Tenant-configured workflow templates
The system SHALL run workflows only from platform-defined, versioned templates, and SHALL let each
tenant set the template's parameters (recipients, timers, channels, wording) without changing its
logic.

#### Scenario: Tenant changes a timer
- GIVEN AcmePay sets its digest time to 08:00
- WHEN the next digest is due
- THEN it is sent at 08:00 AcmePay time and the change does not alter running instances' history

#### Scenario: Workflows never cross tenants
- GIVEN workflow instances for AcmePay and TelcoOne
- WHEN a TelcoOne admin lists or acts on workflows
- THEN no AcmePay instance, recipient, or message is visible or actionable

### Requirement: Durable timers and retries
The system SHALL persist workflow state and timers so that a restart of the workflow service neither
loses nor double-fires a timer, and SHALL retry failed actions with backoff up to a configured limit.

#### Scenario: Restart before a timer fires
- GIVEN a timer due at 10:00 and the service restarts at 09:59
- WHEN the service is back
- THEN the timer fires once, after recovery

### Requirement: Idempotent notification actions
The system SHALL give every outbound notification an idempotency key so that a retry never sends the
same message twice.

#### Scenario: Provider times out after accepting
- GIVEN the SMS provider accepted a message but the response timed out
- WHEN the action is retried
- THEN the caller receives the message once

### Requirement: Notification adapters are wrapped and metered
The system SHALL send notifications only through a `notification_channel` interface, and SHALL emit a
usage event for every message sent, tagged with tenant, workflow, channel, and outcome.

#### Scenario: Un-metered adapter is rejected
- GIVEN a channel adapter without the usage callback
- WHEN it is registered
- THEN registration fails conformance

#### Scenario: Monthly notification cap reached
- GIVEN a tenant at its monthly notification cap
- WHEN a workflow tries to send another message
- THEN the tenant's cap policy applies (hold and alert, or bill overage)

### Requirement: Overdue visibility
The system SHALL alert when a workflow step passes its due time without completing, and SHALL show
per-tenant counts of open, overdue, and completed instances.

#### Scenario: Step overdue
- GIVEN a workflow step due at 12:00
- WHEN it is still open at 12:00
- THEN an overdue alert fires and the tenant dashboard shows it as overdue
