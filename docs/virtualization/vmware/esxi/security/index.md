# VMware ESXi Security

## Hardening Checklist

Apply the following controls to every ESXi host before placing it in production. Use host profiles to enforce these settings consistently across the cluster.

| Control | Command / Action | Notes |
|---|---|---|
| Enable Lockdown Mode (Normal) | vCenter > host > Configure > Security Profile > Lockdown Mode | Restricts direct host access |
| Disable SSH when not in use | `esxcli system ssh set --enabled false` | Re-enable only for break-glass |
| Disable ESXi Shell | vCenter > host > Configure > Security Profile > ESXi Shell | Or via DCUI |
| Set SSH idle timeout | `esxcli system ssh set --permit-user-env=no` | Review SSH advanced settings |
| Configure NTP | `esxcli system ntp set --server=ntp1.example.com --enabled=true` | Time sync required for certificates and logs |
| Restrict management access | `esxcli network firewall ruleset set --ruleset-id=sshServer --allowed-all=false` then add allowed IPs | Limit to admin subnet |
| Enable UEFI Secure Boot | Set in BIOS/UEFI firmware before ESXi install | Prevents unsigned bootloader |
| Remove default self-signed cert | Replace with CA-signed cert via vCenter | Required for production |
| Disable unused services | `esxcli system maintenanceMode` and review running services | Minimise attack surface |

## Lockdown Mode

Lockdown Mode prevents direct host access and forces all configuration through vCenter.

**Normal Lockdown:**

- DCUI (Direct Console UI) is accessible for local console access.
- vCenter API access is permitted.
- SSH is disabled by Lockdown Mode but can be temporarily re-enabled via DCUI for break-glass.

**Strict Lockdown:**

- DCUI is disabled.
- All access must go through vCenter.
- SSH and ESXi Shell cannot be started even from DCUI.
- Use only in environments with highly available vCenter.

**Exception Users List:**

Add break-glass accounts to the exception list so they retain direct host access even when Lockdown Mode is enabled:

```bash
# View exception users
vim-cmd hostsvc/advopt/view Config.HostAgent.plugins.hostsvc.esxAdminsGroup

# Add via vCenter: host > Configure > Security Profile > Lockdown Mode > Exception Users
```

Exception users should be named, individual accounts — not shared credentials — and access should be logged.

## Firewall

ESXi includes a built-in stateless firewall controlling inbound and outbound connections. The firewall is managed per ruleset.

```bash
# Check firewall status
esxcli network firewall get

# List all rulesets
esxcli network firewall ruleset list

# Show allowed IPs for a ruleset
esxcli network firewall ruleset allowedip list --ruleset-id=sshServer

# Restrict a ruleset to specific IPs
esxcli network firewall ruleset set --ruleset-id=sshServer --allowed-all=false
esxcli network firewall ruleset allowedip add --ruleset-id=sshServer --ip-address=10.0.1.0/24
```

**Minimum required rulesets to enable:**

| Ruleset | Purpose |
|---|---|
| vpxHeartbeats | vCenter connectivity |
| ntpClient | NTP sync |
| syslog | Log forwarding |
| vSANTransport | vSAN (if applicable) |
| DHCPv6 | Disable if IPv6 not used |

Disable all rulesets not required by your environment. Review the list after each ESXi upgrade as new rulesets may be added.

## Authentication

**Local users:** Minimise local accounts to root and one named break-glass account. Do not create shared service accounts with local ESXi access.

**Root account:** Set a strong, unique root password per host. Rotate passwords at least annually or after any personnel change. Use a password manager or secrets vault.

```bash
# Set root password via ESXCLI
passwd root
```

**AD authentication:** All administrative access should go through vCenter with Active Directory authentication. Configure vCenter to use AD as the identity source. AD users and groups are assigned roles in vCenter, not directly on ESXi hosts.

**Password policy:** Enforce complexity and history via host profile settings:

- Minimum length: 12 characters
- Complexity: upper, lower, digit, special
- History: last 5 passwords
- Lockout: 5 failed attempts, 15-minute lockout

## Audit Logging

ESXi writes security-relevant events to several log files:

| Log File | Content |
|---|---|
| `/var/log/auth.log` | Authentication events (SSH, local login, sudo) |
| `/var/log/hostd.log` | Host daemon events, API calls, configuration changes |
| `/var/log/shell.log` | ESXi Shell commands executed |
| `/var/log/vpxa.log` | vCenter agent (vpxa) communication |
| `/var/log/vobd.log` | VMkernel observation events |

All logs should be forwarded to a central SIEM via syslog (see Integration > Monitoring Integration for configuration). Logs on ESXi are stored in a ramdisk and lost on reboot unless syslog forwarding is configured to a persistent target.

**Secure Boot for VM integrity:** Enable Secure Boot on ESXi hosts to ensure only signed VIBs and kernel modules are loaded. This prevents unsigned or malicious kernel extensions from being loaded at boot. Verify Secure Boot status:

```bash
/usr/lib/vmware/secureboot/bin/secureBoot.py -s
```

Output should show `Enabled` for production hosts.
