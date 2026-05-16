# Horizon — Hardening

---

## Connection Server Hardening

### locked.properties

The `locked.properties` file enforces security settings that override console configuration:

```powershell
# File location:
$props = "C:\Program Files\VMware\VMware View\Server\sslgateway\conf\locked.properties"

# Restrict admin console to management network only (prevents console access from desktops)
Add-Content $props "checkOrigin=true"
Add-Content $props "allowedHosts=10.10.10.0/24"    # management subnet only

# Disable TLS 1.0 and 1.1
Add-Content $props "sslprotocols=TLSv1.2,TLSv1.3"
Add-Content $props "enabledCipherSuites=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"

Restart-Service "VMware Horizon View Connection Server"
```

### Windows Hardening of Connection Server

```powershell
# Disable unused services
Stop-Service -Name "Fax" -ErrorAction SilentlyContinue
Stop-Service -Name "XblAuthManager" -ErrorAction SilentlyContinue

# AV exclusions for Connection Server (add to your AV policy):
# C:\Program Files\VMware\VMware View\
# C:\ProgramData\VMware\VDM\

# Enable Windows Firewall — allow only required ports
# TCP 443 (HTTPS), TCP 8443 (Blast), TCP 4001 (JMS inter-CS), TCP 22389 (LDAP replica)
```

---

## UAG Hardening

```bash
# UAG Admin UI → Advanced Settings → TLS Settings
  SSL Ciphers: ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256
  TLS Versions: TLSv1.2,TLSv1.3

# UAG Admin UI → Advanced Settings → DoS Mitigation
  Enable DoS protection: Yes
  Max connections per client: 25 (reduce for restrictive environments)

# Restrict UAG admin UI to management IP only
  Admin Interface: bind to management NIC IP only
  Allow access from: management subnet CIDR
```

---

## USB Redirection Policy

```
Group Policy → Computer Configuration → VMware Horizon Agent
  USB Redirection Enabled: No (disable entirely for highly regulated desktops)
  OR:
  Exclude Device Family: Storage,Bluetooth,SmartCard  (allow only specific devices)
  Include Device: <VID>_<PID>  (explicitly allow CAC reader by VID/PID)
```

---

## Clipboard Direction Restriction

```
Group Policy → Computer Configuration → VMware Blast → Clipboard
  Clipboard Direction: Client to Agent only
  (Users can paste into the desktop but cannot copy out — prevents data exfiltration)
```

For kiosk or shared-terminal pools: set to Disabled entirely.

---

## Drive Mapping Restriction

```
Group Policy → Computer Configuration → VMware Horizon Agent
  Client Drive Redirection: Disabled
```

Prevents users from mapping their local drives into the virtual desktop — eliminates a data exfiltration path.

---

## Disable Direct Console Access

Connection Server should not be accessible directly from desktop VMs:

```
locked.properties:
  checkOrigin=true
  allowedHosts=<management-subnet>
```

Physical server hosting Connection Server should not be on the same VLAN as desktop VMs.

---

## Monitor Admin Events

```
Horizon Console → Monitor → Events
  Filter: Role = Administrator, Action = Configuration Change
  Export to CSV for audit trail
```

For automated monitoring, configure Events Database (SQL Server) and query it with scheduled reports.

---

## Security Hardening Checklist

| Control | Status Check |
|---|---|
| TLS 1.0/1.1 disabled on CS | `nmap --script ssl-enum-ciphers -p 443 horizon-cs01.corp.local` |
| CA-signed cert on CS | `openssl s_client -connect horizon-cs01:443 \| openssl x509 -issuer` |
| CA-signed cert on UAG | `openssl s_client -connect uag:443 \| openssl x509 -issuer` |
| 2FA enabled for external access | Horizon Console → Settings → CS → Authentication |
| Clipboard restricted | GPO audit — verify policy applied to desktop OUs |
| USB storage blocked | GPO audit — verify Exclude Device Family includes Storage |
| Drive mapping disabled | GPO audit |
| CS admin UI restricted to mgmt VLAN | Test: access `https://horizon-cs01` from desktop VLAN |
| Events DB configured | Monitor → Events: confirm long history available |
