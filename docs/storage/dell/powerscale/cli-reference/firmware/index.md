# Firmware, Upgrades & Support

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

## Firmware & Upgrades

```bash
# Current version
isi version

# Drive firmware
isi devices drives firmware list
isi devices drives firmware upgrade start

# Cluster upgrade (OneFS rolling)
isi upgrade cluster --upgrade-image <image>
isi upgrade cluster check
isi upgrade nodes list
isi upgrade nodes view <node_id>
```

## Licenses & Support

```bash
# License status
isi license licenses list
isi license licenses view <license_name>

# Support connectivity
isi esrs settings view
isi esrs connectivity test

# Cluster config export
isi config dump
```
