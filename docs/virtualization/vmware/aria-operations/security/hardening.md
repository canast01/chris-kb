---
tags:
  - aria-operations
  - security
  - vmware
---
# Aria Operations Security Hardening
![Aria Operations Security Hardening](../../../../assets/virtualization-vmware-aria-operations-security-hardening.svg)


```bash
# Verify current certificate subject and expiry
echo | openssl s_client -connect vrops-prod-01.example.local:443 2>/dev/null | \
  openssl x509 -noout -subject -dates -issuer

# Confirm it is self-signed (Issuer == Subject)
```

```bash
# Limit SSH access to the management network
# Edit /etc/hosts.allow on the Aria Operations appliance
echo "sshd: 10.0.1.0/24" >> /etc/hosts.allow
echo "ALL: ALL" >> /etc/hosts.deny

# Disable root password login (prefer key-based)
# Edit /etc/ssh/sshd_config
PermitRootLogin prohibit-password
systemctl restart sshd
```
```bash
# Configure syslog forwarding from Aria Operations appliance
cat >> /etc/rsyslog.d/vrops-remote.conf << 'EOF'
*.* @@vrli-prod-01.example.local:514
EOF
systemctl restart rsyslog
```
```bash
# View authentication and admin action logs on the appliance
tail -f /data/vcops/log/casa.log | grep -i "login\|logout\|admin\|role"
```

```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "Aria Operations Core" {shape: hexagon}

external -> perimeter_controls: traffic in
perimeter_controls -> identity_access
identity_access -> audit_logging
audit_logging -> core: secured path
```

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## See also

- [Aria Operations — Access Control](access-control/)
- [Aria Operations — Authentication](authentication/)
- [Aria Operations Health Checks](../operations/health-checks/)
