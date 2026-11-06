## ADDED Requirements

### Requirement: Knowledge-gap detection
The system SHALL create an open enquiry when retrieval returns no relevant content, when answer
confidence falls below the tenant threshold, or when the caller says the answer did not help.

#### Scenario: No relevant content
- GIVEN a question with no relevant tenant chunks
- WHEN the agent responds
- THEN it says it does not have that information yet and offers to send the answer later
- AND an open enquiry is created with the question and a link to the call

#### Scenario: Account-specific question is not a knowledge gap
- GIVEN the caller asks why their own card was declined
- WHEN no relevant content is found
- THEN no knowledge-base enquiry is created
- AND the tenant's escalation rules apply instead

### Requirement: Caller follow-up consent
The system SHALL send a later answer only when the caller agreed during the call, through the channel
they chose, and SHALL use that consent for this enquiry only.

#### Scenario: Caller declines follow-up
- GIVEN the caller says they do not want a message
- WHEN the enquiry is created
- THEN it is recorded for the admin without any caller contact

#### Scenario: Spoken number is confirmed
- GIVEN an unverified caller gives a phone number for the answer
- WHEN the agent records it
- THEN the agent reads it back and records it only after the caller confirms

### Requirement: Grouping of similar enquiries
The system SHALL group open enquiries whose questions are semantically similar within the same tenant,
and SHALL let an admin answer a group once.

#### Scenario: Many callers, one question
- GIVEN 14 callers asked about the new transfer limit this week
- WHEN the admin opens the digest
- THEN they see one group with 14 waiting callers

### Requirement: Admin notification and email reply
The system SHALL notify the tenant's configured admins by email, immediately for enquiries marked
urgent and in a scheduled digest for the rest, and SHALL accept an admin's email reply as a proposed
answer only from a registered admin address carrying a valid signed reply token.

#### Scenario: Admin replies by email
- GIVEN a registered admin receives a gap notification
- WHEN they reply with the answer
- THEN a draft answer is attached to that enquiry group

#### Scenario: Reply from an unknown sender
- GIVEN a reply from an address not registered as an admin, or with an invalid token
- WHEN it arrives
- THEN it is rejected and the tenant's admins are alerted

### Requirement: Approval before publishing
The system SHALL publish an answer to the knowledge base only after an admin approves it, SHALL flag
an answer that conflicts with existing content, and SHALL remove personal data from the published text.

#### Scenario: Conflicting answer
- GIVEN an existing fee document states a fee of 50
- WHEN a proposed answer states a fee of 75
- THEN the approval view shows the conflict and the source document
- AND nothing is published until the admin resolves it

#### Scenario: Approved answer is published and sent
- GIVEN an admin approves an answer for a group with waiting callers
- WHEN approval completes
- THEN the answer is ingested as a knowledge-base entry within one hour
- AND each consenting waiting caller receives it once through their chosen channel

### Requirement: Enquiry expiry
The system SHALL expire an enquiry that stays unanswered beyond the tenant's limit, and SHALL send each
consenting caller a short apology with the tenant's contact route.

#### Scenario: Admin never answers
- GIVEN a tenant expiry limit of 5 days
- WHEN an enquiry is still unanswered after 5 days
- THEN it is marked expired and each consenting caller gets the apology message

### Requirement: Knowledge-gap metrics
The system SHALL show each tenant its gap rate, median time to answer, expired count, and top open
question groups.

#### Scenario: Tenant reviews gaps
- GIVEN a tenant admin opens the gap dashboard
- THEN it shows those metrics for the selected period, for that tenant only
