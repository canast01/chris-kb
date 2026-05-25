# SRM Troubleshooting — Diagnostics

## Log Locations

```text
Windows SRM Server:
  C:\ProgramData\VMware\VMware vCenter Site Recovery Manager\Logs\vmware-dr.log
  C:\ProgramData\VMware\VMware vCenter Site Recovery Manager\Logs\vmware-drconfig.log

Linux SRM Appliance (8.8+):
  /var/log/vmware/dr/vmware-dr.log

vSphere Replication Appliance:
  /var/log/vmware/hbr/

SRA logs (Dell PowerMax SRA example):
  C:\Program Files\VMware\VMware vCenter Site Recovery Manager\storage\sra\dell-emc-srm\logs\
```

## Support Bundle Collection

Collect before opening a Broadcom support ticket:

```powershell
# Trigger SRM support bundle collection
# SRM UI → Help → Collect Support Bundle
# Or via API:
Invoke-WebRequest -Uri "https://<srm-appliance>:443/api/v1/support-bundle" -Method POST
```
