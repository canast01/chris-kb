---
tags:
  - dell
  - security
---
# RecoverPoint — Hardening


<div class="kb-summary">
Hardening reference covering Hardening Checklist, Network Port Reference.
</div>

```text
┌────────────────────────────────────── RecoverPoint — Hardening ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               RecoverPoint — Hardening Checklist                              │   │
│   │               [ ] Disable default/admin accounts; create named admin accounts only            │   │
│   │                   [ ] Enable MFA for all interactive logins via IdP / SAML SSO                │   │
│   │          [ ] Restrict management port (443 (mgmt HTTPS)) to jump host / management VLAN       │   │
│   │               [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)            │   │
│   │                 [ ] Apply all security patches within 30 days of vendor release               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Network Hardening                                       │   │
│   │               [ ] Separate backup VLAN — no direct production host access to repo             │   │
│   │         [ ] Firewall: allow only 443 (mgmt HTTPS) · 2222 (RPA SSH) · 8888 (splitter API)      │   │
│   │                  [ ] Disable unused ports and protocols on management interface               │   │
│   │              [ ] Immutable repository: enable WORM or object lock on backup target            │   │
│   │                 [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites           │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication          │
│  Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA                  │
│  Journal       = write-order-consistent storage capturing all writes for point-in-time access         │
│  Consistency Group= set of volumes protected together; writes are applied in order across all         │
│  Bookmark      = named marker in journal; enables deterministic recovery to a known state             │
│  Image Access  = mounting a journal point-in-time image to a host for testing or recovery             │
│  Failover      = activating the replica at the recovery site; breaks replication relationship         │
│  Test Copy     = non-disruptive image access for validation without breaking replication              │
│  RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero          │
│  RTO           = Recovery Time Objective; time from failover to service restored                      │
│  Reverse       = after failover, replicates from recovery site back to re-sync production             │
│  Splitter Lag  = delay between host write and journal commit; monitor for replication health          │
│  CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps          │
│  Distributed CG= consistency group spanning volumes on multiple storage arrays                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [RecoverPoint](../../index.md) > [Security](../index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

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
