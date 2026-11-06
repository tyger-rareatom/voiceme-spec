# Proposal: mvp2-action-packs

## Status
**Phase: MVP 2 — Blocked by:** `mvp1-caller-verification`, `mvp1-audio-cascaded`,
`mvp1-tenant-config-store`, `mvp1-usage-metering`, `mvp1-crm-escalation`. **Pulls forward** the
read-only subset of Phase 4 `agentic-actions`; write actions stay in Phase 4 and extend this capability.
Sovereign tenants on Nemotron remain gated by `mvp3-nemotron-spike`. **Market-leadership capability 2
of 3.**

## Why
The agent today answers only from uploaded documents. The calls that cost fintechs and telcos the most
are account-specific: a failed transfer, a card status, an airtime purchase that did not arrive, a loan
balance, a KYC (know your customer) check. A document-only agent deflects the cheap calls and escalates
the expensive ones, so the customer's return on investment rests on labour savings alone. **Resolving**
those calls changes the value case and makes per-resolution pricing possible.

Prebuilt, tested flows ("packs") for the common African fintech and telco call reasons also compound:
each new tenant on the same rails reuses the same connector and flow. That integration library is slow
for a global horizontal platform to copy.

## What Changes
- Add a **per-tenant tool registry** and a versioned **pack manifest** format (tools, input schemas,
  required assurance level, confirmation policy, connector binding, resolution criteria).
- Add a **server-side action policy** that every model-proposed tool call must pass before execution.
- Add an **action connector interface** to call tenant systems (through the tenant's API gateway or
  middleware), with credentials held per tenant in a secret store.
- Ship **five read-only packs**: interbank transfer status, card status, airtime/data purchase status,
  loan balance and next repayment, KYC status. Each pack may open a dispute ticket through the existing
  CRM connector (an escalation-class action, not an account write).
- Emit **tool-call and resolution usage events** to metering, so outcome pricing can be evaluated.

## User-visible impact
- Tenants enable packs in the portal, bind them to their systems, and set resolution criteria.
- Verified callers get account answers in the call instead of a hand-off.
- Tenants see resolved-call counts per pack in their dashboard.

## Rollback
Each pack is a per-tenant flag in the tenant config store; disabling it removes its tools from the next
session. The registry is additive; with no packs enabled, behaviour matches MVP 1.

## Out of scope
- Account writes (card block, reversal execution, refunds, password reset): Phase 4 `agentic-actions`.
- A change to the pricing card. Per-resolution pricing needs a separate billing change and a
  `project.md` §7 update; this change only produces the metering data.
