# Device Groups (Legacy)

> Part of the Dell PowerMax CLI Reference (SYMCLI). Device groups are the legacy SYMCLI grouping mechanism (pre-Unisphere for PowerMax). For current deployments, prefer Storage Groups via `symsg`. Device groups remain relevant for SRDF operations and Solutions Enabler scripts.

## List and Inspect

```bash
# List all device groups on an array
symdg list -sid <sid>
symdg list -sid <sid> -v

# Show contents of a specific device group
symdg show <dg_name> -sid <sid>
symdg show <dg_name> -sid <sid> -v

# List device groups containing a specific device
symdg list -dev <devname> -sid <sid>
```

## Create and Delete

```bash
# Create a regular device group
symdg create <dg_name> -type regular -sid <sid>

# Create an RDF device group (for SRDF operations)
symdg create <dg_name> -type RDF1 -sid <sid>   # R1 side
symdg create <dg_name> -type RDF2 -sid <sid>   # R2 side

# Delete a device group (must be empty)
symdg delete <dg_name> -sid <sid>
```

## Add and Remove Devices

```bash
# Add a device to a group
symdg -g <dg_name> add dev <devname> -sid <sid>

# Add a range of devices
symdg -g <dg_name> add dev <start_dev>:<end_dev> -sid <sid>

# Remove a device from a group
symdg -g <dg_name> remove dev <devname> -sid <sid>

# List devices in the group
symdev list -g <dg_name> -sid <sid>
```

## SRDF Operations via Device Group

```bash
# Check SRDF state for all devices in a group
symrdf -g <dg_name> -sid <sid> query

# Suspend SRDF replication for the group
symrdf -g <dg_name> -sid <sid> suspend -noprompt

# Establish / re-establish replication
symrdf -g <dg_name> -sid <sid> establish -noprompt

# Failover to R2 (planned)
symrdf -g <dg_name> -sid <sid> failover -noprompt

# Failback to R1
symrdf -g <dg_name> -sid <sid> restore -noprompt
```
