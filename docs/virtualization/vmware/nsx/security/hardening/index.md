# NSX — Hardening

## Hardening Baseline

Follow the **VMware NSX Security Configuration Guide** published by Broadcom. The SCG maps NSX controls to CIS Benchmarks and DISA STIG requirements. Download from the Broadcom Knowledge Base for the specific NSX version in use.

---

## NSX Manager Hardening Checklist

### Network Access Controls

- [ ] NSX Manager VIP accessible only from admin jump hosts (port 443)
- [ ] SSH (port 22) to NSX Manager nodes restricted to admin jump hosts only
- [ ] Geneve UDP 6081 allowed only on TEP VLANs — not reachable from VM subnets
- [ ] BGP port 179 on Edge uplinks restricted to known physical router IPs
- [ ] NSX Manager management network on a dedicated VLAN, not shared with VM workloads

### Authentication and Access

- [ ] LDAP/AD identity source configured — no shared local admin account for day-to-day use
- [ ] Role assignments match the least-privilege matrix (see Access Control page)
- [ ] `admin` password rotated from default; stored in secrets vault
- [ ] `audit` password set; stored in secrets vault
- [ ] No unused principal identities or stale role bindings
- [ ] Password policy enforced: 20+ characters, 90-day maximum, 5-attempt lockout

### API Security

- [ ] TLS 1.2 minimum enforced — verify with `openssl s_client`
- [ ] API certificate is CA-signed (not default self-signed)
- [ ] API certificate expiry monitored — alert at 60 days
- [ ] Automation uses certificate-based principal identities (not shared admin password)
- [ ] API access logged and forwarded to SIEM

### Audit and Monitoring

- [ ] Syslog configured on all Manager nodes (TLS, port 6514)
- [ ] Syslog configured on all Edge nodes
- [ ] ESXi DFW logs forwarded via host syslog
- [ ] NSX Manager backup configured, tested, and verified on SFTP
- [ ] SIEM alerts defined for authentication failures and role changes

---

## DFW Hardening Configuration

### Default Deny Rule

The built-in default rule (rule 65535) must be `any-any-drop`. Verify it has not been changed:

```bash
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/domains/default/security-policies/default-layer3-section/rules" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for r in d.get('results', []):
    if r.get('sequence_number', 0) == 65535:
        print(f'Rule 65535: action={r.get(\"action\")}')
"
# Expected: action=DROP
```
┌─────────────────────────────────────────── NSX — Hardening ───────────────────────────────────────────┐
│                                                                                                       │
│  CIS NSX benchmark, API security, DFW default-deny, and lockdown posture.                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             CIS / STIG Controls              │  │                 API Security                │   │
│   │         Disable root SSH on manager          │  │                TLS 1.2+ only                │   │
│   │          Change default admin pass           │  │             Disable TLS 1.0/1.1             │   │
│   │         NTP configured on all nodes          │  │          Replace self-signed certs          │   │
│   │          Syslog to SIEM/syslog host          │  │             Rate limit API calls            │   │
│   │            FIPS mode if required             │  │         Named service accounts only         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Baseline hardening → DFW default-deny policy → regular audit reviews.                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              DFW Default Policy              │  │               Hardening Review              │   │
│   │          Default layer: deny + log           │  │           Review DFW rules monthly          │   │
│   │        Emergency allow above default         │  │            Alert on new allow-all           │   │
│   │           Micro-seg by app / zone            │  │           Check cert expiry < 60d           │   │
│   │           Log all blocked traffic            │  │           Verify FIPS if mandated           │   │
│   │        Gateway firewall as perimeter         │  │            Audit role assignments           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager VMs, Edge VMs, ESXi hosts, syslog/SIEM, management network                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CIS         = Center for Internet Security; NSX hardening benchmark                                  │
│  STIG        = Security Technical Implementation Guide; DOD hardening                                 │
│  FIPS 140-2  = US crypto standard; NSX FIPS mode enforces compliant algos                             │
│  DFW default = last DFW rule; set to deny+log to block unmatched traffic                              │
│  Micro-seg   = per-VM/app firewall rules; east-west security enforcement                              │
│  Gateway FW  = NSX Edge firewall; north-south perimeter rule enforcement                              │
│  TLS 1.2     = minimum TLS for NSX API; 1.3 preferred                                                 │
│  SIEM        = Security Info & Event Mgmt; receives NSX syslog                                        │
│  Rate limit  = API throttle; prevents brute force or runaway scripts                                  │
│  Root SSH    = disabled on NSX Manager appliance in hardened config                                   │
│  Named accts = automation uses dedicated named service accounts                                       │
│  NTP         = time sync; required for cert validity and log correlation                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

### Emergency Category Rules

Maintain at least these rules in the Emergency category (highest priority, evaluated first):

| Rule Name | Source | Destination | Service | Action |
|---|---|---|---|---|
| Allow-vCenter-to-ESXi | vCenter IP | All ESXi hosts | TCP 443, 902 | Allow |
| Allow-NSX-Manager | NSX Manager VIPs | All ESXi hosts | TCP 443 | Allow |
| Allow-NTP | All | NTP servers | UDP 123 | Allow |
| Allow-DNS | All | DNS servers | TCP/UDP 53 | Allow |
| Emergency-Block | Specific threat IP | Any | Any | Drop |

These rules prevent a misconfigured Application DFW policy from cutting off NSX management access to ESXi hosts.

### DFW Exclusion List

The DFW Exclusion List bypasses DFW enforcement for specific VMs. Keep this list minimal — it is a security bypass.

Legitimate candidates for exclusion:
- NSX Manager VMs (self-management)
- Active Directory domain controllers (when the only authentication source)
- Physical-to-virtual migration VMs during migration window only

```bash
# List current exclusion list
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/firewall/excludelist"

# Add a VM to the exclusion list (use the VM's external-id from fabric)
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"target_id": "<vm-moref>", "target_type": "VirtualMachine"}' \
  "https://<nsx-manager>/api/v1/firewall/excludelist"
```

---

## Edge Node Hardening

### Remove Unused Services

Edge nodes run multiple services. Disable any not in use:

```bash
# SSH to Edge node — list services
get services

# Disable a specific service (example: LB if not using NSX load balancer)
set service load-balancer stop

# Services that should always be running on production Edge:
#   dataplane, router, manager (agent to NSX Manager)
# Services that may be stopped if unused:
#   load-balancer, dhcp, dns
```

### Edge Node HA — Verify Failover Works

Test failover in a maintenance window at least every 6 months:

```bash
# SSH to Active Edge
set edge-cluster failover
# T0 gateway moves to Standby Edge — BGP reconverges

# Verify BGP on new Active Edge
get bgp neighbor summary
# All peers should be Established within 10–30 seconds

# Verify routing table intact
vrf <tier0-vrf>
get route
```

### BGP Authentication

All BGP sessions must use MD5 authentication:

```bash
# Confirm BGP neighbor has password set
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/tier-0s/<t0-id>/locale-services/default/bgp/neighbors" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d.get('results', []):
    has_pwd = 'YES' if n.get('password') else 'NO'
    print(f'{n.get(\"display_name\",\"?\")}  {n.get(\"neighbor_address\",\"?\")}  password={has_pwd}')
"
```

---

## Transport Node Security

### Verify NSX VIB Acceptance Level on ESXi Hosts

NSX VIBs should be VMwareAccepted or VMwareCertified:

```bash
# On ESXi host
esxcli software vib list | grep -i nsx | awk '{print $1, $4}'
# The acceptance level column should show VMwareCertified or VMwareAccepted
```

### Confirm DFW is Enforcing on Every Host

```bash
# On each ESXi host — confirm DFW filters exist
summarize-dvfilter | grep -c "vmware-sfw"
# Count should equal the number of powered-on VM vNICs on this host
# A count of 0 means DFW is not applying to VMs — escalate immediately
```

---

## Hardening Quick Reference

| Control | Verification Command | Expected State |
|---|---|---|
| TLS 1.2 minimum | `openssl s_client -connect <nsxmgr>:443 -tls1` | Connection refused |
| API cert CA-signed | `openssl s_client -connect <nsxmgr>:443` → check issuer | CA Issuer: internal CA |
| DFW default deny | `get firewall default-rule` via nsxcli | Action: Drop |
| BGP MD5 auth | Check neighbor config via Policy API | `password` field present |
| Syslog configured | `get service syslog exporters` on Manager and Edge | Shows SIEM target |
| Backup current | `GET /api/v1/cluster/backups/history` | Last backup < 25 hours ago |
| Admin password vault | Manual check | Password stored in vault |
| No stale role bindings | `GET /api/v1/aaa/role-bindings` | No former employee accounts |
| DFW filters on ESXi | `summarize-dvfilter` | Count > 0 per host |
