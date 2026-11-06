# Tasks: mvp2-complaint-cases

## 1. Intake
- [ ] 1.1 Complaint intent from turn output + explicit phrases + dispute events
- [ ] 1.2 Spoken confirmation before opening a case
- [ ] 1.3 `complaint.detected` event via outbox on confirmation

## 2. Case workflow
- [ ] 2.1 `complaint_case_v1` state machine
- [ ] 2.2 Tenant-prefixed reference numbers, read out on the call
- [ ] 2.3 Classification against tenant taxonomy; team corrections with history
- [ ] 2.4 Deadline from jurisdiction profile (version stored on the case); reminders, escalation, breach

## 3. Caller communication
- [ ] 3.1 Written acknowledgement (reference + response period)
- [ ] 3.2 Closure message

## 4. Routing and duplicates
- [ ] 4.1 CRM ticket via existing connector; VoiceMe holds the clock of record
- [ ] 4.2 Open-case lookup at session setup; duplicate linking
- [ ] 4.3 Fraud and vulnerability priority routing to a human

## 5. Evidence
- [ ] 5.1 Every state change written to the compliance evidence store
- [ ] 5.2 Complaint section in evidence reports (cases, handling times, breaches)

## 6. Tests
- [ ] 6.1 Cross-tenant denial test (cases, reference lookups)
- [ ] 6.2 Declined confirmation opens no case
- [ ] 6.3 Duplicate complaint links to existing case
- [ ] 6.4 Pre-breach escalation and breach recording
- [ ] 6.5 Fraud report routes to a human immediately
