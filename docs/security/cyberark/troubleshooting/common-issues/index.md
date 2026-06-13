---
tags:
  - security
  - troubleshooting
---
# CyberArk — Common Issues


<div class="kb-summary">
Known issues and resolution steps for frequent CyberArk problems, covering the Vault, PVWA, PSM, and CPM components.
</div>
```text
┌────────────────────────── Security Cyberark Troubleshooting — Common Issues ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Cyberark common issues: quick-reference for frequently encountered problems          │   │
│   │         Issues: path failures, connectivity errors, capacity alerts, and auth failures        │   │
│   │         For each issue: symptoms, root cause, diagnostic steps, and resolution actions        │   │
│   │           Escalate to vendor support if the issue persists after standard procedures          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify symptom → check logs → diagnose root cause → resolve → verify                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Cyberark Troubleshooting infrastructure · management network · monitoring       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Cyberark           = Security Cyberark Troubleshooting platform overview and core concepts         │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Vault Issues

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Vault service fails to start | CorVault.exe crash or locked DR file | Check Windows Event Log and `vault.log` under `C:\Program Files (x86)\PrivateArk\Server\Logs`; verify the Vault license has not expired |
| "ITATS006E" — Vault locked out | Too many failed login attempts from a Vault user account | Unlock the user via PrivateArk Client: `Tools > Administrative Tools > Users and Groups`; review source of repeated failures |
| Vault DR replication lag | Network interruption between Primary and DR Vault | Check `PADR.log` on the DR host; confirm the DR user password matches and the replication service is running |
| Safe ownership mismatch after restore | Backup restored to a different Vault with different internal user IDs | Re-assign Safe Owners via PrivateArk Client after restore; do not rely on SID-based ownership across Vault instances |
| Vault cannot connect to external LDAP | Certificate CN mismatch or LDAPS port blocked | Verify `vault.ini` LDAP settings; confirm port 636 is reachable from the Vault server; check the LDAP server certificate SAN |

## PVWA Issues

| Symptom | Likely Cause | Resolution |
|---|---|---|
| PVWA returns HTTP 500 on login | IIS application pool crash or missing Vault connectivity | Restart the `CyberArk Vault` IIS app pool; check `C:\CyberArk\Password Vault Web Access\Logs\WebApplication.log` for exception detail |
| "Vault is not responding" banner | PVWA lost TCP connection to the Vault on port 1858 | Confirm firewall rules; test with `telnet <vault-ip> 1858`; check Vault service status |
| MFA not prompting for LDAP users | RADIUS integration misconfigured or LDAP bind failing | Verify PVWA `web.config` RADIUS settings; confirm the Vault LDAP directory integration user can bind to AD |
| Session timeout too aggressive | Default `InactivityTimeout` in `web.config` set too low | Adjust `InactivityTimeout` parameter in `C:\CyberArk\Password Vault Web Access\web.config`; redeploy/recycle app pool |
| PVWA certificate error in browser | Self-signed or expired IIS cert | Replace the IIS site binding certificate; ensure the issuing CA is trusted by end-user browsers or the enterprise trust store |

## PSM Issues

| Symptom | Likely Cause | Resolution |
|---|---|---|
| PSM connection fails with "No available connections" | PSM connection components at maximum concurrent sessions | Increase `MaxConcurrentConnections` in `C:\Program Files\CyberArk\PSM\Hardening\PSMHardening.ps1` output policies; or scale out PSM nodes |
| RDP session launches but disconnects immediately | Windows RDP licensing not activated on PSM host | Activate the Remote Desktop Services CAL on the PSM Windows Server; apply through the RD Licensing Manager |
| PSM recording files not appearing in PVWA | PSMRecordings Safe permission issue or storage path misconfigured | Confirm the PSM App user has `Add Files` and `List Files` on the PSMRecordings Safe; verify `PSM.ini` `RecordingsPath` |
| Session recording playback is corrupted | Disk full on PSM recording partition | Free space on the PSM recording disk; purge old recordings per retention policy; extend the volume if needed |
| Privileged account password is not auto-changed after PSM session | CPM exclusion list or reconcile account not configured | Check the platform's CPM settings; ensure the account has a reconcile account configured if the target requires elevated rights to change passwords |

## CPM Issues

| Symptom | Likely Cause | Resolution |
|---|---|---|
| CPM fails to change Windows domain account password | CPM machine account lacks sufficient AD permissions | Grant the CPM service account `Reset Password` rights on the target OU in Active Directory |
| "APPAP007E" — CPM cannot connect to target | Network block or wrong address in account properties | Verify network connectivity from the CPM host; confirm the `Address` field on the account record matches the reachable hostname/IP |
| Password change succeeds but application still fails auth | Platform's `ChangeNotificationService` not configured | Configure the change notification plugin for the application type (e.g., IIS app pool, Windows service) in the platform settings |
| CPM stuck in "Change In Process" state | A previous change attempt left the account locked | Use PVWA to manually unlock the account on the target system; then trigger a CPM `Change` from PVWA |
| SSH key rotation fails for Unix accounts | SSH key method not enabled in the Unix platform | Enable `PerformPeriodicChange` and set the SSH key method in the platform's `Automatic Password Management` settings |

## General / Cross-Component Issues

| Symptom | Likely Cause | Resolution |
|---|---|---|
| CyberArk components not visible in syslog / SIEM | Syslog forwarding not configured in Vault | Configure `SYSLOG` section in `vault.ini` with the SIEM IP and port; restart the Vault service |
| Accounts duplicated after HR feed | CyberArk Privileged Access Manager provisioning rules matching too broadly | Narrow the Provisioner search filter in the directory mapping; enable duplicate detection in the provisioning workflow |
| License capacity warning | Too many active Vault users or too many managed accounts | Run the license report from PrivateArk Client; deactivate stale users; archive unmanaged accounts |
