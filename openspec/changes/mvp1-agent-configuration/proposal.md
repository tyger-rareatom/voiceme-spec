# Proposal: mvp1-agent-configuration

## Why
Tenants must configure persona, greeting, escalation rules, and hours without code.

## What Changes
Portal configuration surface + persisted agent config per tenant, consumed by the runtime at session setup.

## User-visible impact
Self-serve agent setup in the portal.

## Rollback
Defaults applied if config absent.
