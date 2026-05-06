# Superna Eyeglass Troubleshooting

Common Eyeglass issues include SyncIQ policies not being detected, low DR readiness scores, DNS cutover failures, and failover jobs that stall or complete with errors. Most issues trace back to API connectivity between Eyeglass and the PowerScale clusters, configuration drift between the primary and DR cluster, or DNS delegation misconfiguration.

| Issue | Likely Cause | Resolution |
|---|---|---|
| SyncIQ policy not detected | Eyeglass-to-OneFS API connectivity failure | Check Eyeglass cluster credentials and OneFS API reachability; re-register cluster in Eyeglass |
| DR readiness score low | Quota or share mismatch between clusters | Review Eyeglass sync log; re-run share/quota sync; check for manually created shares not in Eyeglass |
| DNS cutover failure | DNS delegation not configured or DNS plugin issue | Verify DNS delegation zone configuration; check Eyeglass DNS plugin logs; test manual DNS cutover |
| Failover stuck / not completing | API timeout, share conflict, or quota error | Review Eyeglass admin UI task log; check OneFS audit log for errors; use manual intervention steps in Eyeglass UI |
| RPO breach alerts | SyncIQ replication lag exceeding threshold | Check SyncIQ job status on source cluster (`isi sync jobs list`); check network bandwidth between sites |
| Eyeglass appliance unreachable | VM or network issue | Verify VM is powered on in vCenter; check management network connectivity; check Eyeglass service status via console |

**Diagnostic commands:**

```bash
# Check Eyeglass service status (from appliance console)
igls adm status

# View Eyeglass sync log
tail -f /var/log/superna/eyeglass/sync.log

# Verify OneFS API connectivity from Eyeglass
curl -sk -u admin https://<onefs-cluster>:8080/platform/1/cluster/identity
```
