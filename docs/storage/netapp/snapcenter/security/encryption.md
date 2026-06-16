---
tags:
  - netapp
  - security
---
# SnapCenter — Encryption


<div class="kb-summary">
SnapCenter encryption: backup data encrypted at-rest on ONTAP volumes, in-transit SSL/TLS configuration, certificate management, and SMB3 encryption enforcement.

*Applies to: SnapCenter 5.x*
</div>
```text
┌─────────────────────────────────── NetApp SnapCenter — Encryption ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       SnapCenter encryption: data at rest and in transit encryption for all stored data       │   │
│   │          At rest: AES-256 encryption using controller-managed or external key manager         │   │
│   │          In transit: TLS 1.2+ for management; protocol encryption for data in flight          │   │
│   │         Key management: external KMIP-compatible KMS or built-in key lifecycle manager        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Enable encryption → configure KMS → verify → audit → rotate keys                                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Server           │  │          Windows VM         │  │       Central control       │   │
│   │           Plug-in           │  │          Host agent         │  │        App-consistent       │   │
│   │            Policy           │  │       Schedule/retain       │  │         Backup rule         │   │
│   │        Resource group       │  │       Grouped targets       │  │        Shared policy        │   │
│   │           Recovery          │  │       Volume/LUN/file       │  │       Granular restore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Standard     │     Key source    │       KMS        │      Notes       │   │
│   │     At rest      │     AES-256      │     Controller    │  Internal/KMIP   │    Always on     │   │
│   │    In transit    │     TLS 1.2+     │      PKI cert     │   Internal CA    │   Mgmt + data    │   │
│   │   Key rotation   │      Annual      │     KMS policy    │   External KMS   │    Automated     │   │
│   │    Key escrow    │     Required     │     KMS vault     │   External KMS   │    DR access     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SnapCenter Server (Windows) · ONTAP clusters · plug-in hosts · application servers       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapCenter         = NetApp backup orchestration; coordinates app-consistent snapshots via plug-ins│
│    Plug-in            = host-side agent; quiesces application before snapshot: SQL, Oracle, VMware    │
│    Resource group     = set of resources sharing a backup policy and schedule in SnapCenter           │
│    Policy             = SnapCenter object defining snapshot frequency, retention, and replication t...│
│    App-consistent     = snapshot taken after DB quiesce; guarantees crash-consistent recovery         │
│    Clone lifecycle    = SnapCenter clone: create from snapshot, provision to host, then delete        │
│    FlexClone          = underlying ONTAP technology; SnapCenter clone maps to an ONTAP FlexClone      │
│    Vault policy       = SnapCenter policy that also replicates snapshots to SnapVault destination     │
│    Mirror policy      = SnapCenter policy that replicates snapshots via SnapMirror to DR cluster      │
│    RBAC               = SnapCenter role-based access; Admin, Backup Operator, Restore Operator roles  │
│    SMF                = SnapCenter MySQL database storing job history, policies, and resource configs │
│    SnapCenter API     = REST API on port 8143; full feature coverage for automation workflows         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## TLS and Certificate Management

SnapCenter exposes its web GUI and REST API on port 8146 over HTTPS. The underlying web server is IIS (Internet Information Services) on Windows Server. By default, SnapCenter installs with a self-signed certificate — this must be replaced with a CA-signed certificate before production use.

### Replace the Self-Signed Certificate

**Step 1 — Generate a Certificate Signing Request (CSR)**

1. Open **IIS Manager** on the SnapCenter Server
2. Click the server node → **Server Certificates** → **Create Certificate Request**
3. Fill in the Common Name (FQDN of the SnapCenter Server, e.g., `snapcenter01.corp.example.com`)
4. Add Subject Alternative Names (SANs) for any additional DNS names or IPs used to access SnapCenter
5. Select **2048-bit** or **4096-bit** key length; RSA-2048 minimum
6. Save the CSR file

**Step 2 — Submit the CSR to Your CA**

- Submit the CSR to your internal CA (Active Directory Certificate Services) or a public CA
- Request a server authentication certificate (EKU: Server Authentication, 1.3.6.1.5.5.7.3.1)
- Obtain the signed certificate in PFX format (certificate + private key) or as a separate CRT + PEM key pair

**Step 3 — Import and Bind the Certificate**

```powershell
# Import the PFX certificate to the Windows certificate store (on SnapCenter Server)
# Run in PowerShell as Administrator

$pfxPath  = "C:\certs\snapcenter01.pfx"
$pfxPass  = (Read-Host "PFX password" -AsSecureString)
$certStore = "Cert:\LocalMachine\My"

$cert = Import-PfxCertificate -FilePath $pfxPath -CertStoreLocation $certStore -Password $pfxPass
Write-Host "Certificate thumbprint: $($cert.Thumbprint)"

# Bind the certificate to IIS port 8146
# In IIS Manager: Sites → SnapCenter_WebApp → Bindings → Edit → Select new certificate
# Or via PowerShell:
Import-Module WebAdministration
$binding = Get-WebBinding -Name "SnapCenter_WebApp" -Protocol https -Port 8146
$binding.AddSslCertificate($cert.Thumbprint, "My")

# Restart IIS to apply the new certificate
iisreset /noforce
```

**Step 4 — Verify the Certificate**

```powershell
# Verify the certificate is bound to port 8146
netsh http show sslcert ipport=0.0.0.0:8146

# Test the certificate from a client
# In a browser: navigate to https://snapcenter01.corp.example.com:8146
# Certificate should show as trusted (green padlock) with the correct FQDN

# Command-line check
$cert = [System.Net.ServicePointManager]::SecurityProtocol
Invoke-WebRequest -Uri "https://snapcenter01.corp.example.com:8146" -UseBasicParsing | Select-Object StatusCode
```

### TLS Version Enforcement

Enforce TLS 1.2 minimum in IIS — disable TLS 1.0 and 1.1 on the SnapCenter Server.

```powershell
# Disable TLS 1.0 in Windows registry (run as Administrator)
$tls10 = "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server"
New-Item -Path $tls10 -Force | Out-Null
New-ItemProperty -Path $tls10 -Name "Enabled" -Value 0 -PropertyType DWORD -Force
New-ItemProperty -Path $tls10 -Name "DisabledByDefault" -Value 1 -PropertyType DWORD -Force

# Disable TLS 1.1
$tls11 = "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server"
New-Item -Path $tls11 -Force | Out-Null
New-ItemProperty -Path $tls11 -Name "Enabled" -Value 0 -PropertyType DWORD -Force
New-ItemProperty -Path $tls11 -Name "DisabledByDefault" -Value 1 -PropertyType DWORD -Force

# Confirm TLS 1.2 is enabled (should be by default on Windows Server 2019+)
$tls12 = "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server"
Get-ItemProperty -Path $tls12 -ErrorAction SilentlyContinue

# Reboot required for SCHANNEL registry changes to take effect
# Restart-Computer -Force
```

### Certificate Expiry Monitoring

```powershell
# Check the SnapCenter Server certificate expiry date
$cert = Get-ChildItem -Path "Cert:\LocalMachine\My" | 
    Where-Object { $_.Subject -like "*snapcenter*" }
$cert | Select-Object Subject, NotAfter, Thumbprint

# Alert if certificate expires within 30 days
$daysUntilExpiry = ($cert.NotAfter - (Get-Date)).Days
if ($daysUntilExpiry -lt 30) {
    Write-Warning "SnapCenter certificate expires in $daysUntilExpiry days — renew immediately"
} else {
    Write-Host "Certificate valid for $daysUntilExpiry more days"
}
```

Include certificate expiry monitoring in weekly operational checks — a SnapCenter certificate expiry causes browser warnings and can block automation scripts that validate TLS certificates.

---

## Encryption of Stored Credentials

SnapCenter encrypts credentials stored in its repository database using Windows DPAPI (Data Protection API) on the SnapCenter Server host. The encryption key is tied to the SnapCenter Server Windows machine account. Key implications:

- Moving the SnapCenter repository database to a different server requires re-entering all credentials — the DPAPI encryption is not portable
- The SnapCenter Server VM must be backed up as a whole (including the Windows machine state) to preserve credential decryptability
- Do not clone the SnapCenter Server VM without also re-initialising credentials — cloned VMs with the same SID can create decryption conflicts

### SnapCenter Repository Backup

The repository database (MySQL) should be backed up separately from the SnapCenter Server VM. A corrupted or inaccessible repository causes SnapCenter to lose all job history, policies, resource groups, and RBAC configuration.

```powershell
# Back up the MySQL repository via SnapCenter built-in backup
# In SnapCenter GUI: Settings → Repository → Backup
# Or via PowerShell:

# Stop MySQL temporarily for a clean backup (brief service interruption)
Stop-Service -Name "MySQL80"

# Copy the MySQL data directory to backup location
$mysqlData   = "C:\Program Files\NetApp\SnapCenter\MySQL Data"
$backupDest  = "\\backup-server\snapcenter-repo\$(Get-Date -Format 'yyyy-MM-dd')"
Copy-Item -Path $mysqlData -Destination $backupDest -Recurse -Force

# Restart MySQL
Start-Service -Name "MySQL80"

# Verify MySQL is running after backup
Get-Service -Name "MySQL80" | Select-Object Name, Status
```

---

## Encryption in SnapCenter-to-ONTAP Communication

SnapCenter communicates with ONTAP via HTTPS (port 443 using ONTAP REST API for SnapCenter 6.x, or ONTAP ZAPI/HTTP for older versions). The ONTAP management LIF must have a valid TLS certificate.

```powershell
# Verify ONTAP storage connection is using HTTPS
Get-SmStorageConnection | Select-Object StorageName, Protocol, Port
# Protocol should be: HTTPS
# Port should be: 443

# Update a storage connection to use HTTPS if it is using HTTP
Set-SmStorageConnection \
    -StorageName "lon-affa400-cl01" \
    -Protocol HTTPS \
    -Port 443 \
    -Credential (Get-Credential)
```

For SnapCenter 6.x, the REST API connection to ONTAP uses TLS 1.2 minimum, enforced by the ONTAP cluster TLS configuration. Verify on the ONTAP cluster:

```bash
# Verify ONTAP HTTPS TLS configuration (run on ONTAP cluster)
security config show
# Check: Is FIPS Enabled: false (or true if FIPS mode)
# Check: Supported Protocols: TLSv1.2,TLSv1.3 (not TLSv1.0 or TLSv1.1)

# Enforce TLS 1.2 minimum
security config modify -interface HTTPS -min-protocol-version TLSv1.2
```

---

## Encryption of SnapCenter Agent Communication

The SnapCenter Server communicates with plugin agents on TCP port 8145. This channel uses TLS encryption. The certificate used for the agent channel is the same server certificate configured on port 8146.

- Plugin agents validate the SnapCenter Server certificate on connection — if the certificate changes (e.g., renewal), agents may require a re-registration or refresh via Settings → Hosts → Refresh
- On Linux plugin hosts, the SnapCenter Linux plug-in service stores a copy of the SnapCenter Server's public certificate to validate the connection

```powershell
# After certificate renewal, refresh all plugin hosts to re-establish trust
Get-SmHost | ForEach-Object {
    Write-Host "Refreshing host: $($_.HostName)"
    Invoke-SmHostRefresh -HostName $_.HostName
}

# Verify all hosts reconnected successfully after refresh
Get-SmHost | Select-Object HostName, PlugInStatus, OverallStatus
# All hosts should show PlugInStatus: Running
```

---

## Compliance Summary

| Control | SnapCenter Feature | How to Verify |
|---|---|---|
| Encryption in transit — GUI/API | TLS 1.2+ on IIS port 8146 | `netsh http show sslcert ipport=0.0.0.0:8146` |
| Encryption in transit — ONTAP | HTTPS on port 443 | `Get-SmStorageConnection \| Select Protocol` |
| Encryption in transit — agent | TLS on port 8145 (same cert as 8146) | `Get-SmHost \| Select HostName, PlugInStatus` |
| Encryption of stored credentials | Windows DPAPI on SnapCenter Server | Repository backup validates decryptability |
| Certificate management | CA-signed cert on IIS | Certificate expiry check weekly |
| TLS version enforcement | SCHANNEL registry (Windows) + IIS | Registry check; `netsh` SSL cert binding |

---

## See also

- [Snapcenter — Hardening](hardening/)
- [Snapcenter — Authentication](authentication/)
- [Snapcenter — Access Control](access-control/)
