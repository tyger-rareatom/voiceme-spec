# Proposal: mvp1-knowledge-gap-loop

## Status
**Phase: MVP 1 — Blocked by:** `mvp1-workflow-engine`, `mvp1-rag-retrieval`,
`mvp1-knowledge-ingestion`, `mvp1-agent-configuration`. **Uses** `mvp1-caller-verification` (verified
number for follow-up) when enabled. **Workflow automation 1 of 3.**

## Why
When retrieval finds nothing, the agent says it does not have the information and the call ends there.
The caller leaves without an answer, the tenant never learns the question was asked, and the same gap
costs another call tomorrow. Closing the loop turns each unanswered question into knowledge-base
coverage and a kept promise to the caller — the continuous-learning differentiator made visible.

## What Changes
- Detect a **knowledge gap** (no relevant content, low answer confidence, or caller dissatisfaction)
  and create an **open enquiry**.
- Ask the caller whether they want the answer later, and by which channel; record consent for that
  follow-up only.
- **Group** similar open enquiries so admins handle one question, not many copies.
- **Notify tenant admins by email** (immediate for urgent, daily digest for the rest) and accept the
  answer as an **email reply**.
- Turn an approved answer into a **draft knowledge-base entry**, publish it through existing ingestion,
  and **send the answer** to every waiting caller.
- Route **account-specific** questions to escalation instead of the knowledge base.

## User-visible impact
- Callers hear "I'll find out and send you the answer" instead of a dead end, and receive it later.
- Admins get grouped questions by email, reply with the answer, and approve it in one click.
- Tenants see gap rate, time to answer, and top unanswered questions.

## Rollback
Per-tenant template flag `knowledge_gap_loop`, default off. Off returns to the MVP 1 "I don't have that
information" behaviour; open enquiries stay readable.
