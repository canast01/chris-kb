# Nexus Dashboard — Hardening

> Part of the [Nexus Dashboard](../../index.md) reference.

---

## Overview

Hardening the Nexus Dashboard cluster reduces the attack surface of the management plane. Apply this baseline during initial deployment and validate quarterly. ND runs on a Kubernetes-based Linux platform — hardening applies to both the ND application configuration and the underlying platform.

---

## 1. Change Default Credentials

```bash
# SSH to the ND cluster
ssh ndadmin@nd-dc1-1.corp.example.com

# Change the default admin password (via GUI: Admin Console > Security > Users > admin)
# For ndadmin OS account on the appliance, change password:
passwd ndadmin
# Use a password meeting corporate complexity policy (20+ characters)
# Store in vault; treat as break-glass
```
┌───────────────────────────── Cisco Nexus Dashboard — Security Hardening ──────────────────────────────┐
│                                                                                                       │
│  Hardening checklist: replace default certs, restrict access, enable AAA, audit logging.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Platform Hardening              │  │              Network Hardening              │   │
│   │           Replace self-signed cert           │  │          IP allowlist: mgmt source          │   │
│   │          Enable SAML/LDAP: no local          │  │           OOB mgmt: dedicated VLAN          │   │
│   │        Disable default admin: rename         │  │           Firewall: port 443 only           │   │
│   │        Password policy: max strength         │  │             NTP auth: keyed NTP             │   │
│   │         Session timeout: 15 min idle         │  │             Syslog TLS: to SIEM             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Replace certs and enable AAA first; then restrict network access; then audit                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             App-Level Hardening              │  │              Ongoing Compliance             │   │
│   │        NDFC: disable unused features         │  │           Quarterly access review           │   │
│   │         NDO: limit deploy approvers          │  │          Cert expiry: monitor < 30d         │   │
│   │         NDI: restrict telemetry read         │  │         Patch: apply within 30 days         │   │
│   │          API: service accounts only          │  │         PSIRT: subscribe advisories         │   │
│   │        Minimal roles: least privilege        │  │            Backup: verify monthly           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster · CA server · SAML IdP · SIEM · NTP server · OOB management switch                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Self-signed cert= Default ND cert; must be replaced with CA-signed before production                 │
│  IP allowlist   = Network-level restriction on which source IPs can reach port 443                    │
│  OOB VLAN       = Dedicated out-of-band management network isolated from data path                    │
│  PSIRT          = Cisco Product Security Incident Response Team; publishes CVEs                       │
│  Least privilege= Each user/service account has only the minimum required permissions                 │
│  Session timeout= Idle UI session automatically terminated after inactivity period                    │
│  NTP auth       = Keyed NTP ensuring time sync from trusted server only                               │
│  Service account= Dedicated ND user for automation; separate from human accounts                      │
│  Deploy approver= NDO role permitted to push templates to production APIC sites                       │
│  Access review  = Periodic audit of all user accounts and role assignments                            │
│  Patch window   = Defined maintenance period for applying ND software updates                         │
│  Syslog TLS     = Encrypted syslog stream forwarding audit events to SIEM                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Restrict Management Network Access

Use firewall or network ACL controls to limit access to the ND management interface:

| Source | Destination | Port | Protocol | Action |
|---|---|---|---|---|
| Management subnet | ND mgmt IPs | 443 | HTTPS | Allow |
| Jump host / VPN subnet | ND mgmt IPs | 22 | SSH | Allow |
| Switch management subnet | ND data IPs | 22, 161, 162, 514 | TCP/UDP | Allow |
| Any | ND mgmt IPs | 443, 22 | TCP | Deny (default) |

ND does not provide a built-in host firewall UI. Apply ACLs on the upstream switch or firewall in front of the ND management network. Do not expose the ND management interface to the open internet.

On the ND node OS (for emergency access control):

```bash
# Check firewall status (ND appliance uses firewalld)
sudo firewall-cmd --list-all

# Restrict SSH to management subnet
sudo firewall-cmd --permanent --remove-service=ssh
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.10.0.0/24" service name="ssh" accept'
sudo firewall-cmd --reload
```

---

## 4. Configure External Authentication

Do not run production with local accounts only. Configure LDAP, TACACS+, or SAML:

1. Navigate to **Admin Console > Security > Authentication**.
2. Configure LDAP or TACACS+ as described in [Authentication](../authentication/index.md).
3. Test authentication with an AD account before retiring local accounts.
4. Retain exactly one local admin account as break-glass.

### Disable Local Login for Non-Break-Glass Accounts

After LDAP/SAML is confirmed working:
1. Navigate to **Admin Console > Security > Local Users**.
2. Delete all local accounts except the break-glass `admin`.
3. Document the break-glass account location in the runbook.

---

## 5. Session Security

Configure under **Admin Console > Security > Security Settings**:

| Setting | Recommended Value |
|---|---|
| Session idle timeout | 15 minutes |
| Maximum session lifetime | 8 hours |
| Concurrent sessions per user | 3 |
| Failed login lockout | 5 attempts / 30 minutes |

---

## 6. Login Banner

Configure a legal warning banner on the ND login page:

1. Navigate to **Admin Console > Security > Security Settings > Login Banner**.
2. Enter:
   ```
   WARNING: This system is for authorized use only.
   All connections are monitored and recorded.
   Unauthorized access is prohibited and may result in legal action.
   ```
3. Click **Save**. The banner appears below the login form.

---

## 7. Backup Encryption

Enable backup encryption to protect backup archives at rest on the remote backup server:

1. Navigate to **Admin Console > Operations > Backup > Settings**.
2. Enable **Encrypt Backups**.
3. Set a strong passphrase (20+ characters).
4. Store the passphrase in vault immediately.

Without backup encryption, backup archives contain all ND configuration including switch credentials in their encrypted form — still sensitive and should not be stored in plain text on a backup server.

---

## 8. Audit Logging

Ensure audit logging is enabled and forwarded to the SIEM:

1. **Admin Console > Operations > Audit Logs** — confirm events are being recorded.
2. Configure syslog forwarding to forward audit events to the SIEM:
   ```bash
   acs system syslog add --server 10.10.3.50 --port 514 --protocol tcp
   ```
3. Set up SIEM alerts for:
   - Multiple failed logins (> 5 in 5 minutes)
   - Admin account login events
   - Configuration changes (zone changes, user additions)
   - Login from unexpected source IP

---

## 9. Kubernetes Security Baseline

ND's Kubernetes control plane has several security defaults that should be verified:

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Confirm no pods are running as root unnecessarily
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.securityContext.runAsUser}{"\n"}{end}' | grep -v "^$"

# Confirm no privileged pods (outside of system namespaces)
kubectl get pods --all-namespaces -o json | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data['items']:
    ns = item['metadata']['namespace']
    name = item['metadata']['name']
    for c in item['spec'].get('containers',[]):
        if c.get('securityContext',{}).get('privileged'):
            print(f'Privileged: {ns}/{name}/{c[\"name\"]}')
" 2>/dev/null | grep -v "kube-system\|kube-proxy\|cilium"
# ND system pods require some elevated privileges; app pods should not

# Confirm NetworkPolicies are in place (Cilium enforces by default in ND)
kubectl get networkpolicies --all-namespaces | grep -c "NetworkPolicy"
# Should be non-zero
```

---

## 10. NTP Synchronization

Correct time is essential for certificate validation, log correlation, and Kerberos authentication:

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Check NTP status on all nodes
acs system ntp show

# If NTP is not configured or not synchronised:
acs system ntp add --server 10.10.0.10 --prefer
acs system ntp add --server 10.10.0.11

# Verify synchronisation (may take 2-5 minutes after adding NTP servers)
acs system ntp show
# Expected: server reachable, stratum ≤ 3, offset < 100ms
```

---

## Hardening Checklist

### Access and Authentication

- [ ] Default admin password changed; stored in vault
- [ ] LDAP or SAML configured and tested
- [ ] Local accounts limited to break-glass admin only
- [ ] Password policy enforced (12+ chars, complexity, 90-day rotation, lockout)
- [ ] Session idle timeout: 15 minutes
- [ ] RBAC roles assigned per least-privilege principle
- [ ] Site scoping applied for multi-site environments

### Network and Transport

- [ ] TLS certificate from corporate CA (not self-signed)
- [ ] TLS 1.0 and 1.1 disabled (verify with openssl s_client -tls1)
- [ ] Management access restricted to authorised subnets
- [ ] SSH restricted to jump host / management subnet
- [ ] Switch management traffic on dedicated data VLAN

### Data Protection

- [ ] Backup encryption enabled; passphrase in vault
- [ ] VM disk encryption enabled (vSphere VM Encryption or SED)
- [ ] Backup restore tested (annually)

### Monitoring and Visibility

- [ ] Login banner configured on ND UI
- [ ] Syslog forwarding to SIEM active
- [ ] SIEM alerts for failed logins and admin activity configured
- [ ] Audit log reviewed quarterly

### Operational

- [ ] NTP synchronized on all nodes (< 100ms offset)
- [ ] TLS certificate expiry monitored (< 60 days = alert)
- [ ] ND platform and app versions current
- [ ] Quarterly hardening review scheduled

---

## Periodic Review Schedule

| Review | Frequency |
|---|---|
| Full hardening checklist | Quarterly |
| Break-glass password rotation | Quarterly |
| User access review | Quarterly |
| TLS certificate expiry check | Monthly |
| ND platform upgrade | Align with Cisco release cadence |
| Backup restore test | Annually |
| Audit log review | Monthly |
