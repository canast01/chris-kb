# Dell PowerPath CLI Reference

Commonly used `powermt` commands for managing Dell PowerPath multipathing on Linux and Windows hosts.

---

## Status & Overview

```bash
# Overall summary
powermt display
powermt display dev=all
powermt display dev=all | head -100

# Path summary per device
powermt display options

# Display dead paths
powermt display dead

# Display powerpath version
powermt version

# Display registration
powermt display reg
```

---

## Devices

```bash
# List all devices
powermt display dev=all

# Single device
powermt display dev=emcpower<n>
powermt display dev=emcpower<n>a

# Logical device info
powermt display ldev

# Device path details
powermt display dev=emcpower<n> | grep -E "path|state|mode"

# Class info
powermt display class=clariion
powermt display class=symmetrix
powermt display class=vplex
```

---

## Paths

```bash
# Count alive paths per device
powermt display dev=all | grep -E "emcpower|alive|dead"

# Restore dead paths
powermt restore

# Remove dead paths
powermt remove dead

# Path failover
powermt fail dev=emcpower<n> path=<hba_port>

# Unblock a failed path
powermt unblock dev=emcpower<n> path=<hba_port>
```

---

## HBA Ports

```bash
# Show HBA ports
powermt display hba
powermt display port
powermt display hba=<hba_id>
```

---

## Load Balancing & Policies

```bash
# Show load balancing policy
powermt display dev=emcpower<n> | grep -i policy

# Set policy on a device
powermt set policy=<policy> dev=emcpower<n>
# Policies: co (CLARiiON Optimized), rr (Round Robin), si (Single Initiator), etc.

# Set globally
powermt set policy=co dev=all class=clariion
```

---

## Checks & Validation

```bash
# Check all paths
powermt check

# Check specific device
powermt check dev=emcpower<n>

# Verify consistency
powermt display options

# Show configuration file
cat /etc/powermt.custom
```

---

## Configuration Management

```bash
# Save configuration
powermt save
powermt save force

# Load / restore config
powermt restore

# Reconfig (after new device attachment)
powermt config

# Remove stale devices
powermt remove dev=emcpower<n>
powermt remove dead
```

---

## Windows PowerPath

```powershell
# From PowerShell / CMD
powermt display
powermt display dev=all
powermt display class=symmetrix

powermt check
powermt restore
powermt save

# PowerPath service
Get-Service -Name "EMCPower*"
Restart-Service -Name "EMCPower*"
```

---

## Common Checks

```bash
# Quick health check sequence
powermt display dev=all | grep -c "alive"
powermt display dev=all | grep -c "dead"
powermt display dead
powermt check
powermt restore

# Count paths per device
powermt display dev=all | awk '/emcpower/{dev=$1} /alive/{count++} /dead/{dead++} /^$/{if(dev) print dev, "alive:"count, "dead:"dead; dev=""; count=0; dead=0}'
```
