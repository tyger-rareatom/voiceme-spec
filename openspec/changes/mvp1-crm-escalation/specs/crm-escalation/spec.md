## ADDED Requirements

### Requirement: Human escalation path
The system SHALL escalate a call to a human per the tenant's escalation rules and pass conversation
context to the destination.

#### Scenario: Agent cannot resolve
- GIVEN an escalation rule "transfer on explicit request or low confidence"
- WHEN the trigger occurs
- THEN the call is handed off with the transcript and retrieved context attached

### Requirement: CRM ticket creation
The system SHALL create a ticket in the tenant's connected CRM on escalation via webhook.

#### Scenario: Escalation creates a ticket
- GIVEN a connected Zendesk integration
- WHEN an escalation fires
- THEN a ticket is created with the conversation summary and metadata
