---
tags:
  - operations
  - san
---
# Cisco DCNM — CLI Reference
![Cisco DCNM — CLI Reference](../../../../assets/san-cisco-cisco-dcnm-operations-cli-reference.svg)


```bash
# Start all DCNM services
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server start

# Stop all DCNM services
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server stop

# Restart all services
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart

# Check status of all services
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status

# Start/stop individual services
systemctl start dcnm-server
systemctl stop dcnm-pm        # performance manager only
systemctl restart dcnm-events
```

```bash
# Test SSH connectivity to a managed switch
ssh -o ConnectTimeout=5 -o BatchMode=yes dcnm_mgmt@<switch-ip> 'show version' 2>&1

# Test SNMP v3 connectivity to a switch
snmpget -v3 -u dcnm_poll -l authPriv -a SHA -A <auth-pass> \
  -x AES -X <priv-pass> <switch-ip> sysDescr.0

# Test if DCNM is receiving traps (capture for 30 seconds)
sudo tcpdump -i eth0 -n udp port 162 -c 20
```
```bash
# Check HA status
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-status.sh

# Initiate manual failover (from active node — forces standby to become active)
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-failover.sh

# Check VIP status
ip addr show | grep <vip-address>
```
```bash
# Login with Basic Auth — returns session cookie
curl -sk -c dcnm-cookie.txt -X POST \
  https://dcnm-dc1.corp.example.com/rest/logon \
  -H "Content-Type: application/json" \
  -d '{"expirationTime": 86400}' \
  -u "svc-automation:<password>"

# All subsequent calls use the session cookie
export DCNM="https://dcnm-dc1.corp.example.com"

# Logout
curl -sk -b dcnm-cookie.txt -X POST "${DCNM}/rest/logout"
```
```bash
# List all switches
curl -sk -b dcnm-cookie.txt "${DCNM}/rest/inventory/switches" \
  | python3 -m json.tool

# Get switch detail by serial number
curl -sk -b dcnm-cookie.txt "${DCNM}/rest/inventory/switches/<serialNumber>" \
  | python3 -m json.tool

# List all fabrics
curl -sk -b dcnm-cookie.txt "${DCNM}/rest/san/fabric" \
  | python3 -m json.tool

# List all VSANs
curl -sk -b dcnm-cookie.txt "${DCNM}/rest/san/vsan" \
  | python3 -m json.tool
```
```bash
# Get zone database for a fabric
curl -sk -b dcnm-cookie.txt \
  "${DCNM}/rest/san/zoning?fabricName=DC1-FABRIC-A" \
  | python3 -m json.tool

# Get active zone set
curl -sk -b dcnm-cookie.txt \
  "${DCNM}/rest/san/zoning/activezonesets?fabricName=DC1-FABRIC-A" \
  | python3 -m json.tool

# Get device aliases
curl -sk -b dcnm-cookie.txt \
  "${DCNM}/rest/san/devicealias?fabricName=DC1-FABRIC-A" \
  | python3 -m json.tool
```
```bash
# Get all active alarms
curl -sk -b dcnm-cookie.txt \
  "${DCNM}/rest/alarms/activealarms" \
  | python3 -m json.tool

# Get events (last 100)
curl -sk -b dcnm-cookie.txt \
  "${DCNM}/rest/events/allevents?size=100&sortby=eventtime&orderby=desc" \
  | python3 -m json.tool
```
```bash
# List firmware images in DCNM repository
curl -sk -b dcnm-cookie.txt "${DCNM}/rest/fm/image" \
  | python3 -m json.tool

# Initiate firmware upgrade on a switch
curl -sk -b dcnm-cookie.txt -X POST "${DCNM}/rest/fm/upgrade" \
  -H "Content-Type: application/json" \
  -d '{
    "switchList": ["<serialNumber>"],
    "imageName": "m9200-s2ek9-mz.8.4.2a.bin",
    "installMode": "non-disruptive"
  }' | python3 -m json.tool
```
```bash
# Count switches by management state
curl -sk -b dcnm-cookie.txt "${DCNM}/rest/inventory/switches" \
  | python3 -c "
import sys, json, collections
data = json.load(sys.stdin)
states = collections.Counter(s.get('managementState','unknown') for s in data)
print(dict(states))
"

# Find all ISLs with errors
curl -sk -b dcnm-cookie.txt "${DCNM}/rest/san/isl" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for isl in data:
    if isl.get('crcErrors', 0) > 0 or isl.get('lossOfSignal', 0) > 0:
        print(isl.get('switchName'), isl.get('port'), 
              'CRC:', isl.get('crcErrors'), 'LOS:', isl.get('lossOfSignal'))
"

# Export switch inventory to CSV
curl -sk -b dcnm-cookie.txt "${DCNM}/rest/inventory/switches" \
  | python3 -c "
import sys, json, csv
data = json.load(sys.stdin)
fields = ['switchName','ipAddress','model','release','managementState','fabricName']
w = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction='ignore')
w.writeheader()
for s in data: w.writerow(s)
" > switches-$(date +%Y%m%d).csv
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Cisco Dcnm — Procedures](procedures/)
- [Cisco Dcnm — Scripts](scripts/)
- [Cisco Dcnm — Health Checks](health-checks/)
