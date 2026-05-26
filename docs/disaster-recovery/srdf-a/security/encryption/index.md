# SRDF/A — Encryption

> Part of the [SRDF/A](../../index.md) reference.

---

## Encryption In-Flight

SRDF/E (SRDF Encryption) encrypts data over FCIP using AES-256. Verify per SRDF group:

```bash
symcfg list -rdfg -v | grep -i encrypt
# Output should show: Encryption: Enabled
```

---

## Notes

- SRDF/E applies to data transmitted over FCIP links; dark fibre (native FC) does not traverse the WAN and does not require SRDF/E, though physical security of the fibre path should be assured.
- Enabling encryption on a live SRDF group requires no downtime but may briefly increase CPU overhead on the SRDF directors.
- Verify encryption status after any firmware upgrade or RDF group reconfiguration.
