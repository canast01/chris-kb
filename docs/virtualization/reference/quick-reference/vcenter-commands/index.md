# vCenter Service Commands

> SSH to the vCenter appliance before running these commands.

```mermaid
flowchart LR
    Service_Commands["Service Commands"]
    Service_Commands --> S0["Check All Services"]
    Service_Commands --> S1["Start All Services"]
    Service_Commands --> S2["Stop All Services"]
    Service_Commands --> S3["Restart All Services"]
    Service_Commands --> S4["Restart a Single Service"]
    Service_Commands --> S5["Check Disk Space"]
    Service_Commands --> S6["Check Uptime"]
    Service_Commands --> S7["Check Certificate Status"]
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
