---
tags:
  - architecture
  - dell
---
# RecoverPoint — Integrations

<div class="kb-summary">
RecoverPoint integrations: vSphere plugin registration, VMAX and XtremIO production array pairing, SRDF coexistence, and management via Unisphere for RecoverPoint.

*Applies to: RecoverPoint 5.x*
</div>
![RecoverPoint — Integrations](../../../../assets/storage-dell-recoverpoint-architecture-integrations.svg)

---

## Splitter Topology

```mermaid
graph TD
    subgraph esxiHost ["ESXi Host (RP4VM)"]
        vmApp["Protected VM"]
        softSplitter["Software Splitter\n(vSphere Kernel Module)"]
        vmdk["VMDK — Datastore"]
        vmApp -->|"write I/O"| softSplitter
        softSplitter -->|"pass-through write"| vmdk
        softSplitter -->|"capture copy"| rpaA
    end

    subgraph powermax ["PowerMax Array"]
        hwSplitter["Hardware Splitter\n(Array Microcode)"]
        prodLUN["Production LUN"]
        hwSplitter -->|"pass-through"| prodLUN
        hwSplitter -->|"capture copy"| rpaA
    end

    rpaA["RPA Cluster Site A"]
    rpaA -->|"WAN replication"| rpaB["RPA Cluster Site B"]
    rpaB --> drJournal["DR Journal Volumes"]
    drJournal --> drReplica["DR Replica Volumes"]
```

---

## VMware SRM Integration

The RecoverPoint SRA enables SRM to use RecoverPoint consistency groups as protection sources:

1. Download RecoverPoint SRA from Dell support portal
2. Install on each SRM server (both sites)
3. Register in SRM → Array Managers:
   - Manager type: EMC RecoverPoint
   - Management IP: `<rpa-cluster-ip>`
   - Username/password: dedicated svc_srm account

SRM recovery plans reference RecoverPoint CGs — failover steps include:
1. Enabling image access on the RecoverPoint CG (exposes the replica copy)
2. Registering VMs at the recovery site
3. Powering on VMs
4. Finalising the recovery (disabling image access, making replica writable)

---

## Storage Array Integration

| Array | Splitter Type | Notes | Why preferred |
|---|---|---|---|
| Dell PowerMax | Array-based (XtremIO or SRDF co-existence) | Integrates via Unisphere | No host agent overhead; best performance |
| Dell Unity | Array-based splitter | Native Unity support | Embedded in array; managed from Unity Unisphere |
| VMware vSphere | Software splitter (RP4VM) | VMDK-level — no array integration needed | Works with any underlying storage — most flexible |

---

## Aria Operations Integration

The RecoverPoint management pack surfaces:
- RPA health (CPU, memory, link state)
- CG lag per consistency group
- Journal fill level and utilisation
- Transfer rate and bandwidth utilisation

Install from Aria Marketplace: Solutions → Browse → "RecoverPoint" → Deploy.

---

## API Integration

RecoverPoint REST API for automation:

```bash
# Authenticate
curl -k -u admin:password -X POST https://<rpa-ip>/rest/users/sessions

# List consistency groups
GET /rest/consistency_groups

# Enable image access (for test failover)
PUT /rest/consistency_groups/{id}/clusters/{clusterId}/image_access/enable
Body: {"scenario": "LOGGED_ACCESS", "consistency": "CRASH_CONSISTENT"}
```


```text title="Expected output"
{
  "sessionID": "a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6",
  "userID": "admin",
  "createdTime": 1699564823000,
  "expirationTime": 1699651223000
}

{
  "consistency_groups": [
    {
      "id": "cg-prod-001",
      "name": "Production_Database",
      "status": "ACTIVE",
      "replicationPairs": 2
    },
    {
      "id": "cg-test-042",
      "name": "Test_Environment",
      "status": "ACTIVE",
      "replicationPairs": 1
    },
    {
      "id": "cg-archive-015",
      "name": "Archive_Data",
      "status": "PAUSED",
      "replicationPairs": 1
    }
  ]
}

{
  "taskID": "task-8f7e6d5c-4b3a-2f1e-0d9c-8b7a6f5e4d3c",
  "status": "IN_PROGRESS",
  "consistency_group_id": "cg-prod-001",
  "cluster_id": "cluster-nyc-01",
  "image_access_scenario": "LOGGED_ACCESS",
  "consistency_level": "CRASH_CONSISTENT",
  "estimatedCompletionTime": 180
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or import the RPA's certificate into your trusted store.
    **`HTTP/1.1 401 Unauthorized`** — Verify the admin credentials are correct and the user has API access permissions enabled in RecoverPoint.
    **`HTTP/1.1 404 Not Found`** — Confirm the consistency group ID and cluster ID exist by listing them first with GET /rest/consistency_groups and GET /rest/clusters.
---

## See also

- [Recoverpoint — How It Works](../how-it-works/)
- [Recoverpoint — Design Standards](../design-standards/)
