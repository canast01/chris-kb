---
tags:
  - security
---
# Security Audit Procedure

<div class="kb-summary">
Security Audit Procedure reference covering Audit Types, Scope Definition, Configuration Audit Checks, Patch Compliance Check, Vulnerability Scan Review and 3 more sections.
</div>

<div class="kb-grid">
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Audit types, configuration checks, evidence collection, findings documentation</div>
  </a>
</div>

## Audit Types

| Type | Frequency | Scope |
|---|---|---|
| Internal configuration audit | Quarterly | Server hardening, patch levels, access controls |
| Access review audit | Quarterly / semi-annual | User and service account permissions |
| Vulnerability scan review | Monthly | Open findings from scan tools |
| Log audit | Monthly | Audit log completeness and retention |
| Backup / DR audit | Semi-annual | Backup job success, restore test records |
| External / penetration test | Annual | Infrastructure and application scope |

## Scope Definition

Before starting, document:
- **In scope:** specific systems, environments, or controls being reviewed
- **Out of scope:** explicitly excluded systems
- **Reference standard:** ISO 27001 Annex A / CIS Controls / PCI-DSS Requirement X
- **Reviewer:** internal or third-party auditor

## Configuration Audit Checks

**Linux server hardening:**
```bash
# SSH hardening
grep -E "^PermitRootLogin|^PasswordAuthentication|^Protocol|^MaxAuthTries" /etc/ssh/sshd_config

# Password policy
cat /etc/security/pwquality.conf
grep -E "^PASS_MAX_DAYS|^PASS_MIN_DAYS|^PASS_MIN_LEN" /etc/login.defs

# Firewall active
systemctl is-active firewalld || systemctl is-active ufw

# Auditd running
systemctl is-active auditd

# SUID/SGID files (unexpected ones are a finding)
find / -perm /6000 -type f -not -path "/proc/*" 2>/dev/null | sort
```

**Windows server hardening:**
```powershell
# Audit policy settings
auditpol /get /category:*

# Password policy
Get-ADDefaultDomainPasswordPolicy | Select-Object MinPasswordLength, PasswordHistoryCount, MaxPasswordAge, LockoutThreshold

# SMBv1 disabled
Get-SmbServerConfiguration | Select-Object EnableSMB1Protocol

# RDP settings
Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections

# Local administrators group membership
Get-LocalGroupMember -Group "Administrators"
```

## Patch Compliance Check

```bash
# RHEL/CentOS — list available security updates
yum check-update --security 2>/dev/null | grep -v "^$"

# Ubuntu/Debian
apt list --upgradable 2>/dev/null | grep -i security
```

```powershell
# Windows — missing updates
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10

# Or query WSUS/Windows Update
(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0 and Type='Software' and IsHidden=0").Updates |
  Select-Object Title, MsrcSeverity
```

## Vulnerability Scan Review

```bash
# Example: pull Nessus / Tenable findings via API (requires API key)
curl -k -X GET "https://<scanner>/scans/<scan_id>/hosts" \
  -H "X-ApiKey: accessKey=<ak>;secretKey=<sk>" | jq '.hosts[] | {hostname,score,critical,high}'
```

Review cadence:
- **Critical findings** — remediate within 15 days
- **High findings** — remediate within 30 days
- **Medium findings** — remediate within 90 days

## Audit Evidence Collection

| Control | Evidence | Command / Location |
|---|---|---|
| SSH root login disabled | sshd_config export | `grep PermitRootLogin /etc/ssh/sshd_config` |
| MFA enforced | Azure AD Conditional Access policy export | Azure Portal → Entra ID → Security → Conditional Access |
| Privileged access audited | Event log exports (4624, 4728) | Windows Event Log → Security |
| Encryption at rest | Storage config screenshot / export | Array vendor console |
| Patch levels | Patch scan report | Vulnerability scanner |

## Findings Documentation

```markdown
Finding ID:      AUDIT-2026-001
Severity:        High
Control:         CIS Control 4 — Controlled Use of Admin Privileges
Description:     Three user accounts have Domain Admin rights with no documented business justification.
Evidence:        Get-ADGroupMember output — see attachment
Risk:            Excessive privilege increases blast radius of credential compromise
Remediation:     Remove unjustified Domain Admin memberships; document approval for remaining
Owner:           IT Operations
Due Date:        2026-06-01
Status:          Open
```

## Audit Close-Out Checklist

- [ ] All in-scope systems reviewed
- [ ] Findings documented with severity, evidence, and owner
- [ ] Critical and High findings acknowledged by system owners
- [ ] Remediation timeline agreed and tracked in ITSM
- [ ] Audit report drafted and reviewed
- [ ] Exceptions documented with risk acceptance sign-off
- [ ] Report distributed to management and stored in audit archive
