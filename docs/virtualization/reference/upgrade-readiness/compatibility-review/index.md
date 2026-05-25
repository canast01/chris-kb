# Compatibility Review

Verify version compatibility across the full VMware stack before any upgrade. Upgrading out of order or with incompatible versions causes silent failures and unsupported configurations.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                     Compatibility Check Matrix                           │
├─────────────────────────┬────────────────────────────────────────────────┤
│  Check                  │  Source                                        │
├─────────────────────────┼────────────────────────────────────────────────┤
│ vCenter ↔ ESXi          │ interopmatrix.vmware.com                       │
│ vCenter ↔ NSX           │ NSX install guide + interop matrix             │
│ VxRail ↔ vCenter/ESXi   │ VxRail release notes (VxRail owns combination) │
│ Aria LCM ↔ Aria products│ Aria LCM release notes                         │
│ HBA/NIC drivers         │ VMware HCL (vmware.com/resources/compatibility)│
│ Storage array           │ VMware HCL + array vendor support matrix       │
│ Veeam                   │ veeam.com/kb2443                               │
│ VM Tools / HW version   │ PowerCLI: Get-VM | ToolsVersionStatus          │
│ Certificates            │ Check expiry before window: openssl s_client   │
└─────────────────────────┴────────────────────────────────────────────────┘
```
## VMware Product Interoperability Matrix

Primary source: [VMware Product Interoperability Matrix](https://interopmatrix.vmware.com/)

Required checks:
- vCenter ↔ ESXi (vCenter must be ≥ ESXi version)
- vCenter ↔ NSX (see NSX install guide for exact vCenter version)
- vCenter ↔ SRM + vSphere Replication
- vSAN ↔ ESXi (same version as ESXi)
- VxRail ↔ vCenter / ESXi / vSAN (VxRail owns this combination — check VxRail release notes)
- Aria LCM ↔ all Aria products (Ops, Automation, Log Insight, vRNI)

## Hardware Compatibility

```powershell
# Check current ESXi version on all hosts
Get-VMHost | Select-Object Name, Version, Build |
    Sort-Object Version

# Get NIC and HBA driver/firmware versions on a host
esxcli software vib list | grep -i "net-\|scsi-\|nfnic\|lpfc\|bnx"
```

Check [VMware HCL](https://www.vmware.com/resources/compatibility/search.php) for:
- Server model + ESXi target version
- NIC model + driver version
- HBA model + driver/firmware version
- Storage array (array model, VAAI support, multipath plugin version)

## Third-Party Tool Compatibility

| Tool | Compatibility Check Location |
|---|---|
| Veeam | [Veeam compatibility matrix](https://www.veeam.com/kb2443) |
| Commvault | Commvault Feature Release notes |
| Veritas NetBackup | [Veritas SORT](https://sort.veritas.com/) |
| Aria Operations | Aria Ops release notes + interop matrix |
| CrowdStrike / AV agents | Vendor ESXi support matrix |
| Dell VxRail | VxRail release notes (VxRail owns ESXi + vCenter + vSAN versions) |
| RecoverPoint | EMC support matrix for RP + vCenter |

## VMware Tools and VM Hardware

```powershell
# VMs with VMware Tools older than target version
Get-VM | Where-Object { $_.Guest.ToolsVersionStatus -eq "guestToolsNeedUpgrade" } |
    Select-Object Name, @{N="ToolsVersion"; E={ $_.Guest.ToolsVersion }} |
    Measure-Object | Select-Object Count

# VMs with hardware version below target
$targetHWVersion = 19   # vSphere 7.0 U3+ = HW19, vSphere 8 = HW21
Get-VM | Where-Object { ($_.HardwareVersion -replace "vmx-", "") -lt $targetHWVersion } |
    Measure-Object | Select-Object Count
```

VMware Tools and VM hardware upgrades are independent of ESXi upgrade — schedule separately after host upgrade.

## Certificate Compatibility

```powershell
# Check VMCA certificate expiry before upgrade (VMCA certs expire 2 years from issuance)
Get-VIObject -MoRef (Get-View ServiceInstance).Content.CertificateManager |
    Invoke-Method -Name QueryCertificates
```

Also verify: custom certificates on VCSA, NSX Manager, and Aria products have not expired.

## Compatibility Review Sign-Off Checklist

| Check | Verified By | Date |
|---|---|---|
| vCenter ↔ ESXi interop confirmed | | |
| NSX ↔ vCenter interop confirmed | | |
| VxRail release compatibility confirmed | | |
| HCL check: server model | | |
| HCL check: NIC drivers | | |
| HCL check: HBA drivers | | |
| HCL check: storage array | | |
| Veeam compatibility confirmed | | |
| Aria LCM interop confirmed | | |
| VM Tools count (plan upgrade schedule) | | |
| Certificates valid through upgrade window | | |
