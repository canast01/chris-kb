---
tags:
  - architecture
  - jira
---
# Jira — How It Works


<div class="kb-summary">
How It Works reference covering Deployment Models, Data Center Reference Architecture, Clustering, Port Reference, Cloud Architecture (Reference).
</div>

## Deployment Models

Jira is available in three deployment models, each with distinct architectural characteristics:

| Model | Hosting | Clustering | DB Control | Customisation |
|---|---|---|---|---|
| **Server** | Self-hosted | Single node | Full | Full |
| **Data Center** | Self-hosted | Active-active | Full | Full |
| **Cloud** | Atlassian-managed | Managed | None | Limited |

!!! warning "Server End-of-Life"
    Jira Server reached end of support on **15 February 2024**. All on-premises deployments should be on Data Center.

---

## Data Center Reference Architecture

```mermaid
graph TB
    subgraph Users["Users / Clients"]
        B[Browser]
        API[API Consumers]
    end

    subgraph LB["Load Balancer Tier"]
        HAP["HAProxy / F5 / AWS ALB<br/>(sticky sessions)"]
    end

    subgraph App["Application Tier (Active-Active)"]
        N1["Jira Node 1<br/>jira-app-01"]
        N2["Jira Node 2<br/>jira-app-02"]
        N3["Jira Node 3<br/>jira-app-03"]
    end

    subgraph Search["Search Tier"]
        OS["OpenSearch / Elasticsearch<br/>(clustered, 3 nodes)"]
    end

    subgraph Data["Data Tier"]
        PG[("PostgreSQL<br/>Primary")]
        PGR[("PostgreSQL<br/>Read Replica")]
    end

    subgraph Storage["Shared File Storage"]
        NFS["NFS / SMB Share<br/>(jira-home shared)"]
        S3["Object Storage<br/>(attachments, avatars)"]
    end

    subgraph Cache["Distributed Cache"]
        EH["Ehcache / Hazelcast<br/>(in-process cluster)"]
    end

    B --> HAP
    API --> HAP
    HAP -->|sticky session| N1
    HAP -->|sticky session| N2
    HAP -->|sticky session| N3
    N1 <--> EH
    N2 <--> EH
    N3 <--> EH
    N1 --> PG
    N2 --> PG
    N3 --> PG
    PG --> PGR
    N1 --> OS
    N2 --> OS
    N3 --> OS
    N1 --> NFS
    N2 --> NFS
    N3 --> NFS
```
```text
┌───────────────────────────────────────── Jira — How It Works ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Jira Request and Data Flow                                  │   │
│   │             Browser → LB → Tomcat (Jira app) → DB read/write; attachments via NFS             │   │
│   │          Issue create: HTTP POST → workflow engine → DB insert → Lucene index update          │   │
│   │          JQL search: parse query → Lucene search → fetch issue data from DB → render          │   │
│   │            Notifications: issue event → notification scheme → email via SMTP relay            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Jira processes issue events synchronously; indexing and notifications are async                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          HTTP Flow          │  │       Workflow Engine       │  │         Search Flow         │   │
│   │         Browser → LB        │  │      Transition trigger     │  │          JQL parse          │   │
│   │         LB → Tomcat         │  │       Condition check       │  │         Lucene query        │   │
│   │          Auth check         │  │        Validator run        │  │        Fetch from DB        │   │
│   │        DB query/write       │  │        Post function        │  │      Permission filter      │   │
│   │         Lucene index        │  │        Status update        │  │       Response render       │   │
│   │       Notify via SMTP       │  │       Assign / comment      │  │          Pagination         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Tomcat JVM VMs · PostgreSQL VM · NFS home · SMTP relay for notifications                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Workflow engine = Jira state machine; processes transitions, conditions, validators, post functions  │
│  Transition      = workflow step moving issue from one status to another                              │
│  Condition       = rule checked before transition is allowed (e.g. user must be assignee)             │
│  Validator       = checks field values before transition executes                                     │
│  Post function   = action executed after transition (e.g. assign to role, fire webhook)               │
│  JQL             = Jira Query Language; parsed to Lucene query for issue search                       │
│  Lucene index    = inverted index of issue fields; stored on NFS shared home                          │
│  Permission filter = search results filtered by current user project/issue permissions                │
│  Notification scheme = defines which events trigger email and to which recipients                     │
│  SMTP relay      = outgoing mail server; Jira sends notifications via configured relay                │
│  Ehcache         = distributed cache; stores resolved permissions and issue data                      │
│  Attachment      = file stored on NFS under JIRA_HOME/data/attachments                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

NFS mount options:

```text
nfs-server:/jira-shared /var/atlassian/application-data/jira/shared \
  nfs4 rw,sync,hard,intr,noatime,rsize=131072,wsize=131072 0 0
```

### Distributed Cache (Hazelcast)

Jira Data Center uses Hazelcast for in-cluster cache invalidation and distributed locking.

| Port | Protocol | Purpose |
|---|---|---|
| 5701 | TCP | Hazelcast cluster communication |
| 40001 | TCP | Ehcache replication (legacy) |

```properties
# /var/atlassian/application-data/jira/cluster.properties
jira.node.id=jira-app-01
jira.shared.home=/var/atlassian/application-data/jira/shared
```

---

## Clustering

### Node Registration

```sql
-- Check active cluster nodes
SELECT node_id, node_name, status, last_heartbeat
FROM clusternodeinfo
ORDER BY last_heartbeat DESC;
```

### Cluster Traffic Flow

```mermaid
sequenceDiagram
    participant U as User Browser
    participant LB as Load Balancer
    participant N1 as Node 1
    participant N2 as Node 2
    participant DB as PostgreSQL
    participant FS as Shared Home

    U->>LB: HTTPS request (create issue)
    LB->>N1: Route (sticky session)
    N1->>DB: INSERT into jiraissue
    DB-->>N1: Commit OK
    N1->>FS: Write attachment
    N1-->>LB: HTTP 200
    LB-->>U: Response

    Note over N1,N2: Cache invalidation via Hazelcast
    N1->>N2: Invalidate issue cache [key=PRJ-123]
```

---

## Port Reference

| Port | Protocol | Component | Direction |
|---|---|---|---|
| 443 | TCP | Load Balancer (HTTPS) | Inbound from clients |
| 8080 | TCP | Jira Tomcat | LB → App nodes |
| 5432 | TCP | PostgreSQL | App nodes → DB |
| 9200 | TCP | OpenSearch HTTP | App nodes → Search |
| 5701 | TCP | Hazelcast | App nodes (internal) |
| 389 / 636 | TCP | LDAP / LDAPS | App nodes → Directory |

---

## Cloud Architecture (Reference)

For Jira Cloud, Atlassian manages all infrastructure on AWS:

- No direct DB or file system access — all operations via REST API or UI
- Data residency configurable for Enterprise plans (EU, US, AUS)
- Atlassian Access required for SAML SSO and enforced MFA
- Connect / Forge app framework replaces Server plugins
