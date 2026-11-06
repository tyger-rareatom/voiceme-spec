# Design: mvp2-action-packs

## Approach
- **Pack = shared code + tenant binding.** The pack (manifest, tool definitions, response templates,
  tests) is shared across tenants and versioned. The tenant binding (connector endpoint, credentials,
  field mapping, resolution criteria) is tenant-scoped config. A tenant upgrades pack versions
  explicitly.
- **Execution flow:** LLM proposes a tool call → **action policy** (allowlist, schema, assurance level,
  subject binding, limits) → **action connector** → tenant system → result redaction → result enters
  model context as a grounded source → answer.
- **Subject binding:** the verified caller's tenant-scoped user reference (from `mvp1-caller-verification`)
  is the only account selector the connector accepts. The model never supplies a raw account identifier
  without the policy matching it to that reference.
- **Connector interface** (`action_connector`): `invoke(tenant_binding, tool, args) -> Result`. First
  implementations:
  1. **Tenant REST connector** — calls tenant-owned endpoints described by an OpenAPI document. Banks
     rarely allow a SaaS vendor to call the core system directly; the expected path is the tenant's API
     gateway or middleware in front of the core system (for example Temenos T24, Finacle, Flexcube).
  2. **One rail-specific connector built with the first design partner** (transfer status or mobile
     money), then generalised into the shared pack.
- **Initial packs (read-only):** `transfer-status`, `card-status`, `airtime-data-status`,
  `loan-balance`, `kyc-status`. Each includes an optional `open-dispute-ticket` step through the
  existing CRM connector.
- **Model:** managed tiers use Claude tool calling (Sonnet for tool turns; the router sends any turn that
  may call a tool to the anchor model). Sovereign tenants keep this capability off until either the
  managed LLM endpoint is accepted in their control mapping or `mvp3-nemotron-spike` passes.

## Tenant isolation
Registry, bindings, credentials (secret store, per-tenant path), and tool events go through the
tenant-scoped repository layer. Cross-tenant denial test is mandatory (spec scenario "Tools never cross
tenants").

## Hot-path sequence note
Turn with a tool: STT → LLM (tool proposal) → policy (< 10 ms, in memory) → connector call → LLM (answer)
→ TTS. This adds one connector round trip and one extra LLM pass to tool turns. **Expected impact:
tool turns exceed the 1.5 s p50 budget by the connector latency plus one LLM pass.** Mitigation: the agent
speaks a short holding phrase as soon as a tool call is accepted; connector timeout default 3 s (not yet
measured); non-tool turns are unaffected. Instrument policy, connector, and second LLM pass as separate
segments.

## Metering
Tool-call and resolution events flow through the existing non-blocking metering spool. Resolution
criteria are evaluated at session end, off the turn path.

## Vendor interfaces wrapped
`action_connector` (tenant systems), existing CRM connector interface, LLM interface for tool calling.

## Open validation
- Measured connector latency with the first design partner.
- Whether per-resolution pricing is margin-positive against the enterprise card (needs data from this
  change before any pricing decision).
