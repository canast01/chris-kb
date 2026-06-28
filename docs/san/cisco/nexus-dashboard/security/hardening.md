---
tags:
  - san
  - security
---
# Cisco Nexus Dashboard — Security Hardening
![Cisco Nexus Dashboard — Security Hardening](../../../../assets/san-cisco-nexus-dashboard-security-hardening.svg)


```bash
# SSH to the ND cluster
ssh ndadmin@nd-dc1-1.corp.example.com

# Change the default admin password (via GUI: Admin Console > Security > Users > admin)
# For ndadmin OS account on the appliance, change password:
passwd ndadmin
# Use a password meeting corporate complexity policy (20+ characters)
# Store in vault; treat as break-glass
```

```text
   WARNING: This system is for authorized use only.
   All connections are monitored and recorded.
   Unauthorized access is prohibited and may result in legal action.
```
   ```text
3. Click **Save**. The banner appears below the login form.

---

```d2
direction: down

external: External / Untrusted {shape: rectangle}
7_backup_encryption: "7. Backup Encryption" {shape: rectangle}
8_audit_logging: "8. Audit Logging" {shape: rectangle}
9_kubernetes_security_baseline: "9. Kubernetes Security Baseline" {shape: rectangle}
core: "Nexus Dashboard Core" {shape: hexagon}

external -> 7_backup_encryption: traffic in
7_backup_encryption -> 8_audit_logging
8_audit_logging -> 9_kubernetes_security_baseline
9_kubernetes_security_baseline -> core: secured path
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

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
```
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

## See also

- [Nexus Dashboard — Authentication](authentication/)
- [Nexus Dashboard — Access Control](access-control/)
- [Nexus Dashboard — Encryption](encryption/)
