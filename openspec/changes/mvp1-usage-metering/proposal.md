# Proposal: mvp1-usage-metering

## Why
A usage-priced business must meter minutes/tokens/STT-TTS/retrieval per tenant in real time to
enforce caps, bill overage, and surface margin leakage immediately. Margin-critical; expensive to retrofit.

## What Changes
Add a metering + telemetry plane that taps every backend's mandatory usage callback and feeds billing
plus an internal margin dashboard.

## User-visible impact
Accurate usage in the portal; overage billing possible; internal real-time margin view.

## Rollback
Metering is read-only telemetry first; billing consumption gated behind a flag.
