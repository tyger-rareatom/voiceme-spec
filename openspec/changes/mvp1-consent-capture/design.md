# Design: mvp1-consent-capture

## Approach
- Consent state captured at call start (channel-appropriate mechanism per ingress adapter).
- Governed store separate from operational data; redaction pipeline; retention policy enforced.
- Export interface feeds the MVP 3 language-pack data pipeline.
