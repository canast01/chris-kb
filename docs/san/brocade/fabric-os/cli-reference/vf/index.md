# Virtual Fabrics (VF)

> Part of the Brocade Fabric OS CLI Reference.

Virtual Fabrics partition a physical Brocade chassis into multiple logical switches (Logical Switches), each with its own Fabric ID (FID) and independent FLOGI domain.

## Virtual Fabric Status

```bash
lscfg --show           # list all logical switches and their FIDs
setContext <fid>       # switch CLI context to a specific logical switch
```

## Create a Logical Switch

```bash
lscfg --create <fid> [-base]    # -base creates a base fabric
```

## Delete a Logical Switch

```bash
lscfg --delete <fid>
```

## Assign a Port to a Logical Switch

```bash
lscfg --config <fid> -port <slot/port>
```

## XISL (Inter-Switch Links Between VFs)

XISLs allow different logical switches on the same chassis to communicate:

```bash
lscfg --port <slot/port> -lport <fid>    # assign port as XISL
```

## Context Switching

```bash
setContext <fid>       # enter the context of logical switch <fid>
# All subsequent commands run in context of that FID
setContext 128         # 128 = default/base fabric
```

## Check Port Assignments per FID

```bash
lscfg --show -slot <slot>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Device not visible | Wrong FID context | `setContext <fid>` then `switchshow` |
| Port in wrong FID | `lscfg --show` | Reassign port to correct FID |
| VF not enabled | License | Verify VF license with `licenseShow` |
| XISL down | Port state | Check port with `portShow` |
