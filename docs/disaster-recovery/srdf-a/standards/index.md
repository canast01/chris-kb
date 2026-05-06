# SRDF/A Standards

SRDF group naming follows the convention `RDFG-<site-pair>-<app-tier>-<seq>` (e.g., `RDFG-DC1DC2-DB-01`). Cycle time defaults to 30 seconds and must be aligned with the agreed RPO SLA per application class. WAN link bandwidth must be sized as: peak change rate (MB/s) × (cycle frequency per second), with a 20% headroom buffer.

| Parameter | Standard Value |
|---|---|
| Default cycle time | 30 seconds |
| Max delta set size | Align with WAN throughput |
| Target volume sizing | 1:1 with source (no thin over-subscription) |
| Consistency group design | One SRDF group per application tier |
| Bandwidth headroom | 20% above peak calculated load |
| SRDF license | Required on both source and target arrays |
