# RASR — Hardening


<div class="kb-summary">
Hardening the RASR recovery environment: storage array management plane, iDRAC, recovery media, and the management hosts used to operate RASR.
</div>

## Hardening Scope

RASR hardening covers four areas:

1. **Dell EMC storage array management plane** — Unisphere, API access, and management network.
2. **iDRAC (server management)** — Out-of-band access used during recovery boot sequences.
3. **Recovery management hosts** — Linux or Windows servers used to run RASR CLI tools and scripts.
4. **Recovery media** — USB drives, PXE images, ISO files used to boot recovery environments.

## Storage Array Management Plane Hardening

### Unisphere Hardening

```bash
# Disable unused management interfaces
# Only HTTPS (443) should be allowed for web management
uemcli /sys/setting set -mgmtInterface https

# Set session inactivity timeout (seconds)
uemcli /sys/setting set -sessionTimeout 900   # 15 minutes

# Disable Telnet and other unencrypted management protocols
uemcli /sys/security set -telnetEnabled false

# Require SNMPv3 only (disable SNMPv1/v2)
uemcli /sys/snmp set -version 3

# Configure SNMPv3 with authentication and privacy
uemcli /sys/snmp set \
  -authProto SHA \
  -authPasswd "AuthPassphrase123!" \
  -privProto AES \
  -privPasswd "PrivPassphrase456!"

# Set banner / MOTD for management access
uemcli /sys/setting set -loginBanner "Authorised access only. All sessions are logged."

# View current security settings
uemcli /sys/security show
uemcli /sys/setting show
```
┌────────────────────────────────────────── RASR — Hardening ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   RASR — Hardening Checklist                                  │   │
│   │               [ ] Disable default/admin accounts; create named admin accounts only            │   │
│   │                   [ ] Enable MFA for all interactive logins via IdP / SAML SSO                │   │
│   │        [ ] Restrict management port (443 (PPDM REST API)) to jump host / management VLAN      │   │
│   │               [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)            │   │
│   │                 [ ] Apply all security patches within 30 days of vendor release               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Network Hardening                                       │   │
│   │               [ ] Separate backup VLAN — no direct production host access to repo             │   │
│   │       [ ] Firewall: allow only 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)     │   │
│   │                  [ ] Disable unused ports and protocols on management interface               │   │
│   │              [ ] Immutable repository: enable WORM or object lock on backup target            │   │
│   │                 [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────────────── RASR — Hardening ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   RASR — Hardening Checklist                                  │   │
│   │               [ ] Disable default/admin accounts; create named admin accounts only            │   │
│   │                   [ ] Enable MFA for all interactive logins via IdP / SAML SSO                │   │
│   │        [ ] Restrict management port (443 (PPDM REST API)) to jump host / management VLAN      │   │
│   │               [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)            │   │
│   │                 [ ] Apply all security patches within 30 days of vendor release               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Network Hardening                                       │   │
│   │               [ ] Separate backup VLAN — no direct production host access to repo             │   │
│   │       [ ] Firewall: allow only 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)     │   │
│   │                  [ ] Disable unused ports and protocols on management interface               │   │
│   │              [ ] Immutable repository: enable WORM or object lock on backup target            │   │
│   │                 [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## iDRAC Hardening

### Baseline iDRAC Configuration

```bash
# Disable unused management protocols
racadm set iDRAC.IPMILan.Enable 0          # Disable IPMI over LAN (use iDRAC interface instead)
racadm set iDRAC.Telnet.Enable 0           # Disable Telnet
racadm set iDRAC.Serial.Enable 0           # Disable serial console if not needed

# Force HTTPS only (redirect HTTP to HTTPS)
racadm set iDRAC.WebServer.HttpsRedirect 1

# Set minimum TLS version
racadm set iDRAC.WebServer.TLSProtocol TLS1_2

# Set session timeout (seconds)
racadm set iDRAC.WebServer.Timeout 900

# Disable unused USB ports (prevent booting from rogue media)
racadm set iDRAC.Usb.ManagementPortMode Disabled

# Enable iDRAC lockdown mode (restricts configuration changes without iDRAC admin auth)
racadm set iDRAC.Lockdown.SystemLockdown Enabled

# Set login banner
racadm set iDRAC.WebServer.LoginBanner "Authorised personnel only. All sessions logged."

# Verify settings
racadm get iDRAC.WebServer
racadm get iDRAC.IPMILan
```

### iDRAC Alert Configuration

```bash
# Configure SNMP trap destination for iDRAC alerts
racadm set iDRAC.SNMPTrapIPv4.Address 10.10.20.5   # SNMP trap receiver
racadm set iDRAC.SNMP.AgentEnable 1

# Configure email alerts for critical events
racadm set iDRAC.EmailAlert.1.Enable 1
racadm set iDRAC.EmailAlert.1.Address "dr-alerts@corp.local"
racadm set iDRAC.RemoteHosts.SMTPServerIPAddress smtp.example.local

# Enable alerts for hardware failures and power events
racadm alertcfg -g system -s enabled
```

### iDRAC Firmware

```bash
# Check iDRAC firmware version
racadm getversion

# Verify against Dell security advisories
# Download firmware from Dell support; verify checksum before applying
racadm update -f /tmp/iDRAC-firmware.EXE -u 1   # -u 1 = update after upload
```

## Recovery Management Host Hardening

The Linux or Windows hosts used to run RASR CLI tools and scripts are privileged systems and must be hardened equivalently to Tier-0 infrastructure.

### Linux Management Host

```bash
# Apply standard Linux hardening (see Linux Hardening page)
# Additional RASR-specific controls:

# Restrict SSH access to DR management host — key-based only, from jump host
# /etc/ssh/sshd_config:
PermitRootLogin no
PasswordAuthentication no
AllowGroups dr-operators
ListenAddress 10.10.20.10   # Management interface only

# Restrict who can run RASR CLI tools using sudo
# /etc/sudoers.d/rasr-operators
%dr-operators  ALL=(root) /usr/local/bin/uemcli, /usr/bin/racadm, /opt/rasr/bin/rasr-cli

# Audit all RASR tool invocations
# /etc/audit/rules.d/rasr.rules
-w /usr/local/bin/uemcli -p x -k rasr_mgmt
-w /usr/bin/racadm -p x -k rasr_mgmt
-w /opt/rasr/bin/ -p x -k rasr_mgmt

augenrules --load

# Restrict access to RASR credential files
chmod 600 /etc/rasr/credentials.conf
chown root:dr-operators /etc/rasr/credentials.conf
```

### Windows Management Host

```powershell
# Enable PowerShell script block logging for RASR management host
$path = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"
New-Item -Path $path -Force
Set-ItemProperty -Path $path -Name "EnableScriptBlockLogging" -Value 1

# Enable PowerShell transcription to a central log share
$tPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription"
New-Item -Path $tPath -Force
Set-ItemProperty -Path $tPath -Name "EnableTranscripting" -Value 1
Set-ItemProperty -Path $tPath -Name "OutputDirectory" -Value "\\logserver\rasr-transcripts"

# AppLocker — restrict which tools can run on the management host
# Allow only approved RASR management executables
Get-AppLockerPolicy -Local | Format-List

# Constrained Language Mode for non-admin PowerShell sessions
# Enforce via AppLocker or WDAC policy

# Restrict RDP to the management host — DR operators only, from jump host
New-NetFirewallRule -DisplayName "RDP - Jump Host Only" `
  -Direction Inbound -Protocol TCP -LocalPort 3389 `
  -RemoteAddress 10.10.20.1 -Action Allow
```

## Recovery Media Hardening

### USB Media Hardening

```bash
# Verify recovery USB is created from a trusted source (SHA-256 check)
sha256sum rasr-recovery-image.iso
# Compare against vendor-published hash

# Scan recovery USB for malware before use
clamscan --recursive /mnt/rasr-usb/

# After use, securely wipe the staging area
shred -vzn 3 /mnt/rasr-stage/*
```

### PXE Boot Environment Hardening

```yaml
PXE-based RASR recovery hardening:
- DHCP option 67 (bootfile) served only to authorised MAC addresses
- TFTP server access restricted by IP source (management VLAN only)
- PXE image signed and verified via Secure Boot
- PXE recovery environment has no writable network shares outside of the recovery target
- PXE boot triggers an alert to the DR team (iDRAC alert on next boot device = PXE)
```

```bash
# Restrict TFTP to management VLAN (dnsmasq example)
# /etc/dnsmasq.conf
bind-interfaces
interface=eth1   # Management interface only
dhcp-range=10.10.20.100,10.10.20.200,12h

# /etc/hosts.allow — restrict TFTP access
in.tftpd: 10.10.20.

# /etc/hosts.deny
in.tftpd: ALL
```

## Logging and Monitoring

All RASR-related operations must generate immutable audit logs.

```bash
# Forward array management logs to centralised SIEM
# Unity — configure syslog forwarding
uemcli /sys/log/syslog create \
  -address siem.example.local \
  -port 514 \
  -protocol UDP \
  -facility local0

# iDRAC — configure syslog
racadm set iDRAC.SysLog.SysLogEnable 1
racadm set iDRAC.SysLog.Server1 siem.example.local
racadm set iDRAC.SysLog.Port1 514

# Linux management host — forward auditd logs
# /etc/rsyslog.d/90-rasr-audit.conf
if $programname == "audit" then @@siem.example.local:514
& ~

systemctl restart rsyslog

# Verify syslog forwarding is working
logger -t rasr "Test log entry from management host"
# Check SIEM for receipt
```

### Monitoring Alerts

| Event | Alert Trigger | Severity |
|---|---|---|
| Failed Unisphere login (5+ in 10 min) | SIEM correlation rule | High |
| iDRAC login from unexpected IP | SIEM geo/IP rule | High |
| RASR recovery initiated | All recovery initiations | Medium |
| Recovery USB access (iDRAC virtual media mount) | iDRAC audit event | Medium |
| Array firmware change | Unisphere configuration change event | High |
| KMIP key server unreachable | Array health alert | Critical |
| Replication lag > threshold | Unity performance alert | High |

## Hardening Verification Checklist

```bash
# Array management
uemcli /sys/security show | grep -E "telnet|http|session"
uemcli /sys/setting show | grep -E "timeout|banner"

# iDRAC
racadm get iDRAC.WebServer | grep -E "TLS|Timeout|HttpsRedirect"
racadm get iDRAC.IPMILan | grep Enable

# Management host (Linux)
sshd -T | grep -E "permitroot|passwordauth|allowgroups"
auditctl -l | grep rasr
systemctl is-active rsyslog

# Verify logs flowing to SIEM (send test and confirm receipt)
logger -t rasr "Hardening verification test"

# Check no default/weak accounts on array
uemcli /user show | grep -E "admin|root|default"

# Verify encryption on array
uemcli /sys/security/encryption show | grep "Encryption status"
```

## Quick Reference

| Topic | Command / Setting |
|---|---|
| Array session timeout | `uemcli /sys/setting set -sessionTimeout 900` |
| Array syslog forwarding | `uemcli /sys/log/syslog create -address siem.example.local` |
| Disable iDRAC IPMI | `racadm set iDRAC.IPMILan.Enable 0` |
| iDRAC TLS minimum | `racadm set iDRAC.WebServer.TLSProtocol TLS1_2` |
| iDRAC lockdown mode | `racadm set iDRAC.Lockdown.SystemLockdown Enabled` |
| iDRAC syslog | `racadm set iDRAC.SysLog.SysLogEnable 1` |
| Management host audit | `augenrules --load` after adding rules to `/etc/audit/rules.d/rasr.rules` |
| PowerShell logging (Windows) | `EnableScriptBlockLogging = 1` in registry |
| Recovery USB verification | `sha256sum <image>` before use |
| PXE restriction | DHCP + TFTP restricted to management VLAN |
