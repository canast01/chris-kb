# SRM — Diagnostics

```text
  SRM Diagnostic Data Sources
┌──────────────────────────────────────────────────────────────┐
│  SRM Server (Windows)           SRM Appliance (Linux)        │
│  ┌──────────────────────────┐   ┌──────────────────────────┐ │
│  │ C:\ProgramData\VMware\   │   │ /var/log/vmware/srm/     │ │
│  │  VMware vCenter SRM\     │   │  vmware-dr.log           │ │
│  │  Logs\vmware-dr.log      │   │                          │ │
│  └──────────────────────────┘   └──────────────────────────┘ │
│                                                              │
│  VR Appliance Logs              SRA Logs                     │
│  ┌──────────────────────────┐   ┌──────────────────────────┐ │
│  │ /var/log/vmware/hms/     │   │ Pure: C:\ProgramData\    │ │
│  │ /var/log/vmware/vrms/    │   │  Pure Storage\SRA\Logs\  │ │
│  │ VRA VAMI → Support →     │   │ Dell: C:\ProgramData\    │ │
│  │  Download Bundle         │   │  EMC\SRA\Logs\           │ │
│  └──────────────────────────┘   └──────────────────────────┘ │
│                                                              │
│  Support Bundle: Site Recovery → Summary → Download          │
└──────────────────────────────────────────────────────────────┘
```

---

## SRM Log Locations

**Windows SRM Server:**
```text
C:\ProgramData\VMware\VMware vCenter Site Recovery Manager\Logs\
  vmware-dr.log        # Main SRM log
  vmware-dr-*.log      # Rotated logs
```

**SRM Appliance (Linux):**
```bash
ssh admin@srm-protected.example.local
/var/log/vmware/srm/
  vmware-dr.log
```

---

## Collect SRM Support Bundle

```text
Site Recovery → Summary → Download SRM Support Bundle
  Includes: SRM logs, configuration, site pairing state
  Download from both protected and recovery site SRM Servers
```

Manual collection if UI unavailable:
```bash
# SRM Appliance:
ssh admin@srm-protected.example.local
/opt/vmware/srm/bin/support-bundle.sh
# Bundle location: /tmp/srm-support-<timestamp>.tar.gz
```

---

## vSphere Replication Log Collection

```bash
# SSH to VRA appliance
ssh admin@vra-protected.example.local

# Log locations:
/var/log/vmware/hms/      # Replication management
/var/log/vmware/vrms/     # VRA service
/var/log/vmware/vcd/      # Cloud director integration (if applicable)

# Download support bundle via VRA VAMI:
# https://vra-protected.example.local:5480 → Support → Download Support Bundle
```

---

## SRA Logs

SRA logs location depends on the array vendor:

| Vendor | Log Location |
|---|---|
| Pure Storage | `C:\ProgramData\Pure Storage\SRA\Logs\` (Windows) |
| Dell PowerStore | `C:\ProgramData\EMC\SRA\Logs\` |
| NetApp | `C:\Program Files\NetApp\SnapMirror SRA\log\` |

```powershell
# Check Pure Storage SRA log (Windows SRM Server)
Get-Content "C:\ProgramData\Pure Storage\SRA\Logs\pure-sra.log" -Tail 50
```

---

## Check SRM Service Status

```powershell
# Protected site
Get-Service -ComputerName srm-protected.example.local `
  -Name "VMware vCenter Site Recovery Manager" | Select-Object Status, StartType

# Recovery site
Get-Service -ComputerName srm-recovery.example.local `
  -Name "VMware vCenter Site Recovery Manager" | Select-Object Status, StartType

# If stopped, start:
Start-Service -ComputerName srm-protected.example.local `
  -Name "VMware vCenter Site Recovery Manager"
```

---

## Verify Site Pairing Certificate

```bash
# Test TLS connection between SRM Servers (inter-site port)
echo | openssl s_client -connect srm-recovery.example.local:9086 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer

# Test admin HTTPS
echo | openssl s_client -connect srm-protected.example.local:443 2>/dev/null \
  | openssl x509 -noout -dates -subject
```

---

## Review Recovery Plan Step Logs

```bash
Site Recovery → Recovery Plans → [plan] → History → [run] → Steps
  Click any step to see detailed sub-step log
  Export history as CSV for external analysis
```

```powershell
# Export full history via PowerCLI
$plans = $srm.ExtensionData.Recovery.ListPlans()
foreach ($plan in $plans) {
    $history = $srm.ExtensionData.Recovery.GetHistory($plan)
    $history | Export-Csv "srm-history-$($plan.Name).csv" -NoTypeInformation
}
```

---

## Test SRA Connectivity Manually

```bash
# Test FlashArray reachability from SRM Server:
curl -sk -H "x-auth-token: <api-token>" \
  "https://<flasharray-ip>/api/2.0/array" | python3 -m json.tool
# Should return array info — if error, SRA connectivity is broken

# Check certificate used by FlashArray:
echo | openssl s_client -connect <flasharray-ip>:443 2>/dev/null \
  | openssl x509 -noout -dates
```
