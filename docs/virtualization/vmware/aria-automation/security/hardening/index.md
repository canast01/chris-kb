# Aria Automation — Hardening


<div class="kb-summary">
Hardening reference covering Default Account Hardening, Certificate Replacement, Service Account Principle of Least Privilege, SSH and Console Access, Kubernetes Security and 3 more sections.
</div>

## Default Account Hardening

The `admin` account is a local system account in the VIDM System Domain. Change its password immediately after deployment:

```text
VAMI (https://vra-prod-01.example.local:5480) → Services → Change Admin Password
```
```text
┌───────────────────────────────────── Aria Automation — Hardening ─────────────────────────────────────┐
│                                                                                                       │
│  Harden vRA by disabling unused services, enforcing TLS, MFA, and minimal access.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Network Hardening               │  │               Access Hardening              │   │
│   │       Firewall: allow only 443 inbound       │  │       MFA mandatory for all vRA users       │   │
│   │      Disable SSH after setup (use VAMI)      │  │     Minimum privilege: member not admin     │   │
│   │       Management VLAN: restrict access       │  │      Break-glass: change after each use     │   │
│   │      No direct DB access from prod nets      │  │       vIDM: enforce device compliance       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Configuration hardening removes attack surface and enforces secure defaults.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Configuration Hardening            │  │             Audit and Compliance            │   │
│   │      TLS 1.2+ only; disable TLS 1.0/1.1      │  │        Aria Ops: vRA operations audit       │   │
│   │      No self-signed certs in production      │  │       vRA activity log: 90d retention       │   │
│   │     Approval policies on all prod items      │  │       SIEM: forward vRA syslog events       │   │
│   │       Lease policies: no unlimited VMs       │  │       VMware STIG: apply vRA hardening      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliance VMs · management VLAN · firewall rules · vIDM · SIEM for log forwarding                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VAMI SSH disable  = After setup, SSH on vRA appliance is disabled; use VAMI for mgmt tasks           │
│  Management VLAN   = Isolated network segment for vRA appliance management interfaces                 │
│  Break-glass acct  = Local admin used only in emergency; password rotated after every use             │
│  Device compliance = vIDM policy requiring managed/enrolled device for vRA access                     │
│  TLS enforcement   = vRA config disabling TLS 1.0 and 1.1 on all endpoints                            │
│  VMware STIG       = Security Technical Implementation Guide published by VMware/DISA                 │
│  Syslog forwarding = vRA sends audit events to SIEM via rsyslog or vRealize Log Insight               │
│  Lease policy      = Enforces time limit on deployments; prevents VM sprawl                           │
│  Approval policy   = Prevents unreviewed production deployments; mandatory for prod catalog           │
│  Minimum privilege = Users assigned lowest role that meets their work requirements                    │
│  Activity log      = vRA built-in audit trail of all requests, approvals, and actions                 │
│  SIEM integration  = Security Information and Event Management; aggregates vRA and vIDM logs          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

**Via vracli (standalone deployments):**

```bash
ssh root@vra-prod-01.example.local

# Import certificate
vracli certificate import \
  --cert /tmp/vra-prod-01.pem \
  --key /tmp/vra-prod-01.key \
  --ca /tmp/chain.pem

# Verify the certificate is active
echo | openssl s_client -connect vra-prod-01.example.local:443 2>/dev/null | \
  openssl x509 -noout -subject -issuer -dates
```

---

## Service Account Principle of Least Privilege

The vCenter service account used for Aria Automation cloud accounts should have only the required permissions — not the `Administrator` role:

| Permission | Scope |
|---|---|
| Virtual Machine — Create New | Target folders/clusters |
| Virtual Machine — Power (on/off/reset) | All VMs in project scope |
| Virtual Machine — Config (all) | All VMs in project scope |
| Datastore — Allocate Space | Target datastores |
| Network — Assign Network | Target port groups |
| Resource — Assign VM to Pool | Target resource pools |
| vApp — Import | Datacenter |

Create a dedicated service account: `svc-vra@vsphere.local` or a domain account `svc-vra@corp.local`. Store the password in the enterprise vault and rotate annually (or after any staff change).

---

## SSH and Console Access

```bash
# Restrict SSH access to management network CIDR
echo "sshd: 10.0.1.0/24" >> /etc/hosts.allow
echo "ALL: ALL" >> /etc/hosts.deny

# Disable root password login — require key-based SSH
# Edit /etc/ssh/sshd_config:
PermitRootLogin prohibit-password
systemctl restart sshd
```

For the VAMI (port 5480), restrict access to the management network at the firewall level — VAMI does not natively support IP-based access control.

---

## Kubernetes Security

The embedded Kubernetes cluster should not be accessible outside the appliance:

```bash
# Verify kubectl is only usable from within the appliance (localhost)
kubectl config view | grep "server:"
# Should show: server: https://127.0.0.1:<port>
```

Do not expose the Kubernetes API port externally. All management is done via `kubectl` on the appliance SSH session or via the Aria Automation REST API.

---

## Network Firewall Rules

| Source | Destination | Port | Protocol | Purpose |
|---|---|---|---|---|
| Admin workstations | vra-prod-* | 443 | TCP | Web UI and API |
| Admin workstations | vra-prod-* | 5480 | TCP | VAMI (restrict to admins only) |
| Admin workstations | vra-prod-* | 22 | TCP | SSH |
| vra-prod-* | vCenter | 443 | TCP | vSphere cloud account |
| vra-prod-* | NSX Manager | 443 | TCP | NSX cloud account |
| vra-prod-* | VIDM | 443 | TCP | SSO |
| vra-prod-* | SMTP relay | 25/587 | TCP | Notifications |
| vra-prod-* | DNS | 53 | UDP | Name resolution |
| vra-prod-* | NTP | 123 | UDP | Time sync |
| vra-prod-* | Code repo (GitHub/GitLab) | 443 | TCP | Blueprint Git sync (if enabled) |

Block all other inbound traffic, especially direct access to internal Kubernetes ports.

---

## Audit and Compliance

Aria Automation logs all deployment requests, approval decisions, and administrative actions in the audit log.

```bash
# Access audit events via API
TOKEN=<your-token>
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/audit/api/events?size=100&sort=timestamp,desc" | \
  jq '.content[] | {type: .type, user: .principal, resource: .resource, time: .timestamp}'
```

Forward syslog to Aria Ops for Logs or SIEM for centralised audit trail:

```bash
echo '*.* @@vrli-prod-01.example.local:514' > /etc/rsyslog.d/vra-audit.conf
systemctl restart rsyslog
```

---

## Hardening Checklist

- [ ] Admin password changed and stored in vault
- [ ] Self-signed certificate replaced with CA-signed certificate
- [ ] VIDM AD integration configured; AD groups mapped to Aria Automation roles
- [ ] Local admin account not used for day-to-day access
- [ ] vCenter service account follows least privilege — not using Administrator role
- [ ] SSH restricted to management network CIDR
- [ ] VAMI (port 5480) access restricted at firewall to admin team
- [ ] Blueprint Git content source uses a service account with read-only repository access
- [ ] Encrypted Property Groups used for all secrets in cloud templates — no plaintext passwords
- [ ] Syslog forwarding to Aria Ops for Logs or SIEM configured
- [ ] Aria Automation software at current patch level (verify via LCM or VAMI)
- [ ] Certificate expiry tracked and renewal scheduled before 30-day warning
- [ ] NTP configured and synchronised: `chronyc tracking` on each appliance node
