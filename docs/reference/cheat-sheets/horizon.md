---
tags:
  - horizon
  - operations
---
# Horizon Cheat Sheet

<div class="kb-summary">
Top-10 Horizon commands for desktop pool management, agent control, and session operations via <code>vdmadmin</code> and PowerShell.
</div>
![Horizon Cheat Sheet](../../assets/reference-cheat-sheets-horizon.svg)

## vdmadmin (Connection Server command line)

```bash
# Run on Connection Server as Administrator
vdmadmin -L                                    # list all pools and desktops
vdmadmin -S -pool_id mypool                    # summary of pool mypool
vdmadmin -N -pools                             # entitlements (user→pool mappings)

# Session control
vdmadmin -O -u domain\\username               # log off all sessions for user
vdmadmin -D -desktop desktop01 -u domain\\user # unassign dedicated desktop

# Agent and machine ops
vdmadmin -A -dns desktop01.lab.local          # machine detail (state, pool, user)
vdmadmin -M -machine desktop01 -remove        # remove machine from inventory
```


```text title="Expected output"
Pool: mypool
  Display Name: My Pool
  Type: Dedicated
  State: Available
  Total Machines: 24
  Available: 18
  In Use: 6

Pool Summary for mypool:
  Pool ID: mypool
  Machine Type: Windows 10
  Provisioning: Manual
  Sessions: 6/24

User Entitlements:
  domain\jsmith → mypool (Dedicated)
  domain\achen → mypool (Floating)
  domain\mrodriguez → engineering_pool (Dedicated)
  ...

User domain\username logged off from 2 sessions.

Desktop desktop01 unassigned from user domain\user.

Machine Details: desktop01.lab.local
  State: Available
  Pool: mypool
  Current User: None
  IP Address: 192.168.1.45
  Last Heartbeat: 2024-01-15 14:32:18

Machine desktop01 removed from inventory.
```

!!! warning "Common errors"
    **`Error: Pool mypool not found`** — Verify the pool ID exists with `vdmadmin -L` and check for typos in the pool name.
    **`Error: Access Denied. Administrator privileges required`** — Run the Command Prompt as Administrator or use an account with Horizon administrator role.
    **`Error: Machine desktop01 is currently in use by domain\username`** — Log off the user first with `vdmadmin -O -u domain\username` before removing the machine.
## PowerShell (VMware.Hv.Helper module)

```powershell
Import-Module VMware.Hv.Helper
Connect-HVServer -Server cs.lab.local -User admin -Password VMware1!

# Pools and desktops
Get-HVPool                                     # list all desktop and app pools
Get-HVMachine -PoolName mypool                 # machines in a pool
Get-HVLocalSession                             # active sessions on this CS

# Machine lifecycle
Reset-HVMachine -MachineName desktop01         # reboot machine
Remove-HVMachine -MachineName desktop01        # delete machine from pool
Add-HVMachine -PoolName mypool -MachineCount 5 # add machines to pool
```

## See also

- [Horizon Operations](../../../virtualization/vmware/horizon/operations/procedures/)
- [Horizon Troubleshooting](../../../virtualization/vmware/horizon/troubleshooting/common-issues/)
