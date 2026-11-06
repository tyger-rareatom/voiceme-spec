# Tasks: mvp1-knowledge-gap-loop

## 1. Detection and capture
- [ ] 1.1 Gap signals on the turn (retrieval threshold, ungrounded flag, dissatisfaction intent)
- [ ] 1.2 Account-specific exclusion → escalation
- [ ] 1.3 Spoken follow-up offer, channel choice, number read-back, consent record
- [ ] 1.4 `enquiry.unanswered` event via outbox

## 2. Workflow template
- [ ] 2.1 `knowledge_gap_v1` state machine on the workflow engine
- [ ] 2.2 Similarity grouping within the tenant
- [ ] 2.3 Urgent email + scheduled digest to registered admins

## 3. Answer intake
- [ ] 3.1 Signed single-use reply tokens in Reply-To
- [ ] 3.2 Inbound reply webhook: token, sender, SPF/DKIM checks; strip quoted text
- [ ] 3.3 Portal approval view with conflict check against existing chunks

## 4. Publish and notify
- [ ] 4.1 Approved answer → `gap_answer` knowledge source via ingestion (PII scrubbed)
- [ ] 4.2 Caller follow-up via SMS (once per caller, idempotent)
- [ ] 4.3 Expiry timer + apology message

## 5. Visibility
- [ ] 5.1 Gap dashboard: gap rate, median time to answer, expired, top groups

## 6. Tests
- [ ] 6.1 Cross-tenant denial test (enquiries, digests, reply tokens)
- [ ] 6.2 Unknown-sender and invalid-token rejection tests
- [ ] 6.3 Conflict detection test
- [ ] 6.4 Approved answer retrievable within one hour + callers notified once
- [ ] 6.5 Account-specific question routed to escalation, not KB
