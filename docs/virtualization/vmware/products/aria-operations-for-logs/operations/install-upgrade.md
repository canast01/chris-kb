---
tags:
  - aria-logs
  - operations
  - vmware
---
# Aria Operations for Logs — Install and Upgrade

*Applies to: VMware Aria 8.x*
![Aria Operations for Logs — Install and Upgrade](../../../../../assets/virtualization-vmware-aria-operations-for-logs-operations-in.svg)

```bash
# From master node — confirm all cluster members
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, role: .role}'
```


```text title="Expected output"
{
  "host": "vrli-prod-01.example.local",
  "state": "ONLINE",
  "role": "MASTER"
}
{
  "host": "vrli-prod-02.example.local",
  "state": "ONLINE",
  "role": "WORKER"
}
{
  "host": "vrli-prod-03.example.local",
  "state": "ONLINE",
  "role": "WORKER"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification (already present; if still failing, verify the hostname matches the certificate CN). |
    | `jq: parse error: Invalid JSON text at line 1` | Confirm the API endpoint is correct and the cluster is fully initialized; check logs with `tail -f /var/log/vrli/api.log`. |
    | `401 Unauthorized` | Verify the admin password is correct and URL-encoded if it contains special characters; test credentials with a simpler endpoint first. |
```bash
# Confirm version
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/version" | jq '.version'

# Confirm cluster health
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, version: .version}'

# Confirm ingestion is running
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/stats" | \
  jq '.eventsIngested'
```


```text title="Expected output"
"8.10.2"
{
  "host": "vrli-prod-01.example.local",
  "state": "RUNNING",
  "version": "8.10.2"
}
{
  "host": "vrli-prod-02.example.local",
  "state": "RUNNING",
  "version": "8.10.2"
}
{
  "host": "vrli-prod-03.example.local",
  "state": "RUNNING",
  "version": "8.10.2"
}
1847293847
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag (already present) or import the CA certificate into your system trust store if `-k` is not permitted. |
    | `jq: parse error: Cannot index string with string "version"` | Verify the API endpoint is responding with valid JSON and the authentication credentials are correct; test with `curl -sk -u 'admin:<password>' "https://vrli-prod-01.example.local/api/v2/version"` alone first. |
    | `curl: (401) Unauthorized` | Confirm the admin password is correct and the user account has API access permissions in Aria Operations for Logs. |
## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

!!! warning "Host enters maintenance mode"
    ESXi remediation puts hosts into maintenance mode, triggering DRS evacuation. Confirm DRS is Fully Automated and HA admission control is satisfied before starting.

---

## See also

- [Aria Operations for Logs — Health Checks](../health-checks/)
- [Aria Operations for Logs — Common Issues](../../troubleshooting/common-issues/)
- [Aria Ops for Logs — Procedures](../procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
