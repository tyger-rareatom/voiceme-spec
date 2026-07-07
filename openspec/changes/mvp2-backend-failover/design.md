# Design: mvp2-backend-failover

## Approach
- Failover controller monitors backend health (error rate, latency SLO breach, vendor status).
- Mid-session switch: re-establish the pipeline on cascaded, carrying conversation state from the
  session runtime; accept a brief transition utterance ("one moment").
- Usage attribution splits at the failover point (metering correctness).
- Failback policy: new sessions return to Gemini after sustained health; in-flight sessions finish
  where they are.

## Dependency: externalized session state is the substrate (noted 2026-07-07)

> "Carrying conversation state from the session runtime" above assumes a mechanism this change
> does not itself build. Do not invent a private context-handoff here — consume the shared one.

- **Sequencing:** a `mvp2-session-continuity` change (propose when MVP 2 is reached) should land
  first: turn-boundary checkpoints of the serializable session state (seeded in
  `mvp1-audio-cascaded`) to a tenant-scoped Postgres `session_state` store (Redis only if volume
  ever justifies it). Backend failover then *hydrates the replacement pipeline from the same
  checkpoint* — failover is the second trigger of one mechanism (client-reconnect resume is the
  first; pod-death recovery the third).
- **Inherited constraints:** checkpoints are async best-effort at turn boundaries, never awaited
  (non-blocking persistence rule); resume point is the last completed turn — no mid-turn recovery;
  transcript checkpoints are PII with aggressive TTL (operational data, not training data).
- **Metering:** a failed-over/resumed session is a **child session with a parent link** — metered
  separately (no double-count), joined for continuity in transcripts/analytics. Aligns with the
  usage-attribution split above.
- **Rejected:** "caller never notices" warm-standby rehydration (from the scalability-proposal
  review) — cost/complexity out of proportion; a brief transition utterance is acceptable.
