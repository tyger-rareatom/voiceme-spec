# Design: mvp1-crm-escalation

## Approach
- Escalation hangs off the LLM/runtime layer (explicit-request + low-confidence triggers in MVP 1;
  sentiment-aware triggers arrive in Phase 4 — leave the trigger interface open).
- CRM connectors behind an interface; Zendesk/Freshdesk first, HubSpot/custom next.
- Context bundle = transcript + retrieved chunks + metadata. Webhook delivery with retry.
