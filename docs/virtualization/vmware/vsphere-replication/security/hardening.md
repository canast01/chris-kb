---
tags:
  - security
  - vmware
  - vsphere-replication
---
# vSphere Replication — Hardening


<div class="kb-summary">
Hardening reference covering Post-Deployment Checklist, Restrict SSH Access, Restrict VRA Management Access, Least-Privilege VR Service Account, Enable Encryption for WAN Replications and 3 more sections.

*Applies to: vSphere Replication 8.x*
</div>

  VR Hardening Controls
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Credentials                 Network Restrictions                                                     │
│  ┌──────────────────────┐    ┌──────────────────────────┐                                             │
│  │ Change admin / root  │    │ Port 5480 (VAMI):        │                                             │
│  │  passwords post-     │    │  mgmt subnet only        │                                             │
│  │  deploy              │    │ Port 31031 (repl data):  │                                             │
│  │ SSH: key-based only  │    │  source ESXi IPs only    │                                             │
│  │ PermitRootLogin: no  │    │ Port 443 (API):          │                                             │
│  └──────────────────────┘    │  mgmt subnet only        │                                             │
│                              └──────────────────────────┘                                             │
│  Certificate                 WAN Encryption                                                           │
│  ┌──────────────────────┐    ┌──────────────────────────┐                                             │
│  │ Replace self-signed  │    │ Enable replication       │                                             │
│  │  with CA-signed cert │    │  data encryption for     │                                             │
│  │ Renew 30 days before │    │  all WAN replications    │                                             │
│  │  expiry              │    └──────────────────────────┘                                             │
│  └──────────────────────┘                                                                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Post-Deployment Checklist

| Control | Action | Priority |
|---|---|---|
| Change VRA admin password | VRA VAMI → Administration → Change Admin Password | Critical |
| Replace self-signed certificate | VRA VAMI → SSL → Upload Certificate | High |
| Restrict SSH to jump hosts only | Firewall or VRA iptables | High |
| Enable replication encryption for WAN links | Per-VM replication config | High |
| Use read-only vCenter service account (read) | Assign minimum vCenter privileges | High |
| Update site pair thumbprints after cert change | Site Recovery → Sites → Edit | Medium |
| Enable monitoring/alerting for RPO violations | Pure1 / vRealize Operations / custom script | Medium |
| Test recovery monthly | Document results | Critical (process) |

---

## Restrict SSH Access

```bash
# SSH to VRA
ssh admin@vra-london.example.local

sudo vim /etc/ssh/sshd_config
# Set:
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers admin

sudo systemctl restart sshd
```

Firewall rule: allow SSH (TCP 22) to VRA only from jump host IPs.

---

## Restrict VRA Management Access

```bash
# Limit who can reach VRA VAMI (port 5480) and REST API (port 443)
sudo iptables -A INPUT -p tcp --dport 5480 -s 10.10.10.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5480 -j DROP
sudo iptables -A INPUT -p tcp --dport 443 -s 10.10.10.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j DROP
sudo iptables-save > /etc/iptables/rules.v4
```

Port 31031 (replication data receiver) should only accept connections from source site ESXi management IPs:
```bash
# Allow replication traffic from source ESXi subnet only:
sudo iptables -A INPUT -p tcp --dport 31031 -s 10.10.10.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 31031 -j DROP
```

---

## Least-Privilege VR Service Account

```yaml
vCenter → Administration → Roles → Create Custom Role
  Name: VR-ServiceAccount
  Privileges:
    vSphere Replication → Monitor
    vSphere Replication → Manage
    Virtual machine → Inventory (view)
    Datastore → Browse
    (Do NOT include vSphere Replication → Recover for the service account)

vCenter → Administration → Global Permissions → Add
  User: svc-vsphere-replication@corp.local
  Role: VR-ServiceAccount
  Propagate: Yes
```

Keep the Recovery privilege in a separate role assigned only to the DR team.

---

## Enable Encryption for WAN Replications

```text
vCenter → Site Recovery → Replications → [VM] → Edit
  Encryption: Enable
```

Enable for all VMs replicating over untrusted WAN links. For same-datacenter replications (internal LAN), encryption is optional — rely on network security instead.

---

## Regular Test Recovery

Monthly test is the most important operational security measure — an untested DR capability is not a capability:

```text
vCenter → Site Recovery → Replications → [VM]
  → Recover → Test mode
  Use isolated network (no access to production)
  After test: delete recovered test VM, do NOT remove replication
```

Document: test date, VMs tested, RPO at time of recovery, pass/fail.

---

## Certificate Rotation

```bash
# Check VRA cert expiry
echo | openssl s_client -connect vra-london.example.local:443 2>/dev/null \
  | openssl x509 -noout -enddate

# Renew 30 days before expiry:
# VRA VAMI → SSL → Upload Certificate
```

After rotating VRA certificate at either site:
```text
Site Recovery → Sites → [pair] → Edit → Refresh Thumbprints
```

---

## Monitoring and Alerting

Configure alerting for RPO violations — do not rely solely on manual dashboard checks:

```powershell
# Script to run as a scheduled task — alert on non-OK replication states
# (see Scripts page for full implementation)

# Or use vRealize Operations: create alert rule for metric "vsphere.replication.rpm_status"
# Alert when value != 0 (0=OK, 1=Warning, 2=Error)
```

## See also

- [vSphere Replication — Access Control](access-control/)
- [vSphere Replication — Authentication](authentication/)
- [vSphere Replication — Health Checks](../operations/health-checks/)
