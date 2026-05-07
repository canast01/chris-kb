# Status & Devices

> Part of the Dell PowerPath CLI Reference.
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
