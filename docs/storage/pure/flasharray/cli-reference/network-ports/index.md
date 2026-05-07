# Network & Ports

> Part of the Pure FlashArray CLI Reference.
## Network Interfaces

```bash
# List all network interfaces (management, replication, iSCSI)
purenetwork list

# Show interface detail
purenetwork list --resolve-hostnames
```

## FC and Ethernet Ports

```bash
# List all array ports
pureport list

# FC ports only
pureport list --type fc

# Ethernet ports only
pureport list --type eth

# Filter to a specific controller
pureport list --raw --filter "name='CT0.FC*'"
pureport list --raw --filter "name='CT1.FC*'"
```

## Initiator (Host) Ports

```bash
# Show connected host initiator ports
pureport list --initiator

# Filter by WWN
pureport list --initiator --raw --filter "initiator.wwn='1000000000000001'"
```

## Bandwidth Monitoring

```bash
pureport monitor --bandwidth
```

## FC Port WWNs

To identify array target WWNs for SAN zoning:

```bash
pureport list --type fc
```

The `wwn` column shows the array-side WWN for each FC port. Zone each host initiator port to the array target WWNs on the corresponding switch.

## iSCSI Port IP Addresses

```bash
purenetwork list
```

iSCSI initiators connect to the array using the IP addresses shown for iSCSI-enabled ports.

## Port Health

```bash
pureport list --type fc
# Check: speed, status — all ports should show expected link speed
```

Any port showing `0Gb` or no speed may indicate a disconnected or failed port.

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Host can't see array via FC | Port WWN not zoned | Verify SAN zoning matches `pureport list --type fc` |
| iSCSI sessions not establishing | IP reachability | Ping array iSCSI IP from host |
| Bandwidth below expected | Port speed | `pureport list --type eth` — check link speed |
| Initiator not registering | WWN mismatch | Verify host HBA WWN vs. registered initiator |
