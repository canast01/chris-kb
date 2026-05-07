# ISLs & Trunking

> Part of the Cisco MDS NX-OS CLI Reference.

## ISL Status

```bash
show topology          # fabric-wide ISL topology
show trunk             # trunk port states and allowed VSANs
show interface trunk   # trunk interface detail
```

## ISL Interface Status

```bash
show interface fc<slot/port>            # single port detail
show interface brief | include E        # E-port (ISL) ports only
```

## Configure a TE Port (Trunking ISL)

```bash
interface fc<slot/port>
  switchport mode TE
  switchport trunk allowed vsan <vsan_id>
  no shutdown
```

## Restrict VSANs on an ISL

```bash
interface fc<slot/port>
  switchport trunk allowed vsan add <vsan_id>
  switchport trunk allowed vsan remove <vsan_id>
```

## ISL Error Counters

```bash
show interface fc<slot/port> counters          # TX/RX frames, errors
show interface fc<slot/port> counters errors
```

Watch for:
- `link-failures` — physical link instability
- `loss-of-sync` — signal issues; check SFP and cable
- `input-crc` — bad frames; replace SFP or cable

## Port Channel (LAG for ISLs)

```bash
# Create a port channel
interface port-channel <id>
  switchport mode E
  no shutdown

# Add FC ports to channel
interface fc<slot/port>
  channel-group <id>
  no shutdown

show port-channel summary
show interface port-channel <id>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| ISL down | Port mode and status | Verify `switchport mode TE/E` |
| VSAN not crossing ISL | Trunk allowed VSANs | Add VSAN to trunk: `vsan add` |
| CRC errors | SFP and cable | Replace SFP; check cable quality |
| Port channel member not up | Channel-group config | Verify all members in same channel |
