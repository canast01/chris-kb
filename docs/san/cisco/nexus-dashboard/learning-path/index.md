---
tags:
  - learning-path
  - san
description: "Recommended reading order for Cisco Nexus Dashboard. Follow these stages in order to build a complete mental model before working with it in production."
---
# Cisco Nexus Dashboard — Learning Path

<div class="kb-summary">
Recommended reading order for Cisco Nexus Dashboard. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Cisco MDS · Nexus*
</div>

```d2
direction: right

S1: "Architecture" {shape: rectangle}
S2: "Deploy" {shape: rectangle}
S3: "Operations" {shape: rectangle}
S4: "Security" {shape: rectangle}
S5: "Troubleshoot" {shape: rectangle}

S1 -> S2
S2 -> S3
S3 -> S4
S4 -> S5
```

## Stage 1 — Architecture

**Goal**: Understand Nexus Dashboard as a multi-fabric management platform and the app-hosting model that underpins NDFC, NAE, and NDI.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — Nexus Dashboard cluster model (3 or 5 nodes), fabric inventory aggregation, app-hosting platform: Nexus Dashboard Fabric Controller (NDFC), Network Assurance Engine (NAE), Network Insights (NDI); data pipeline from fabric to analytics
- [Design Standards](../architecture/design-standards/) — Node sizing for app combinations, network interface design (management vs data vs cluster), multi-site federation design, app co-residency constraints
- [Integrations](../architecture/integrations/) — ACI APIC integration for NDFC SAN, Cisco Intersight for cloud management plane, LDAP/TACACS+ for RBAC, syslog and SNMP export, Cisco ThousandEyes for path analytics

**Why first**: Nexus Dashboard is a platform that hosts apps — understanding the app model and resource allocation before deployment avoids undersizing and helps you know which app handles which management function.

---

## Stage 2 — Deployment

**Goal**: Deploy the Nexus Dashboard cluster, configure networking, and install required apps (NDFC, NAE, NDI).

**Read**:

- [Deploy](../deploy/) — Nexus Dashboard cluster node deployment (bare-metal or VM), networking configuration, cluster formation, app installation from Cisco app store, initial fabric onboarding
- [Install & Upgrade](../operations/install-upgrade/) — Nexus Dashboard platform upgrade, app upgrade sequence (platform before apps), rolling upgrade considerations, app data migration

---

## Stage 3 — Operations

**Goal**: Use Nexus Dashboard apps to monitor fabrics, manage zones, validate changes, and investigate insights.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; check cluster node health, app operational status, fabric connectivity, pending change validation alerts
- [Fabric Health](../operations/fabric-health/) — NDFC fabric health view: switch reachability, interface status, fabric compliance, POAP device queue
- [Visibility](../operations/visibility/) — NDI real-time topology view, flow telemetry, latency heatmaps, change impact analysis before deployment
- [CLI Reference](../operations/cli-reference/) — Nexus Dashboard REST API for fabric queries, app status, site inventory; `nd` CLI for cluster management
- [Procedures](../operations/procedures/) — Onboard a new fabric to NDFC, run a pre-change analysis in NDI, create a compliance check in NAE, multi-site topology view configuration
- [Backup & Restore](../operations/backup-restore/) — Nexus Dashboard cluster backup, app configuration export, restore to replacement cluster, individual app backup procedures
- [Scripts](../operations/scripts/) — Automated fabric inventory extraction via REST API, compliance report scheduling, change management integration scripts

---

## Stage 4 — Security

**Goal**: Enforce Nexus Dashboard RBAC, secure the cluster, and control app-level permissions.

**Read**:

- [Access Control](../security/access-control/) — Nexus Dashboard roles (Site Admin, Fabric Admin, Operator, Viewer), app-scoped role assignment, fabric-level access restriction
- [Authentication](../security/authentication/) — LDAP/AD integration for Nexus Dashboard login, local admin hardening, TACACS+ for audit trail, certificate management for cluster TLS
- [Encryption](../security/encryption/) — Inter-node cluster encryption, HTTPS enforcement for management portal, TLS for fabric API connections, app data encryption at rest
- [Hardening](../security/hardening/) — Restrict cluster management network access, disable unused apps, enforce session timeout, export audit logs to SIEM

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose cluster node failures, app health issues, fabric discovery problems, and NDI insight gaps.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Cluster node unhealthy (quorum risk), app stuck in degraded state, fabric not discovered after onboarding, NDI missing flow data, NDFC zone push failing
- [Diagnostics](../troubleshooting/diagnostics/) — Nexus Dashboard cluster health UI, `nd cluster status`, app log collection, fabric re-discovery trigger, REST API health endpoint validation
- [Escalation](../troubleshooting/escalation/) — Cisco TAC case for Nexus Dashboard platform bugs, `techsupport` bundle from cluster, app-specific log collection procedure

**Why last**: Nexus Dashboard troubleshooting requires understanding both the app model and the underlying fabric — context built across the Architecture and Operations stages.

---

## See also

- [Nexus Dashboard — Deploy](../deploy/)
- [Nexus Dashboard — Procedures](../operations/procedures/)
- [Nexus Dashboard — Common Issues](../troubleshooting/common-issues/)
