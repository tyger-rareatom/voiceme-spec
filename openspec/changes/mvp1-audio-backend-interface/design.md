# Design: mvp1-audio-backend-interface

## Approach
- Interface contract lives in the shared platform; `cascaded` is the first implementation.
- Router reads the flag from the tenant config store at session start (never per turn — latency).
- The usage callback is **mandatory in the contract**: a backend that does not emit usage fails the
  conformance suite and cannot register.

## Conformance
Ship a conformance test suite any backend must pass (lifecycle, usage emission, error behavior).
This is the gate MVP 2/3 backends will be held to.
