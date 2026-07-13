---
tags:
  - reference
description: "VMware Logs Quick Reference reference covering ESXi Log Locations, vCenter Appliance Log Locations, Collecting a vCenter Support Bundle, Collecting an..."
---
# VMware Logs Quick Reference

<div class="kb-summary">
VMware Logs Quick Reference reference covering ESXi Log Locations, vCenter Appliance Log Locations, Collecting a vCenter Support Bundle, Collecting an ESXi Support Bundle, Using Aria Operations for Logs.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

esxi_log_locations: "ESXi Log Locations" {shape: rectangle}
vcenter_appliance_log_locations: "vCenter Appliance Log Locations" {shape: rectangle}
collecting_a_vcenter_support_bundle: "Collecting a vCenter Support Bundle" {shape: rectangle}
collecting_an_esxi_support_bundle: "Collecting an ESXi Support Bundle" {shape: rectangle}
using_aria_operations_for_logs: "Using Aria Operations for Logs" {shape: rectangle}

esxi_log_locations -> vcenter_appliance_log_locations: uses
vcenter_appliance_log_locations -> collecting_a_vcenter_support_bundle: uses
collecting_a_vcenter_support_bundle -> collecting_an_esxi_support_bundle: uses
collecting_an_esxi_support_bundle -> using_aria_operations_for_logs: uses
```

## ESXi Log Locations

```bash
/var/log/hostd.log       # Host daemon — VM and host operations
/var/log/vpxa.log        # vCenter agent on the host
/var/log/vmkernel.log    # Kernel-level events — storage, network, hardware
/var/log/vobd.log        # Hardware and storage event observer
/var/log/syslog.log      # General system log
/var/log/auth.log        # Authentication events
```


```text title="Expected output"
(no output — command completes silently)
```
## vCenter Appliance Log Locations

```bash
/var/log/vmware/vpxd/          # vCenter Server daemon logs
/var/log/vmware/sso/           # SSO and identity service logs
/var/log/vmware/vapi/          # vAPI endpoint logs
/var/log/vmware/applmgmt/      # Appliance management logs
```


```text title="Expected output"
(no output — these are directory path references only)
```
## Collecting a vCenter Support Bundle

In vSphere Client: **Menu** → **Administration** → **Support** → **Export Support Bundle**

Or from VAMI at `https://<vcenter>:5480` → **Support**

## Collecting an ESXi Support Bundle

Via vSphere Client: Right-click host → **Export System Logs**

Or via SSH:
```bash
vm-support -n <bundle-name>
```


```text title="Expected output"
Generating support bundle: vm-support-2024-01-15-14-32-45.tar.gz
Collecting system logs...
Collecting configuration files...
Collecting performance data...
Collecting network diagnostics...
Bundle generation complete.
Bundle location: /var/log/vm-support-2024-01-15-14-32-45.tar.gz
Bundle size: 487.3 MB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vm-support: command not found` | Ensure you are running this command on an ESXi host or vCenter Server where vm-support is installed, or use the full path `/usr/lib/vmware/bin/vm-support`. |
    | `Permission denied` | Run the command with root privileges using `sudo vm-support -n <bundle-name>` or log in as root. |
    | `Error: Bundle name contains invalid characters` | Use only alphanumeric characters, hyphens, and underscores in the bundle name; avoid spaces and special characters. |
## Using Aria Operations for Logs

- Search by hostname, IP, or keyword
- Set a time range before searching
- Filter by log source (hostd, vpxa, vmkernel)
- Export results as CSV for evidence or support cases
