---
tags:
  - architecture
  - vmware
  - vxrail
---
# VxRail — Integrations

<div class="kb-summary">
VxRail integrates natively with vCenter, NSX-T, Aria Operations, and Dell SupportAssist. External CMDB and monitoring integrations consume the VxRail Manager REST API.

*Applies to: VxRail 7.x · 8.x*
</div>
![VxRail — Integrations](../../../../assets/virtualization-vmware-vxrail-architecture-integrations.svg)

## vCenter Integration

VxRail Manager embeds a vCenter Server plugin that adds HCI-specific capabilities:

| Feature | Description |
|---|---|
| VxRail plugin tab | Cluster health, LCM bundle status, node expansion wizard |
| vSAN datastore | Automatically created and managed by VxRail Manager |
| HA / DRS | Configured by VxRail at deployment; treat as standard vSphere HA/DRS |
| vCenter appliance | Can be embedded on VxRail (VxRail-managed vCenter) or external |

**External vCenter**: VxRail Manager manages the ESXi and vSAN layers; vCenter manages the VM and DRS layers independently.

## NSX-T Integration

| Aspect | Detail |
|---|---|
| Overlay networking | VxRail nodes act as ESXi Transport Nodes in the NSX-T fabric |
| VDS configuration | NSX-T VDS is deployed on VxRail nodes via standard NSX-T host prep |
| LCM compatibility | NSX-T version must be validated in the VxRail Compatibility Matrix before upgrade |
| Network requirement | TEP VLAN required; 9000 MTU on TEP VMkernel |

## Aria Operations Integration

| Management Pack | Data Collected | Configuration |
|---|---|---|
| vCenter adapter | VMs, hosts, cluster, vSAN performance | Standard Aria Ops vCenter adapter |
| vSAN adapter (built-in) | Disk group health, vSAN capacity, IOPS | Part of vCenter adapter — no separate config |
| VxRail Management Pack | VxRail Manager health, LCM status, firmware versions | Install VxRail MP from VMware Marketplace |

## Dell SupportAssist Integration

SupportAssist (formerly "Secure Remote Services") provides:

| Function | Detail |
|---|---|
| Proactive monitoring | Dell monitors hardware health; opens support cases automatically on failure |
| Remote support tunnel | Dell engineers can open a secure session with customer approval |
| Firmware update eligibility | SupportAssist registration required for LCM bundle downloads |

Configure SupportAssist during initial VxRail deployment — it cannot be retrofitted easily without re-running the VxRail initialisation workflow.

## VxRail Manager REST API

```bash
# Authenticate
curl -k -X POST https://vxrail-mgr.corp.example.com/rest/vxm/v1/tokens \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<pass>"}'

# Get cluster info
curl -k -H "X-AUTH-TOKEN: <token>" \
  https://vxrail-mgr.corp.example.com/rest/vxm/v1/cluster

# List nodes and health
curl -k -H "X-AUTH-TOKEN: <token>" \
  https://vxrail-mgr.corp.example.com/rest/vxm/v1/hosts
```


```text title="Expected output"
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwOTMxNjgwMH0.x7K9mN2pQrS4vWxYzAbCdEfGhIjKlMnOpQrStUvWxYz","token_type":"Bearer","expires_in":3600}

{"cluster_id":"cluster-1","name":"VxRail-Cluster-01","version":"8.0.200.12345","health":"Healthy","node_count":4,"storage_capacity_gb":102400,"used_capacity_gb":51200}

{"hosts":[{"host_id":"host-1","hostname":"vxrail-node-01.corp.example.com","ip_address":"192.168.1.101","health":"Healthy","cpu_cores":32,"memory_gb":512,"model":"VxRail G560F"},{"host_id":"host-2","hostname":"vxrail-node-02.corp.example.com","ip_address":"192.168.1.102","health":"Healthy","cpu_cores":32,"memory_gb":512,"model":"VxRail G560F"},{"host_id":"host-3","hostname":"vxrail-node-03.corp.example.com","ip_address":"192.168.1.103","health":"Healthy","cpu_cores":32,"memory_gb":512,"model":"VxRail G560F"},{"host_id":"host-4","hostname":"vxrail-node-04.corp.example.com","ip_address":"192.168.1.104","health":"Degraded","cpu_cores":32,"memory_gb":512,"model":"VxRail G560F"}]}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to bypass SSL verification, or import the VxRail manager's certificate into your system's trusted store.
    **`{"error":"Invalid credentials","error_code":401}`** — Verify the username and password are correct and the admin account is not locked; check VxRail manager logs for authentication failures.
    **`{"error":"Token expired","error_code":401}`** — Re-authenticate to obtain a fresh token, as the previous token has exceeded its 3600-second expiration window.
## CMDB Integration

VxRail nodes and the vSAN datastore should be registered in the CMDB:

| CI Type | Source of Truth | Sync Method |
|---|---|---|
| VxRail node | VxRail Manager API `/hosts` | Script or ServiceNow Discovery via MID Server |
| vSAN datastore | vCenter API | ServiceNow Discovery or Aria Automation CMDB sync |
| VxRail Manager VM | vCenter | Auto-discovered by ServiceNow Discovery |

## See also

- [VxRail — How It Works (VMware Platform)](../how-it-works/)
- [VxRail — Deploy](../../deploy/)
