---
tags:
  - troubleshooting
  - vcenter
  - vmware
  - vsphere-8
search:
  boost: 1.5
---
# vCenter — Diagnostics

<div class="kb-summary">
vCenter Server diagnostic commands: check disk partitions and service health with vmon-cli, tail vpxd.log and SSO logs, validate DNS and NTP, check certificate expiry with vecs-cli, diagnose SSO identity source with ldapsearch, query the vCenter REST API, run PowerCLI cluster health checks, and collect the VCSA support bundle.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌──────────────────────────────────── vCenter Server — Diagnostics ─────────────────────────────────────┐
│                                                                                                       │
│  vCenter diagnostics use log bundles, service status checks, and database queries                     │
│  to identify root causes of connectivity, performance, and auth failures.                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Collection                │  │             Service Diagnostics             │   │
│   │            Support bundle: VC UI             │  │             vmon-cli -l (status)            │   │
│   │          vc-support.sh on appliance          │  │            journalctl -u vmware-*           │   │
│   │              Key logs: vpxd.log              │  │           service-control --status          │   │
│   │           SSO: ssoAdminServer.log            │  │           Check port 443/9443 open          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Collect support bundle first; vpxd.log and SSO logs cover 90% of issues.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            DB & Performance Diag             │  │             Network Diagnostics             │   │
│   │      Postgres: select pg_stat_activity       │  │            Ping VC from ESXi host           │   │
│   │          DB size: /storage/db usage          │  │           nslookup: VC FQDN + PTR           │   │
│   │           Slow UI: vpxd CPU usage            │  │         traceroute: management path         │   │
│   │          Stats rollup: latency logs          │  │           Port test: nc -zv vc 443          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  VCSA VM on ESXi · management network · vSphere Client browser → VCSA port 443 / VAMI 5480            │
│                                                                                                       │
│  Key terms:                                                                                           │
│  vc-support.sh = generates support bundle on VCSA; exports to /tmp                                    │
│  vpxd.log      = main vCenter Server log; task, event, error messages                                 │
│  ssoAdminServer= SSO authentication service log; login failures here                                  │
│  pg_stat_activity= Postgres view; shows active DB queries                                             │
│  vmon-cli      = service monitor; shows RUNNING/STOPPED state for all services                        │
│  journalctl    = systemd log; vmware-* services write here                                            │
│  /storage      = VCSA data partition; contains DB, logs, stats                                        │
│  nc -zv        = netcat; test TCP port reachability                                                   │
│  nslookup PTR  = reverse DNS check; must match forward A record                                       │
│  Support bundle= ZIP of all VCSA logs + config; send to GSS                                           │
│  Stats rollup  = scheduled job; aggregates perf metrics; latency = problem                            │
│  vecs-cli      = VMware Endpoint Certificate Store CLI; lists all certs with expiry                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TD
    A([vCenter Issue]) --> B{What type of problem?}
    B -->|UI slow or unresponsive| C[vmon-cli -l to check service state\ndf -h for /storage/db and /storage/log]
    B -->|SSO login failure| D[tail ssoAdminServer.log\nCheck NTP: chronyc tracking]
    B -->|ESXi host disconnected| E[nslookup vcenter-fqdn from ESXi\nnc -zv vcenter 443 to test port]
    B -->|Certificate error| F[vecs-cli entry list store MACHINE_SSL_CERT\nopenssl s_client -connect vcenter:443 for expiry]
    B -->|Task or event missing / slow| G[vpxd.log for task errors\nPostgres: select pg_stat_activity to check stuck queries]
    B -->|API returning errors| H[curl -sk REST API session acquire\nCheck vpxd.log for API error codes]
    C --> I{Service state?}
    I -->|Service STOPPED| J[journalctl -u vmware-vpxd -n 100\nservice-control --start vpxd]
    I -->|Running but slow| K[df -h /storage/db — check if >80%\nps aux to check vpxd CPU]
    D --> L{NTP OK?}
    L -->|Drift > 5 minutes| M[chronyc makestep to force sync\nCheck timedatectl for AD time source]
    L -->|NTP OK| N[ldapsearch -H ldaps://DC:636 to test AD connectivity\nCheck ssoAdminServer.log for bind error]
    E --> O[ping vcenter-fqdn from ESXi\nCheck management vmk0 vlan and routing]
    F --> P[vecs-cli entry list store MACHINE_SSL_CERT for expiry\nRenew via VAMI: Certificate Management]
    G --> Q[grep -i error vpxd.log or tail -200\nCheck /storage/db partition usage]
    H --> R[Collect vc-support.sh bundle\nOpen Broadcom VMware SR]
    J --> R
    K --> R
    M --> R
    N --> R
    O --> R
    P --> R
    Q --> R
    R --> S[VAMI: Support → Create Support Bundle\nUpload to mysupport.broadcom.com]

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,I,L dark
    class C,D,E,F,G,H,J,K,M,N,O,P,Q action
    class R,S escalate
```

## Before you begin

- **Access:** SSH to the VCSA appliance (root or administrator); vSphere Client admin credentials; VAMI access at `https://<vcenter>:5480`
- **Gather first:** the specific symptom (login failure, host disconnect, slow UI, task error), the affected object name or user account, and when the issue started
- **Scope:** confirm whether the issue affects one user, one host, one cluster, or the entire vCenter

---

## Step 1 — Check disk partitions and service health

Full partitions are the most common cause of cascading vCenter failures. Check before and after any service restart.

```bash
# SSH to VCSA as root
ssh root@<vcenter-ip>

# Partition usage — check ALL key partitions
df -h
```

Key partitions and alert thresholds:

| Partition | Purpose | Alert Threshold |
|---|---|---|
| `/storage/log` | vCenter and service logs | 80% |
| `/storage/db` | vCenter PostgreSQL database | 80% |
| `/storage/core` | Core appliance data, config | 80% |
| `/storage/seat` | Stats, events, alarms, and tasks DB | 80% |
| `/` | Root filesystem | 85% |

```bash
# All vCenter service status
vmon-cli -l
# Expected: all services RUNNING
# Problem: any service STOPPED — note which service

# Recent service events (for any stopped service)
journalctl -u vmware-vpxd -n 100 --no-pager | grep -i "error\|fail\|crash"
journalctl -u vmware-stsd -n 100 --no-pager | grep -i "error\|fail"

# Service-level status summary
service-control --status --all | grep -v RUNNING

# Clear old compressed logs if /storage/log is full
find /var/log/vmware -name "*.gz" -mtime +30 -delete
find /storage/log -name "*.gz" -mtime +30 -delete
```

---

## Step 2 — Review key log files

```bash
# Core vCenter log — tasks, events, errors
tail -200 /var/log/vmware/vpxd/vpxd.log | grep -i "error\|fatal\|panic"

# Watch vpxd live during an operation
tail -f /var/log/vmware/vpxd/vpxd.log | grep -i "error\|fatal"

# SSO login failures
tail -200 /var/log/vmware/sso/vmware-sts-idmd.log | grep -i "fail\|error\|bind"

# SSO admin server (token issuance failures)
tail -200 /var/log/vmware/sso/ssoAdminServer.log | grep -i "fail\|error"

# Certificate operations
tail -100 /var/log/vmware/vmcad/certificate-manager.log

# vSphere Client errors
tail -100 /var/log/vmware/vsphere-ui/logs/vsphere_client_virgo.log | grep -i "error\|exception"
```

All logs on the VCSA appliance:

| Component | Primary Log Path |
|---|---|
| vpxd (core vCenter) | `/var/log/vmware/vpxd/vpxd.log` |
| SSO identity daemon | `/var/log/vmware/sso/vmware-sts-idmd.log` |
| SSO admin server | `/var/log/vmware/sso/ssoAdminServer.log` |
| vSphere Client | `/var/log/vmware/vsphere-ui/logs/vsphere_client_virgo.log` |
| Certificate manager | `/var/log/vmware/vmcad/certificate-manager.log` |
| PostgreSQL | `/var/log/vmware/vpostgres/postgresql-*.log` |
| vmdird (LDAP/vmdir) | `/var/log/vmware/vmdird/vmdird-syslog.log` |
| Lookup service | `/var/log/vmware/lookupsvc/lookup-service.log` |
| Appliance mgmt | `/var/log/vmware/applmgmt/applmgmt.log` |

---

## Step 3 — Validate DNS and NTP

DNS and NTP failures cascade into certificate, SSO, and agent failures.

```bash
# Forward DNS — vCenter must resolve its own FQDN
nslookup vcenter.example.local

# Reverse DNS — must resolve back to the FQDN
nslookup <vcenter-ip>
# Expected: match the forward FQDN — mismatch breaks certificate validation

# Test ESXi host resolution from vCenter
nslookup esxi-01.example.local

# NTP status
timedatectl
chronyc sources -v
chronyc tracking
# Expected: System time offset < 1 second

# Force NTP sync if drift > 5 minutes (breaks Kerberos)
chronyc makestep
```

NTP drift over 5 minutes breaks Kerberos — SSO login failures for AD-backed accounts will occur. Fix NTP before investigating SSO.

---

## Step 4 — Check certificate expiry

```bash
# Machine SSL certificate expiry (what the browser connects to)
echo | openssl s_client -connect vcenter.example.local:443 \
    -servername vcenter.example.local 2>/dev/null \
    | openssl x509 -noout -dates
# Problem: notAfter date in the past

# VAMI certificate (port 5480)
echo | openssl s_client -connect vcenter.example.local:5480 2>/dev/null \
    | openssl x509 -noout -dates

# List all certificate stores on VCSA
/usr/lib/vmware-vmafd/bin/vecs-cli store list

# Machine SSL cert with expiry date
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text \
    | grep -E "Alias|Subject|Not After"

# VMCA root certificate
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store TRUSTED_ROOTS --text \
    | grep -E "Alias|Subject|Not After"

# Solution user certificates
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store vpxd-extension --text \
    | grep -E "Alias|Not After"
```

Certificate renewals: **VAMI → `https://<vcenter>:5480` → Certificate Management** — shows all certs with expiry and a renewal button.

---

## Step 5 — Diagnose SSO and identity source

```bash
# SSO service health
service-control --status vmware-stsd
service-control --status vmware-sts-idmd

# SSO domain info
/usr/lib/vmware-vmafd/bin/vmafd-cli get-domain-name --server-name localhost

# Lookup service endpoint (must be reachable for SSO to work)
/usr/lib/vmware-vmafd/bin/vmafd-cli get-ls-location --server-name localhost

# Test LDAP connectivity to AD domain controller from VCSA
ldapsearch -x \
    -H ldaps://dc01.example.local:636 \
    -b "DC=corp,DC=local" \
    -D "svc-vcenter-ldap@corp.local" \
    -W \
    "(objectClass=*)" dn
# Error: LDAP_SERVER_DOWN = DC unreachable; LDAP_INVALID_CREDENTIALS = wrong svc account pw

# Check vmdir (embedded LDAP for vsphere.local) health
/usr/lib/vmware-vmafd/bin/dir-cli ssogroup list --login administrator@vsphere.local
```

---

## Step 6 — Query vCenter REST API health

```bash
# Authenticate
TOKEN=$(curl -sk -u 'administrator@vsphere.local:<password>' \
    -X POST https://vcenter.example.local/api/session | tr -d '"')

# System health
curl -sk -H "vmware-api-session-id: $TOKEN" \
    https://vcenter.example.local/api/vcenter/health/system
# Expected: GREEN

# List all hosts and their connection state
curl -sk -H "vmware-api-session-id: $TOKEN" \
    https://vcenter.example.local/api/vcenter/host | \
    python3 -c "
import json,sys
for h in json.load(sys.stdin):
    if h.get('connection_state') != 'CONNECTED':
        print(f\"PROBLEM: {h['name']} state={h.get('connection_state','?')}\")
"

# Delete session when done
curl -sk -H "vmware-api-session-id: $TOKEN" \
    -X DELETE https://vcenter.example.local/api/session
```

---

## Step 7 — Run PowerCLI diagnostics

```powershell
# Connect
Connect-VIServer -Server vcenter.example.local

# Host connection states — should return empty in healthy env
Get-VMHost | Where-Object { $_.ConnectionState -ne "Connected" } |
    Select-Object Name, ConnectionState, PowerState

# Cluster HA and DRS state
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel

# Datastore accessibility and capacity
Get-Datastore | Select-Object Name,
    @{N="Accessible";E={$_.ExtensionData.Summary.Accessible}},
    @{N="CapGB";E={[math]::Round($_.CapacityGB,1)}},
    @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}},
    @{N="FreePct";E={[math]::Round($_.FreeSpaceGB/$_.CapacityGB*100,1)}} |
    Sort-Object FreePct

# Recent error events (last 6 hours)
Get-VIEvent -Start (Get-Date).AddHours(-6) |
    Where-Object { $_.GetType().Name -match "Error|Fault|Warning" } |
    Select-Object CreatedTime, UserName, FullFormattedMessage |
    Format-Table -Wrap

# Active alarms across all objects
Get-VM | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="Alarms";E={$_.ExtensionData.TriggeredAlarmState.Count}}

# vCenter version
$global:DefaultVIServer | Select-Object Name, Version, Build
```

---

## Step 8 — Collect support bundle and escalation evidence

```bash
# Generate support bundle via VCSA shell (recommended)
/usr/bin/vm-support -n vcenter.example.local
ls -lh /var/core/esx-*.tgz
scp /var/core/esx-<timestamp>.tgz user@transfer-host:/path/

# Or: via VAMI
# https://<vcenter>:5480 → Support → Create Support Bundle

# Or: via vSphere Client
# Administration → Deployment → System Configuration → Export System Logs
```

Evidence to collect before escalation:

| Evidence Item | How to Collect |
|---|---|
| VCSA disk usage | `df -h` output |
| Service status | `service-control --status --all` output |
| vpxd.log excerpt | `tail -500 /var/log/vmware/vpxd/vpxd.log` |
| SSO log excerpt | `tail -200 /var/log/vmware/sso/vmware-sts-idmd.log` |
| Certificate expiry | VAMI → Certificate Management screenshot |
| Recent error events | vCenter → Monitor → Events, last 24 hours |
| Failed tasks | vCenter → Monitor → Tasks, filter by Error |
| vCenter build number | `https://<vcenter>/ui` → Help → About |

---

## Log locations

| Component | Path | What to look for |
|---|---|---|
| vpxd (core) | `/var/log/vmware/vpxd/vpxd.log` | Task failures, API errors |
| SSO identity | `/var/log/vmware/sso/vmware-sts-idmd.log` | LDAP bind errors, auth failures |
| SSO admin | `/var/log/vmware/sso/ssoAdminServer.log` | Token issuance failures |
| Certificate mgr | `/var/log/vmware/vmcad/certificate-manager.log` | Cert renewal and replacement |
| PostgreSQL | `/var/log/vmware/vpostgres/postgresql-*.log` | DB slow query and crash events |
| Lookup service | `/var/log/vmware/lookupsvc/lookup-service.log` | Endpoint registration errors |

---

## See also

- [vCenter Troubleshooting — Common Issues](common-issues/)
- [vCenter — Escalation](escalation/)

## Verify resolution

- `vmon-cli -l` shows all services RUNNING with no STOPPED state
- `df -h` shows all `/storage/*` partitions below 80% used
- `GET /api/vcenter/health/system` returns GREEN
- SSO login test: log out and log back in to vSphere Client — authentication succeeds
- `nslookup <vcenter-fqdn>` and reverse PTR match; `chronyc tracking` shows time offset < 1s
- The triggering event or alarm no longer appears in vCenter → Monitor → Events
