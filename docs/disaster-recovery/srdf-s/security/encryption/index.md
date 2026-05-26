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
