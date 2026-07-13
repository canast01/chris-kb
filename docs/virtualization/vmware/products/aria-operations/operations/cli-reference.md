---
tags:
  - aria-operations
  - operations
  - vmware
description: "CLI Reference reference covering vracli Commands, chkconfig (Legacy / Service Enable/Disable), Useful Paths, REST API Quick Reference, Related Sections."
---
# Aria Operations — CLI Reference

<div class="kb-summary">
CLI Reference reference covering vracli Commands, chkconfig (Legacy / Service Enable/Disable), Useful Paths, REST API Quick Reference, Related Sections.

*Applies to: Aria Ops 8.x*
</div>
![Aria Operations — CLI Reference](../../../../../assets/virtualization-vmware-aria-operations-operations-cli-referen.svg)

Aria Operations — CLI Command Reference Map

## vcops-admin CLI

### Adapter Management

```bash
# List all adapters and collection status
vracli adapter list

# List adapters with verbose output
vracli adapter list --verbose

# Restart a specific adapter (get ID from list output)
vracli adapter restart --id <adapter-id>
```


```text title="Expected output"
NAME                          ID                                    TYPE              STATUS
vSphere Adapter               adapter-vsphere-prod-01               VMware vSphere    ACTIVE
Kubernetes Adapter            adapter-k8s-cluster-01                 Kubernetes        ACTIVE
NSX Adapter                   adapter-nsx-mgmt-01                   NSX               ACTIVE
vSAN Adapter                  adapter-vsan-prod-01                  vSAN              ACTIVE
Custom REST Adapter           adapter-rest-webhook-01               REST              INACTIVE

NAME: vSphere Adapter
ID: adapter-vsphere-prod-01
TYPE: VMware vSphere
STATUS: ACTIVE
COLLECTION_INTERVAL: 300s
LAST_COLLECTION: 2024-01-15T14:32:18Z
OBJECTS_COLLECTED: 1247
ERROR_COUNT: 0

NAME: Kubernetes Adapter
ID: adapter-k8s-cluster-01
TYPE: Kubernetes
STATUS: ACTIVE
COLLECTION_INTERVAL: 120s
LAST_COLLECTION: 2024-01-15T14:33:05Z
OBJECTS_COLLECTED: 892
ERROR_COUNT: 2

Restarting adapter 'adapter-vsphere-prod-01'...
Adapter restart initiated successfully. Restart will complete in 30-60 seconds.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: adapter not found: adapter-invalid-id` | Verify the adapter ID from `vracli adapter list` output and ensure it is spelled correctly. |
    | `Error: permission denied - insufficient privileges` | Run the command with appropriate sudo privileges or as a user with vRealize Operations administrator role. |
### Status and Services

```bash
# Overall service health summary
vracli status

# Check individual service
systemctl status vmware-vcops-<service-name>

# List all VMware services
systemctl list-units 'vmware-*'
```


```text title="Expected output"
● vmware-vcops-controller.service - VMware vRealize Operations Controller
     Loaded: loaded (/etc/systemd/system/vmware-vcops-controller.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:23:47 UTC; 2 days ago
   Main PID: 4521 (java)
     CGroup: /system.slice/vmware-vcops-controller.service
             └─4521 /usr/java/default/bin/java -Xmx8192m -Xms4096m...

vmware-vcops-ui.service - VMware vRealize Operations UI
     Loaded: loaded (/etc/systemd/system/vmware-vcops-ui.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:24:12 UTC; 2 days ago
   Main PID: 5847 (java)

vmware-vcops-analytics.service - VMware vRealize Operations Analytics
     Loaded: loaded (/etc/systemd/system/vmware-vcops-analytics.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:25:33 UTC; 2 days ago
   Main PID: 6234 (java)

vmware-vcops-collector.service - VMware vRealize Operations Collector
     Loaded: loaded (/etc/systemd/system/vmware-vcops-collector.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:26:01 UTC; 2 days ago
   Main PID: 7102 (java)

vmware-vcops-gateway.service - VMware vRealize Operations Gateway
     Loaded: loaded (/etc/systemd/system/vmware-vcops-gateway.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:26:45 UTC; 2 days ago
   Main PID: 8456 (java)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unit vmware-vcops-<service-name>.service could not be found.` | Replace `<service-name>` with an actual service name like `controller`, `ui`, `analytics`, or `collector`. |
    | `Failed to get unit file state for vmware-vcops-controller.service: Connection refused` | Ensure the systemd daemon is running with `systemctl daemon-reexec` and verify the service file exists in `/etc/systemd/system/`. |
    | `No units matching 'vmware-*' were found.` | Confirm VMware vRealize Operations is installed and systemd service files are present in `/etc/systemd/system/` or `/usr/lib/systemd/system/`. |
### Certificate Management

```bash
# View current certificate info
vracli certificate show

# Replace certificate (PEM format)
vracli certificate import --cert /tmp/aria-ops.crt --key /tmp/aria-ops.key --ca /tmp/ca-chain.crt
```


```text title="Expected output"
Certificate Information:
  Issuer: CN=aria-ops.example.com,O=IT Operations,C=US
  Subject: CN=aria-ops.example.com,O=IT Operations,C=US
  Valid From: 2024-01-15 10:23:45 UTC
  Valid Until: 2025-01-15 10:23:45 UTC
  Fingerprint (SHA256): a7:b2:c9:d4:e1:f6:2a:3b:4c:5d:6e:7f:8a:9b:0c:1d:2e:3f:4a:5b
  Serial Number: 0x1A2B3C4D5E6F7A8B

Certificate import initiated...
Validating certificate chain...
Installing certificate on all nodes...
  Node 1 (aria-ops-node1.local): ✓ Complete
  Node 2 (aria-ops-node2.local): ✓ Complete
  Node 3 (aria-ops-node3.local): ✓ Complete
Certificate installation successful. Services will restart in 30 seconds.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Certificate file not found: /tmp/aria-ops.crt` | Verify the certificate file path exists and is readable with `ls -la /tmp/aria-ops.crt`. |
    | `Error: Private key and certificate do not match` | Ensure the key and certificate were generated as a pair; regenerate both from the same CSR if mismatch persists. |
    | `Error: CA chain validation failed - untrusted root` | Verify the CA chain file contains the complete certificate hierarchy in correct order (leaf to root) using `openssl crl2pkcs7 -nocrl -certfile /tmp/ca-chain.crt | openssl pkcs7 -print_certs -text -noout`. |
### Support

```bash
# Generate support bundle
vracli support bundle generate

# List existing support bundles
ls -lh /storage/log/support-bundle/

# View recent logs
vracli log tail --lines 100
```


```text title="Expected output"
Generating support bundle...
Support bundle generated successfully: /storage/log/support-bundle/vra-support-bundle-2024-01-15-143022.tar.gz
Bundle size: 487 MB
Timestamp: 2024-01-15T14:30:22Z

total 2.3G
-rw-r--r-- 1 root root 487M Jan 15 14:30 vra-support-bundle-2024-01-15-143022.tar.gz
-rw-r--r-- 1 root root 512M Jan 14 09:15 vra-support-bundle-2024-01-14-091502.tar.gz
-rw-r--r-- 1 root root 495M Jan 13 16:42 vra-support-bundle-2024-01-13-164215.tar.gz
-rw-r--r-- 1 root root 501M Jan 12 11:28 vra-support-bundle-2024-01-12-112847.tar.gz

2024-01-15 14:29:58 [INFO] Cluster health check passed
2024-01-15 14:29:45 [INFO] Database connection pool: 45/50 active
2024-01-15 14:29:32 [WARN] Memory usage at 78% on node-02
2024-01-15 14:29:15 [INFO] vRealize Operations Agent v8.10.2 heartbeat received
2024-01-15 14:28:58 [INFO] Collector sync completed in 2.3s
2024-01-15 14:28:42 [INFO] Policy engine evaluation cycle: 847ms
2024-01-15 14:28:25 [DEBUG] Metric ingestion rate: 125,430 points/sec
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vracli: command not found` | Ensure vRealize Operations is installed and the vracli binary is in your PATH, or run with full path `/opt/vmware/vrealize-operations/bin/vracli`. |
    | `Permission denied` | Run the command with sudo or as the root user, as support bundle generation requires elevated privileges. |
    | `/storage/log/support-bundle/: No such file or directory` | Verify the storage mount is accessible and the support-bundle directory exists; check with `df -h /storage` and create the directory if needed. |
### Authentication and Users

```bash
# List configured auth sources
vracli auth list

# Test LDAP connectivity
vracli auth test --source <ldap-source-name>
```


```text title="Expected output"
Authentication Sources:
  Name: corp-ldap
  Type: LDAP
  Server: ldap.corp.local
  Port: 389
  Base DN: dc=corp,dc=local
  Status: ACTIVE

  Name: local-users
  Type: LOCAL
  Status: ACTIVE

Testing LDAP connectivity for 'corp-ldap'...
Connection: SUCCESS
Bind Test: SUCCESS
Search Test: SUCCESS (5 users found)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Authentication source 'corp-ldap' not found` | Verify the exact source name with `vracli auth list` and use the correct spelling. |
    | `Error: LDAP connection timeout after 30 seconds` | Check network connectivity to the LDAP server and confirm the hostname/port are correct with `telnet ldap.corp.local 389`. |
    | `Error: LDAP bind failed: Invalid credentials` | Verify the bind DN and password configured for the LDAP source are correct in the auth source settings. |
---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## chkconfig (Legacy / Service Enable/Disable)

```bash
# List services and their runlevel status
chkconfig --list | grep vmware

# Enable a service at boot
chkconfig vmware-vcops on
```


```text title="Expected output"
vmware-vcops       	0:off	1:off	2:on	3:on	4:on	5:on	6:off
vmware-postgres    	0:off	1:off	2:on	3:on	4:on	5:on	6:off
vmware-mariadb     	0:off	1:off	2:on	3:on	4:on	5:on	6:off
vmware-rabbitmq    	0:off	1:off	2:on	3:on	4:on	5:on	6:off
vmware-nginx       	0:off	1:off	2:on	3:on	4:on	5:on	6:off
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `chkconfig: command not found` | Use `systemctl list-unit-files | grep vmware` on systemd-based systems (RHEL 7+, CentOS 7+). |
    | `error reading information on service vmware-vcops: No such file or directory` | Verify the exact service name with `systemctl list-unit-files | grep vmware` and use the correct name in the chkconfig command. |
---

## Useful Paths

| Path | Contents |
|------|----------|
| `/storage/log/` | All Aria Operations logs |
| `/storage/log/support-bundle/` | Generated support bundles |
| `/storage/core/` | Core data directory |
| `/usr/lib/vmware-vcopssuite/utilities/` | vracli utilities location |

---

## REST API Quick Reference

Base URL: `https://<aria-ops-fqdn>/suite-api/api`

```bash
# Authenticate and get token
curl -sk -X POST "https://<aria-ops>/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","authSource":"LOCAL","password":"<password>"}' | jq .

# List resources
curl -sk -H "Authorization: vRealizeOpsToken <token>" \
  "https://<aria-ops>/suite-api/api/resources" | jq .

# Get all active alerts
curl -sk -H "Authorization: vRealizeOpsToken <token>" \
  "https://<aria-ops>/suite-api/api/alerts?activeOnly=true" | jq .
```


```text title="Expected output"
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwNDY3MjAwMH0.a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "validity": 7200,
  "expiryTime": 1704679200000
}
{
  "pageInfo": {
    "pageSize": 100,
    "totalCount": 47,
    "page": 1
  },
  "resources": [
    {
      "identifier": "vc-prod-01",
      "resourceKey": {
        "name": "vc-prod-01",
        "resourceType": "VMwareAdapter Instance"
      },
      "resourceStatus": "STARTED"
    },
    {
      "identifier": "esx-host-12.corp.local",
      "resourceKey": {
        "name": "esx-host-12.corp.local",
        "resourceType": "HostSystem"
      },
      "resourceStatus": "STARTED"
    },
    {
      "identifier": "vm-web-prod-04",
      "resourceKey": {
        "name": "vm-web-prod-04",
        "resourceType": "VirtualMachine"
      },
      "resourceStatus": "STARTED"
    }
  ]
}
{
  "pageInfo": {
    "pageSize": 100,
    "totalCount": 12,
    "page": 1
  },
  "alerts": [
    {
      "alertId": "alert-8472",
      "resourceName": "esx-host-12.corp.local",
      "alertDefinitionName": "CPU Contention",
      "severity": "WARNING",
      "startTime": 1704668400000
    },
    {
      "alertId": "alert-8471",
      "resourceName": "vm-web-prod-04",
      "alertDefinitionName": "Memory Pressure",
      "severity": "CRITICAL",
      "startTime": 1704665800000
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip SSL verification, or import the Aria Operations certificate into your system trust store. |
    | `jq: parse error: Invalid JSON at line 1` | Verify the API endpoint URL is correct and the Aria Operations service is running; check response with `curl -sk ... | head -20` to see actual content. |
    | `{"error":"Invalid token or token expired"}` | Re-authenticate to get a fresh token using the first curl command and update the Authorization header with the new token value. |
---

## Related Sections

- [Operations](index.md) — operational runbooks
- [Scripts](scripts.md) — automation using the API
- [Troubleshooting](../troubleshooting/index.md) — diagnostic commands

---

## See also

- [Aria Operations Procedures](../procedures/)
- [Aria Operations Scripts](../scripts/)
- [Aria Operations Health Checks](../health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
