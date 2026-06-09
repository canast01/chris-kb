# PowerCLI — Authentication

<div class="kb-summary">
PowerCLI authentication methods: credential objects, encrypted credential files, certificate-based auth, SSO token reuse, and multi-session management for automation pipelines.
</div>

```text
┌────────────────────────────────── PowerCLI — Authentication Methods ──────────────────────────────────┐
│                                                                                                       │
│   PowerCLI authentication options range from interactive prompts to fully automated pipelines         │
│   Never hardcode credentials in script files; use credential store or pipeline secrets                │
│   Service accounts must authenticate with the minimum required vCenter role (not Administrator)       │
│                                                                                                       │
│   Credential methods                                                                                  │
│   Interactive (dev only): Get-Credential → prompts for username and password at runtime               │
│   Credential store: Store-VICredentialStoreItem saves host-bound encrypted credentials to disk        │
│   Secure string export: Export-Clixml saves PSCredential encrypted to a file (machine-bound)          │
│   Environment variables: pass credentials via $env:VCENTER_USER and $env:VCENTER_PASS in CI/CD        │
│   Pipeline secrets: store in GitHub Actions Secrets, Azure KeyVault, or HashiCorp Vault               │
│                                                                                                       │
│   Multi-session management                                                                            │
│   $global:DefaultVIServers: array of all active vCenter connections in the current session            │
│   Connect to multiple vCenters: Connect-VIServer called multiple times; -Server targets each          │
│   Disconnect cleanly: Disconnect-VIServer -Server * at end of script; prevents orphaned sessions      │
│                                                                                                       │
│   Certificate validation                                                                              │
│   Lab: Set-PowerCLIConfiguration -InvalidCertificateAction Ignore (accept any cert)                   │
│   Production: import vCenter CA cert into OS trust store; use -InvalidCertificateAction Fail          │
│   Mutual TLS: available for VCSA REST API endpoints; requires client certificate provisioning         │
│                                                                                                       │
│   Key terms:                                                                                          │
│   PSCredential          = PowerShell credential object; contains username and SecureString password   │
│   Store-VICredentialStoreItem = encrypted host-bound credential saved to local Windows credential store│
│   SecureString          = encrypted in-memory password; only readable by the current user/process     │
│   DefaultVIServers      = global variable holding all active PowerCLI connection objects              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Credential Methods

### Interactive (development only)

```powershell
Connect-VIServer -Server vcenter.example.com
# Prompts for username and password
```

### PSCredential Object

```powershell
$cred = Get-Credential -UserName "DOMAIN\svc-automation" -Message "vCenter credentials"
Connect-VIServer -Server vcenter.example.com -Credential $cred
```

### Encrypted Credential File

```powershell
# Save credentials (encrypted with current user's DPAPI key — machine/user-bound)
$cred = Get-Credential
$cred | Export-Clixml -Path "$HOME\.vcenter-creds.xml"

# Load in script (only works as the same user on the same machine)
$cred = Import-Clixml -Path "$HOME\.vcenter-creds.xml"
Connect-VIServer -Server vcenter.example.com -Credential $cred
```

### Environment Variables (CI/CD)

```powershell
# Set in pipeline secret store; read in script
$cred = New-Object System.Management.Automation.PSCredential(
    $env:VCENTER_USER,
    (ConvertTo-SecureString $env:VCENTER_PASS -AsPlainText -Force)
)
Connect-VIServer -Server $env:VCENTER_HOST -Credential $cred
```

### Session Token Reuse

```powershell
# Connect once, save session ID
$conn = Connect-VIServer -Server vcenter.example.com -Credential $cred
$sessionId = $conn.SessionId

# Re-use in another process (avoids repeated credential prompts)
Connect-VIServer -Server vcenter.example.com -Session $sessionId
```

## Certificate Validation

```powershell
# Disable cert check (lab/self-signed environments only)
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

# Warn but continue
Set-PowerCLIConfiguration -InvalidCertificateAction Warn -Confirm:$false

# Enforce valid certificates (production default)
Set-PowerCLIConfiguration -InvalidCertificateAction Fail -Confirm:$false

# Add CA cert to trust store (Linux/macOS)
# Copy the vCenter CA PEM to /etc/ssl/certs/ and run update-ca-certificates
```

## SSO / vCenter Token Behaviour

- PowerCLI sessions are vCenter SSO tokens valid for 8 hours by default
- Token lifetime set in vCenter SSO policy: **vCenter → Administration → Single Sign On → Configuration → Token Policy**
- Long-running scripts should reconnect before expiry:

```powershell
function Ensure-VIConnection {
    param([string]$Server, [PSCredential]$Credential)
    $conn = $global:DefaultVIServers | Where-Object { $_.Name -eq $Server -and $_.IsConnected }
    if (-not $conn) {
        Connect-VIServer -Server $Server -Credential $Credential
    }
}
```

## Multi-vCenter Sessions

```powershell
# Connect to multiple vCenters simultaneously
Connect-VIServer -Server vc1.example.com -Credential $cred1
Connect-VIServer -Server vc2.example.com -Credential $cred2

# View all active sessions
$global:DefaultVIServers | Select-Object Name, IsConnected, SessionId, User

# Target specific server in a cmdlet
Get-VM -Server vc1.example.com

# Disconnect all
Disconnect-VIServer -Server * -Confirm:$false
```

## Service Account Best Practices

| Practice | Detail |
|---|---|
| Dedicated service account per automation function | Never share one account across all scripts |
| Use DPAPI-encrypted XML files on dedicated automation hosts | Prevents credential exposure in scripts |
| Rotate credentials on schedule | Update Export-Clixml file after rotation |
| Log all connections | Source IP, timestamp, account in vCenter audit log |
| Avoid storing passwords in script files | Use environment variables or secret stores |
