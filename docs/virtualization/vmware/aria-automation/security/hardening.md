---
tags:
  - aria-automation
  - security
  - vmware
---
# Aria Automation — Hardening


<div class="kb-summary">
Hardening reference covering Default Account Hardening, Certificate Replacement, Service Account Principle of Least Privilege, SSH and Console Access, Kubernetes Security and 3 more sections.

*Applies to: Aria Automation 8.x*
</div>
![Aria Automation — Hardening](../../../../assets/virtualization-vmware-aria-automation-security-hardening.svg)


```d2
direction: down

external: External / Untrusted {shape: rectangle}
default_account_hardening: "Default Account Hardening" {shape: rectangle}
service_account_principle_of_least_p: "Service Account Principle of Least Privilege" {shape: rectangle}
ssh_and_console_access: "SSH and Console Access" {shape: rectangle}
kubernetes_security: "Kubernetes Security" {shape: rectangle}
network_firewall_rules: "Network Firewall Rules" {shape: rectangle}
audit_and_compliance: "Audit and Compliance" {shape: rectangle}
core: "Aria Automation Core" {shape: hexagon}

external -> default_account_hardening: traffic in
default_account_hardening -> service_account_principle_of_least_p
service_account_principle_of_least_p -> ssh_and_console_access
ssh_and_console_access -> kubernetes_security
kubernetes_security -> network_firewall_rules
network_firewall_rules -> audit_and_compliance
audit_and_compliance -> core: secured path
```

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Default Account Hardening

The `admin` account is a local system account in the VIDM System Domain. Change its password immediately after deployment:


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

## See also

- [Aria Automation — Access Control](access-control/)
- [Aria Automation — Authentication](authentication/)
- [Aria Automation — Health Checks](../operations/health-checks/)
