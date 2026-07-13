---
tags:
  - vcenter
  - operations
description: "Top-10 vCenter commands for appliance management, inventory queries, and service control via govc and dcli."
---
# vCenter Cheat Sheet

*Applies to: All products*

<div class="kb-summary">
Top-10 vCenter commands for appliance management, inventory queries, and service control via <code>govc</code> and <code>dcli</code>.
</div>
![vCenter Cheat Sheet](../../assets/reference-cheat-sheets-vcenter.svg)

## Common commands

```bash
# Connection (set once per session)
export GOVC_URL=https://vcenter.lab.local
export GOVC_USERNAME=administrator@vsphere.local
export GOVC_PASSWORD=VMware1!
export GOVC_INSECURE=true                      # skip TLS verify in lab

# Inventory
govc about                                     # vCenter version and build
govc ls /DC/host                               # list clusters and hosts
govc ls /DC/vm                                 # list all VMs
govc find / -type d                            # all datacenters and folders

# VMs
govc vm.info /DC/vm/my-vm                      # power state, CPU, mem, IPs
govc vm.power -on /DC/vm/my-vm                 # power on
govc vm.power -off -force /DC/vm/my-vm         # force power off
govc vm.clone -vm /DC/vm/template /DC/vm/clone # clone from template

# Hosts and clusters
govc host.info /DC/host/cluster/esx01          # host summary (CPU, mem, version)
govc cluster.usage /DC/host/cluster            # cluster capacity and usage

# Datastores
govc datastore.info /DC/datastore/vsanDS       # type, capacity, free
govc datastore.ls /DC/datastore/vsanDS         # list files on datastore
```


```text title="Expected output"
# about
Name:         vCenter Server
Vendor:       VMware
Version:      7.0.3
Build:        19480866
OS type:      linux64
API type:     VirtualCenter
API version:  7.0.3.0

# ls /DC/host
Cluster-01
Cluster-02

# ls /DC/vm
my-vm
web-server-01
db-server-02
...

# find / -type d
/DC
/DC/host
/DC/host/Cluster-01
/DC/host/Cluster-02
/DC/vm
/DC/datastore

# vm.info /DC/vm/my-vm
Name:           my-vm
Path:           /DC/vm/my-vm
UUID:           502e8e3d-1234-5678-90ab-cdef12345678
Guest OS:       ubuntu64Guest
Memory:         8192 MB
CPU:            4
Power state:    poweredOn
IP addresses:   192.168.1.45, fe80::250:56ff:fe9a:b1c2

# vm.power -on /DC/vm/my-vm
Powering on /DC/vm/my-vm...

# vm.power -off -force /DC/vm/my-vm
Powering off /DC/vm/my-vm...

# vm.clone -vm /DC/vm/template /DC/vm/clone
Cloning /DC/vm/template to /DC/vm/clone...
Clone complete

# host.info /DC/host/cluster/esx01
Name:                esx01.lab.local
Hostname:            esx01.lab.local
Version:             7.0.3
Build:               19482429
CPU Model:           Intel(R) Xeon(R) CPU E5-2680 v4
CPU Cores:           16
Memory:              262144 MB
Power state:         poweredOn

# cluster.usage /DC/host/cluster
Name:               Cluster-01
CPU Usage:          45600 MHz / 153600 MHz (29.7%)
Memory Usage:       512 GB / 768 GB (66.7%)
```

!!! warning "Common errors"
    **`Error: Post "https://vcenter.lab.local/sdk": dial tcp: lookup vcenter.lab.local: no such host`** — Verify the vCenter hostname is resolvable and reachable, or update GOVC_URL to the correct IP address.
    **`Error: Login failed with error: Invalid credentials`** — Confirm GOVC_USERNAME and GOVC_PASSWORD are correct and the account has not been locked due to failed login attempts.
    **`Error: The object 'vm' of type 'VirtualMachine' was not found`** — Verify the VM path is correct by running `govc ls /DC/vm` to list available VMs and check for typos in the path.
## Appliance (VCSA shell)

```bash
# Run on VCSA via SSH
service-control --status                       # all VCSA service states
service-control --start vpxd                   # start vCenter service
vmon-cli -l                                    # list all services with health
dcli com vmware cis tagging tag list           # list all tags via dcli
```


```text title="Expected output"
SERVICE                                        RUNNING  ENABLED
applmgmt                                       true     true
certificatemanagement                          true     true
eam                                            true     true
envoy                                          true     true
vapi-endpoint                                  true     true
vpxd                                           true     true
vpxd:vpxd-svcs                                 true     true
vsphere-client                                 true     true
vsphere-ui                                     true     true
wcp                                            false    false
...

Service 'vpxd' is already running.

Service                                        Health
applmgmt                                       HEALTHY
certificatemanagement                          HEALTHY
eam                                            HEALTHY
envoy                                          HEALTHY
vpxd                                           HEALTHY
vsphere-client                                 HEALTHY
vsphere-ui                                      HEALTHY

Tag: prod-vms (ID: urn:vmomi:InventoryServiceTag:12a4c5d8-9f2e-4b1a-8c3e-7d6f5a2b1c9e:GLOBAL)
Tag: backup-exclude (ID: urn:vmomi:InventoryServiceTag:3f7e2a1d-5c4b-9a8f-6e3d-2c1b4a5f8e7d:GLOBAL)
Tag: maintenance (ID: urn:vmomi:InventoryServiceTag:8b2f4e9c-1a7d-3f5e-9b6c-4d8a2e1f7c3b:GLOBAL)
```

!!! warning "Common errors"
    **`Error: Could not connect to service-control. Is VCSA running?`** — Ensure you are connected via SSH to the VCSA appliance itself, not a vCenter Server running on Windows.
    **`Error: Unknown service 'vpxd'. Run 'service-control --list' to see available services.`** — Use the exact service name from `service-control --list` output; service names are case-sensitive.
    **`Error: Authentication failed for dcli command.`** — Run `dcli +server localhost +username administrator@vsphere.local` first to authenticate, or ensure your VCSA credentials are correct.
## See also

- [vCenter Operations](../../../virtualization/vmware/products/vcenter/operations/procedures/)
- [vCenter Troubleshooting](../../../virtualization/vmware/products/vcenter/troubleshooting/common-issues/)
- [PowerCLI Cheat Sheet](../powercli/)
