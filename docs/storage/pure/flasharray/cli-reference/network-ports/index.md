# Network & Ports

> Part of the [Pure FlashArray CLI Reference](../).

---

## purenetwork — Network

Displays management and replication network configuration.

```bash
purenetwork list
```

---

## pureport — Ports

Displays array host connection ports.

```bash
pureport list
pureport list --initiator
pureport list --type fc
pureport list --type eth
pureport list --raw --filter "name='*FC*'"
pureport list --raw --filter "name='*ETH*'"
pureport list --raw --filter "name='CT0.FC*'"
pureport list --initiator --raw --filter "name='CT0.FC0'"
pureport list --initiator --raw --filter "initiator.wwn='1000000000000001'"
pureport monitor --bandwidth
```
