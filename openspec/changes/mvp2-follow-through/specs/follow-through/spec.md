## ADDED Requirements

### Requirement: Every promise becomes a commitment
The system SHALL create a commitment whenever the agent offers or agrees to a later action (callback,
status notice, after-hours follow-up), recording the action, the caller reference, the due time, the
channel, and the call it came from.

#### Scenario: Vendor failure path offers a callback
- GIVEN the failover path offers the caller a callback and the caller accepts
- WHEN the call ends
- THEN a callback commitment exists with a due time and a link to the call

#### Scenario: Offer the caller declines
- GIVEN the caller declines a callback
- WHEN the call ends
- THEN no commitment is created and no follow-up is sent

### Requirement: Scheduling within allowed hours
The system SHALL schedule every follow-up inside the tenant's business hours, the caller's stated
preference, and the jurisdiction profile's contact rules, and SHALL tell the caller the expected time.

#### Scenario: After-hours call
- GIVEN a call at 22:30 and tenant hours of 08:00–18:00
- WHEN the caller accepts a callback
- THEN the agent states the callback will come after 08:00
- AND the commitment is due within the tenant's first-hour window

### Requirement: Human callback with context
The system SHALL place each callback commitment in the tenant's callback queue (or CRM) with the call
summary, transcript link, and verification level, and SHALL send the caller a message before the
callback that names the tenant and the number that will call.

#### Scenario: Pre-callback notice
- GIVEN a callback due at 10:00
- WHEN the callback is about to be made
- THEN the caller receives a message naming the tenant and the calling number

### Requirement: Re-verification on callback
The system SHALL require the caller to be verified again on a callback before any account information is
shared.

#### Scenario: Callback reaches the number
- GIVEN a human agent places a callback
- WHEN the person answers
- THEN account information is shared only after verification succeeds

### Requirement: Status watch notifications
The system SHALL, for a status-watch commitment, check the tenant system through the action-pack
connector on a schedule or by tenant webhook, and SHALL notify the caller once when the status reaches
the watched outcome or the watch expires.

#### Scenario: Reversal completes
- GIVEN a status watch on a transfer reversal
- WHEN the tenant system reports the reversal completed
- THEN the caller receives one message saying so and the commitment closes

### Requirement: Pre-breach escalation
The system SHALL escalate an open commitment to the tenant's supervisor contact before its due time
passes, at a tenant-configured lead time.

#### Scenario: Callback not yet made
- GIVEN a lead time of 30 minutes
- WHEN a callback is still open 30 minutes before it is due
- THEN the supervisor is alerted

### Requirement: Duplicate-safe closure
The system SHALL close or update an open commitment when the same caller contacts the tenant about the
same matter first, so the caller does not receive a redundant follow-up.

#### Scenario: Caller calls back first
- GIVEN an open callback commitment for a caller
- WHEN that caller calls again and the matter is resolved
- THEN the commitment closes and the scheduled callback is cancelled

### Requirement: Unreachable caller handling
The system SHALL retry an unanswered callback according to the tenant's retry policy and, when attempts
are exhausted, SHALL send a message with the tenant's contact route and mark the commitment as
attempted.

#### Scenario: Three missed attempts
- GIVEN a retry policy of 3 attempts
- WHEN all 3 go unanswered
- THEN the caller gets a message with the contact route and the commitment is marked attempted

### Requirement: Promise-keeping metrics
The system SHALL report per tenant the share of commitments kept on time, kept late, attempted, and
broken.

#### Scenario: Tenant reviews follow-through
- GIVEN a tenant admin opens the follow-through dashboard
- THEN it shows those shares for the selected period, for that tenant only
