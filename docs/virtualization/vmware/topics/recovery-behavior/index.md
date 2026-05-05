# Recovery Behavior Expectations

## After Host Failure

Expected:

HA restart time: 1–5 minutes
Resync begins automatically
Temporary performance impact

## After Storage Failure

Expected:

Object rebuild begins
Reduced performance
Possible latency increase

## After Network Failure

Expected:

Temporary VM isolation
HA or DRS response
Possible alarm storm
