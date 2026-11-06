# Design: mvp1-knowledge-gap-loop

## Approach
- **Detection** uses signals already computed on the turn: top retrieval score below threshold,
  the model's grounded/ungrounded flag, and a dissatisfaction intent ("that didn't answer it"). The
  account-specific check uses the same intent classification the router already performs; no extra
  model call.
- **Template `knowledge_gap_v1`** on `mvp1-workflow-engine`:
  `open → grouped → notified → answered (draft) → approved → published → callers notified → closed`,
  with `expired` reachable from any open state via the tenant's expiry timer.
- **Grouping:** enquiry questions are embedded with the tenant's existing embedding model and grouped by
  similarity threshold within the tenant's open enquiries.
- **Email reply ingestion:** the notification's Reply-To carries a signed, single-use token
  (`answers+<token>@…`). The inbound webhook accepts a reply only if the token is valid for that group,
  the sender is a registered admin, and SPF/DKIM (email sender authentication) pass. Quoted history and
  signatures are stripped.
- **Publishing:** the approved answer becomes a tenant knowledge source of type `gap_answer` with its
  own `document_version`, ingested through `mvp1-knowledge-ingestion`. Personal data is removed by the
  ingestion scrubber before chunking.
- **Conflict check:** before approval, the draft is retrieved against existing chunks; high-similarity
  chunks with differing numbers or dates are shown side by side.
- **Caller follow-up:** SMS in MVP 1 (verified number when `mvp1-caller-verification` gives L1+,
  otherwise a read-back-confirmed number); WhatsApp when `mvp2-follow-through` adds that adapter.

## Tenant isolation
Enquiries, groups, tokens, and drafts are tenant-scoped; grouping never compares across tenants.
Cross-tenant denial test covers enquiries, digests, and reply tokens (a token for tenant A cannot
attach an answer to tenant B).

## Hot-path sequence note
Detection reuses scores already on the turn; the offer to follow up is part of the same spoken reply;
the enquiry event is written at turn end via the outbox. **Expected impact on the ≤ 1.5 s p50 turn
budget: none.** Instrument the detection decision and outbox lag.

## Metering
Admin emails and caller messages are metered by the engine's notification adapters. Grouping
embeddings are metered as retrieval/embedding usage.

## Vendor interfaces wrapped
Uses `notification_channel` and the existing embedding interface; no new vendors.
