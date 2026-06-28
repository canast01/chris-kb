---
tags:
  - san
  - security
---
# Brocade SANnav — Security Hardening
![Brocade SANnav — Security Hardening](../../../../assets/san-brocade-sannav-security-hardening.svg)

```bash
# SSH to SANnav appliance
ssh admin@sannav-dc1.corp.example.com

# Change default admin password immediately after deployment
passwd admin
# Use a password that meets the corporate complexity policy (20+ characters)
# Store in vault; treat as break-glass

# Change default OS root password (if accessible)
sudo passwd root
```

```bash
sudo vi /etc/ssh/sshd_config

# Recommended settings:
Protocol 2
PermitRootLogin no
PasswordAuthentication yes     # or 'no' if using SSH key auth
PubkeyAuthentication yes
PermitEmptyPasswords no
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300        # disconnect idle sessions after 5 minutes
ClientAliveCountMax 2
X11Forwarding no
AllowTcpForwarding no
AllowUsers admin sannav        # restrict SSH to specific local accounts

sudo systemctl restart sshd

# Verify
sudo sshd -T | grep -E "permitrootlogin|passwordauthentication|protocol|maxauthtries"
```
```bash
# Check for available security updates
sudo yum updateinfo list security

# Apply security patches only (does not touch SANnav application packages)
sudo yum update --security -y

# Verify SANnav services still running after OS update
sannav status
```
```bash
# Check NTP synchronization
timedatectl status
# Expected: "synchronized: yes", NTP service active

# If not synchronized, configure NTP
sudo vi /etc/chrony.conf
# Add: server 10.10.0.10 prefer
#       server 10.10.0.11

sudo systemctl enable --now chronyd
chronyc tracking
# Expected: Reference ID should match your NTP server, offset < 1ms
```
```text
WARNING: This system is for authorized use only.
All connections are monitored and recorded.
Unauthorized access or use is prohibited and may be subject to legal action.
```
```bash
sudo vi /etc/issue.net
# Add:
# WARNING: Authorized access only. All activities are monitored and logged.

sudo vi /etc/ssh/sshd_config
# Banner /etc/issue.net
sudo systemctl restart sshd
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Sannav — Authentication](../authentication/)
- [Sannav — Access Control](../access-control/)
- [Sannav — Encryption](../encryption/)
