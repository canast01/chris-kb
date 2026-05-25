# VMware Logs Quick Reference

```text
┌────────────────────────────────┬──────────────────────┬─────────────────────────────┐
│   Component                    │  Log Path            │  Key Events / grep patterns │
├────────────────────────────────┼──────────────────────┼─────────────────────────────┤
│ ESXi – host daemon             │ /var/log/hostd.log   │ VM power, config, errors    │
│ ESXi – vCenter agent           │ /var/log/vpxa.log    │ vCenter comms, reconnects   │
│ ESXi – kernel                  │ /var/log/vmkernel.log│ Storage, network, hardware  │
│ ESXi – hardware events         │ /var/log/vobd.log    │ Disk, NIC, PSU events       │
│ ESXi – auth                    │ /var/log/auth.log    │ Login attempts, SSH         │
├────────────────────────────────┼──────────────────────┼─────────────────────────────┤
│ vCenter – server daemon        │ /var/log/vmware/vpxd/│ Inventory, task, alarm logs │
│ vCenter – SSO                  │ /var/log/vmware/sso/ │ Login failures, token errors│
│ vCenter – appliance mgmt       │ /var/log/vmware/appl.│ Backup, upgrade, cert events│
└────────────────────────────────┴──────────────────────┴─────────────────────────────┘
  Collect: vCenter → Administration → Support → Export Support Bundle
           ESXi   → Right-click host → Export System Logs
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

## vCenter Appliance Log Locations

```bash
/var/log/vmware/vpxd/          # vCenter Server daemon logs
/var/log/vmware/sso/           # SSO and identity service logs
/var/log/vmware/vapi/          # vAPI endpoint logs
/var/log/vmware/applmgmt/      # Appliance management logs
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

## Using Aria Operations for Logs

- Search by hostname, IP, or keyword
- Set a time range before searching
- Filter by log source (hostd, vpxa, vmkernel)
- Export results as CSV for evidence or support cases
