# Aria Operations CLI Reference


<div class="kb-summary">
Aria Operations (formerly vRealize Operations) is managed via the REST API and the `vracli` tool on the vApp node. The REST API base URL is `https://<ariaops_fqdn>/suite-api/api`. SSH to the analytics node as root for appliance-level operations.
</div>

---

## Appliance Status

```bash
# SSH to Aria Operations node
ssh root@<ariaops_fqdn>

# Check cluster node status
vracli status

# Check service health
vracli services

# View logs
tail -f /data/vcops/log/analytics.log
tail -f /data/vcops/log/collector.log
```
┌─────────────────────────────────── Aria Operations — CLI Reference ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 Aria Operations CLI — vracli and vami_config Command Reference                │   │
│   │        vracli: cluster management · service control · support bundle · user management        │   │
│   │         vami_config: network settings · NTP · DNS · proxy · password on VAMI interface        │   │
│   │      REST API: curl -s -k -u admin:<pw> https://<vrops>/api/alerts | python3 -m json.tool     │   │
│   │          SSH access: root@<vrops-master> — key-based or password per security policy          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Always run vracli cluster status before and after any service restart                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       vracli Commands       │  │       vami_config Cmds      │  │        REST API Calls       │   │
│   │        cluster status       │  │         network get         │  │       GET /api/alerts       │   │
│   │       cluster restart       │  │         ntp get/set         │  │      GET /api/resources     │   │
│   │        services list        │  │         dns get/set         │  │        POST /api/auth       │   │
│   │        support-bundle       │  │          proxy set          │  │      DELETE /api/alerts     │   │
│   │       cassandra status      │  │          passwd set         │  │       GET /api/reports      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CLI runs on Aria Ops nodes via SSH · vami_config runs as root on VAMI management console             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vracli            = Primary Aria Ops CLI; available via SSH on master and replica nodes              │
│  vami_config       = VAMI appliance management CLI for network, DNS, NTP, and proxy settings          │
│  cluster status    = Reports node connectivity, service state, and Cassandra ring health              │
│  support-bundle    = Collects logs, configs, and diagnostics into a .tar.gz for GSS/TAM               │
│  cassandra status  = Checks Cassandra ring membership, token distribution, and replication            │
│  VAMI              = Virtual Appliance Management Infrastructure; web UI on port 5480                 │
│  REST API          = HTTPS API on port 443; requires token or Basic auth                              │
│  Bearer token      = JWT returned by POST /api/auth; used in Authorization header                     │
│  GSS               = Global Support Services; VMware/Broadcom first-line support                      │
│  TAM               = Technical Account Manager; assigned VMware support engineer                      │
│  services list     = Lists all Aria Ops services and their running/stopped state                      │
│  proxy set         = Configures HTTP proxy for Aria Ops outbound internet connectivity                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## Resources & Inventory

```bash
# List all resources
curl -k -X GET "https://<ariaops_fqdn>/suite-api/api/resources?pageSize=1000"   -H "Authorization: OpsToken <token>"

# Search for a resource by name
curl -k -X GET "https://<ariaops_fqdn>/suite-api/api/resources?name=<vm_name>"   -H "Authorization: OpsToken <token>"

# Get resource health
curl -k -X GET "https://<ariaops_fqdn>/suite-api/api/resources/<resource_id>/health"   -H "Authorization: OpsToken <token>"
```

---

## Metrics

```bash
# Get metrics for a resource
curl -k -X GET "https://<ariaops_fqdn>/suite-api/api/resources/<resource_id>/statkeys"   -H "Authorization: OpsToken <token>"

# Query metric values
curl -k -X POST "https://<ariaops_fqdn>/suite-api/api/resources/stats/query"   -H "Authorization: OpsToken <token>"   -H "Content-Type: application/json"   -d '{"resourceId":["<resource_id>"],"statKey":["cpu|usage_average"]}'
```

---

## Adapter & Collector Health

```bash
# List adapter instances
curl -k -X GET "https://<ariaops_fqdn>/suite-api/api/adapters"   -H "Authorization: OpsToken <token>"

# Check collector status
curl -k -X GET "https://<ariaops_fqdn>/suite-api/api/collectors"   -H "Authorization: OpsToken <token>"
```
