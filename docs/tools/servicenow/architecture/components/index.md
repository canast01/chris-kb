# ServiceNow — Components

## CMDB

CI classes, discovery, relationships, CMDB health, and querying the CMDB.

## CMDB Overview

The Configuration Management Database (CMDB) stores Configuration Items (CIs) and their relationships. It underpins change management, incident routing, and impact analysis.

```
Core CI hierarchy:
  cmdb_ci                   (base class)
  └── cmdb_ci_hardware       (physical hardware)
  └── cmdb_ci_computer       (servers, VMs)
  └── cmdb_ci_app_server     (application servers)
  └── cmdb_ci_database       (database instances)
  └── cmdb_ci_service        (business/technical services)
  └── cmdb_ci_network_gear   (switches, routers, firewalls)
  └── cmdb_ci_storage_device (SANs, NFS)
```

## Common CI Classes

| Class | Table | Use Case |
|-------|-------|----------|
| Server | `cmdb_ci_server` | Physical and virtual servers |
| Application | `cmdb_ci_appl` | Installed software |
| Database | `cmdb_ci_database` | DB instances |
| Service | `cmdb_ci_service` | Business/IT services |
| Network Device | `cmdb_ci_netgear` | Switches, routers |
| Cloud Instance | `cmdb_ci_vm_instance` | AWS EC2, Azure VM |
| Container | `cmdb_ci_container` | Docker, Kubernetes pods |

```bash
# Query all servers in a specific environment
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/cmdb_ci_server" \
  --data-urlencode 'sysparm_query=install_status=1^environment=Production' \
  --data-urlencode 'sysparm_fields=name,ip_address,os,environment,assigned_to'

# Get a specific CI by name
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/cmdb_ci_server" \
  --data-urlencode 'sysparm_query=name=prod-db-01'
```

## Discovery

ServiceNow Discovery populates and updates CIs automatically.

```bash
# Trigger a discovery scan via API
curl -u user:token -X POST \
  "https://your-instance.service-now.com/api/now/table/discovery_status" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "manual",
    "ip_range": "10.0.1.0/24",
    "discovery_profile": "default"
  }'

# Check last discovery date for a CI
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/cmdb_ci_server" \
  --data-urlencode 'sysparm_query=name=prod-app-01' \
  --data-urlencode 'sysparm_fields=name,last_discovered,discovery_source'
```

Discovery prerequisites:
- MID Server deployed in target network segment
- Credentials stored in ServiceNow credential store
- Network scan range defined in discovery schedule

## CI Relationships

Relationships model how CIs connect to and depend on each other.

```bash
# Get all relationships for a CI
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/cmdb_rel_ci" \
  --data-urlencode 'sysparm_query=parent=CI_SYS_ID' \
  --data-urlencode 'sysparm_fields=type,child,parent'

# Create a relationship between two CIs
curl -u user:token -X POST \
  "https://your-instance.service-now.com/api/now/table/cmdb_rel_ci" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": "PARENT_CI_SYS_ID",
    "child": "CHILD_CI_SYS_ID",
    "type": "Runs on::Hosted on"
  }'
```

| Relationship Type | Example | Direction |
|------------------|---------|-----------|
| Runs on::Hosted on | App runs on Server | App → Server |
| Uses::Used by | App uses Database | App → DB |
| Depends on::Used by | Service depends on API | Service → API |
| Contains::Contained by | Cluster contains Node | Cluster → Node |

## CMDB Health Score

CMDB health measures completeness, compliance, and correctness of CI data.

```bash
# Query CMDB health scorecard
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sn_cmdb_health_score" \
  --data-urlencode 'sysparm_query=ci_class=cmdb_ci_server' \
  --data-urlencode 'sysparm_fields=ci,overall_score,completeness,compliance,correctness'

# Find CIs with low health scores
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sn_cmdb_health_score" \
  --data-urlencode 'sysparm_query=overall_score<50^ci_class=cmdb_ci_server' \
  --data-urlencode 'sysparm_limit=50'
```

| Health Dimension | Measures | Target |
|-----------------|----------|--------|
| Completeness | Required fields populated | > 90% |
| Compliance | CI conforms to class rules | > 95% |
| Correctness | Data matches actual state | > 85% |
| Overall | Combined weighted score | > 80% |
