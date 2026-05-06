# PowerMax Health Checks

Daily and pre/post-change checks for Dell PowerMax arrays.

## Array Connectivity and Status

```bash
# Verify Solutions Enabler can reach the array
symcfg list
symcfg -sid <sid> show | grep -E "Product|Microcode|Online"

# Check array health via Unisphere REST (requires curl + valid token)
curl -sk -X GET "https://<unisphere-ip>:8443/univmax/restapi/system/symmetrix/<sid>" \
    -H "Authorization: Bearer <token>" | python3 -m json.tool | grep -E "model|health|microcode"
```

## Director and Port Status

```bash
# Check all directors — flag any offline
symcfg -sid <sid> list -dir all | grep -v Online

# Check all ports — flag any not RDY
symcfg -sid <sid> list -port all | grep -v RDY

# FA port login count (host connectivity)
symcfg -sid <sid> list -fa -online | grep -E "Port|Logins"
```

## Events and Alerts

```bash
# Active/uncleared events
symevent list -sid <sid> -v | grep -i "uncleared\|Warning\|Error\|Fatal" | head -20

# Events in last 24 hours
symevent list -sid <sid> -start_time "$(date -d 'yesterday' '+%m/%d/%Y') 00:00:00" -v | head -30
```

## Storage Pool (SRP) Capacity

```bash
# SRP subscription and free capacity
symcfg -sid <sid> list -srp

# Thin pool usage detail
symcfg -sid <sid> show -pool -thin -demand

# Flag SRP above 80% subscribed
symcfg -sid <sid> list -srp | awk '$5+0 > 80 {print "WARNING:", $0}'
```

## SRDF Replication State

```bash
# Check all SRDF groups
symrdf -sid <sid> list -rdfg all

# Check for any pairs not in Synchronized state
symrdf -sid <sid> query -rdfg all | grep -v "Synchronized\|InSync" | grep -v "^$\|Group\|Pair\|---"
```

## Device Status

```bash
# Failed or degraded devices
symdev list -sid <sid> -failed

# Devices not ready
symdev list -sid <sid> -NR

# Spare devices available
symdev list -sid <sid> -spare
```

## Cache Health

```bash
# Cache write pending percentage — alert if > 50%
symstat -sid <sid> list -type cache | grep -E "WP\|Write Pending"
```

## Health Check Summary

| Check | Command | Healthy |
|---|---|---|
| Array reachable | `symcfg list` | Array listed, Online |
| All directors online | `symcfg list -dir all` | All = Online |
| All ports ready | `symcfg list -port all` | All = RDY |
| No active events | `symevent list -v` | 0 uncleared |
| SRP < 80% subscribed | `symcfg list -srp` | < 80% used |
| SRDF synchronized | `symrdf query -rdfg all` | All = Synchronized |
| No failed devices | `symdev list -failed` | 0 failed |
| Cache WP < 31% | `symstat list -type cache` | WP% < 31% |
