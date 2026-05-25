# RecoverPoint — Hardening

> Part of the [RecoverPoint](../../index.md) > [Security](../index.md) reference.

---

## Hardening Checklist

| Control | Standard | Action |
|---|---|---|
| **Root login disabled** | SSH root login off | Confirm `PermitRootLogin no` in `/etc/ssh/sshd_config` on each RPA node. Use named admin accounts and `sudo` for privileged operations. |
| **SSH access restriction** | Management jump hosts only | Restrict SSH to the management VLAN and specific jump host IPs using the RecoverPoint CLI: `set_system_ssh_restrictions -allow <jump_host_ip>/32`. Deny SSH from general server VLANs. |
| **SSH idle session timeout** | 10 minutes | Set `TMOUT=600` in `/etc/profile` on each RPA node to enforce automatic session termination after 10 minutes of inactivity. |
| **SSH host key documentation** | CMDB entry per RPA | Record SSH host key fingerprints for each RPA node in the CMDB. Validate fingerprints after any RPA replacement or OS-level rebuild to detect unauthorised key changes. |
| **Admin account control** | Named accounts only | Create individual named admin accounts for each administrator. Remove or disable the default `admin` account after initial setup. Enforce a minimum 16-character password with complexity requirements. |
| **Admin password rotation** | Every 90 days | Rotate all RecoverPoint admin account passwords on a 90-day cycle. Store credentials in a secrets vault. Do not reuse passwords across accounts or systems. |
| **RPA network isolation** | Dedicated replication VLAN | Place RPA replication interfaces on a dedicated replication VLAN, separate from management and production data VLANs. Apply ACLs to permit only inter-site RPA traffic on replication ports (TCP 2049, 7225, and 11111). |
| **Replication traffic encryption** | WAN Encryption enabled | Enable WAN Encryption on journal-to-journal replication links traversing untrusted networks (internet WAN, shared MPLS). RecoverPoint uses AES-256 for replication traffic encryption when this feature is active. Verify the setting under System > WAN Encryption in Unisphere for RecoverPoint. |
| **API access control** | Service accounts only | Use dedicated service accounts for any integration with the RecoverPoint REST API or Unisphere for RecoverPoint. Assign the minimum required role (Monitor where read-only access suffices). Rotate API credentials every 90 days. |
| **Certificate management** | Trusted CA-signed certificates | Replace the default self-signed certificate on the Unisphere for RecoverPoint management interface with a certificate signed by your internal CA or a trusted public CA. Document the certificate expiry date and set a renewal reminder at 60 days before expiry. |
| **Audit log configuration** | Remote syslog enabled | Configure RecoverPoint to forward audit logs to a centralised syslog server or SIEM. Review logs monthly for unexpected login attempts, configuration changes, and replication policy modifications. Retain logs for a minimum of 90 days. |
| **Unisphere for RecoverPoint access** | HTTPS only, restricted IPs | Ensure Unisphere for RecoverPoint is only accessible over HTTPS (TLS 1.2+). Restrict access to the management VLAN. If the environment supports IP-based access control at the load balancer or firewall level, allowlist only administrator workstations and jump hosts. |
| **Firmware and software currency** | Current supported release | Apply RecoverPoint software updates within 90 days of general availability. Critical security patches should be applied within 30 days. Track the RecoverPoint release notes for security-relevant changes. |
| **Consistency group access** | Least-privilege role per team** | Assign RecoverPoint roles (Admin, Operator, Monitor) at the consistency group level where possible. Do not grant site-wide Admin to teams that only manage specific applications. |

## Network Port Reference

| Port | Protocol | Direction | Purpose |
|---|---|---|---|
| TCP 443 | HTTPS | Inbound to RPA cluster | Unisphere for RecoverPoint management |
| TCP 22 | SSH | Inbound to RPA (restricted) | CLI administration from jump hosts |
| TCP 2049 | TCP | Inter-site RPA | Journal replication |
| TCP 7225 | TCP | Inter-site RPA | RecoverPoint communication |
| TCP 11111 | TCP | Inter-site RPA | RecoverPoint communication |

All other inbound connections to RPA nodes should be denied by perimeter and internal firewall policy.
