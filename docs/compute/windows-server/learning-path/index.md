---
tags:
  - learning-path
  - windows
---
# Windows Server — Learning Path

<div class="kb-summary">
Recommended reading order for Windows Server administration. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌─────────────────────────────────── Windows Server — Learning Path ────────────────────────────────────┐
│                                                                                                       │
│    5 stages in order: Architecture → Deploy → Operations → Security → Troubleshoot                    │
│                                                                                                       │
│   ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│   │  Architecture  │  │     Deploy     │  │    Operations   │  │    Security    │  │  Troubleshoot  │ │
│   │                │  │                │  │                 │  │                │  │                │ │
│   │  How It Works  │  │ Initial Setup  │  │  Health Checks  │  │ Access Control │  │ Common Issues  │ │
│   │Design Standards│  │Install/Upgrade │  │  CLI Reference  │  │ Authentication │  │  Diagnostics   │ │
│   │  Integrations  │  │                │  │    Procedures   │  │   Encryption   │  │   Escalation   │ │
│   │                │  │                │  │ Backup & Restore│  │   Hardening    │  │                │ │
│   │                │  │                │  │     Scripts     │  │                │  │                │ │
│   └────────────────┘  └────────────────┘  └─────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                                                       │
│    Stage 1 (Architecture) builds understanding. Stage 3 (Operations) is daily work. Troubleshoot last.│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | SCM, Registry, Group Policy, storage stack | 4–5 h |
| 2 — Deployment | WDS/MDT, Sysprep, unattend.xml, GPO application | 2–3 h |
| 3 — Operations | Event Viewer, PowerShell, WSUS, backup | ongoing |
| 4 — Security | LAPS, BitLocker, WinRM TLS, Defender | 3–4 h |
| 5 — Troubleshooting | Event logs, WinPE, ProcMon, BSOD analysis | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand Windows Server's core subsystems — the service control manager, storage stack, networking model, and how Group Policy applies configuration from domain to machine to user.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — boot sequence (UEFI → Windows Boot Manager → `winload.efi` → kernel → Session Manager → service control manager → Winlogon), the service control manager (SCM) dependency model, Windows Registry hive structure (`HKLM`, `HKCU`, `HKU`, `HKCR`), and the NT object namespace (`\Device\`, `\BaseNamedObjects\`)
- [Design Standards](../architecture/design-standards/) — server role placement decisions (member server vs domain controller, separate roles per server), Storage Spaces pool and volume naming, network adapter teaming standards for HA, and Server Core vs Desktop Experience selection criteria
- [Integrations](../architecture/integrations/) — Active Directory domain join and GPO linkage for configuration management, WSUS for centralised update approval and deployment, WinRM and PowerShell remoting for automation, and iSCSI initiator for SAN storage

**Key concepts before moving on**:

- Services have dependency relationships managed by the SCM — if a dependency service fails to start, dependent services will also fail, sometimes silently
- Group Policy applies in LSDOU order (Local → Site → Domain → OU) with later policies winning unless enforced — understanding this is essential before creating any new GPO
- WinRM (Windows Remote Management) is the transport for PowerShell remoting — it must be explicitly enabled (`Enable-PSRemoting`) and configured with the correct listener (HTTP or HTTPS)
- Windows does not have a single unified log like `syslog` — events are distributed across System, Application, Security, and application-specific event logs in Event Viewer

**Why first**: Windows Server's Group Policy and service dependency model mean configuration errors cascade. Understanding the architecture before making changes prevents hard-to-reverse GPO side effects and service startup failures.

---

## Stage 2 — Deployment

**Goal**: Deploy Windows Servers repeatably using WDS/MDT or cloud images with baseline configuration baked in before they join the domain.

**Read**:

- [Deploy](../deploy/) — WDS image capture and deployment, MDT task sequence configuration for unattended install (`unattend.xml`), Sysprep generalisation for image capture, and post-deploy domain join with automatic OU placement and GPO application
- [Install & Upgrade](../operations/install-upgrade/) — Windows Server in-place upgrade procedure (Server 2016 → 2019 → 2022), WSUS approval workflow for cumulative updates and feature updates, and offline cumulative update installation via DISM for air-gapped environments

**Deployment principles**:

- Sysprep removes machine-specific identifiers (SID, computer name, hardware profile) — always Sysprep before capturing a reference image for deployment
- Set a meaningful computer name in `unattend.xml` using a naming convention — renaming after domain join requires a second reboot and can break Kerberos SPNs
- Apply the security baseline GPO (Microsoft Security Compliance Toolkit) to new servers before opening them to network traffic

---

## Stage 3 — Operations

**Goal**: Keep Windows Servers healthy — monitoring services, event logs, storage, and update compliance on every shift.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; `Get-Service | Where-Object Status -eq Stopped` for unexpected stopped services, `Get-WinEvent -LogName System -Level 2 -MaxEvents 20` for errors, `Get-PSDrive C` for disk space, `Get-HotFix` for last patch date, and WSUS compliance dashboard
- [CLI Reference](../operations/cli-reference/) — `Get-Service`, `Start-Service`, `Get-EventLog`, `Get-WinEvent`, `Get-Process`, `Get-HotFix`, `netstat -ano`, `ipconfig /all`, `netsh winsock reset`, `diskpart`, `sfc /scannow`, and `Repair-Volume -DriveLetter C -Scan`
- [Procedures](../operations/procedures/) — service restart with dependency order check, Storage Spaces volume extension, iSCSI initiator new target connection, scheduled task creation and monitoring, and Windows Update manual installation
- [Backup & Restore](../operations/backup-restore/) — `wbadmin start backup` for Windows Server Backup, VSS shadow copy schedule for application-consistent snapshots, System State backup for domain controller recovery, and bare-metal recovery via `wbadmin start sysrecovery`
- [Scripts](../operations/scripts/) — PowerShell scripts for Event Log critical error alerting, service watchdog with auto-restart and alert on repeated failure, disk space threshold alerting, WSUS compliance report, and scheduled task health check

**Daily rhythm**: Stopped services check → critical Event Log errors → disk space → WSUS patch compliance → backup job status.

---

## Stage 4 — Security

**Goal**: Enforce least-privilege administration, keep systems patched, and audit all privileged access end to end.

**Read**:

- [Access Control](../security/access-control/) — local Administrator account restrictions (rename, disable, or LAPS-manage), LAPS (Local Administrator Password Solution) deployment for unique managed passwords, User Account Control (UAC) elevation prompts and `SeDebugPrivilege` auditing, and `Protected Users` group for high-privilege accounts
- [Authentication](../security/authentication/) — WinRM HTTPS listener configuration with a certificate, Credential Guard for protecting LSASS from Pass-the-Hash, and Protected Users security group membership for service accounts to prevent Kerberos delegation abuse
- [Encryption](../security/encryption/) — BitLocker volume encryption with TPM + PIN protector, recovery key escrow to Active Directory or Azure AD, TLS configuration for WinRM HTTPS (disable TLS 1.0/1.1 via registry/GPO), and EFS for individual file encryption where applicable
- [Hardening](../security/hardening/) — Windows Firewall inbound rule baseline (allow only required ports per role), SMB signing enforcement via GPO (`RequireSecuritySignature`), NTLMv2-only policy (`LAN Manager Authentication Level = Send NTLMv2 response only, refuse LM & NTLM`), and Windows Defender Antivirus with real-time protection enforced via GPO

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose Windows Server failures — service crashes, blue screens, network connectivity, and storage issues — using built-in and Sysinternals tooling.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — service fails to start (dependency or binary missing — check Event ID 7034/7038), BSOD STOP error analysis (minidump via WinDbg), GPO not applying (security group filter, WMI filter, replication lag), iSCSI disconnects (iSCSI initiator reconnect timer), and disk not initialised after hot-add
- [Diagnostics](../troubleshooting/diagnostics/) — Event Viewer System and Application log filtering by Level=Error and Source, `Get-WinEvent` with `-FilterHashtable`, Windows Memory Diagnostic (`mdsched.exe`), WinPE boot for offline `sfc /scannow` and `chkdsk`, ProcMon for process file and registry activity, and `netsh winsock reset` + `netsh int ip reset` for network stack corruption
- [Escalation](../troubleshooting/escalation/) — Microsoft CSS Support case creation with `msinfo32` export, `ProcDump -ma lsass.exe` for LSASS crash capture, Sysinternals Process Explorer and Autoruns for malware investigation, and hardware vendor escalation for STOP errors caused by driver or hardware failures

**Why last**: Troubleshooting makes most sense once you understand the Windows boot sequence, service dependency model, and what healthy Event Viewer output looks like for the roles running on the server.
