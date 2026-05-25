# SRDF/S — Encryption

> Part of the [SRDF/S Security](../index.md) reference.

---

## FCIP Encryption

SRDF/E encrypts data over FCIP links using AES-256:

```bash
# Check encryption status per SRDF group
symcfg list -rdfg -v | grep -E "RDF Group|Encryption"

# Enable encryption on an existing group (requires group to be in Split state)
symrdf -g <rdfg> split -noprompt
symrdf -g <rdfg> set encrypt enable
symrdf -g <rdfg> establish -noprompt
```

---

## FC Fabric Zoning

SRDF director ports must be hard-zoned to prevent unauthorised array-to-array communication:

- Create dedicated SRDF zones containing only the SRDF director port WWPNs of the two arrays
- No other initiators/targets in SRDF zones
- Use hard zoning (WWPN-based) — soft zone aliases are acceptable for documentation only
- Zone naming: `SRDF_<source_array_port>_<target_array_port>`

Verify SRDF director port WWPNs:
```bash
symcfg list -rdfg <rdfg> -v | grep "Director"
```
