# ESXi Access Control

```text
ESXi Access Control Model
┌──────────────────────────────────────────────────────┐
│  vCenter (Primary path — day-to-day operations)      │
│  ├── AD / SSO identity source                        │
│  ├── Role-based permissions propagated to ESXi       │
│  └── Lockdown Mode: blocks all direct host access    │
└──────────────────────┬───────────────────────────────┘
                       │ vpxa / hostd (HTTPS 443/902)
┌──────────────────────▼───────────────────────────────┐
│  ESXi Host                                           │
│                                                      │
│  Lockdown Mode — Normal (recommended)                │
│  ├── SSH: BLOCKED for all except exception users     │
│  ├── API: BLOCKED for direct connections             │
│  ├── DCUI: ACCESSIBLE (local console only)           │
│  └── Exception users: 1 named break-glass account    │
│                                                      │
│  Lockdown Mode — Strict                              │
│  ├── SSH: BLOCKED                                    │
│  ├── DCUI: BLOCKED (no local console)                │
│  └── Only vCenter or IPMI for recovery               │
│                                                      │
│  Local Accounts (keep minimal)                       │
│  ├── root            break-glass, unique password    │
│  └── infra-breakglass  Admin role, in exception list │
└──────────────────────────────────────────────────────┘
         │
    ┌────▼────────────────────────────────┐
    │  Firewall (host-based ruleset)      │
    │  ├── sshServer → admin subnet only  │
    │  ├── vSphereClient → vCenter only   │
    │  ├── ntpClient, syslog → allowed    │
    │  └── All other rulesets → disabled  │
    └─────────────────────────────────────┘
```

## Access Model Overview

ESXi host access is managed through two independent control planes:

| Plane | Mechanism | Normal State |
|---|---|---|
| vCenter-mediated | vCenter roles and permissions → propagated to host | Primary operational path |
| Direct host access | Local ESXi accounts, SSH, DCUI | Disabled in production (lockdown mode) |

The goal is to make vCenter the only administrative interface to ESXi hosts. Direct host access should be reserved for break-glass scenarios.

---

## Lockdown Mode

Lockdown mode is the primary access control mechanism at the ESXi host level. It prevents all direct connections to the host outside of vCenter.

| Mode | Direct SSH | Direct API | DCUI | Exception Users |
|---|---|---|---|---|
| Disabled | Yes | Yes | Yes | Not applicable |
| Normal | No | No | Yes (local console) | Can override |
| Strict | No | No | No | Not applicable (DCUI off) |

### Enable Lockdown Mode

Via vCenter: **Host → Configure → System → Security Profile → Lockdown Mode → Edit**

Via PowerCLI:

```powershell
# Enable Normal Lockdown on all hosts in a cluster
Get-Cluster "CL-PROD" | Get-VMHost | ForEach-Object {
    $_.ExtensionData.EnterLockdownMode()
    Write-Host "Lockdown enabled: $($_.Name)"
}

# Verify
Get-VMHost | Select-Object Name,
    @{N="LockdownMode"; E={$_.ExtensionData.Config.LockdownMode}}
```

Via ESXCLI (must be run from DCUI or existing shell session):

```bash
vim-cmd hostsvc/lockdown_mode_enter
vim-cmd hostsvc/lockdown_mode_exit    # to disable
```

### Exception Users

Exception users in Normal Lockdown can still connect directly to the host via SSH. Keep this list minimal:

- One named break-glass local account
- No shared accounts

Configure via vCenter: **Host → Configure → Security Profile → Exception Users → Add**

### Strict Lockdown Considerations

Use Strict Lockdown only if vCenter is highly available (HA'd appliance or VCF). If vCenter is unavailable in Strict Lockdown, the only recovery path is physical IPMI/iDRAC console access to the DCUI, which itself does not permit root login under Strict Lockdown — a second local account with DCUI access must be pre-configured.

---

## Local Account Management

Minimise local accounts. Production ESXi hosts should have at most two local accounts:

| Account | Purpose | State |
|---|---|---|
| `root` | Primary break-glass | Enabled; strong unique password per host |
| Break-glass named account | Secondary break-glass | Enabled; in exception users list |
| All other accounts | Application-specific (deprecated) | Delete or disable |

### View Local Accounts

```bash
# Via ESXCLI (SSH or shell)
esxcli system account list

# Via vSphere API (PowerCLI)
(Get-VMHost "esxi-01.example.local").ExtensionData.Config.LocalAccountManager.QueryUserList()
```

### Add a Local Account

```bash
esxcli system account add \
  -i "breakglass" \
  -p "Str0ngP@ssw0rd!!" \
  -d "Break-glass account"

# Set role on the account
esxcli system permission set -i "breakglass" -r Admin
```

### Delete an Unused Local Account

```bash
esxcli system account remove -i <username>
```

### Set Root Password

```bash
# Interactively
passwd root

# Via PowerCLI (across all hosts)
Get-VMHost | ForEach-Object {
    $hostObj = $_
    $spec = New-Object VMware.Vim.HostAccountSpec
    $spec.id = "root"
    $spec.password = "NewRootPassword!!"
    $hostObj.ExtensionData.ConfigManager.AccountManager.UpdateUser($spec)
    Write-Host "Root password updated: $($hostObj.Name)"
}
```

---

## vCenter Role-Based Access Control

Roles assigned in vCenter propagate to ESXi hosts — this is the primary access control mechanism for day-to-day operations.

### Standard Role Hierarchy

| vCenter Role | ESXi Permissions | Typical Assignee |
|---|---|---|
| Administrator | Full host access | Named admin users only |
| Read-only | Host monitoring, no changes | NOC, L1 teams |
| VM Operator (custom) | Power ops on VMs only | App team |
| Network Admin (custom) | vSwitch and port group management | Network team |

Create custom roles in vCenter with only the privileges required for the specific use case.

### Assign a Role (PowerCLI)

```powershell
# Create a custom role
New-VIRole -Name "VM-Operator" -Privilege (Get-VIPrivilege "VirtualMachine.Interact.*")

# Assign role to a user on a specific cluster
New-VIPermission -Entity (Get-Cluster "CL-PROD") \
    -Principal "CORP\vm-operators" \
    -Role "VM-Operator" \
    -Propagate $true
```

### Least-Privilege Assignment Checklist

- [ ] No AD accounts assigned the built-in `Administrator` role at the vCenter root level
- [ ] Break-glass `administrator@vsphere.local` account password in vault; not used for daily work
- [ ] Custom roles scoped to specific clusters or objects — not the vCenter root
- [ ] AD group memberships reviewed and documented
- [ ] Service accounts (backup, monitoring) assigned read-only or the minimum required role

---

## ESXi Shell and SSH Access Controls

The ESXi Shell and SSH service provide direct command-line access to the host. Both must be disabled in production and enabled only during maintenance or break-glass.

### Disable Shell and SSH

```bash
# Via ESXCLI on the host
vim-cmd hostsvc/disable_ssh
vim-cmd hostsvc/disable_esx_shell

# Via PowerCLI across a cluster
Get-VMHost | Get-VMHostService | Where-Object {$_.Key -in "TSM-SSH","TSM"} | Stop-VMHostService -Confirm:$false
Get-VMHost | Get-VMHostService | Where-Object {$_.Key -in "TSM-SSH","TSM"} | Set-VMHostService -Policy Off
```

### Set Shell Timeout

If ESXi Shell or SSH must remain enabled temporarily:

```bash
# Shell auto-closes after 10 minutes of inactivity
esxcli system settings advanced set -o /UserVars/ESXiShellTimeOut -i 600

# Interactive shell sessions timeout after 5 minutes
esxcli system settings advanced set -o /UserVars/ESXiShellInteractiveTimeOut -i 300
```

### Restrict SSH Access by IP

Use the ESXi built-in firewall to limit SSH access to specific source IPs:

```bash
esxcli network firewall ruleset set --ruleset-id sshServer --allowed-all false
esxcli network firewall ruleset allowedip add --ruleset-id sshServer --ip-address 10.0.1.0/24

# Verify
esxcli network firewall ruleset allowedip list --ruleset-id sshServer
```

---

## Firewall Ruleset Management

ESXi's host-based firewall controls which services are accessible and from which source IPs.

### Review Current State

```bash
# All rulesets and their state
esxcli network firewall ruleset list

# Specific ruleset detail
esxcli network firewall ruleset get --ruleset-id sshServer
esxcli network firewall ruleset get --ruleset-id webAccess
esxcli network firewall ruleset get --ruleset-id vSphereClient
```

### Minimum Required Rulesets (Production)

| Ruleset | Port | Required For |
|---|---|---|
| `vpxHeartbeats` | TCP 80 | vCenter HA heartbeat |
| `vSphereClient` | TCP 443, 902 | vCenter API access |
| `ntpClient` | UDP 123 | NTP outbound |
| `syslog` | UDP/TCP 514 | Log forwarding |
| `vSANTransport` | TCP/UDP various | vSAN if enabled |
| `CIMHttpsServer` | TCP 5989 | Hardware monitoring (if CIM used) |

All other rulesets (FTP, telnet, etc.) should be disabled:

```bash
# Disable an unused ruleset
esxcli network firewall ruleset set --enabled false --ruleset-id ftpClient
```

### Host Profile Enforcement

Firewall ruleset configuration is captured in Host Profiles. Changes on individual hosts that drift from the profile are flagged as non-compliant. Use **Check Compliance** after any firewall change to confirm the host profile still matches.

---

## Auditing ESXi Access Events

### Key Log Files for Access Events

| Log | Path | Content |
|---|---|---|
| auth.log | `/var/log/auth.log` | SSH logins, PAM authentication |
| shell.log | `/var/log/shell.log` | Commands entered in ESXi Shell |
| hostd.log | `/var/log/hostd.log` | API calls, vCenter agent actions |
| vobd.log | `/var/log/vobd.log` | DCUI logins, hardware events |

```bash
# Find all SSH login events (successful and failed)
grep -i "sshd\|Accepted\|Failed\|Invalid" /var/log/auth.log | tail -30

# Find shell commands executed
grep -i "exec\|cmd" /var/log/shell.log | tail -20

# Find DCUI logins
grep -i "dcui\|login" /var/log/vobd.log | tail -20
```

### Syslog Forwarding

All access events must be forwarded to a central SIEM. Logs stored only in ESXi ramdisk are lost on reboot.

```bash
# Configure syslog forwarding
esxcli system syslog config set --loghost="tcp://syslog.example.local:514"
esxcli system syslog reload

# Verify
esxcli system syslog config get | grep loghost
```

Configure via Host Profile to enforce consistently across all cluster hosts.
