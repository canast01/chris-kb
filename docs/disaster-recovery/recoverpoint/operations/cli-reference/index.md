# RecoverPoint CLI Reference

> Part of the [RecoverPoint](../../index.md) > [Operations](../index.md) reference.

---

## Overview

RecoverPoint management interfaces:

| Interface | Access | Purpose | When to use |
|---|---|---|---|
| `boxmgmt` CLI | SSH to RPA appliance | Menu-driven system management | On-call triage; image access; manual failover |
| RPAPI REST | HTTPS to cluster IP | Automation, CG control, status | Scripted DR tests; monitoring integrations |
| Unisphere for RecoverPoint | Web UI | GUI management | Configuration, visual health checks |

## Image Access Flow

```mermaid
flowchart TD
    drTestStart["DR Test or Recovery Initiated"]
    listCGs["List CG State\ngroupsStatus"]
    cgHealthy{"CGs ACTIVE\nand Journal < 70%?"}
    createBookmark["Create Pre-Test Bookmark\ngroup create_bookmark --gname cgname\n--name dr-test-date"]
    enableAccess["Enable Image Access\ngroup enable-image-access\n--copy DR_Copy --image latest --access-mode virtual"]
    confirmAccess["Confirm ImageAccess State\ngroup status --gname cgname"]
    mountVolumes["Mount DR Volumes at DR Site\n(SAN / vSphere step)"]
    validate["Validate Application Data\n(app team confirms)"]
    disableAccess["Disable Image Access\ngroup disable-image-access --gname cgname"]
    confirmActive["Confirm CG ACTIVE\ngroups status"]
    abortTest["Do Not Proceed\nResolve CG issues first"]

    drTestStart --> listCGs
    listCGs --> cgHealthy
    cgHealthy -->|"Yes"| createBookmark
    cgHealthy -->|"No"| abortTest
    createBookmark --> enableAccess
    enableAccess --> confirmAccess
    confirmAccess --> mountVolumes
    mountVolumes --> validate
    validate --> disableAccess
    disableAccess --> confirmActive

    style drTestStart fill:#2563eb,color:#fff
    style confirmActive fill:#15803d,color:#fff
    style abortTest fill:#be123c,color:#fff
    style enableAccess fill:#b45309,color:#fff
    style disableAccess fill:#b45309,color:#fff
```

---

## boxmgmt CLI

SSH to any RPA (RecoverPoint Appliance) in the cluster. The default management user is `admin` or `boxmgmt`.

```bash
ssh admin@rpa01.example.com
# or
ssh boxmgmt@rpa01.example.com

# Launch the interactive management menu
boxmgmt
```

The `boxmgmt` interface is menu-driven. Navigate by number. Common menu paths:

```text
1 → System Management
2 → Cluster Management
3 → Group (CG) Management
4 → RPA Hardware
5 → Diagnostics
```

### System Status Commands

```bash
# From boxmgmt shell — type at the boxmgmt> prompt after logging in

# Overall cluster state
boxmgmt> system status

# All CG (Consistency Group) states
boxmgmt> groups status

# RPA appliance info and version
boxmgmt> get_all_rps_info

# Verify RPA software version on each appliance
boxmgmt> verify_rpa_version

# Check cluster quorum
boxmgmt> cluster quorum check

# Check WAN link / connectivity between sites
boxmgmt> network connectivity check
```

### Image Access (CG Operations)

Image access enables read/write access to a point-in-time copy at the DR site.

```bash
# Enable image access for a CG (DR copy — read/write, virtual access)
boxmgmt> enable image access
  → Select CG: <cg_name>
  → Select copy: DR_Copy
  → Select image: <point-in-time-timestamp>
  → Access type: Virtual (no data movement) or Logged (allows writes, tracked)

# Disable image access (return to normal replication)
boxmgmt> disable image access
  → Select CG: <cg_name>

# Test failover (non-disruptive validation — accesses a snapshot without impacting replication)
boxmgmt> test failover
  → Select CG: <cg_name>
  → Confirm: yes

# Group suspend (pause replication for maintenance)
boxmgmt> groups suspend
  → Select CG or all

# Group resume (resume replication)
boxmgmt> groups resume
  → Select CG or all
```

---

## RPAPI REST

Base URL: `https://<cluster-mgmt-ip>/fapi/rest/5_1`  
Authentication: HTTP Basic (admin credentials).

```bash
RP="https://recoverpoint.example.com/fapi/rest/5_1"
AUTH="-u admin:password --insecure"
```

### Cluster Information

```bash
# All cluster details
curl -s $AUTH "$RP/cluster/all_clusters_details" | python3 -m json.tool

# Cluster connectivity (inter-site links)
curl -s $AUTH "$RP/cluster/all_clusters_details" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for cluster in data.get('clustersDetails', []):
    print(f\"Cluster: {cluster.get('clusterUID',{}).get('id','?')}  \
name={cluster.get('name','?')}\")
"
```

### Consistency Groups

```bash
# All CG details (state, links, copies)
curl -s $AUTH "$RP/group/all_groups_details" | python3 -m json.tool

# Summary: CG name + enabled/disabled + replication state
curl -s $AUTH "$RP/group/all_groups_details" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for grp in data.get('innerSet', []):
    gname = grp.get('name','?')
    enabled = grp.get('enabled', '?')
    copies  = [c.get('name','?') for c in grp.get('groupCopies', {}).get('innerSet', [])]
    print(f\"CG={gname:30s}  enabled={str(enabled):5s}  copies={copies}\")
"

# Get specific CG details by UID
CG_UID="1"
curl -s $AUTH "$RP/group/${CG_UID}/all_details" | python3 -m json.tool
```

### CG Operations via REST

```bash
# Suspend a CG
curl -s -X PUT $AUTH "$RP/group/${CG_UID}/suspend" | python3 -m json.tool

# Resume a CG
curl -s -X PUT $AUTH "$RP/group/${CG_UID}/resume" | python3 -m json.tool

# Enable image access (virtual) for a CG copy
curl -s -X PUT $AUTH "$RP/group/${CG_UID}/copy/${COPY_UID}/enable_image_access" \
  -H "Content-Type: application/json" \
  -d '{
    "imageAccessMode": "VIRTUAL_ACCESS",
    "scenario": "DR"
  }' | python3 -m json.tool

# Disable image access (resume replication)
curl -s -X PUT $AUTH "$RP/group/${CG_UID}/copy/${COPY_UID}/disable_image_access" | \
  python3 -m json.tool

# Test consistency of a CG (verify RPO bookmarks)
curl -s -X PUT $AUTH "$RP/group/${CG_UID}/test_consistency" | python3 -m json.tool
```

### RPA Health

```bash
# All RPA hardware details
curl -s $AUTH "$RP/rp/all_rps_details" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for rp in data.get('innerSet', []):
    rpid  = rp.get('rpUID', {}).get('id','?')
    state = rp.get('rpState','?')
    print(f\"RPA ID={rpid}  state={state}\")
"

# Cluster quorum status
curl -s $AUTH "$RP/cluster/all_clusters_details" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data.get('clustersDetails', []):
    quorum = c.get('quorum','?')
    print(f\"Cluster: {c.get('name','?'):20s}  Quorum: {quorum}\")
"
```

### Journal Usage

```bash
# Journal usage per CG copy
curl -s $AUTH "$RP/group/all_groups_details" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for grp in data.get('innerSet', []):
    for copy in grp.get('groupCopies', {}).get('innerSet', []):
        journal = copy.get('journalVolumeList', {})
        print(f\"CG={grp['name']:25s}  copy={copy.get('name','?'):15s}  \
journal_vols={len(journal.get('innerSet',[]))}\")
"
```

---

## Key Operational Scenarios

### DR Failover with Image Access

```bash
# 1. Check CG state — confirm replication is healthy
curl -s $AUTH "$RP/group/all_groups_details" | python3 -m json.tool

# 2. Enable image access on the DR copy (virtual, read-write)
curl -s -X PUT $AUTH "$RP/group/${CG_UID}/copy/${COPY_UID}/enable_image_access" \
  -H "Content-Type: application/json" \
  -d '{"imageAccessMode":"VIRTUAL_ACCESS","scenario":"DR"}' | python3 -m json.tool

# 3. Mount volumes at DR site (ESX or host level — outside RecoverPoint)
# 4. Start applications, validate data
# 5. When done — disable image access to resume replication
curl -s -X PUT $AUTH "$RP/group/${CG_UID}/copy/${COPY_UID}/disable_image_access" | \
  python3 -m json.tool
```
