# Proposal: mvp2-follow-through

## Status
**Phase: MVP 2 — Blocked by:** `mvp1-workflow-engine`, `mvp1-crm-escalation`,
`mvp1-caller-verification`, `mvp1-agent-configuration`. Status watches **blocked by**
`mvp2-action-packs`; contact rules **blocked by** `mvp2-compliance-evidence` (jurisdiction profiles).
**Extended by** Phase 4 `outbound-voice` (automated voice callbacks). **Workflow automation 2 of 3.**

## Why
The agent already makes promises it cannot keep: `mvp1-failover-baseline` offers a callback on vendor
failure, `mvp2-action-packs` offers a callback when a tenant system times out, and after-hours or
full-queue calls end with "someone will call you". Nothing records, schedules, or fulfils those
promises. A callback that never comes creates a repeat call and often a formal complaint.

## What Changes
- Create a **commitment** for every promise the agent makes: what, to whom, due by when, through which
  channel.
- **Schedule** within the tenant's business hours and the caller's preferred time.
- Fulfil by **human callback booking** (with full call context) or a **status watch** that notifies the
  caller when a tenant-system status changes (for example a reversal completing).
- **Escalate** to a supervisor before a commitment goes overdue.
- **Close** a commitment when the caller calls back first, so no duplicate follow-up happens.
- Add a **WhatsApp notification adapter** to the workflow engine.
- Report **promises kept %** per tenant.

## User-visible impact
- Callers get a stated follow-up time and a reminder message, and the follow-up happens.
- Human agents get a callback queue with context.
- Tenants see promises kept, overdue, and broken.

## Rollback
Per-tenant template flag `follow_through`, default off. Off returns to the current behaviour (the
offer is spoken, nothing is tracked).
