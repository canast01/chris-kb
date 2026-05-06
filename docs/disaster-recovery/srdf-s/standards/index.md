# SRDF/S Standards

SRDF/S groups are designed one per application tier to isolate failure domains and simplify failover scoping. Site RTT must be validated and documented prior to production enablement; any link upgrade or re-route must trigger an RTT re-validation. Bandwidth is sized at peak write IOPS × average block size, with 25% headroom to absorb burst I/O without impacting host write latency.

| Parameter | Standard Value |
|---|---|
| SRDF group design | One group per application tier |
| Maximum site RTT | 5ms round-trip |
| Bandwidth sizing | Peak write throughput × 1.25 |
| Target volume sizing | 1:1 with source |
| Consistency group naming | `RDFG-S-<site-pair>-<tier>-<seq>` |
| Three-site cascade | SRDF/S → primary, SRDF/A → tertiary |
