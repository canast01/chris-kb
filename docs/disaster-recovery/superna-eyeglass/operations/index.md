# Superna Eyeglass Operations

Daily operations focus on the Eyeglass dashboard: check SyncIQ policy health (all policies in a healthy replication state), verify RPO compliance per policy (confirm replication lag is within defined thresholds), review the overall DR readiness score, confirm DNS sync status is current, and check quota policy sync status. Any policies showing degraded or failed state require immediate investigation.

Weekly operations include running the Eyeglass DR readiness report to confirm all shares, quotas, and DNS mappings are synchronised and the environment is ready for a failover if needed.

**Daily checklist:**

- [ ] Eyeglass dashboard — all SyncIQ policies healthy (green)
- [ ] RPO compliance per policy — no policies exceeding RPO threshold
- [ ] DR readiness score — confirm at expected level (target: 100%)
- [ ] DNS sync status — all zones synchronised
- [ ] Quota policy sync status — no mismatches flagged

**Weekly checklist:**

- [ ] Run DR readiness report from Eyeglass UI
- [ ] Review any share or quota mapping drift
- [ ] Confirm Eyeglass-to-OneFS API connectivity on both sites
