---
tags:
  - operations
  - san
---
# Cisco Nexus Dashboard — Operations Health Checks

```bash
# SSH to any cluster node
ssh ndadmin@nd-dc1-1.corp.example.com

# Show cluster health summary
acs health

# Show all nodes
acs nodes list
# Expected: all nodes in Active or Standby state, no Unhealthy

# Show app deployment status
acs apps status
# Expected: all apps in Running state (NDFC, NDI if installed)

# Show any failing Kubernetes pods
kubectl get pods --all-namespaces | grep -Ev "Running|Completed"
# Zero output = all pods healthy; any output needs investigation
```

```d2
direction: right

run_this_routine: "Run This Routine" {shape: rectangle}
verify: "Verify" {shape: rectangle}

run_this_routine -> verify
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. Nexus Dashboard UI → System → Services — verify all platform services show **Running**; any Stopped or Error state needs investigation
2. Nexus Dashboard → Sites — confirm all registered sites show **Connected**; Disconnected sites block policy deployment
3. NDFC → Fabric Builder → switch inventory — verify all fabric switches appear as **Managed** with no discovery errors
4. NDFC → Fabric → deployment status — check for any switches with **pending** or **failed** configuration deployments; resolve before next change window
5. Nexus Dashboard → Alerts → open alarms — filter Critical and Major severity; review, assign, and escalate unacknowledged alarms
6. NDFC → Operations → Backup — confirm last successful backup timestamp is within the last 24 hours; trigger manual backup if overdue
7. SSH to each ND node: `df -h /data` — alert and escalate if any node filesystem usage exceeds **80%** (Elasticsearch fills fast)

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# List recent backups
acs backup list

# Check backup destination
acs backup remote show
```

```text title="Expected output"
Last login: Wed Jan 15 14:32:18 2025 from 10.45.12.89
Cisco Nexus Dashboard
nd-dc1-1.corp.example.com#

Backup ID                          Status    Size      Date                 Type
backup-2025-01-15-143022          SUCCESS   2.3 GB    2025-01-15 14:30:22  FULL
backup-2025-01-14-020015          SUCCESS   2.2 GB    2025-01-14 02:00:15  FULL
backup-2025-01-13-020008          SUCCESS   2.1 GB    2025-01-13 02:00:08  FULL
backup-2025-01-12-020012          SUCCESS   2.2 GB    2025-01-12 02:00:12  FULL
backup-2025-01-11-020005          SUCCESS   2.1 GB    2025-01-11 02:00:05  FULL

Remote Backup Destination:
  Protocol: SFTP
  Host: backup-server.corp.example.com
  Port: 22
  Path: /backups/nexus-dashboard
  Username: ndbackup
  Status: Connected
  Last Backup: 2025-01-15 14:30:22
```

!!! warning "Common errors"
    **`Authentication failed for ndadmin@nd-dc1-1.corp.example.com`** — Verify SSH key is loaded with `ssh-add` or use password authentication if key-based auth is not configured.
    **`Remote destination unreachable: Connection refused on backup-server.corp.example.com:22`** — Confirm the backup server is online and SFTP service is running; check firewall rules allow traffic from the Nexus Dashboard to the backup server.
```bash
# Check ND UI certificate expiry
openssl s_client -connect nd-dc1.corp.example.com:443 \
  -servername nd-dc1.corp.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -dates

# Days until expiry
python3 -c "
from datetime import datetime
import subprocess, re
r = subprocess.run(['openssl','s_client','-connect','nd-dc1.corp.example.com:443',
  '-servername','nd-dc1.corp.example.com'], capture_output=True, input=b'')
c = subprocess.run(['openssl','x509','-noout','-enddate'], input=r.stdout, capture_output=True).stdout.decode()
d = re.search(r'notAfter=(.*)', c).group(1).strip()
exp = datetime.strptime(d, '%b %d %H:%M:%S %Y %Z')
print(f'Expires in {(exp - datetime.utcnow()).days} days ({exp.date()})')
"
# Alert if < 60 days remaining
```

```text title="Expected output"
notBefore=Aug 15 09:22:14 2023 GMT
notAfter=Aug 14 09:22:14 2025 GMT
Expires in 47 days (2025-08-14)
```

!!! warning "Common errors"
    **`unable to get local issuer certificate`** — Add the Nexus Dashboard root CA certificate to your system's trusted store or use `openssl s_client -connect nd-dc1.corp.example.com:443 -CAfile /path/to/ca-bundle.crt` to bypass validation.
    **`Name or service not known`** — Verify DNS resolution with `nslookup nd-dc1.corp.example.com` and ensure the hostname matches your ND deployment's FQDN.
    **`Connection refused`** — Confirm the Nexus Dashboard UI is running and accessible on port 443 with `curl -k https://nd-dc1.corp.example.com/login` before checking the certificate.
```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Check NTP status
acs system ntp show
# Expected: all configured NTP servers reachable, synchronized

# Check cluster time consistency across nodes
acs nodes list --format json | python3 -c "
import sys, json
nodes = json.load(sys.stdin)
for n in nodes:
    print(n.get('hostname'), n.get('currentTime'))
"
# All nodes should show times within 1 second of each other
```


```text title="Expected output"
Last login: Mon Jan 15 14:32:18 2024 from 10.50.12.45

nd-dc1-1# acs system ntp show
NTP Status: synchronized
Stratum: 2
Reference Clock: 10.20.1.50 (ntp-primary.corp.example.com)
Last Update: 12 seconds ago
Poll Interval: 64 seconds

NTP Servers:
  10.20.1.50     reachable, offset: +2.145ms
  10.20.1.51     reachable, offset: -1.823ms
  10.20.2.50     reachable, offset: +0.956ms

nd-dc1-1# acs nodes list --format json | python3 -c "
> import sys, json
> nodes = json.load(sys.stdin)
> for n in nodes:
>     print(n.get('hostname'), n.get('currentTime'))
> "
nd-dc1-1 2024-01-15T14:32:45.123Z
nd-dc1-2 2024-01-15T14:32:44.891Z
nd-dc1-3 2024-01-15T14:32:45.456Z
```

!!! warning "Common errors"
    **`error: NTP Status: unsynchronized`** — Verify NTP server connectivity with `acs system ntp servers test` and check firewall rules allowing UDP port 123 to configured NTP servers.
    **`json.decoder.JSONDecodeError: Expecting value`** — Ensure the `acs` CLI is properly initialized by running `acs login` and verify cluster is fully operational with `acs cluster status`.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Nexus Dashboard — Procedures](../procedures/)
- [Nexus Dashboard — CLI Reference](../cli-reference/)
- [Nexus Dashboard — Common Issues](../../troubleshooting/common-issues/)
