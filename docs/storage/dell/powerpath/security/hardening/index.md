# PowerPath — Hardening

```text
┌────────────────────────────────── Dell PowerPath Security Hardening ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Hardening: restrict powermt to named accounts via sudo; protect config and license files   │   │
│   │   Binary integrity: verify PowerPath RPM/DEB signature before install; use Dell repo GPG key  │   │
│   │          Config file /etc/powermt.custom: perms root:root 600; no group or world read         │   │
│   │        Disable unused features: unused emulations should be removed from powermt config       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Verify package signature → restrict CLI → protect config file → enable audit → review monthly      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         OS Hardening        │  │       Config Hardening      │  │       Audit Hardening       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Named sudo only       │  │        powermt.custom       │  │         auditd rule         │   │
│   │        No shared root       │  │          Perms 600          │  │         SIEM forward        │   │
│   │       Package GPG sig       │  │        Remove unused        │  │        Monthly review       │   │
│   │       MFA for storage       │  │       License protect       │  │          Change log         │   │
│   │       SELinux context       │  │        Minimal emul.        │  │       Integrity check       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Harden OS → restrict config file perms → audit all powermt commands → alert on anomaly             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │    Hardening     │      Action      │      Standard     │   Verify with    │ Risk if skipped  │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    CLI access    │    Named sudo    │   No shared root  │  sudo -l output  │   Uncontrolled   │   │
│   │   Config file    │    chmod 600     │   root:root only  │   ls -la /etc    │   Config leak    │   │
│   │     Package      │    GPG verify    │  Dell signed RPM  │   rpm --verify   │ Tampered binary  │   │
│   │      Audit       │   auditd rule    │     All execve    │     ausearch     │     No trail     │   │
│                                                                                                       │
│    Physical: /sbin/powermt binary root-owned; /etc/powermt.custom 600; auditd rule on /sbin           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    GPG signature  = Dell signs PowerPath packages; verify with rpm --checksig or dpkg verify          │
│    powermt.custom = Persisted config file; world-readable allows path policy enumeration              │
│    Named sudo     = Individual storage admin accounts with specific sudo rule for powermt only        │
│    SELinux context= AppArmor/SELinux policy for PowerPath binary and config file access               │
│    Minimal emul.  = Remove unused array emulations from powermt config to reduce attack surface       │
│    auditd rule    = /etc/audit/rules.d entry: -w /sbin/powermt -p x -k powerpath_exec                 │
│    ausearch       = auditd log query tool: ausearch -k powerpath_exec to review executions            │
│    Integrity check= Periodic rpm --verify on PowerPath package to detect binary modification          │
│    SIEM           = Security Information and Event Management; ingest auditd events for alerting      │
│    License protect= Store registration key file with 600 perms; do not commit to version control      │
│    Uncontrolled   = Risk when shared root used; any user with root can modify path policy silently    │
│    Change log     = Record of every powermt policy or config change; tied to CR number                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Hardening Checklist

- [ ] Install PowerPath only on hosts that have a valid support contract and license; do not run unlicensed instances (paths show as `unlic` and are unmanaged)
- [ ] Restrict `powermt` CLI access to root / administrators only — PowerPath configuration changes can cause I/O disruption if misused
- [ ] On Linux, ensure the PowerPath configuration file (`/etc/powermt.custom` or equivalent) has permissions `600` owned by root
- [ ] Keep PowerPath version current — outdated versions may have kernel compatibility issues that can cause I/O errors or kernel panics
- [ ] Verify DM-Multipath is blacklisting Dell/EMC devices to prevent dual management of the same path (see Integration section)
- [ ] Include PowerPath host configuration in the host hardening baseline audit; confirm no unauthorised policy changes after maintenance windows
- [ ] Run `powermt check_registration` after any OS upgrade or license renewal; an expired license causes paths to become `unlic` and is not automatically alerted

## Compliance

PowerPath itself is not a compliance boundary, but as a host-side component it is in scope for:

| Framework | Consideration |
|---|---|
| CIS Benchmarks (OS level) | Ensure PowerPath kernel module and config files have correct permissions per OS hardening guide |
| PCI DSS | PowerPath hosts in the CDE must have access controls, patching (version currency), and audit logging per PCI requirements |
| Change management | Any `powermt set policy` or `powermt config` operation should be performed within an approved change window and documented |
