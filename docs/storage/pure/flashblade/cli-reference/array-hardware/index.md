# Array Status & Hardware

> Part of the [Pure FlashBlade CLI Reference](../).
---

## Array Status & Identity

```bash
# Array info
purefb array show
purefb array show --version

# Hardware status
purefb hardware show
purefb hardware show --blades
purefb hardware show --chassis

# Alerts
purefb alert show
purefb alert show --filter "state='open'"

# Capacity
purefb array show --space
purefb filesystem show --space
```

---

## Blades & Hardware

```bash
# Blade status
purefb blade show
purefb blade show --id <blade_id>

# Drive health
purefb drive show
purefb drive show --blade <blade_id>

# Chassis
purefb chassis show
```
