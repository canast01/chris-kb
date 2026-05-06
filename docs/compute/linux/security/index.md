# Linux Security

All Linux servers are hardened to CIS Benchmark Level 1 at provisioning using an Ansible hardening role. SSH is restricted to key-based authentication with `PermitRootLogin no` and only approved ciphers/MACs. Sudo access is granted via AD group membership with `NOPASSWD` disabled. `auditd` is configured to log privilege escalation, file access on sensitive paths, and network configuration changes. SELinux is enforced on RHEL; AppArmor profiles are applied on Ubuntu. AIDE is deployed for file integrity monitoring with daily scans.

| Control | Implementation |
|---|---|
| SSH hardening | Key-only, `PermitRootLogin no`, restricted ciphers |
| Sudo policy | AD group-based, no `NOPASSWD` for privileged ops |
| Audit logging | `auditd` with CIS ruleset |
| MAC | SELinux (RHEL), AppArmor (Ubuntu) |
| Firewall | `firewalld` zones (RHEL), `ufw` (Ubuntu) |
| File integrity | AIDE daily baseline scan |
| Password policy | PAM `pam_pwquality` — min 12 chars, complexity enforced |
