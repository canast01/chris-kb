# NSX — Hardening

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
```text
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
```
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
```bash
# On ESXi host
esxcli software vib list | grep -i nsx | awk '{print $1, $4}'
# The acceptance level column should show VMwareCertified or VMwareAccepted
```
```bash
# On each ESXi host — confirm DFW filters exist
summarize-dvfilter | grep -c "vmware-sfw"
# Count should equal the number of powered-on VM vNICs on this host
# A count of 0 means DFW is not applying to VMs — escalate immediately
```
