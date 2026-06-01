# SRM — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Collect SRM Support Bundle, vSphere Replication Log Collection, SRA Logs, Check SRM Service Status, Verify Site Pairing Certificate and 2 more sections.
</div>

  SRM Diagnostic Data Sources
```
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
┌────────────────────────────────────── VMware SRM — Diagnostics ───────────────────────────────────────┐
│                                                                                                       │
│  SRM diagnostics use support bundles, SRM Server logs, vSphere Replication logs,                      │
│  SRA diagnostic files, and vCenter events to diagnose failures.                                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               SRM Server Logs                │  │               vSphere Rep Logs              │   │
│   │   C:\ProgramData\VMware\VMware vCenter SRM   │  │       vSphere Rep appliance: /var/log       │   │
│   │          vmware-dr-*.log: main log           │  │           hbrsrv.log: replication           │   │
│   │            vmware-srmserver-*.log            │  │           hbrfilter.log: I/O path           │   │
│   │            Support bundle: SRM UI            │  │           vR appliance: VM on ESXi          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Start with SRM support bundle; vmware-dr-*.log has full plan execution detail.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               SRA Diagnostics                │  │                vCenter Events               │   │
│   │          SRA: vendor-specific tool           │  │              Filter: SRM events             │   │
│   │            Dell: SRDF/Metro diag             │  │          Tasks: SRM plan run tasks          │   │
│   │           NetApp: snapmirror show            │  │          Events: site pair connect          │   │
│   │             SRA log: C:\SRA\logs             │  │          Alarms: replication error          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SRM Server logs accessed via RDP to Windows VM; vSphere Rep logs via SSH to appliance;               │
│  support bundle generated via SRM vSphere Client plugin.                                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vmware-dr-*.log= main SRM log; plan execution, steps, errors                                         │
│  vmware-srmserver= SRM application service log                                                        │
│  hbrsrv.log    = vSphere Replication server log; replication status                                   │
│  hbrfilter.log = I/O filter log; per-VM replication I/O path                                          │
│  SRA log       = array adapter log; in C:\SRA\logs on SRM Server                                      │
│  Support bundle= SRM UI > Administration > Support; ZIP download                                      │
│  vSphere Rep   = vSphere Replication appliance; separate VM from SRM                                  │
│  snapmirror show= NetApp CLI; shows replication relationship status                                   │
│  SRDF          = Dell EMC array replication; vendor CLI for diag                                      │
│  vCenter events= Administration > Events; filter to SRM events                                        │
│  Plan tasks    = vCenter Tasks; SRM records plan steps as vCenter tasks                               │
│  ProgramData   = Windows hidden folder; SRM writes logs here                                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
