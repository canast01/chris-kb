---
tags:
  - nutanix
  - security
  - hardening
  - cis
description: "CVM OS hardening, AHV hypervisor hardening, Prism Element/Central security configuration, port lockdown, SSL/TLS settings, and Nutanix Security..."
---
# Nutanix — Hardening

<div class="kb-summary">
CVM OS hardening, AHV hypervisor hardening, Prism Element/Central security configuration, port lockdown, SSL/TLS settings, and Nutanix Security Configuration Guide alignment (CIS Nutanix benchmark).

*Applies to: AOS 6.x · AHV*
</div>
![Nutanix — Hardening](../../../assets/virtualization-nutanix-security-hardening.svg)

---

## Before you begin

- **Access:** CVM SSH (nutanix), Prism Element admin
- **Reference:** Nutanix Security Configuration Guide (available from Nutanix Portal — search "SCG") — aligns with STIG/CIS benchmarks
- **Snapshot first:** Take a Prism snapshot of CVMs before making security config changes

---

## CVM Password Policy

```bash
# Check current password policy (Prism Element → Settings → Security → Cluster Lockdown not for password policy)
# Password policy is configured via ncli:
ncli cluster get-password-complexity-policy

# Enforce password complexity
ncli cluster edit-password-complexity-policy \
  enabled=true \
  min-length=14 \
  min-uppercase=1 \
  min-lowercase=1 \
  min-numeric=1 \
  min-special-chars=1 \
  history=6

# Set max password age (days)
ncli cluster edit-password-aging-policy enabled=true max-age=90

# Lock account after failed logins
ncli cluster edit-lockout-policy \
  enabled=true \
  failed-login-attempts=5 \
  lockout-period=30
```


```text title="Expected output"
Password Complexity Policy:
  Enabled: true
  Min Length: 14
  Min Uppercase: 1
  Min Lowercase: 1
  Min Numeric: 1
  Min Special Chars: 1
  History: 6

Password Aging Policy:
  Enabled: true
  Max Age (days): 90

Account Lockout Policy:
  Enabled: true
  Failed Login Attempts: 5
  Lockout Period (minutes): 30
```

!!! warning "Common errors"
    **`Error: Invalid value for failed-login-attempts. Must be between 1 and 10.`** — Reduce the failed-login-attempts value to a maximum of 10 or check your Nutanix version's supported range.
    **`Error: ncli: command not found`** — Ensure you are running this command on a Nutanix cluster node with ncli installed, not a remote management workstation.
    **`Error: Permission denied. User does not have cluster admin privileges.`** — Execute the command as a cluster administrator or use an account with full cluster permissions.
---

## SSH Hardening

### Restrict SSH Access (Cluster Lockdown)

Nutanix Cluster Lockdown disables SSH root access and allows key-only login per approved IP/key list.

```text
Prism Element → Settings → Security → Cluster Lockdown
  Enable Cluster Lockdown: Yes
  Add SSH public keys for each admin user
  Optionally restrict to specific source IPs
```

```bash
# Verify lockdown is enabled via CLI
ncli cluster get-security-config | grep -i lockdown
```


```text title="Expected output"
Lockdown Mode                    : ENABLED
Lockdown Mode Status             : Active
Lockdown Mode Last Modified      : 2024-01-15 14:32:18
```

!!! warning "Common errors"
    **`ncli: command not found`** — Ensure you are logged into a Nutanix cluster node or have the Nutanix CLI tools installed and in your PATH.
    **`Error: Unable to connect to cluster`** — Verify cluster connectivity and that your user account has appropriate permissions to query security configuration.
### CVM SSH Key Management

```bash
# Add an authorized key to all CVMs
allssh "echo 'ssh-rsa AAAA... user@host' >> ~/.ssh/authorized_keys"

# Remove a key (find and delete the specific line)
allssh "sed -i '/user@host/d' ~/.ssh/authorized_keys"

# List current authorized keys
allssh "cat ~/.ssh/authorized_keys"
```


```text title="Expected output"
node-1-cvm: ssh-rsa AAAA...B3Z9 user@host
node-1-cvm: ssh-rsa AAAA...K7M2 admin@bastion
node-2-cvm: ssh-rsa AAAA...B3Z9 user@host
node-2-cvm: ssh-rsa AAAA...K7M2 admin@bastion
node-3-cvm: ssh-rsa AAAA...B3Z9 user@host
node-3-cvm: ssh-rsa AAAA...K7M2 admin@bastion
node-4-cvm: ssh-rsa AAAA...B3Z9 user@host
node-4-cvm: ssh-rsa AAAA...K7M2 admin@bastion
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Verify the CVM SSH service is running with `allssh "systemctl status sshd"` and that your current SSH key is already in authorized_keys.
    **`sed: can't read ~/.ssh/authorized_keys: No such file or directory`** — Create the ~/.ssh directory and authorized_keys file first with `allssh "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"`.
    **`allssh: command not found`** — Ensure you are running this from a Nutanix cluster node or Prism Element host where allssh is available in the PATH.
### SSH Server Config (AHV Hypervisor)

Apply on each AHV host (requires root access — only via Prism Element → Hardware → host console):

```bash
# /etc/ssh/sshd_config recommended settings:
PermitRootLogin no
PasswordAuthentication no
Protocol 2
MaxAuthTries 4
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers nutanix
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`sshd[12345]: error: /etc/ssh/sshd_config line 1: unsupported option "PermitRootLogin no"`** — Ensure you are editing the actual sshd_config file with a text editor (e.g., `sudo nano /etc/ssh/sshd_config`) rather than pasting into the shell directly.
    **`sshd: no hostkeys available -- exiting.`** — Verify SSH host keys exist in `/etc/ssh/` with `ls -la /etc/ssh/ssh_host_*` and regenerate them if missing using `ssh-keygen -A`.
    **`Permission denied (publickey).`** — Confirm the nutanix user has a valid public key in `~nutanix/.ssh/authorized_keys` and restart sshd with `sudo systemctl restart sshd` after making config changes.
---

## TLS / SSL Configuration

```bash
# Check current cipher suite policy
ncli cluster get-ssl-key-config

# Enforce TLS 1.2+ (disable TLS 1.0/1.1)
ncli cluster edit-ssl-key-config \
  key-type=RSA_2048 \
  cluster-certification-chain-key=""  # leave blank to use Nutanix self-signed

# For custom SSL cert (recommended — avoids browser warnings):
# Prism Element → Settings → SSL Certificate → Import Certificate
# Upload your PEM-encoded cert, intermediate chain, and private key
```


```text title="Expected output"
SSL Key Configuration
=====================
Key Type: RSA_2048
Certificate Chain Length: 1
TLS Version Support: TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3
Cipher Suite: DEFAULT
Certificate Expiry: 2025-03-15 14:22:18
Issuer: Nutanix, Inc.

Request ID: 00057d8a-0001-0000-0000-000000003a98
Status: SUCCEEDED

(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Invalid key-type value. Supported types: RSA_2048, RSA_4096`** — Verify the key-type parameter matches one of the supported values exactly.
    **`Error: Certificate chain validation failed: Intermediate certificate not in PEM format`** — Ensure the intermediate certificate is PEM-encoded (-----BEGIN CERTIFICATE-----) and concatenated in the correct order (leaf → intermediate → root).
    **`Error: Private key does not match certificate: Key mismatch detected`** — Confirm the private key file corresponds to the certificate being imported by comparing their modulus values.
---

## Port Exposure Lockdown

Nutanix uses a firewall (iptables on CVM, firewalld on AHV). The key principle is: **only ports listed in the Nutanix Port Reference should be open**.

Key ports that must remain open:

| Port | Protocol | Purpose |
|---|---|---|
| 9440 | TCP | Prism UI (HTTPS) |
| 2009 | TCP | CVM to CVM (inter-cluster replication) |
| 2100 | TCP | CVM to hypervisor |
| 9443 | TCP | Prism Central HTTPS |
| 5988, 5989 | TCP | CIM provider (vCenter) |
| 443 | TCP | HTTPS (outbound to LCM, Insights) |
| 80 | TCP | HTTP (redirect to 443 only) |

```bash
# Review iptables rules on a CVM
sudo iptables -L -n

# Verify AHV firewall
allssh "sudo iptables -L -n -v | grep -E 'DROP|REJECT' | head -20"
```


```text title="Expected output"
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
target     prot opt source               destination         
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:22
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:2009
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:2010
DROP       tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:23
DROP       tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:25
REJECT     tcp  --  192.168.1.50/32      0.0.0.0/0           tcp dpt:3389

Chain FORWARD (policy DROP 0 packets, 0 bytes)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
target     prot opt source               destination         

10.20.30.40: DROP       tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:23
10.20.30.40: DROP       tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:25
10.20.30.41: DROP       tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:23
10.20.30.41: REJECT     tcp  --  172.16.0.0/16       0.0.0.0/0           tcp dpt:3389
10.20.30.42: DROP       tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:25
```

!!! warning "Common errors"
    **`sudo: iptables: command not found`** — Install iptables with `sudo yum install iptables-services` or verify the CVM is running a supported OS.
    **`allssh: command not found`** — Run this command from a Nutanix cluster node where allssh is available in the PATH, or source the Nutanix environment setup script.
---

## Prism Element Security Settings

```text
Prism Element → Settings → Security:

1. HTTP Strict Transport Security (HSTS)
   Enable HSTS for Prism Web Console

2. Cluster Lockdown (SSH management — see above)

3. Data-at-Rest Encryption
   Enable per-container or cluster-wide (see Encryption page)

4. Authentication
   Configure LDAP/AD (see Authentication page)
```

---

## Network Segmentation

- Place **CVM management traffic** on a dedicated management VLAN (IPMI, CVM, AHV management IPs)
- Place **VM traffic** on separate VLANs — never mix VM and CVM management traffic
- Restrict **Prism port 9440** to admin jump hosts only via firewall rules upstream
- Disable **IPMI default credentials** before deploying (change BMC/IPMI password immediately after imaging)

---

## Nutanix Security Dashboard

```text
Prism Central → Security → Security Planning
  Shows STIG/CIS compliance status per cluster
  Identifies deviations from the Security Configuration Guide
  Generates compliance reports

Prism Central → Alerts → Security Alerts
  Monitors for brute force, unusual API access, failed auth, etc.
```

---

## Nutanix Insights (Call-Home)

Nutanix Insights sends cluster health telemetry to Nutanix for proactive support. Review what data is sent before disabling:

```text
Prism Element → Settings → Pulse → Disable Pulse
```

For air-gapped clusters, disable Pulse and LCM dark site mode:

```bash
# Configure LCM dark site (local LCM repository)
# Prism Central → LCM → Settings → Use Dark Site
# Point to your internal LCM mirror URL
```

---

## Hardening Verification Checklist

| Check | Command / Path |
|---|---|
| Cluster Lockdown enabled | Prism → Settings → Security → Cluster Lockdown = On |
| Password complexity policy | `ncli cluster get-password-complexity-policy` |
| Account lockout policy | `ncli cluster edit-lockout-policy` |
| TLS 1.0/1.1 disabled | `ncli cluster get-ssl-key-config` |
| Custom SSL cert installed | Prism → Settings → SSL Certificate |
| Default admin password changed | `ncli user change-password username=admin` |
| IPMI/BMC default password changed | Via each node's IPMI console |
| NCC security checks | `ncc --health_checks run_all` → filter security category |

---

## See also

- [Nutanix — Access Control](../access-control/)
- [Nutanix — Authentication](../authentication/)
- [Nutanix — Health Checks](../../operations/health-checks/)
