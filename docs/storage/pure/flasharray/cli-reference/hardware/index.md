# Drives & Hardware

> Part of the [Pure FlashArray CLI Reference](../).
---

## puredrive — Drives

Displays information about Flash Drives and NVRAM modules.

```bash
puredrive list
puredrive list --spec
puredrive list --total
puredrive list CH0.BAY10
puredrive list CH0.BAY10 --pack
puredrive admit
```

---

## purehw — Hardware

Displays hardware components and manages visual identification.

```bash
purehw list
purehw list --spec
purehw list --type bay
purehw list --type bay --spec
purehw list --type ct
purehw list --type eth
purehw list --type fc
purehw list --type fan
purehw list --type psu
purehw list --type nvram
purehw list --type sas
purehw list --spec --type drive
purehw list CT0 --spec
purehw list CT0.FC0
```
