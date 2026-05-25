# CyberArk — How It Works

CyberArk Privileged Access Manager (PAM) is built around the Digital Vault, an encrypted hardened credential store that is the sole authoritative source for managed passwords and SSH keys. The Central Policy Manager (CPM) rotates credentials automatically, the Privileged Session Manager (PSM) proxies and records sessions, and the Password Vault Web Access (PVWA) provides the web UI and REST API gateway.

---

## Component Overview

| Component | Role | Typical Count |
|---|---|---|
| Digital Vault | Encrypted credential store, core engine | 2 (primary + DR) |
| CPM (Central Policy Manager) | Automated password rotation | 1–2 per site |
| PSM (Privileged Session Manager) | Session proxy, recording, isolation | 2+ (load-balanced) |
| PVWA (Password Vault Web Access) | Web UI and REST API | 2+ (load-balanced) |
| PSMP | SSH proxy for Linux privileged access | 1–2 per site |
| DR Vault | Asynchronous replication replica of Vault | 1 per DR site |

---

## PAM Component Topology

```mermaid
graph TB
  PVWA["PVWA\n(web interface)"] & PSM["PSM\n(session proxy)"] & CPM["CPM\n(rotation engine)"] --> VAULT["CyberArk Vault\n(encrypted credential store)"]
  USER(["Privileged User"]) -->|"browser"| PVWA
  PSM -->|"RDP / SSH proxy\nsession recording"| TARGET(["Target Servers"])
  CPM -->|"password rotation"| TARGET
  VAULT -.->|"audit stream"| SIEM(["SIEM"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VAULT store
  class PVWA,PSM,CPM ctrl
  class USER,TARGET,SIEM host
```

---

## Network Topology

```text
[Admin workstation / PAW]
         |
         | HTTPS (443)
         v
[PVWA (load-balanced pair)]  <-- AD LDAP/LDAPS (389/636)
         |
         | Vault SDK (1858)
         v
[Digital Vault (primary)]  <--> [DR Vault]
         |                      (replication: 1858)
         |
    +---------+----------+
    |                    |
[CPM]                 [PSM (load-balanced)]
    |                    |
    | (target protocols) | RDP/SSH (through session)
    v                    v
[Target systems]     [Target systems]
```

Key ports:

- PVWA → Vault: TCP 1858
- CPM → Vault: TCP 1858
- PSM → Vault: TCP 1858
- Admin → PVWA: TCP 443
- PSM → Targets: TCP 22 (SSH), TCP 3389 (RDP), TCP 1521 (Oracle), TCP 1433 (MSSQL)
- PSMP → Targets: TCP 22

---

## Credential Checkout Sequence

```mermaid
sequenceDiagram
    participant user as Privileged User
    participant pvwa as PVWA
    participant vault as Vault
    participant cpm as CPM

    user->>pvwa: Authenticate (AD + MFA)
    pvwa->>vault: SDK connect (port 1858)
    user->>pvwa: Request credential checkout
    pvwa->>vault: Retrieve encrypted credential
    vault-->>pvwa: Return credential
    pvwa-->>user: Display / use credential
    user->>pvwa: Check-in (or auto check-in on expiry)
    pvwa->>cpm: Trigger rotation job
    cpm->>vault: Retrieve current credential
    cpm->>vault: Store rotated credential
```

---

## High Availability and DR

| Scenario | Recovery Method |
|---|---|
| Primary Vault hardware failure | Activate DR Vault; reconfigure CPM/PSM/PVWA to point to DR Vault |
| PVWA node failure | Load balancer removes failed node; remaining node serves traffic |
| CPM failure | Accounts queue for rotation; failover CPM picks up queue on restart |
| PSM node failure | Active sessions on failed node terminate; load balancer routes new sessions to healthy node |

---

## DR Activation Flow

```mermaid
flowchart TD
    failure["Primary Vault failure detected"] --> stopSync["Stop replication on DR Vault\n(dbsync.exe service stopped)"]
    stopSync --> promDR["Change DR Vault to standalone mode\n(PrivateArk Client)"]
    promDR --> updateIni["Update vault.ini on CPM / PSM / PVWA\nto point to DR Vault IP"]
    updateIni --> restartSvc["Restart CyberArk services\non CPM, PSM, PVWA"]
    restartSvc --> validate["Validate connectivity\n(Test-NetConnection :1858)"]
    validate --> testCred["Test credential retrieval\nfrom DR Vault"]
    testCred --> ops["Operations resume from DR Vault"]
```

DR Vault activation procedure:

1. Stop replication on the DR Vault: `C:\Program Files (x86)\PrivateArk\Server\dbsync.exe` — stop the sync service.
2. Change DR Vault to standalone mode via PrivateArk Client.
3. Update CPM, PSM, and PVWA `vault.ini` to point to the DR Vault IP.
4. Restart CyberArk services on CPM, PSM, PVWA.
5. Validate connectivity and test a credential retrieval.
