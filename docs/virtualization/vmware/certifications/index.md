---
tags:
  - certifications
  - vmware
---
# VMware Certification

<div class="kb-summary">
VMware Certification reference covering Overview, Core Certification Paths, Daily Study Focus, Useful Commands, Renewal Notes.
</div>

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="exam-tracking/">
  <strong>Exam Tracking</strong>
  <span>Exam scheduling, scores, and certification tracking.</span>
</a>

<a class="kb-card" href="practice-notes/">
  <strong>Practice Notes</strong>
  <span>Practice exam notes and study materials.</span>
</a>

<a class="kb-card" href="products/">
  <strong>Products</strong>
  <span>Product portfolio and certification paths.</span>
</a>

<a class="kb-card" href="review-plan/">
  <strong>Review Plan</strong>
  <span>Study plan and review schedule.</span>
</a>

<a class="kb-card" href="weak-areas/"><strong>Weak Areas</strong><span>Topics needing additional study and focus.</span></a>
<a class="kb-card" href="vcp-dcv/"><strong>VCP-DCV</strong><span>VMware Certified Professional – Data Center Virtualization study notes and exam prep.</span></a>

</div>

## Overview

VMware certifications validate skills in virtualization, storage, networking, and cloud infrastructure using VMware platforms.

## Core Certification Paths

- VCTA Associate
- VCP Professional
- VCAP Advanced Professional
- VCDX Expert

## Daily Study Focus

- Review vSphere architecture
- Practice host and cluster configuration
- Study storage and networking design
- Review troubleshooting scenarios

## Useful Commands

```bash
esxcli system version get
vim-cmd hostsvc/hostsummary
esxcli network nic list
esxcli storage core device list
```


```text title="Expected output"
Product: VMware ESXi
Version: 7.0.3
Build: 19193900
Update: 3
Release: VMware ESXi 7.0 U3 (build 19193900)

Host Summary:
   config.hardware.version = vmx-18
   config.product.name = VMware ESXi
   config.product.version = 7.0.3
   runtime.powerState = poweredOn
   runtime.connectionState = connected

Name          PCI           Driver      Admin Status  Runtime State  Speed    Duplex  MTU  MAC Address
vmnic0        0000:02:00.0  bnx2x       Up            Up              10000    Full    1500 00:0a:95:9d:68:a2
vmnic1        0000:02:00.1  bnx2x       Up            Down            10000    Full    1500 00:0a:95:9d:68:a3
vmnic2        0000:03:00.0  ixgbe       Up            Up              1000     Full    1500 00:50:56:c0:00:08

Device Name  Display Name                    Size      Device Type  Multipath Plugin  Path Count  Vendor   Model
naa.6001405  NETAPP LUN 1                    1099.5GB  SSD          NMP              2            NETAPP   LUN
naa.6001406  NETAPP LUN 2                    549.8GB   SSD          NMP              2            NETAPP   LUN
naa.6001407  Local SSD                       279.9GB   SSD          NMP              1            ATA      Samsung
```

!!! warning "Common errors"
    **`Unknown command at token esxcli`** — Verify esxcli is in PATH or run commands from an ESXi host shell, not a vCenter server.
    **`Error: Unable to connect to the local hostd agent`** — Ensure the hostd service is running with `systemctl status hostd` and restart if needed.
## Renewal Notes

VMware certifications may require continuing education or recertification depending on level.
