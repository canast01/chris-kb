---
tags:
  - aria-lcm
  - operations
  - vmware
description: "Scripts reference covering Pre-Upgrade Disk Check, Environment Health Summary, Bulk Locker Password Export (Alias List), NTP Validation Across All Product..."
---
# Aria Suite Lifecycle — Scripts

<div class="kb-summary">
Scripts reference covering Pre-Upgrade Disk Check, Environment Health Summary, Bulk Locker Password Export (Alias List), NTP Validation Across All Product Nodes, Trigger Upgrade via API (Non-Interactive).

*Applies to: Aria LCM 8.x*
</div>
![Aria Suite Lifecycle — Scripts](../../../../../assets/virtualization-vmware-aria-suite-lifecycle-operations-script.svg)

  LCM Automation Scripts

---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Environment Health Summary

Queries LCM API and prints the health status of all environments and products.

```bash
#!/usr/bin/env bash
# Usage: ./lcm-health-summary.sh <lcm-fqdn> <username> <password>
LCM=$1; USER=$2; PASS=$3

TOKEN=$(curl -sk -X POST "https://$LCM/lcm/authz/api/v2/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}" | jq -r '.token')

echo "=== LCM Environment Health ==="
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://$LCM/lcm/lcmservice/api/v2/environments" | \
  jq -r '.[] | "Environment: \(.environmentName)  Health: \(.environmentHealth)"'

echo ""
echo "=== Running Requests ==="
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://$LCM/lcm/lcmservice/api/v2/requests?state=RUNNING" | \
  jq -r '.[] | "[\(.requestType)] ID:\(.requestId)  Started:\(.startTime)"'

echo ""
echo "=== Disk Usage on LCM Appliance ==="
df -h / /data /var/log 2>/dev/null | column -t
```


```text title="Expected output"
=== LCM Environment Health ===
Environment: prod-vcenter-01  Health: HEALTHY
Environment: prod-vcenter-02  Health: HEALTHY
Environment: staging-env  Health: DEGRADED
Environment: dr-site  Health: UNKNOWN

=== Running Requests ===
[UPGRADE] ID:req-2024-08-15-001  Started:2024-08-15T09:32:14.521Z
[PATCH] ID:req-2024-08-15-002  Started:2024-08-15T10:18:47.893Z

=== Disk Usage on LCM Appliance ===
Filesystem     Size  Used  Avail  Use%  Mounted on
/dev/sda1      50G   38G   9.2G   82%  /
/dev/sdb1      500G  412G  65G    87%  /data
/dev/sdc1      100G  94G   3.2G   97%  /var/log
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `jq: parse error: Invalid JSON text at line 1` | Verify the LCM token is valid by checking credentials and confirming the LCM service is responding with valid JSON. |
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to curl (already present) or import the LCM's CA certificate into your system trust store. |
    | `curl: (7) Failed to connect to <lcm-fqdn> port 443: Connection refused` | Confirm the LCM FQDN is correct, resolvable, and the LCM appliance is running and accessible on port 443. |
---

## Bulk Locker Password Export (Alias List)

Exports the list of password aliases and associated usernames stored in Locker (values are never exposed via API).

```bash
#!/usr/bin/env bash
LCM=$1; USER=$2; PASS=$3

TOKEN=$(curl -sk -X POST "https://$LCM/lcm/authz/api/v2/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}" | jq -r '.token')

echo "alias,username,description"
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://$LCM/lcm/locker/api/v2/passwords" | \
  jq -r '.passwords[] | [.alias, .userName, .description] | @csv'
```


```text title="Expected output"
alias,username,description
"vcenter-admin","administrator@vsphere.local","vCenter root password"
"esxi-root","root","ESXi host root credential"
"nsxt-admin","admin","NSX-T manager admin account"
"vsan-witness","root","vSAN witness node access"
"backup-svc","backup_user","Automated backup service account"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to curl (already present) or import the LCM's CA certificate into your system trust store. |
    | `jq: parse error: Cannot index string with string "token"` | Verify the LCM hostname is correct and the login endpoint is reachable; the response is likely an error message, not JSON. |
    | `curl: (7) Failed to connect to <LCM>: Name or service not known` | Ensure the LCM hostname or IP address is resolvable and the LCM appliance is running and network-accessible. |
---

## NTP Validation Across All Product Nodes

After LCM deploys products, verify NTP sync on all appliances to prevent certificate failures.

```bash
#!/usr/bin/env bash
# Usage: ./ntp-check.sh
# Edit NODES to match your environment
NODES=(
  "lcm-prod-01.example.local"
  "vidm-prod-01.example.local"
  "vrops-prod-01.example.local"
  "vrops-prod-02.example.local"
  "vra-prod-01.example.local"
  "vrli-prod-01.example.local"
)

for node in "${NODES[@]}"; do
  echo -n "$node: "
  ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@"$node" \
    "chronyc tracking 2>/dev/null | grep 'System time'" 2>/dev/null || echo "SSH failed"
done
```


```text title="Expected output"
lcm-prod-01.example.local: System time   : 0.000000234 seconds fast of NTP time
vidm-prod-01.example.local: System time   : -0.000000891 seconds slow of NTP time
vrops-prod-01.example.local: System time   : 0.000000156 seconds fast of NTP time
vrops-prod-02.example.local: SSH failed
vra-prod-01.example.local: System time   : 0.000001023 seconds slow of NTP time
vrli-prod-01.example.local: System time   : 0.000000445 seconds fast of NTP time
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `SSH failed` | Verify SSH key-based authentication is configured for root on the target node, or add the node's IP to `/etc/hosts` if DNS resolution is failing. |
    | `Permission denied (publickey,password)` | Ensure the root user's SSH public key is in `/root/.ssh/authorized_keys` on each target node with correct permissions (600). |
    | `connect timed out` | Increase the `ConnectTimeout` value or verify network connectivity and firewall rules allow SSH (port 22) from the LCM appliance to all nodes. |
---

## Trigger Upgrade via API (Non-Interactive)

Useful for scripted maintenance windows. Substitute environment ID and payload from UI inspection.

```bash
#!/usr/bin/env bash
LCM=$1; USER=$2; PASS=$3; ENV_ID=$4; PRODUCT_ID=$5; TARGET_VERSION=$6

TOKEN=$(curl -sk -X POST "https://$LCM/lcm/authz/api/v2/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}" | jq -r '.token')

# Trigger upgrade
RESPONSE=$(curl -sk -X POST -H "x-xenon-auth-token: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://$LCM/lcm/lcmservice/api/v2/environments/$ENV_ID/products/$PRODUCT_ID/upgrade" \
  -d "{\"targetVersion\":\"$TARGET_VERSION\"}")

REQUEST_ID=$(echo "$RESPONSE" | jq -r '.requestId')
echo "Upgrade triggered — Request ID: $REQUEST_ID"
echo "Monitor: https://$LCM/lcm/lcmservice/api/v2/requests/$REQUEST_ID"

# Poll until complete
while true; do
  STATE=$(curl -sk -H "x-xenon-auth-token: $TOKEN" \
    "https://$LCM/lcm/lcmservice/api/v2/requests/$REQUEST_ID" | jq -r '.state')
  echo "$(date '+%H:%M:%S') — Request state: $STATE"
  [[ "$STATE" == "COMPLETED" || "$STATE" == "FAILED" ]] && break
  sleep 60
done
```


```text title="Expected output"
Upgrade triggered — Request ID: req-8f4c2a91-7e3d-4b12-9c5a-1d6e2f8a3b4c
Monitor: https://lcm.corp.local/lcm/lcmservice/api/v2/requests/req-8f4c2a91-7e3d-4b12-9c5a-1d6e2f8a3b4c
14:23:45 — Request state: INPROGRESS
15:24:12 — Request state: INPROGRESS
16:25:33 — Request state: INPROGRESS
17:26:47 — Request state: COMPLETED
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `jq: error (at <stdin>:1): Cannot index null with string "token"` | Verify LCM hostname is correct and credentials are valid; check that the login endpoint is accessible. |
    | `jq: error (at <stdin>:1): Cannot index null with string "requestId"` | Confirm the environment ID and product ID exist and the target version is available in the LCM catalog. |
    | `curl: (60) SSL certificate problem: self signed certificate` | The `-k` flag is already present; if the error persists, verify the LCM server's SSL certificate is trusted or use `curl -sk` with an explicit CA bundle via `--cacert`. |
---

## See also

- [Aria Suite Lifecycle — CLI Reference](../cli-reference/)
- [Aria Suite Lifecycle — Procedures](../procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
