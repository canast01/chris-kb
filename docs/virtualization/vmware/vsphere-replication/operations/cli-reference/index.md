# vSphere Replication — CLI Reference

```
  VR CLI and API Access
┌──────────────────────────────────────────────────────────────┐
│  VRA Appliance SSH                                           │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ systemctl status hms vrms nginx                      │    │
│  │ systemctl restart hms                                │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  VRA REST API                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ POST /api/rest/vr/authentication/token → Bearer tok  │    │
│  │ GET  /api/rest/vr/replications                       │    │
│  │ GET  /api/rest/vr/health                             │    │
│  │ POST /api/rest/vr/replications/<id>/sync             │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  ESXi host (source) — connectivity test                      │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ nc -vz <target-VRA> 31031   (replication data port)  │    │
│  │ vmkping -I vmk0 <target-VRA-IP>                      │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## VRA Appliance SSH Access

```bash
# SSH to VRA appliance (admin user)
ssh admin@vra-london.example.local
# Or: admin user → use appliance shell

# Check VRA service status
systemctl status hms        # Home Management Server — core VRA service
systemctl status vrms       # vSphere Replication Management Service
systemctl status nginx      # HTTPS proxy

# Restart VRA services (use with care — interrupts active replications briefly)
systemctl restart hms
systemctl restart vrms
```

---

## VRA REST API Authentication

```bash
# Authenticate to VRA REST API
TOKEN=$(curl -sk -X POST \
  "https://vra-london.example.local/api/rest/vr/authentication/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' | \
  python3 -c "import json,sys; print(json.load(sys.stdin).get('token',''))")

HEADERS="-H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json'"
```

---

## Get Replication Status via REST API

```bash
# List all replications on this VRA
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-london.example.local/api/rest/vr/replications" | python3 -m json.tool

# Get replication status for a specific VM (by replication ID)
REPL_ID="<replication-id>"
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-london.example.local/api/rest/vr/replications/$REPL_ID" | python3 -m json.tool
```

---

## PowerCLI — Replication Status

```powershell
# Connect to vCenter
Connect-VIServer -Server vcenter.example.local

# Get all VMs with replication configured
$replicatedVMs = Get-VM | Where-Object {
    (Get-VIObjectByVIView -MORef $_.ExtensionData.MoRef |
     Get-View).Config.Hardware.Device |
    Where-Object { $_.GetType().Name -eq "VirtualDisk" } |
    Where-Object { $_.Backing.ChangeId }
}

# Using SRM module for VR-managed replications:
Import-Module VMware.VimAutomation.Srm
$srm = Connect-SrmServer -SrmServerAddress srm-london.example.local

# List protection groups with VR replications
$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()
foreach ($pg in $pgs) {
    $vms = $srm.ExtensionData.Protection.ListProtectedVms($pg)
    foreach ($vm in $vms) {
        Write-Host "$($vm.Vm.Name): $($vm.ReplicationState)"
    }
}
```

---

## VRA Health API

```bash
# Check VRA health (no auth required for health endpoint)
curl -sk https://vra-london.example.local/api/rest/vr/health | python3 -m json.tool

# Check VRA API version
curl -sk https://vra-london.example.local/api/rest/vr/deployment | python3 -m json.tool
```

---

## Test Connectivity from Source ESXi to Target VRA

```bash
# From ESXi host shell (SSH to ESXi host)
nc -vz vra-amsterdam.example.local 31031
# Must succeed for replication data transfer

nc -vz vra-amsterdam.example.local 44046
# VRA management port

# Or using vmkping from ESXi:
vmkping -I vmk1 vra-amsterdam.example.local
```

---

## Force Replication Sync (Immediate Sync)

When you need a VM to sync immediately regardless of scheduled interval:

```
vCenter → Site Recovery → Replications → [VM] → Sync Now
```

There is no CLI for immediate sync — use the vCenter UI or the VRA REST API:

```bash
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://vra-london.example.local/api/rest/vr/replications/$REPL_ID/sync"
```
