# Tasks: mvp2-action-packs

## 1. Registry and manifest
- [ ] 1.1 Pack manifest schema (tools, schemas, assurance level, confirmation, connector, resolution criteria)
- [ ] 1.2 Manifest validator (rejects write operations in MVP 2)
- [ ] 1.3 Tenant-scoped tool registry resolved at session setup

## 2. Action policy
- [ ] 2.1 Policy engine: allowlist, argument schema, assurance level, per-session limits
- [ ] 2.2 Subject binding to the verified caller's user reference
- [ ] 2.3 Policy-violation events

## 3. Connectors
- [ ] 3.1 `action_connector` interface + stub
- [ ] 3.2 Tenant REST connector (OpenAPI-described endpoints, per-tenant secrets)
- [ ] 3.3 First rail connector with design partner
- [ ] 3.4 Timeout, error, and holding-phrase handling

## 4. Packs
- [ ] 4.1 `transfer-status`
- [ ] 4.2 `card-status`
- [ ] 4.3 `airtime-data-status`
- [ ] 4.4 `loan-balance`
- [ ] 4.5 `kyc-status`
- [ ] 4.6 `open-dispute-ticket` step via CRM connector

## 5. Safety and data
- [ ] 5.1 Result redaction before model context, transcripts, telemetry

## 6. Metering and visibility
- [ ] 6.1 Tool-call usage events + conformance test (un-metered connector rejected)
- [ ] 6.2 Resolution evaluation at session end + resolution events
- [ ] 6.3 Per-pack resolution view in tenant dashboard

## 7. Tests
- [ ] 7.1 Cross-tenant denial test for tools, bindings, credentials
- [ ] 7.2 Assurance-level refusal and step-up tests
- [ ] 7.3 Subject-binding test (other account refused)
- [ ] 7.4 Prompt-injection test set (documents and utterances)
- [ ] 7.5 Connector timeout test: no invented facts
- [ ] 7.6 Tool-turn latency instrumentation per segment
