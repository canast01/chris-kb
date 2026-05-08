# ESXi — Hardening

## Hardening Checklist

Apply the following controls to every ESXi host before placing it in production. Use host profiles to enforce these settings consistently across the cluster.

| Control | Command / Action | Notes |
|---|---|---|
| Enable Lockdown Mode (Normal) | vCenter > host > Configure > Security Profile > Lockdown Mode | Restricts direct host access |
| Disable SSH when not in use | `esxcli system ssh set --enabled false` | Re-enable only for break-glass |
| Disable ESXi Shell | vCenter > host > Configure > Security Profile > ESXi Shell | Or via DCUI |
| Configure NTP | `esxcli system ntp set --server=ntp1.example.com --enabled=true` | Time sync required for certificates and logs |
| Restrict management access | `esxcli network firewall ruleset set --ruleset-id=sshServer --allowed-all=false` | Limit to admin subnet |
| Enable UEFI Secure Boot | Set in BIOS/UEFI firmware before ESXi install | Prevents unsigned bootloader |
| Remove default self-signed cert | Replace with CA-signed cert via vCenter | Required for production |
| Disable unused services | Review running services | Minimise attack surface |

## Lockdown Mode

Lockdown Mode prevents direct host access and forces all configuration through vCenter.

**Normal Lockdown:**
- DCUI accessible for local console access
- vCenter API access permitted
- SSH disabled but can be temporarily re-enabled via DCUI for break-glass

**Strict Lockdown:**
- DCUI disabled
- All access must go through vCenter
- Use only in environments with highly available vCenter

**Exception Users List:**

```bash
# Add via vCenter: host > Configure > Security Profile > Lockdown Mode > Exception Users
vim-cmd hostsvc/advopt/view Config.HostAgent.plugins.hostsvc.esxAdminsGroup
```

Exception users should be named, individual accounts — not shared credentials — and access should be logged.

## Firewall

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

Minimum required rulesets: `vpxHeartbeats`, `ntpClient`, `syslog`, `vSANTransport`. Disable all others.

## Audit Logging

| Log File | Content |
|---|---|
| `/var/log/auth.log` | Authentication events |
| `/var/log/hostd.log` | Host daemon events, API calls |
| `/var/log/shell.log` | ESXi Shell commands |
| `/var/log/vpxa.log` | vCenter agent communication |

All logs should be forwarded to a central SIEM via syslog. Logs are stored in ramdisk and lost on reboot without forwarding.

## Secure Boot

```bash
/usr/lib/vmware/secureboot/bin/secureBoot.py -s
```

Output should show `Enabled` for production hosts.
