# Pure1 — Array Health

Pure1 provides a cloud-hosted dashboard showing real-time and historical health status across all registered FlashArray and FlashBlade systems.

## Health Dashboard — What to Check

**Pure1 → Arrays → select array → Overview tab**

| Indicator | Location | Healthy state |
|---|---|---|
| Array status | Banner / Overview | Green — no active alerts |
| Drive health | Hardware → Drives | All drives Healthy |
| Controller status | Hardware → Controllers | Both controllers Online |
| Network interfaces | Hardware → Network | All interfaces Up |
| Purity version | Overview | Current or within supported versions |
| Phone Home | Settings → Phone Home | Last contact < 24h |

## Quick Health Check via CLI

```bash
# Connect to FlashArray
ssh pureuser@<flasharray-ip>

# Overall array health
purehw list              # all hardware components and states

# Drive status
purehw list --type drive | grep -v Healthy   # show non-healthy drives

# Controller status
purehw list --type ct

# Network interfaces
purenetwork list --type eth,fc

# Active alerts
purealert list --flagged

# Purity version
purearray list
```

## FlashBlade Health

```bash
ssh pureuser@<flashblade-ip>

# Blade and chassis health
purehw list

# Network interfaces
purenetwork list

# Active alerts
purealert list --flagged

# NFS/SMB service state
pureservice list
```

## Health via Pure1 REST API

```bash
# Authenticate
TOKEN=$(curl -s -X POST "https://api.pure1.purestorage.com/oauth2/1.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  --data-urlencode "subject_token=<api-key-id>:<private-key-jwt>" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Array health overview
curl -s "https://api.pure1.purestorage.com/api/1.latest/arrays" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Arrays with active alerts
curl -s "https://api.pure1.purestorage.com/api/1.latest/alerts?filter=state='open'" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

## Connectivity Health — Phone Home

Pure1 requires outbound HTTPS connectivity (TCP 443) from the array to Pure Storage cloud. If Phone Home is failing:

```bash
# Test outbound connectivity from array
purentp list           # NTP also tests DNS/network

# Check Phone Home status
purearray list --csv   # includes phone_home_enabled, phone_home_last_contact

# Proxy configuration (if internet access is via proxy)
puresupport proxy list
puresupport proxy set --host <proxy-ip> --port 8080
```

## Health Monitoring Integration

Pure1 can send health events to external systems:

- **SNMP:** Configure under Settings → Notification → SNMP. Use the Pure Storage MIB.
- **Syslog:** Settings → Notification → Syslog → add syslog server IP
- **Webhooks:** Settings → Notification → Webhooks (FlashArray 6.3+)
- **Email:** Settings → Notification → Email → add recipients

## Common Health Issues

| Symptom | Cause | Action |
|---|---|---|
| Drive shows Failed | Drive hardware fault | Open Pure support case — drive replacement covered by Evergreen |
| Controller Offline | Controller fault | Open Priority support case immediately |
| Phone Home last contact > 24h | Firewall blocking TCP 443 to pure1.purestorage.com | Check proxy/firewall; test with `curl https://pure1.purestorage.com` from array |
| Array not visible in Pure1 | Array not registered or API key expired | Re-register array under Pure1 → Settings → Arrays |
