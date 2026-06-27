---
tags:
  - architecture
  - git
---
# Git — How It Works


<div class="kb-summary">
Git is a distributed version control system where every working copy is a full repository with complete history.

*Applies to: Git 2.x*
</div>
![Git — How It Works](../../../../assets/itsm-git-architecture-how-it-works-index.svg)


---

## Distributed Model

Unlike centralised VCS tools, every Git clone contains the entire repository history. By convention teams designate one remote (GitHub, GitLab, Bitbucket) as the integration point.

```mermaid
graph TD
    subgraph "Developer A"
        WTA[Working Tree] --> LA[Local Repo<br/>.git/]
    end
    subgraph "Developer B"
        WTB[Working Tree] --> LB[Local Repo<br/>.git/]
    end
    subgraph "Developer C — Fork"
        WTC[Working Tree] --> LC[Local Repo<br/>.git/]
    end

    LA -->|git push| REMOTE[Remote — origin<br/>github.com / gitlab.com]
    LB -->|git push| REMOTE
    REMOTE -->|git pull / fetch| LA
    REMOTE -->|git pull / fetch| LB

    REMOTE -->|fork| FORK[Fork Remote<br/>github.com/user/repo]
    FORK -->|git push| LC
    LC -->|git push| FORK
    FORK -->|Pull Request / MR| REMOTE
```


---

## Refs and Branches

![Git — How It Works — Diagram](../../../../assets/itsm-git-architecture-how-it-works-diagram.svg)

| Ref | Purpose |
|-----|---------|
| `HEAD` | Currently checked-out commit or branch pointer |
| `ORIG_HEAD` | Previous HEAD before a merge/rebase/reset |
| `MERGE_HEAD` | The commit being merged in |
| `FETCH_HEAD` | Last fetched commit from a remote |

---

## GitHub Enterprise / GitLab Self-Managed Architecture

### GitHub Enterprise Server (GHES)

```mermaid
graph TD
    subgraph "GHES Primary Appliance"
        HAPROXY[HAProxy / Load Balancer]
        NGINX[Nginx — HTTPS / SSH]
        GITALY[Gitaly<br/>Git RPC service]
        RAILS[GitHub Rails App]
        MYSQL[(MySQL — Metadata)]
        REDIS[(Redis — Cache / Queues)]
        ELASTIC[(Elasticsearch — Search)]
        STORAGE[(NFS / Block Storage<br/>Git Object Data)]
    end

    subgraph "GHES Replica — HA"
        REPLICA[Passive Replica<br/>Continuous replication]
    end

    DEV[Developers] -->|HTTPS / SSH| HAPROXY
    HAPROXY --> NGINX
    NGINX --> RAILS
    NGINX --> GITALY
    RAILS --> MYSQL
    RAILS --> REDIS
    GITALY --> STORAGE
    STORAGE -.->|rsync / drbd| REPLICA
```

### Key Server Components

| Component | Role |
|-----------|------|
| **Gitaly** | gRPC service that owns all Git repository access |
| **Puma / Rails** | Web application, API, and business logic |
| **Sidekiq** | Asynchronous job processing (webhooks, emails, CI scheduling) |
| **Workhorse** | Reverse proxy for large payloads (git push/pull, uploads) |
| **PostgreSQL** | Relational metadata (users, projects, MRs, CI records) |
| **Redis** | Session cache, queues, rate limiting, ActionCable |
| **MinIO / S3** | Object storage for LFS, CI artifacts, container registry layers |

---

## Data Flow — git push

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Git as Git client
    participant WH as Workhorse
    participant Gitaly as Gitaly
    participant Rails as Rails App
    participant PG as PostgreSQL

    Dev->>Git: git push origin main
    Git->>WH: pack-objects stream
    WH->>Gitaly: SmartHTTP / SSHUploadPack RPC
    Gitaly->>Gitaly: receive-pack, update refs
    Gitaly-->>WH: success
    WH->>Rails: POST /internal/allowed (auth check)
    Rails->>PG: validate permissions, record push event
    Rails-->>WH: 200 OK
    WH-->>Git: remote refs updated
    Rails->>Rails: trigger webhooks / CI pipelines (async)
```

---

## Storage Layout

![Git — How It Works — Diagram](../../../../assets/itsm-git-architecture-how-it-works-d2.svg)

---

## See also

- [Git — Design Standards](../design-standards/)
- [Git — Integrations](../integrations/)
- [Git — Deploy](../../deploy/)
