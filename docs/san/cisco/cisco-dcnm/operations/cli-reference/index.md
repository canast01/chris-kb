# Cisco DCNM — CLI Reference

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
```text
┌───────────────────────────────────── Cisco DCNM — CLI Reference ──────────────────────────────────────┐
│                                                                                                       │
│  DCNM management CLI and key NX-OS MDS commands for fabric operations and troubleshooting.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                DCNM Admin CLI                │  │            NX-OS MDS SAN Commands           │   │
│   │         appmgr status: service check         │  │             show flogi database             │   │
│   │        appmgr backup: trigger backup         │  │             show zoneset active             │   │
│   │            appmgr stop/start dcnm            │  │            show vsan: VSAN state            │   │
│   │           dcnm_root passwd change            │  │          show interface fc: errors          │   │
│   │          tail -f /var/log/dcnm/...           │  │            show port-channel: ISL           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  appmgr manages DCNM services; NX-OS MDS CLI verifies switch-level fabric state.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           REST API Quick Reference           │  │          Common Troubleshooting CLI         │   │
│   │           POST /rest/logon → token           │  │              curl /rest/health              │   │
│   │             GET /rest/san/fabric             │  │              appmgr status all              │   │
│   │         GET /rest/san/zone/{fabric}          │  │              netstat -tlnp 443              │   │
│   │          POST /rest/san/zone/deploy          │  │              df -h: disk usage              │   │
│   │          DELETE /rest/san/zone/{id}          │  │            show tech-support: TAC           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM Linux VM · SSH access · REST API port 443 · Cisco MDS management Ethernet                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  appmgr          = DCNM VM management CLI; controls service lifecycle and backups                     │
│  show flogi database= NX-OS; shows all FC logins; confirms HBA access to fabric                       │
│  show zoneset active= NX-OS; shows active zone set members in each VSAN                               │
│  show vsan        = NX-OS; VSAN state; all should be active                                           │
│  show interface fc= NX-OS; per-port FC counters: errors, throughput, credits                          │
│  show port-channel= NX-OS; ISL port-channel (PortChannel) status and members                          │
│  /rest/logon      = DCNM REST auth endpoint; POST credentials; returns JWT token                      │
│  /rest/san/fabric = DCNM REST; lists all managed SAN fabrics                                          │
│  /rest/san/zone/deploy= DCNM REST; triggers zone set activation in VSAN                               │
│  show tech-support= NX-OS MDS full diagnostic bundle; send to Cisco TAC                               │
│  df -h            = Linux disk free; check DCNM disk for Elasticsearch fill                           │
│  netstat -tlnp    = verify DCNM port 443 is listening; basic health check                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
