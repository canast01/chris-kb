# Interfaces & Ports

> Part of the Cisco MDS NX-OS CLI Reference.

## Interface Status

```bash
# Summary of all interfaces
show interface brief

# Detailed single port
show interface fc<slot/port>

# Error counters
show interface fc<slot/port> counters
show interface fc<slot/port> counters errors

# Transceiver / SFP details
show interface fc<slot/port> transceiver
```

## Port Modes

| Mode | Use Case |
|---|---|
| F | Host / initiator (N_Port) |
| E | ISL to another switch (E_Port) |
| TE | Trunking ISL (VSAN-aware) |
| NP | N-Port Virtualization (NPV mode) |
| auto | Auto-detect (default) |
| SD | SPAN destination |

## Configure a Port

```bash
interface fc<slot/port>
  switchport mode F         # force F-port for host
  shutdown
  no shutdown
```

## Administratively Enable/Disable a Port

```bash
interface fc<slot/port>
  shutdown
  no shutdown
```

## Range Operations

```bash
# Apply config to a range of ports
interface fc<slot/port> - fc<slot/port>
  shutdown
```

## FC Domain

```bash
show fcdomain               # domain IDs across fabric
show fcdomain domain-list   # all domain IDs in VSAN
```

Each switch in a fabric must have a unique domain ID per VSAN.

## Error Counter Reference

| Counter | Cause | Action |
|---|---|---|
| link-failures | Cable/SFP; port resets | Replace SFP; check cable |
| loss-of-sync | Signal quality | Check SFP power levels |
| input-crc | Bad frames | Replace SFP; check cable |
| bb-credit-zero | Buffer-to-buffer credit depleted | Increase BB credits; check ISL design |

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Port stays down | SFP, cable, peer | `show interface` — check reason |
| Port mode mismatch | Expected F, got E | Force mode: `switchport mode F` |
| CRC errors | SFP quality | Replace SFP |
| No FLOGI on F-port | Host HBA not sending login | Check host HBA and driver |
