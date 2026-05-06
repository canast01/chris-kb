# SRDF/S Architecture

SRDF/S provides synchronous replication between two PowerMax arrays, committing every write to both source and target before returning an ACK to the host, resulting in RPO=0. This write-commit model requires low-latency inter-site connectivity, with a recommended maximum of 5ms round-trip time to keep write response times within acceptable production bounds. SRDF/S is supported on PowerMax 2000 and 8000 series running HYPERMAX OS.

- **Write commit model**: Host write → source commit → target commit → ACK; no data loss on failure.
- **RTT budget**: ≤5ms round-trip; every 1ms of additional RTT adds directly to host write latency.
- **SRDF groups**: Device pairs within a group maintain write-order consistency across failover.
- **Cascade protection**: SRDF/S to primary DR site can be cascaded with SRDF/A to a third site for tiered protection.
