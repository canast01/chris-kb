# Discovery & Array Info

> Part of the Dell PowerMax CLI Reference (SYMCLI). Run `symcfg discover` when a new array is added to the environment or after a network change that affects Solutions Enabler connectivity.

## Array Discovery

```bash
# Discover all arrays visible to this Solutions Enabler host
symcfg discover

# List all known arrays
symcfg list

# List with detailed info (model, microcode, capacity)
symcfg list -v

# Show full array configuration
symcfg -sid <sid> show
symcfg -sid <sid> list -v
```

## Directors and Front-End Ports

```bash
# List all directors
symcfg -sid <sid> list -dir all

# List all ports on all directors
symcfg -sid <sid> list -port all

# Show specific director details
symcfg -sid <sid> show -dir <director_id>

# Show FA (Fibre Channel front-end) port details
symcfg -sid <sid> show -dir <director_id> -p <port_number>

# List only online FA ports
symcfg -sid <sid> list -fa -online
```

## Cache and Memory

```bash
# Show cache configuration and usage
symcfg -sid <sid> list -cache

# Show all storage resource pools (SRP)
symcfg -sid <sid> list -pool -all

# Show thin pool subscription and usage
symcfg -sid <sid> show -pool -thin -demand
```

## Array Software and Licenses

```bash
# Show HYPERMAX OS version
symcfg -sid <sid> list | grep -i "microcode\|Enginuity\|HYPERMAX"

# Show installed feature licenses
symlmf -sid <sid> list

# Show available capacity by SRP
symcfg -sid <sid> list -srp
```

## SymmWin / Gatekeeper

```bash
# Check Solutions Enabler connection method to array
syminq -symmids

# Show local gatekeeper devices
symgate list -sid <sid>

# Verify SE version
symcfg -V
```

## Quick Reference

| Task | Command |
|---|---|
| Discover arrays | `symcfg discover` |
| List all arrays | `symcfg list` |
| Show array detail | `symcfg -sid <sid> show` |
| List directors | `symcfg -sid <sid> list -dir all` |
| List all ports | `symcfg -sid <sid> list -port all` |
| Show cache usage | `symcfg -sid <sid> list -cache` |
| Show SRP pools | `symcfg -sid <sid> list -pool -all` |
