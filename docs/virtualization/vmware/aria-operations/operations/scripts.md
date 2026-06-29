---
tags:
  - aria-operations
  - operations
  - vmware
---
# Aria Operations Scripts
![Aria Operations Scripts](../../../../assets/virtualization-vmware-aria-operations-operations-scripts.svg)

```powershell

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Export cluster capacity summary via REST API
$AriaOpsHost = "aria-ops.domain.local"
$Token       = "your-token-here"

$Headers = @{ Authorization = "vRealizeOpsToken $Token" }

## Get all cluster compute resources
$Uri = "https://$AriaOpsHost/suite-api/api/resources?resourceKind=ClusterComputeResource"
$Response = Invoke-RestMethod -Uri $Uri -Headers $Headers -SkipCertificateCheck

foreach ($cluster in $Response.resourceList) {
    Write-Output "Cluster: $($cluster.resourceKey.name)"
}
```
```bash
#!/usr/bin/env bash
## Quick Aria Operations cluster health check
HOST="aria-ops.domain.local"

echo "=== Aria Operations Cluster Health ==="
ssh admin@$HOST "vracli cluster health"

echo ""
echo "=== Adapter Status ==="
ssh admin@$HOST "vracli adapter list"

echo ""
echo "=== Service Status ==="
ssh admin@$HOST "vracli status"
```

```text title="Expected output"
=== Aria Operations Cluster Health ===
Cluster Status: HEALTHY
Node 1 (aria-ops-node1.domain.local): ONLINE
Node 2 (aria-ops-node2.domain.local): ONLINE
Node 3 (aria-ops-node3.domain.local): ONLINE
Database Replication: SYNCHRONIZED
Last Health Check: 2024-01-15 14:32:18 UTC

=== Adapter Status ===
Adapter ID                           Name                    Status      Version
adapter-vmware-001                   vSphere Adapter         CONNECTED   8.12.1
adapter-kubernetes-002               Kubernetes Adapter      CONNECTED   8.12.1
adapter-vrops-internal               Internal Adapter        CONNECTED   8.12.1
adapter-custom-app-003               Custom App Monitor      DISCONNECTED 8.11.5

=== Service Status ===
Service Name                         Status      Port    Health
aria-operations-api                  RUNNING     443     HEALTHY
aria-operations-ui                   RUNNING     80      HEALTHY
aria-operations-collector            RUNNING     9000    HEALTHY
aria-operations-database             RUNNING     5432    HEALTHY
aria-operations-analytics            RUNNING     8080    HEALTHY
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname aria-ops.domain.local: Name or service not known`** — Verify the hostname is correct and resolvable in DNS, or use the IP address directly.
    **`Permission denied (publickey,password)`** — Ensure the admin user has SSH access configured and your SSH key or password authentication is properly set up on the Aria Operations appliance.
    **`vracli: command not found`** — Confirm you are connected to an Aria Operations node (not a standard Linux host) and that the vracli CLI tool is installed and in the PATH.
```bash
#!/usr/bin/env bash
HOST="aria-ops.domain.local"
USER="admin"
PASS="changeme"

## Get token
TOKEN=$(curl -sk -X POST "https://$HOST/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USER\",\"authSource\":\"LOCAL\",\"password\":\"$PASS\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

echo "Token acquired"

## Export active alerts
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://$HOST/suite-api/api/alerts?activeOnly=true" \
  | python3 -m json.tool > /tmp/aria-ops-alerts-$(date +%Y%m%d).json

echo "Alerts saved to /tmp/aria-ops-alerts-$(date +%Y%m%d).json"
```


```text title="Expected output"
Token acquired
Alerts saved to /tmp/aria-ops-alerts-20240315.json
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to curl to skip SSL verification, or import the aria-ops certificate into your system's CA bundle.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Verify the HOST, USER, and PASS variables are correct and the aria-ops API is responding; check curl output by removing the pipe to python3 temporarily.
    **`curl: (7) Failed to connect to aria-ops.domain.local port 443: Name or service not known`** — Ensure aria-ops.domain.local resolves in DNS or update the HOST variable to the correct FQDN or IP address.
---

## See also

- [Aria Operations — CLI Reference](../cli-reference/)
- [Aria Operations Procedures](../procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
