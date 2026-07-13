---
tags:
  - horizon
  - security
  - vmware
description: "Hardening reference covering Windows Hardening of Connection Server, UAG Hardening, USB Redirection Policy, Clipboard Direction Restriction, Drive Mapping..."
---
# Horizon — Hardening

<div class="kb-summary">
Hardening reference covering Windows Hardening of Connection Server, UAG Hardening, USB Redirection Policy, Clipboard Direction Restriction, Drive Mapping Restriction and 3 more sections.

*Applies to: Horizon 8.x*
</div>
![Horizon — Hardening](../../../../../assets/virtualization-vmware-horizon-security-hardening.svg)

  Hardening Checklist Coverage

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

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


```text title="Expected output"
(no output — command completes silently)

Note: These are configuration settings applied through the UAG Admin UI web interface, not CLI commands. Changes are persisted to the UAG configuration database upon clicking "Apply" or "Save" in the Advanced Settings panel. Verification can be performed via:

# Verify TLS configuration applied
openssl s_client -connect uag-hostname:9443 -tls1_2 2>/dev/null | grep -A2 "Cipher"

# Expected verification output:
Cipher    : ECDHE-RSA-AES256-GCM-SHA384
Protocol  : TLSv1.2
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Connection refused on port 9443` | Verify the UAG Admin UI service is running with `systemctl status vmware-uag-admin` and that the management NIC binding is correctly configured in the network settings. |
    | `SSL: CERTIFICATE_VERIFY_FAILED` | Ensure the UAG's SSL certificate is valid and trusted; regenerate or import a valid certificate through Admin UI > Certificates if the cert has expired or is self-signed without proper CA chain. |
    | `DoS protection blocking legitimate traffic` | Increase the "Max connections per client" threshold in Admin UI > Advanced Settings > DoS Mitigation if legitimate admin sessions are being dropped. |
---

## USB Redirection Policy

```text
Group Policy → Computer Configuration → VMware Horizon Agent
  USB Redirection Enabled: No (disable entirely for highly regulated desktops)
  OR:
  Exclude Device Family: Storage,Bluetooth,SmartCard  (allow only specific devices)
  Include Device: <VID>_<PID>  (explicitly allow CAC reader by VID/PID)
```

---

## Clipboard Direction Restriction

```text
Group Policy → Computer Configuration → VMware Blast → Clipboard
  Clipboard Direction: Client to Agent only
  (Users can paste into the desktop but cannot copy out — prevents data exfiltration)
```

For kiosk or shared-terminal pools: set to Disabled entirely.

---

## Drive Mapping Restriction

```text
Group Policy → Computer Configuration → VMware Horizon Agent
  Client Drive Redirection: Disabled
```

Prevents users from mapping their local drives into the virtual desktop — eliminates a data exfiltration path.

---

## Disable Direct Console Access

Connection Server should not be accessible directly from desktop VMs:

```text
locked.properties:
  checkOrigin=true
  allowedHosts=<management-subnet>
```

Physical server hosting Connection Server should not be on the same VLAN as desktop VMs.

---

## Monitor Admin Events

```bash
Horizon Console → Monitor → Events
  Filter: Role = Administrator, Action = Configuration Change
  Export to CSV for audit trail
```


```text title="Expected output"
Event ID,Timestamp,User,Role,Action,Object,Details,Status
EVT-2847392,2024-01-15 14:32:18,admin@corp.local,Administrator,Configuration Change,Connection Server,SSL Certificate Updated,Success
EVT-2847391,2024-01-15 13:45:02,svc_horizon@corp.local,Administrator,Configuration Change,Security Settings,Password Policy Modified,Success
EVT-2847390,2024-01-15 12:18:47,admin@corp.local,Administrator,Configuration Change,LDAP Configuration,Domain Controller Added,Success
EVT-2847389,2024-01-14 16:22:33,admin@corp.local,Administrator,Configuration Change,Entitlements,Pool Access Rules Updated,Success
EVT-2847388,2024-01-14 09:15:11,svc_horizon@corp.local,Administrator,Configuration Change,Broker Settings,Session Timeout Adjusted,Success
...
Total Events Exported: 247
Export completed successfully to: /var/log/horizon/audit_export_20240115_143218.csv
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unable to connect to Horizon Event Database — connection timeout after 30 seconds` | Verify the Event Database service is running and accessible on the configured hostname/port in Horizon Administrator settings. |
    | `Error: Insufficient permissions to export events — user role does not have Audit:Read privilege` | Grant the user the "Audit" role or add explicit "Audit:Read" permission in Horizon Administrator > Users and Groups. |
    | `Error: CSV export failed — disk space insufficient (required: 512MB, available: 128MB)` | Free up disk space on the Horizon Connection Server or configure event export to an alternate location with adequate storage. |
For automated monitoring, configure Events Database (SQL Server) and query it with scheduled reports.

---

## Security Hardening Checklist

| Control | Status Check |
|---|---|
| TLS 1.0/1.1 disabled on CS | `nmap --script ssl-enum-ciphers -p 443 horizon-cs01.example.local` |
| CA-signed cert on CS | `openssl s_client -connect horizon-cs01:443 \| openssl x509 -issuer` |
| CA-signed cert on UAG | `openssl s_client -connect uag:443 \| openssl x509 -issuer` |
| 2FA enabled for external access | Horizon Console → Settings → CS → Authentication |
| Clipboard restricted | GPO audit — verify policy applied to desktop OUs |
| USB storage blocked | GPO audit — verify Exclude Device Family includes Storage |
| Drive mapping disabled | GPO audit |
| CS admin UI restricted to mgmt VLAN | Test: access `https://horizon-cs01` from desktop VLAN |
| Events DB configured | Monitor → Events: confirm long history available |

## See also

- [Horizon — Access Control](../access-control/)
- [Horizon — Authentication](../authentication/)
- [VMware Horizon — Health Checks](../../operations/health-checks/)
