# Windows Server — Initial Deployment

This guide covers deploying a new Windows Server from OS install through network configuration, NTP, Windows Update, domain join, firewall, WinRM, and security baseline application.

---

## Install the OS

Boot from the Windows Server 2022 ISO. At the installation type selection screen, choose:

- **Server Core** — recommended for most server roles (smaller attack surface, lower memory footprint)
- **Desktop Experience** — use only where a GUI is explicitly required (e.g., some legacy applications)

**During installation:**

1. Select the target disk and configure partitions. For OS-only disks, a single partition is acceptable; for data disks, add a separate volume.
2. Set the local Administrator password — use a strong, unique password stored in your PAM solution.
3. Activate with a KMS key during setup or via `slmgr.vbs` post-install.

**Post-install from Server Core (SConfig):**

Run `SConfig` to set the computer name and enable remote management before proceeding.

```cmd
SConfig
```

Use option 2 (Computer Name) and option 4 (Configure Remote Management) from the SConfig menu.

---

## Configure Network

Set a static IP, default gateway, and DNS servers. Run from an elevated PowerShell session.

```powershell
# Set static IP
New-NetIPAddress `
    -InterfaceAlias Ethernet `
    -IPAddress <IP> `
    -PrefixLength <prefix> `
    -DefaultGateway <GW>

# Set DNS servers
Set-DnsClientServerAddress `
    -InterfaceAlias Ethernet `
    -ServerAddresses <DNS1>, <DNS2>
```

Verify connectivity:

```powershell
Get-NetIPAddress -InterfaceAlias Ethernet
Test-NetConnection -ComputerName <GW>
Resolve-DnsName corp.local
```

Rename the network adapter to something descriptive if there are multiple NICs:

```powershell
Rename-NetAdapter -Name "Ethernet" -NewName "LAN"
```

---

## Configure NTP

Standalone servers (before domain join) should sync directly with an NTP source. After domain join, the domain hierarchy handles NTP automatically.

```powershell
w32tm /config /manualpeerlist:"<NTP-server>" /syncfromflags:manual /reliable:yes /update
Restart-Service w32tm
w32tm /resync /force
```

Verify synchronisation:

```powershell
w32tm /query /status
```

Confirm `Source` shows your NTP server and `Last Successful Sync Time` is recent. After domain join, run `w32tm /query /source` to verify the DC is the time source.

---

## Configure Windows Update (WSUS or Direct)

Apply all available updates before domain join to reduce the time between domain join and security baseline application.

**Enable and start Windows Update service:**

```powershell
Set-Service -Name wuauserv -StartupType Automatic
Start-Service wuauserv
```

**If using direct Microsoft Update (lab or internet-connected):**

```powershell
# Install PSWindowsUpdate module if not present
Install-Module PSWindowsUpdate -Force
Install-WindowsUpdate -AcceptAll -AutoReboot
```

**If using WSUS (enterprise environments):**

Configure the WSUS server and target group via GPO:

```text
Computer Configuration → Administrative Templates → Windows Components → Windows Update
→ Specify intranet Microsoft update service location: http://<wsus-server>:8530
```

Or set directly in the registry:

```powershell
$wsus = "http://<wsus-server>:8530"
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" `
    -Name WUServer -Value $wsus
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" `
    -Name WUStatusServer -Value $wsus
```

Check update status:

```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
```

---

## Join the Domain

Join the server to Active Directory and place it in the correct OU.

```powershell
Add-Computer `
    -DomainName corp.local `
    -OUPath "OU=Member Servers,OU=Servers,DC=corp,DC=local" `
    -Credential (Get-Credential) `
    -Restart
```

After reboot, log in as `CORP\Administrator` or a domain admin account.

Verify domain membership:

```powershell
(Get-WmiObject Win32_ComputerSystem).Domain
nltest /sc_verify:corp.local
```

`nltest` should return `Flags: ... WRITABLE ... DNS_DC ... CLOSE_SITE ... FULL_SECRET ... DS ...` and `The command completed successfully`.

---

## Configure Windows Firewall

Enable Windows Firewall on all profiles and add only the rules required for this server's role.

```powershell
# Enable firewall on all profiles
Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled True

# Allow RDP (adjust source IP range in production)
New-NetFirewallRule `
    -DisplayName "Allow RDP" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 3389 `
    -Action Allow

# Allow WinRM (HTTPS) from management subnet
New-NetFirewallRule `
    -DisplayName "Allow WinRM HTTPS" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 5986 `
    -RemoteAddress <mgmt-subnet> `
    -Action Allow
```

Verify active rules:

```powershell
Get-NetFirewallRule | Where-Object { $_.Enabled -eq "True" -and $_.Direction -eq "Inbound" } |
    Select-Object DisplayName, LocalPort, Action
```

---

## Configure WinRM for Remote Management

Enable PowerShell remoting and set WinRM to start automatically.

```powershell
Enable-PSRemoting -Force
Set-Service WinRM -StartupType Automatic
```

For HTTPS-only remoting (recommended for production), create a WinRM listener on port 5986 using a certificate from your internal CA:

```powershell
$cert = Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Subject -like "*$env:COMPUTERNAME*" }
New-WSManInstance -ResourceURI winrm/config/Listener `
    -SelectorSet @{Address="*"; Transport="HTTPS"} `
    -ValueSet @{Hostname=$env:COMPUTERNAME; CertificateThumbprint=$cert.Thumbprint}
```

Test remoting from an admin workstation:

```powershell
Test-WSMan -ComputerName <server> -UseSSL
Enter-PSSession -ComputerName <server> -UseSSL
```

---

## Enable Windows Defender and Security Baseline

Ensure Windows Defender is active and real-time protection is enabled.

```powershell
# Enable real-time monitoring
Set-MpPreference -DisableRealtimeMonitoring $false

# Verify Defender status
Get-MpComputerStatus | Select-Object AMRunningMode, RealTimeProtectionEnabled, AntivirusEnabled
```

**Apply Microsoft Security Compliance Toolkit baseline via GPO:**

1. Download the Microsoft Security Compliance Toolkit for Windows Server 2022.
2. Import the GPO backup to the domain:

```powershell
Import-GPO `
    -BackupGpoName "MSFT Windows Server 2022 - Member Server" `
    -Path "C:\SCT\GPOs" `
    -TargetName "Server Baseline - Member Servers" `
    -CreateIfNeeded

New-GPLink `
    -Name "Server Baseline - Member Servers" `
    -Target "OU=Member Servers,OU=Servers,DC=corp,DC=local"
```

Force policy application and verify:

```powershell
gpupdate /force
gpresult /r /scope computer
```

Confirm the baseline GPO appears under `Applied Group Policy Objects`.

---

## Validate the Deployment

```powershell
# Check for recent errors in the System log
Get-EventLog -LogName System -EntryType Error -Newest 10

# Confirm domain membership
(Get-WmiObject Win32_ComputerSystem).Domain

# Confirm NTP is syncing from the domain
w32tm /query /source

# Confirm Windows Defender is running
Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled

# Confirm Windows Firewall is active on all profiles
Get-NetFirewallProfile | Select-Object Name, Enabled

# Test RDP from admin workstation (run from remote machine)
Test-NetConnection -ComputerName <server> -Port 3389

# Test PowerShell remoting (run from remote machine)
Test-WSMan -ComputerName <server>
```

All checks should return the expected values with no errors. Resolve any `Get-EventLog` errors before handing the server off for role configuration.
