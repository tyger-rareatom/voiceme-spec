# Design: mvp1-observability

## Approach
- Metrics/traces/logs pipeline; dashboards per tenant + global. Alerts on latency/error SLOs.
- Segment tagging matches the metering event schema so cost and performance correlate per tenant.
