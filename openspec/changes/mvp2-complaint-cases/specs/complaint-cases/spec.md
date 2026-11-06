## ADDED Requirements

### Requirement: Confirmed complaint intake
The system SHALL open a formal complaint case only after the caller confirms they want one, when the
caller asks to complain, complaint intent is detected, or an action pack opens a dispute.

#### Scenario: Frustrated caller, no formal complaint
- GIVEN a caller expresses frustration about a delay
- WHEN the agent asks whether to log a formal complaint and the caller says no
- THEN no complaint case is opened and the call continues

#### Scenario: Caller confirms a complaint
- GIVEN a caller says they want to complain about a failed transfer
- WHEN they confirm
- THEN a complaint case is opened with the transcript, classification, and caller reference

### Requirement: Reference number on the call
The system SHALL give the caller a case reference number during the call, and SHALL state the response
period from the tenant's jurisdiction profile.

#### Scenario: Reference read out
- GIVEN a confirmed complaint
- WHEN the case is opened
- THEN the agent reads out the reference number and the response period before the call ends

### Requirement: Classification
The system SHALL classify each case by product, category, and severity using the tenant's taxonomy, and
SHALL let the owning team correct the classification with the change recorded.

#### Scenario: Team corrects the category
- GIVEN a case classified as "card"
- WHEN the owning team changes it to "transfer"
- THEN the case shows the new category and the change is in its history

### Requirement: Deadline clock and escalation
The system SHALL start a deadline clock for each case from the jurisdiction profile's complaint period
for its category, send reminders to the owning team, and escalate before the deadline breaches.

#### Scenario: Case nears its deadline
- GIVEN a case due in 2 days with an escalation lead time of 24 hours
- WHEN it is still open 24 hours before the deadline
- THEN the escalation contact is alerted

#### Scenario: Breach is recorded
- GIVEN a case still open at its deadline
- WHEN the deadline passes
- THEN the case is marked breached and the breach appears in evidence reports

### Requirement: Written acknowledgement and closure
The system SHALL send the caller a written acknowledgement with the reference number and response period
after the call, and a closure message when the case is resolved.

#### Scenario: Case closed
- GIVEN the owning team resolves a case
- WHEN they record the resolution
- THEN the caller receives a closure message with the reference number

### Requirement: Duplicate merging
The system SHALL link a new complaint to an open case for the same caller and matter instead of opening
a second case, and SHALL tell the caller the existing reference number.

#### Scenario: Caller complains again
- GIVEN an open case for a caller's failed transfer
- WHEN the same caller complains about the same transfer
- THEN the new call is added to the existing case and the caller hears its reference number

### Requirement: Priority routing for fraud and vulnerable callers
The system SHALL route a complaint that reports fraud or indicates a vulnerable caller directly to a
human, ahead of the normal queue, and SHALL still open the case.

#### Scenario: Caller reports fraud
- GIVEN a caller says money was taken without their permission
- WHEN the complaint is confirmed
- THEN the call is handed to a human immediately
- AND a high-severity case is opened

### Requirement: Complaint evidence
The system SHALL record every case event (opened, classified, reminded, escalated, breached, closed) in
the tenant's compliance evidence store.

#### Scenario: Quarterly report includes complaints
- GIVEN complaint cases in the last quarter
- WHEN a compliance user exports the evidence report
- THEN it lists cases, handling times, and breaches for that tenant only
