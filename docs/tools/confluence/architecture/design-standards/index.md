# Confluence — Design Standards

```bash
# List global templates
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/template?type=global"

# List space-level templates
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/template?type=space&spaceKey=ENG"

# Get a specific template by ID
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/template/TEMPLATE_ID"
```
```text
┌──────────────────────────────────── Confluence — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Confluence Design and Sizing Standards                            │   │
│   │            Node sizing: min 8 vCPU / 16 GB RAM per app node; JVM heap 4-6 GB (-Xmx)           │   │
│   │           DB sizing: 4 vCPU / 8 GB RAM; SSD storage; autovacuum tuned for Confluence          │   │
│   │         NFS sizing: 500 GB starting point; monitor confluence.home/attachments growth         │   │
│   │     HA topology: 2+ app nodes behind LB with sticky sessions; PostgreSQL streaming replica    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Design standards define the minimum viable and production-grade deployment topologies              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Infrastructure Standards           │  │           Configuration Standards           │   │
│   │           App node: 8 vCPU / 16 GB           │  │              JVM: -Xms2g -Xmx6g             │   │
│   │            DB: 4 vCPU / 8 GB SSD             │  │            DB pool: max 60 conns            │   │
│   │          NFS: 10 Gbps, low latency           │  │           Tomcat: max threads 200           │   │
│   │           LB: sticky session rules           │  │           Scheduler: cluster-aware          │   │
│   │           Replica: streaming repl            │  │           Backup: nightly pg_dump           │   │
│   │           DR: cross-site NFS sync            │  │           Retention: 30-day backup          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere HA cluster · SSD-backed datastores · 10 GbE NFS network · dedicated DB VLAN                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  -Xmx         = JVM max heap flag; set in setenv.sh; controls Confluence memory ceiling               │
│  Sticky session = LB routes same user to same node; needed for non-Hazelcast session stores           │
│  autovacuum   = PostgreSQL background process; reclaims dead row storage (critical for Jira)          │
│  Streaming replica = PostgreSQL standby receiving WAL stream for hot-standby reads and failover       │
│  DB pool      = JDBC connection pool; Confluence default uses c3p0; tune maxPoolSize                  │
│  Tomcat threads = max simultaneous HTTP request handlers; tune based on concurrent users              │
│  Scheduler    = Confluence background job scheduler; DC-aware to avoid duplicate execution            │
│  pg_dump      = PostgreSQL dump tool; use --format=custom for parallel restore with pg_restore        │
│  NFS latency  = shared home latency directly impacts Confluence page render time                      │
│  Attachment   = binary stored in NFS; large attachments slow backup and NFS throughput                │
│  Cluster node = each Confluence instance in DC must share the same DB URL and home path               │
│  WAL          = Write-Ahead Log; PostgreSQL durability mechanism, source for replication              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```json
// atlassian-connect.json blueprint module entry
{
  "blueprints": [{
    "key": "incident-blueprint",
    "name": "Incident Report",
    "createResult": "edit",
    "template": {"url": "/templates/incident.xml"},
    "wizard": {
      "steps": [{
        "title": "Incident Details",
        "instructions": "Fill in the key incident fields below"
      }]
    }
  }]
}
```
