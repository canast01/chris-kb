---
tags:
  - architecture
  - security
description: "CyberArk Privileged Access Manager (PAM) is built around the Digital Vault, an encrypted hardened credential store that is the sole authoritative source..."
---
# CyberArk — How It Works

<div class="kb-summary">
CyberArk Privileged Access Manager (PAM) is built around the Digital Vault, an encrypted hardened credential store that is the sole authoritative source for managed passwords and SSH keys.

*Applies to: CyberArk PAM*
</div>

 The Central Policy Manager (CPM) rotates credentials automatically, the Privileged Session Manager (PSM) proxies and records sessions, and the Password Vault Web Access (PVWA) provides the web UI and REST API gateway.

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

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

```d2
direction: right

PVWA: "PVWA\n(web interface" {shape: rectangle}
PSM: "PSM\n(session proxy" {shape: rectangle}
CPM: "CPM\n(rotation engine" {shape: rectangle}
VAULT: "CyberArk Vault\n(encrypted credential store" {shape: rectangle}
USER: "Privileged User" {shape: rectangle}
TARGET: "Target Servers" {shape: rectangle}

PVWA -> PSM
PSM -> CPM
CPM -> VAULT
USER -> PVWA
PSM -> TARGET
CPM -> TARGET
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

```d2
direction: right

failure: "Primary Vault failure detected" {shape: rectangle}
stopSync: "Stop replication on DR Vault\n(dbsync.exe service stopped" {shape: rectangle}
promDR: "Change DR Vault to standalone mode\n(PrivateArk Client" {shape: rectangle}
updateIni: "Update vault.ini on CPM / PSM / PVWA\nto point to DR Vault IP" {shape: rectangle}
restartSvc: "Restart CyberArk services\non CPM, PSM, PVWA" {shape: rectangle}
validate: "Validate connectivity\n(Test-NetConnection :1858" {shape: rectangle}
testCred: "Test credential retrieval\nfrom DR Vault" {shape: rectangle}
ops: "Operations resume from DR Vault" {shape: rectangle}

failure -> stopSync
stopSync -> promDR
promDR -> updateIni
updateIni -> restartSvc
restartSvc -> validate
validate -> testCred
testCred -> ops
```

DR Vault activation procedure:

1. Stop replication on the DR Vault: `C:\Program Files (x86)\PrivateArk\Server\dbsync.exe` — stop the sync service.
2. Change DR Vault to standalone mode via PrivateArk Client.
3. Update CPM, PSM, and PVWA `vault.ini` to point to the DR Vault IP.
4. Restart CyberArk services on CPM, PSM, PVWA.
5. Validate connectivity and test a credential retrieval.
