# Nexus Dashboard CLI Reference


<div class="kb-summary">
Nexus Dashboard is managed via its REST API and the `nd` CLI available on the appliance via SSH. The REST API base URL is `https://<nd_fqdn>/login`. SSH as `rescue-user` for appliance-level operations.
</div>

---

## Appliance Access

```bash
# SSH to Nexus Dashboard
ssh rescue-user@<nd_fqdn>

# Check ND services status
acs health

# Check cluster node status
acs cluster info

# Show ND version
cat /var/lib/nd/version.txt

# View logs
kubectl logs -n nd-base <pod_name>
```
┌─────────────────────────────────── Nexus Dashboard — CLI Reference ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 Nexus Dashboard admin CLI — SSH to any master node, admin user                │   │
│   │                      acs health — show cluster node health and app status                     │   │
│   │                        acs backup create — create cluster config backup                       │   │
│   │                acs logs download — download app logs bundle for troubleshooting               │   │
│   │                   acs restart — restart cluster services (use with caution)                   │   │
│   │                   kubectl (on ND) — inspect Kubernetes pods hosting ND apps                   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  SSH to ND management IP · admin user · commands affect entire cluster                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  acs = Admin CLI Suite; Nexus Dashboard command-line interface                                        │
│  acs health = Returns node status: ACTIVE/STANDBY/FAILURE for each master                             │
│  acs backup create = Creates config snapshot; stored locally or exported to SCP/NFS                   │
│  acs logs download = Collects app and system logs bundle for Dell/Cisco support                       │
│  acs restart = Restarts all ND services; use only during maintenance window                           │
│  kubectl = Kubernetes CLI available on ND for pod inspection                                          │
│  Pod = Container instance running an ND app (NDI, NDFC, NDO, or ND service)                           │
│  acs upgrade = Initiates cluster upgrade from uploaded image                                          │
│  acs cluster status = Shows cluster quorum state and node roles                                       │
│  acs app status = Lists installed apps and their running/stopped state                                │
│  NDI REST API = https://<nd-ip>/sedgeapi/v1; auth via /api/v1/auth/token                              │
│  APIC Read-Only = Minimum privilege for NDI APIC credentials: Observer role                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Nodes & Inventory

```bash
# List all nodes across managed fabrics
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/nodes   -H "Authorization: <token>"

# Get node detail
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/nodes/<node_id>   -H "Authorization: <token>"

# Check software versions
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/software-upgrades/compatibility   -H "Authorization: <token>"
```

---

## Services (Insights / Orchestrator)

```bash
# List installed ND services
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/services   -H "Authorization: <token>"

# Get status of a specific service
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/services/<service_id>   -H "Authorization: <token>"
```
