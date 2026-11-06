# Proposal: mvp2-complaint-cases

## Status
**Phase: MVP 2 — Blocked by:** `mvp1-workflow-engine`, `mvp1-crm-escalation`,
`mvp2-compliance-evidence` (jurisdiction profiles, evidence store). **Uses** `mvp2-action-packs`
dispute tickets and `mvp2-follow-through` notifications when present. **Workflow automation 3 of 3.**

## Why
Regulated banks and telcos must log complaints, resolve them within set periods, and report on them.
Many still track this by hand from call notes, so cases are missed, deadlines breach, and regulator
reports are assembled late. A voice agent that hears the complaint is the natural place to open the case
correctly, start the clock, and keep the evidence. This sells to both the CX (customer experience)
buyer and the compliance team that blocks AI purchases.

## What Changes
- Detect complaint intent and **confirm with the caller** before opening a formal case.
- Give the caller a **reference number** on the call.
- **Classify** each case (product, category, severity) and **start a deadline clock** from the tenant's
  jurisdiction profile.
- **Route** the case to the owning team, remind, and escalate before the deadline breaches.
- Send a **written acknowledgement** and a **closure confirmation** to the caller.
- **Merge duplicates**; send fraud reports and vulnerable callers **straight to a human**.
- Record every case event in the compliance evidence store for regulator reports.

## User-visible impact
- Callers leave with a reference number and a stated response period.
- Complaint teams get classified cases with deadlines and transcripts.
- Compliance users see handling times and breaches in evidence reports.

## Rollback
Per-tenant template flag `complaint_cases`, default off. Off returns to the current escalation and CRM
ticket behaviour.
