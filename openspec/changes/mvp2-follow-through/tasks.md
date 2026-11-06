# Tasks: mvp2-follow-through

## 1. Commitment capture
- [ ] 1.1 Shared `offer_follow_up()` in the runtime; wire failover and action-pack offers to it
- [ ] 1.2 `commitment.created` event via outbox (accepted offers only)
- [ ] 1.3 Spoken expected follow-up time

## 2. Workflow template
- [ ] 2.1 `follow_through_v1` state machine
- [ ] 2.2 Scheduler: tenant hours, caller preference, jurisdiction contact rules
- [ ] 2.3 Pre-breach escalation timer to supervisor

## 3. Fulfilment
- [ ] 3.1 Human callback via CRM connector or VoiceMe callback queue
- [ ] 3.2 Pre-callback notice naming tenant and calling number
- [ ] 3.3 Re-verification requirement surfaced to the human agent
- [ ] 3.4 Status watch (poll or tenant webhook) via action-pack connector
- [ ] 3.5 Retry policy + exhausted-attempts message

## 4. Duplicates and channels
- [ ] 4.1 Open-commitment lookup at session setup; close on resolution
- [ ] 4.2 WhatsApp `notification_channel` adapter (approved templates)

## 5. Visibility
- [ ] 5.1 Promises kept / late / attempted / broken dashboard

## 6. Tests
- [ ] 6.1 Cross-tenant denial test (commitments, watches)
- [ ] 6.2 Declined offer creates nothing
- [ ] 6.3 After-hours scheduling test
- [ ] 6.4 Caller-calls-first cancellation test
- [ ] 6.5 Status watch notifies once
