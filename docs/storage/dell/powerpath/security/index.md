# PowerPath Security
## Hardening Checklist

- [ ] Install PowerPath only on hosts that have a valid support contract and license; do not run unlicensed instances (paths show as `unlic` and are unmanaged)
- [ ] Restrict `powermt` CLI access to root / administrators only — PowerPath configuration changes can cause I/O disruption if misused
- [ ] On Linux, ensure the PowerPath configuration file (`/etc/powermt.custom` or equivalent) has permissions `600` owned by root
- [ ] Keep PowerPath version current — outdated versions may have kernel compatibility issues that can cause I/O errors or kernel panics
- [ ] Verify DM-Multipath is blacklisting Dell/EMC devices to prevent dual management of the same path (see Integration section)
- [ ] Include PowerPath host configuration in the host hardening baseline audit; confirm no unauthorised policy changes after maintenance windows
- [ ] Run `powermt check_registration` after any OS upgrade or license renewal; an expired license causes paths to become `unlic` and is not automatically alerted

## RBAC

PowerPath does not have its own RBAC system — access control is delegated entirely to the host OS.

| Role | OS Mechanism | PowerPath Access |
|---|---|---|
| Storage Admin | root (Linux) / Local Administrator (Windows) | Full `powermt` access — can change policy, config, save |
| Server Admin | Standard OS admin account | Read-only view via `powermt display` (requires root on Linux for most commands) |
| Read-only monitoring | Non-privileged user | Limited; `powermt display` may require sudo on Linux |
| Automation service account | Dedicated service account with sudo for `powermt` commands only | Configure via `/etc/sudoers` with specific command allowlist |

Recommended sudoers entry for a monitoring service account on Linux:

```
svc-monitoring ALL=(root) NOPASSWD: /usr/sbin/powermt display dev=all, /usr/sbin/powermt display ports class=all, /usr/sbin/powermt check_registration
```

## Encryption

PowerPath operates at the block I/O layer and does not encrypt data in transit between the host and array. Encryption at this layer is handled by:

- **Array-side encryption**: PowerMax, Unity, and PowerStore provide AES-256 encryption at rest on the array; PowerPath is transparent to this
- **Host-side encryption**: Use OS-level encryption (dm-crypt/LUKS on Linux, BitLocker on Windows) on top of the PowerPath pseudo device if host-side encryption is required
- **FC fabric encryption**: Some FC switch vendors (Brocade, Cisco MDS) offer in-flight FC frame encryption; PowerPath is transparent to this

## Audit Logging

PowerPath does not generate its own audit log, but path state changes are written to the OS syslog. Capture these for operational visibility:

- **Linux**: Events logged to `/var/log/messages` or `journalctl` under the `kernel` facility; keywords include `emcp`, `PowerPath`, `dead path`, `path restored`
- **Windows**: Events logged to the Windows Event Log under the PowerPath source; forward via Windows Event Forwarding to a SIEM
- **AIX**: Events logged to `/var/adm/ras/errlog`; use `errpt` to review

Log `powermt check_registration` and `powermt save` operations as part of any change management process — these are the two highest-impact administrative actions.

## Compliance

PowerPath itself is not a compliance boundary, but as a host-side component it is in scope for:

| Framework | Consideration |
|---|---|
| CIS Benchmarks (OS level) | Ensure PowerPath kernel module and config files have correct permissions per OS hardening guide |
| PCI DSS | PowerPath hosts in the CDE must have access controls, patching (version currency), and audit logging per PCI requirements |
| Change management | Any `powermt set policy` or `powermt config` operation should be performed within an approved change window and documented |
