# Design: mvp2-backend-failover

## Approach
- Failover controller monitors backend health (error rate, latency SLO breach, vendor status).
- Mid-session switch: re-establish the pipeline on cascaded, carrying conversation state from the
  session runtime; accept a brief transition utterance ("one moment").
- Usage attribution splits at the failover point (metering correctness).
- Failback policy: new sessions return to Gemini after sustained health; in-flight sessions finish
  where they are.
