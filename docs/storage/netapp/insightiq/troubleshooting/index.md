---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
---
# InsightIQ — Troubleshooting

```bash
# Verify InsightIQ can reach the PowerScale API from the appliance
ssh admin@insightiq.example.com

# Test connectivity to PowerScale platform API
curl -sk https://powerscale.example.com:8080/platform/1/protocols/nfs/exports \
  -u "insightiq-svc:password" | jq '.total'

# Check InsightIQ collector service status
sudo systemctl status iiq-collector

# View collector logs
sudo tail -f /var/log/insightiq/collector.log

# Restart the collector if it has stopped
sudo systemctl restart iiq-collector
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> verify_resolution: investigate
verify_resolution -> resolution
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Architecture](../architecture/)
- [Capacity](../capacity/)
- [Cli Reference](../cli-reference/)
- [Deploy](../deploy/)
- [Design Standards](../design-standards/)
- [Integration](../integration/)
- [Learning Path](../learning-path/)
- [Lifecycle](../lifecycle/)
- [Operations](../operations/)
- [Performance](../performance/)
- [Reports](../reports/)
- [Scripts](../scripts/)
- [Security](../security/)
- [Vendor Support](../vendor-support/)
- [Workloads](../workloads/)
- [InsightIQ — Overview](../)
