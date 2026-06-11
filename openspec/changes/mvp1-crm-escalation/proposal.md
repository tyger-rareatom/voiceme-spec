# Proposal: mvp1-crm-escalation

## Why
"Fallback to human" and CRM ticketing are sold on the deck; they are core product, not add-ons.

## What Changes
Add a human-escalation path with context handoff + CRM connectors (Zendesk/Freshdesk first) via webhook.

## User-visible impact
Unresolved calls escalate to a human with full context; tickets are created automatically.

## Rollback
Escalation disabled → agent-only mode per tenant.
