# vCenter Service Commands

> SSH to the vCenter appliance before running these commands.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                  vCenter Command Categories                             │
├──────────────────────┬──────────────────────────────────────────────────┤
│  Services            │  Inventory (PowerCLI)                            │
├──────────────────────┼──────────────────────────────────────────────────┤
│ service-control      │ Get-VMHost | Select Name,Version,State           │
│  --status            │ Get-Cluster | Select Name,HAEnabled,DrsEnabled   │
│  --start --all       │ Get-Datastore | Select Name,FreeSpaceGB          │
│  --stop --all        │ Get-VM | Where PowerState -ne PoweredOn          │
│  --restart vpxd      │ Get-VIPermission | Select Entity,Principal,Role  │
├──────────────────────┼──────────────────────────────────────────────────┤
│  System              │  Certificates                                    │
├──────────────────────┼──────────────────────────────────────────────────┤
│ df -h                │ VAMI :5480 → Certificate Management              │
│ uptime               │ vecs-cli entry list --store TRUSTED_ROOTS        │
│ date                 │ openssl s_client -connect vcenter:443            │
└──────────────────────┴──────────────────────────────────────────────────┘
```
## Check All Services

```bash
service-control --status
```

## Start All Services

```bash
service-control --start --all
```

## Stop All Services

```bash
service-control --stop --all
```

## Restart All Services

```bash
service-control --stop --all && service-control --start --all
```

## Restart a Single Service

```bash
service-control --restart vmware-vpxd
service-control --restart vmware-sts
service-control --restart vmware-lookupsvc
```

## Check Disk Space

```bash
df -h
```

## Check Uptime

```bash
uptime
```

## Check Certificate Status

Access VAMI at `https://<vcenter>:5480` → **Certificate Management**

## When Not to Restart Services

- If disk partitions are full — free space first
- If a restore is needed — restarting services will not fix a corrupt database
- During active vMotion or vSAN resync operations without change approval

## Escalation

If services do not recover after a restart, collect a support bundle from VAMI and open a VMware support case.
