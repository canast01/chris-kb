---
tags:
  - esxi
  - security
  - vmware
  - vsphere-8
---
# ESXi — Hardening

<div class="kb-summary">
Hardening reference covering Firewall Hardening, Advanced Security Settings, Secure Boot, Audit Logging, Host Profile Enforcement and 2 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>
![ESXi — Hardening](../../../../../assets/virtualization-vmware-esxi-security-hardening.svg)

ESXi Host Hardening Layers

Configure via vCenter: **Host → Configure → Security Profile → Lockdown Mode → Exception Users**

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Firewall Hardening

```bash
# Check firewall is enabled
esxcli network firewall get
# Expected: Enabled: true, Default Action: DROP

# List all rulesets and their state
esxcli network firewall ruleset list

# Show allowed IPs for a specific ruleset
esxcli network firewall ruleset allowedip list --ruleset-id sshServer

# Restrict SSH access to admin subnet
esxcli network firewall ruleset set --ruleset-id sshServer --allowed-all false
esxcli network firewall ruleset allowedip add --ruleset-id sshServer --ip-address 10.0.1.0/24

# Restrict vSphere Client access
esxcli network firewall ruleset set --ruleset-id webAccess --allowed-all false
esxcli network firewall ruleset allowedip add --ruleset-id webAccess --ip-address 10.0.1.0/24

# Disable unused rulesets (examples)
esxcli network firewall ruleset set --enabled false --ruleset-id ftpClient
esxcli network firewall ruleset set --enabled false --ruleset-id ftpServer
```


```text title="Expected output"
Enabled: true
Default Action: DROP

Name                    Enabled  Ports  Protocols  Direction  Stateless
----------              -------  -----  ---------  ---------  ---------
sshServer               true     22     tcp        inbound    false
webAccess               true     443    tcp        inbound    false
webClient               true     443    tcp        inbound    false
vpxHeartbeats           true     902    tcp        inbound    false
ftpClient               true     20,21  tcp        outbound   false
ftpServer               true     20,21  tcp        inbound    false
...

Ruleset: sshServer
  Allowed IP Addresses: 0.0.0.0/0

(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Unknown option or malformed command line.`** — Verify the ruleset ID exists by running `esxcli network firewall ruleset list` and use the exact name from the "Name" column.
    **`Error: Invalid IP address or CIDR notation.`** — Ensure the IP address is in valid CIDR format (e.g., 10.0.1.0/24) and rerun the allowedip add command.
### Minimum Required Rulesets

| Ruleset | Port | Required For |
|---|---|---|
| `vpxHeartbeats` | TCP 80 | vCenter HA heartbeat |
| `vSphereClient` | TCP 443, 902 | vCenter API and management |
| `ntpClient` | UDP 123 | NTP time sync |
| `syslog` | UDP/TCP 514 | Log forwarding |
| `DHCPv6` | — | Disable if not using IPv6 |
| `vSANTransport` | Various | vSAN cluster traffic (if vSAN enabled) |

Disable all rulesets not in the above list.

---

## Advanced Security Settings

Configure via `esxcli system settings advanced set` or via Host Profile.

| Setting | Recommended Value | ESXCLI Option Path |
|---|---|---|
| Shell idle timeout | 600 seconds | `/UserVars/ESXiShellTimeOut` |
| Shell interactive timeout | 300 seconds | `/UserVars/ESXiShellInteractiveTimeOut` |
| Failed login lockout threshold | 5 attempts | `/Security/AccountLockFailures` |
| Account unlock time | 900 seconds (15 min) | `/Security/AccountUnlockTime` |
| Login banner | Legal warning text | `/Config/Etc/issue` |
| Suppress hyperthreading warning | false | (Leave unset) |

```bash
# Apply security settings
esxcli system settings advanced set -o /UserVars/ESXiShellTimeOut -i 600
esxcli system settings advanced set -o /UserVars/ESXiShellInteractiveTimeOut -i 300
esxcli system settings advanced set -o /Security/AccountLockFailures -i 5
esxcli system settings advanced set -o /Security/AccountUnlockTime -i 900
esxcli system settings advanced set -o /Config/Etc/issue \
  -s "AUTHORISED USERS ONLY. Unauthorised access to this system is prohibited."

# Verify
esxcli system settings advanced get -o /Security/AccountLockFailures
esxcli system settings advanced get -o /UserVars/ESXiShellTimeOut
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
   Integer Value: 5
   Default Value: 0
   Configured Value: 5
   Integer Value: 600
   Default Value: 0
   Configured Value: 600
```

!!! warning "Common errors"
    **`Error: Unknown option /Security/AccountLockFailures`** — Verify the exact parameter name with `esxcli system settings advanced list | grep -i lock` as option names are case-sensitive and vary by ESXi version.
    **`Error: Could not connect to the host`** — Ensure you are connected to the ESXi host via SSH or that the esxcli command is being run directly on the host with proper authentication.
---

## Secure Boot

UEFI Secure Boot verifies the bootloader and VIBs are signed by VMware before loading. It prevents unsigned kernel modules from running.

```bash
# Verify Secure Boot is active
/usr/lib/vmware/secureboot/bin/secureBoot.py -s
# Expected: Enabled

# Detailed check
/usr/lib/vmware/secureboot/bin/secureBoot.py --status
```


```text title="Expected output"
Secure Boot Status: Enabled
UEFI Firmware: Version 2.4.1
Secure Boot Mode: Strict
Platform Key (PK): Installed
Key Exchange Key (KEK): Installed
Database (db): 4 signatures loaded
Forbidden Database (dbx): 127 revoked hashes
Last Updated: 2024-01-15 14:32:18 UTC
Compliance: UEFI 2.8 Specification
```

!!! warning "Common errors"
    **`secureBoot.py: command not found`** — Verify the ESXi version supports Secure Boot (6.7+) and the secureboot module is installed with `esxcli software vib list | grep secureboot`.
    **`Permission denied`** — Run the command with root privileges using `sudo` or ensure your user account has administrative permissions on the ESXi host.
    **`Secure Boot Status: Disabled`** — Enable Secure Boot in the ESXi host's BIOS/UEFI firmware settings, then reboot the host for changes to take effect.
If Secure Boot reports `Disabled`, check the server BIOS/UEFI settings. Secure Boot must be enabled before installing ESXi — it cannot be turned on retroactively on a running host without a clean installation.

VIB acceptance levels must be VMwareCertified or VMwareAccepted when Secure Boot is enabled — CommunitySupported and PartnerSupported VIBs are rejected:

```bash
esxcli software acceptance get
# Must return: VMwareCertified or VMwareAccepted (not CommunitySupported)
```


```text title="Expected output"
VMwareCertified
```

!!! warning "Common errors"
    **`Unknown command or namespace software.acceptance.get`** — Verify you are running this command on an ESXi host with SSH enabled and proper ESXCLI access; this command requires ESXi 5.0 or later.
    **`Permission denied`** — Ensure your user account has Administrator privileges on the ESXi host or is part of a role with Host.Config.Settings permission.
---

## Audit Logging

All ESXi security-relevant events must be forwarded off-host. Logs are stored in ramdisk and are **lost on reboot** without syslog forwarding.

| Log | Path | Security-Relevant Content |
|---|---|---|
| auth.log | `/var/log/auth.log` | SSH logins, PAM failures |
| shell.log | `/var/log/shell.log` | ESXi Shell commands |
| hostd.log | `/var/log/hostd.log` | API calls, vCenter agent actions |
| vobd.log | `/var/log/vobd.log` | DCUI logins, hardware events |

### Configure Syslog Forwarding

```bash
# Configure syslog target
esxcli system syslog config set --loghost="tcp://syslog.example.local:514"

# Multiple targets
esxcli system syslog config set \
  --loghost="tcp://syslog1.example.local:514,udp://syslog2.example.local:514"

# Apply config
esxcli system syslog reload

# Verify
esxcli system syslog config get
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
Loghost: tcp://syslog.example.local:514,udp://syslog2.example.local:514
LogLevel: info
QueueDropMark: 90
Datastore: [] /scratch/log
DefaultRotate: 10
DefaultSize: 1024
```

!!! warning "Common errors"
    **`Error: Unknown option --loghost`** — Use `esxcli system syslog config set --loghost=` syntax without spaces around the equals sign.
    **`Error: Unable to resolve hostname syslog.example.local`** — Verify DNS resolution on the ESXi host with `nslookup syslog.example.local` and ensure the syslog server hostname is reachable.
    **`Error: Connection refused to syslog server`** — Confirm the syslog daemon is running on the target server and listening on port 514 with `netstat -tuln | grep 514`.
Configure via Host Profile to apply uniformly across all cluster hosts.

---

## Host Profile Enforcement

Host Profiles enforce the security baseline across all cluster hosts. Deviations are reported as non-compliant.

Security settings captured in a Host Profile:
- SSH and ESXi Shell service state and startup policy
- Firewall ruleset state and allowed IPs
- Advanced settings (shell timeout, lockout thresholds, banner text)
- NTP configuration
- Syslog target
- VIB acceptance level
- Lockdown mode

```powershell
# Create a host profile from the hardened reference host
New-VMHostProfile -Name "Cluster-Security-Profile" \
    -ReferenceHost (Get-VMHost "esxi-01.example.local") \
    -Description "Production security baseline — v1.2"

# Attach profile to all hosts in cluster
Get-Cluster "CL-PROD" | Get-VMHost | ForEach-Object {
    Set-VMHost -VMHost $_ -Profile (Get-VMHostProfile "Cluster-Security-Profile")
}

# Check compliance — identify drifted hosts
Get-Cluster "CL-PROD" | Get-VMHost | ForEach-Object {
    Test-VMHostProfileCompliance -VMHost $_ |
        Where-Object {$_.ComplianceStatus -ne "Compliant"} |
        Select-Object VMHost, ComplianceStatus, IncomplianceDescription
}
```

Run **Check Compliance** after every change to a host. Non-compliant hosts should be remediated within the change window.

---

## VIB Acceptance Level Policy

ESXi enforces VIB (driver/plugin) signing requirements through acceptance levels:

| Level | Signing | Production Use |
|---|---|---|
| VMwareCertified | VMware tested and certified | Approved |
| VMwareAccepted | Partner signed; VMware accepted | Approved |
| PartnerSupported | Vendor signed only | Review case-by-case |
| CommunitySupported | No signing | Not in production |

Enforce minimum acceptance level:

```bash
# Check current acceptance level
esxcli software acceptance get

# Set minimum to VMwareAccepted
esxcli software acceptance set --level=VMwareAccepted

# List all installed VIBs and their acceptance level
esxcli software vib list | awk '{print $1, $4}' | sort
```


```text title="Expected output"
Acceptance Level: CommunitySupported
(no output — command completes silently)
esx-ui VMwareAccepted
esx-vsan VMwareAccepted
lsi-mr3 VMwareAccepted
net-bnx2 VMwareAccepted
net-e1000 VMwareAccepted
net-ixgbe VMwareAccepted
sata-ahci VMwareAccepted
...
```

!!! warning "Common errors"
    **`Error: Unknown option or flag '--level=VMwareAccepted'`** — Use the correct syntax `esxcli software acceptance set --level VMwareAccepted` (space instead of equals sign).
    **`Error: Access denied`** — Run the command with root privileges or ensure your user account has Administrator role on the ESXi host.
Any VIB with `CommunitySupported` acceptance level in production should be removed or replaced with a supported alternative.

---

## TPM 2.0 and Attestation

vSphere 7.0+ supports TPM 2.0 host attestation, which verifies the ESXi host's boot measurements have not changed since the last known-good state.

Requirements:
- Physical TPM 2.0 chip in the server
- UEFI Secure Boot enabled
- vSphere Trust Authority (optional — adds attestation enforcement)

```bash
# Check TPM status from ESXi Shell
esxcli system settings advanced get -o /UserVars/TpmBiosDeviceEnabled

# View TPM details
cat /var/run/tpm/tpminfo.json 2>/dev/null
```


```text title="Expected output"
Value of IntOption /UserVars/TpmBiosDeviceEnabled is 1
{
  "tpm_version": "2.0",
  "tpm_device": "/dev/tpm0",
  "tpm_enabled": true,
  "manufacturer": "IFX",
  "firmware_version": "7.63.3144.0",
  "pcr_banks": ["sha1", "sha256"],
  "last_measured": "2024-01-15T09:42:17Z"
}
```

!!! warning "Common errors"
    **`cat: /var/run/tpm/tpminfo.json: No such file or directory`** — TPM is not enabled or not present on this host; verify with `esxcli system settings advanced get -o /UserVars/TpmBiosDeviceEnabled` that TPM is set to 1.
    **`Value of IntOption /UserVars/TpmBiosDeviceEnabled is 0`** — TPM is disabled in BIOS or ESXi settings; enable it in the host's BIOS firmware setup or use `esxcli system settings advanced set -o /UserVars/TpmBiosDeviceEnabled -i 1` and reboot.
View in vCenter: **Host → Configure → System → TPM**

If TPM attestation fails, investigate recent firmware or BIOS changes. A failed attestation indicates the host's boot chain has changed — investigate before trusting the host.

## See also

- [ESXi Access Control](../access-control/)
- [ESXi — Authentication](../authentication/)
- [ESXi — Health Checks](../../operations/health-checks/)
