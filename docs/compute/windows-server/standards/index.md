# Windows Server — Standards
## Hostname Convention

Format: `<env>-<function>-<nn>`

| Segment | Values | Example |
|---------|--------|---------|
| env | prod, preprod, uat, dev, dr | prod |
| function | dc, sql, web, app, fs, jump, mgmt | sql |
| nn | 01–99 (zero-padded) | 01 |

Examples:

- `prod-sql-01` — Production SQL Server node 1
- `prod-dc-01` — Production Domain Controller 1
- `dev-web-01` — Development web server
- `dr-sql-01` — DR SQL Server

## Active Directory OU Structure

```
domain.local
└── Servers
    ├── Production
    │   ├── SQL
    │   ├── Web
    │   ├── AppServers
    │   └── DomainControllers
    ├── PreProd
    │   └── ...
    ├── Development
    │   └── ...
    └── Management
        ├── JumpServers
        └── MonitoringServers
```

All servers must be placed in the correct OU before applying GPOs. Computer accounts should not remain in the default `Computers` container.

## Drive Letter Conventions

| Drive | Purpose | Notes |
|-------|---------|-------|
| C: | Operating system | Minimum 100 GB; OS and program files only |
| D: | Data / application files | Size based on workload |
| E: | Logs | Application and IIS logs |
| T: | TempDB (SQL Server) | High-IOPS volume; separate spindle or tier |
| X: | Backup staging | Optional; separate from data |

## PowerShell Remoting

PowerShell remoting (WinRM) must be enabled on all managed servers:

```powershell
# Enable PowerShell remoting
Enable-PSRemoting -Force

# Verify WinRM is running
Get-Service WinRM

# Test remote connectivity
Test-WSMan -ComputerName <servername>

# Connect remotely
Enter-PSSession -ComputerName <servername> -Credential (Get-Credential)
```

WinRM listener configuration:

```powershell
# View WinRM listeners
winrm enumerate winrm/config/listener

# Configure HTTPS listener (requires certificate)
New-WSManInstance -ResourceURI winrm/config/Listener `
  -SelectorSet @{Address="*"; Transport="HTTPS"} `
  -ValueSet @{Hostname="<fqdn>"; CertificateThumbprint="<thumbprint>"}
```

## WinRM Configuration Baseline

| Setting | Required Value |
|---------|---------------|
| Service startup type | Automatic |
| HTTP listener | Enabled (or HTTPS only in high-security environments) |
| MaxEnvelopeSizekb | 500 minimum |
| MaxTimeoutms | 60000 minimum |
| Authentication | Negotiate (Kerberos preferred) |
| TrustedHosts | Set to domain FQDN or specific hosts |

## Server Build Baseline Checklist

- [ ] Hostname set per naming convention
- [ ] Joined to correct AD domain and OU
- [ ] Drive layout per conventions above
- [ ] WinRM/PowerShell remoting enabled
- [ ] Windows Update configured (WSUS or Windows Update for Business)
- [ ] Windows Defender enabled and updated
- [ ] NTP configured (domain-joined servers sync from DC hierarchy)
- [ ] Local Administrator account renamed or disabled; LAPS deployed
- [ ] Remote Desktop enabled; restricted to jump servers via firewall/GPO
- [ ] Monitoring agent installed (Zabbix/Nagios/Datadog)
- [ ] Backup agent installed and job configured
- [ ] Event log sizes configured (System: 64 MB, Application: 64 MB, Security: 256 MB)
- [ ] Page file: system-managed or fixed on dedicated volume
- [ ] Server documented in CMDB

## Group Policy Baseline

All servers must receive the following GPO categories at minimum:

| GPO | Scope |
|-----|-------|
| Security Baseline | All servers |
| Audit Policy | All servers |
| WinRM / PS Remoting | All servers |
| Windows Update | All servers (or managed via WSUS) |
| Defender ATP settings | All servers |
| Role-specific settings | Applied at role-level OUs |

## Related Sections

- [Architecture](../architecture/) — server roles and topology
- [Security](../security/) — hardening and CIS benchmarks
- [Lifecycle](../lifecycle/) — version support and patching cadence
