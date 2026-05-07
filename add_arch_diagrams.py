#!/usr/bin/env python3
"""Add ASCII topology diagrams to all architecture pages and move index diagrams."""
import os, re

BASE = '/Users/chrisanastasiadis/chris-kb/docs'

def read(p): return open(p).read()
def write(p, c): open(p, 'w').write(c)

def insert_after_first_heading(content, section_md):
    """Insert section_md before the second ## heading (or at end)."""
    lines = content.split('\n')
    h2s = [i for i, l in enumerate(lines) if l.startswith('## ')]
    insert_at = h2s[1] if len(h2s) >= 2 else len(lines)
    result = lines[:insert_at] + ['', section_md, ''] + lines[insert_at:]
    return '\n'.join(result)

def insert_after_front_matter(content, section_md):
    """For pages with no ## headings, append after the intro paragraph."""
    return content.rstrip() + '\n\n' + section_md + '\n'

def has_diagram(content):
    return any(c in content for c in ['┌', '──►', '◄──'])

def add_diagram(path, section_md):
    full = os.path.join(BASE, path)
    content = read(full)
    if has_diagram(content):
        print(f'SKIP (has diagram): {path}')
        return
    h2s = [l for l in content.split('\n') if l.startswith('## ')]
    if h2s:
        new = insert_after_first_heading(content, section_md)
    else:
        new = insert_after_front_matter(content, section_md)
    write(full, new)
    print(f'ADDED: {path}')

# ─────────────────────────────────────────────────────────────────────────────
# DIAGRAMS
# ─────────────────────────────────────────────────────────────────────────────

DIAGRAMS = {}

DIAGRAMS['architecture/index.md'] = """\
## Enterprise Architecture Overview

```
  ┌────────────────────────────────────────────────────────────────────────────┐
  │                        Enterprise Data Centre                              │
  │                                                                            │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐     │
  │  │   Compute Tier   │  │   Storage Tier   │  │   Network Tier       │     │
  │  │                  │  │                  │  │                      │     │
  │  │  vSphere Cluster │  │  FlashArray      │  │  Core (leaf/spine)   │     │
  │  │  ESXi hosts      │  │  PowerMax        │  │  FC fabric (SAN)     │     │
  │  │  VCF / HCI       │  │  ONTAP AFF       │  │  NSX overlay         │     │
  │  └────────┬─────────┘  └────────┬─────────┘  └──────────┬───────────┘     │
  │           │                     │                       │                 │
  │  ┌────────▼─────────────────────▼───────────────────────▼───────────┐     │
  │  │                     Management Plane                              │     │
  │  │   vCenter   Pure1   CloudIQ   Aria Operations   NSX Manager      │     │
  │  └──────────────────────────────────────────────────────────────────┘     │
  │                                                                            │
  │  ┌──────────────────────────────────────────────────────────────────┐     │
  │  │                    DR / Data Protection                           │     │
  │  │   SRDF (PowerMax)  SnapMirror (ONTAP)  ActiveCluster (FlashArray)│     │
  │  │   Veeam / NetBackup / CommVault         SRM (VMware)             │     │
  │  └──────────────────────────────────────────────────────────────────┘     │
  └────────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['compute/linux/architecture/index.md'] = """\
## Server Role Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                       Linux Infrastructure                               │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Identity & Access                                               │    │
  │  │  SSSD ──► Active Directory (Kerberos / LDAP)                    │    │
  │  │  PAM  ──► MFA / CyberArk PSM proxy                              │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
  │  │  App Server  │  │  DB Server   │  │  Web Server  │  │  Bastion   │  │
  │  │  RHEL / Ubuntu│  │ Oracle/PGSQL │  │  Nginx/Apache│  │  SSH jump  │  │
  │  │  systemd     │  │  ASM / data  │  │  TLS cert    │  │  host      │  │
  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │
  │         │                 │                  │                │         │
  │  ┌──────▼─────────────────▼──────────────────▼────────────────▼──────┐  │
  │  │                    Shared Services                                  │  │
  │  │  NFS mounts (ONTAP)   iSCSI/FC LUNs   Syslog ──► SIEM             │  │
  │  │  NTP (Chrony)         DNS (resolv.conf) Monitoring (node exporter) │  │
  │  └─────────────────────────────────────────────────────────────────── ┘  │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['disaster-recovery/commvault/architecture/index.md'] = """\
## Component Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                     CommVault Architecture                               │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  CommServe (CS) — SQL Server backend                            │    │
  │  │  Job Manager / Scheduler / Index Cache / Web Console            │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │          │  job control              │  REST API                        │
  │  ┌───────▼──────────────────┐  ┌────▼──────────────────────────────┐   │
  │  │  Media Agents (MA)       │  │  Access Nodes (proxy)             │   │
  │  │  Dedup DB (DDB)          │  │  VSA proxy (VMware)               │   │
  │  │  Aux copy / replication  │  │  DB agent hosts                   │   │
  │  └───────┬──────────────────┘  └────────────────────────────────── ┘   │
  │          │  data path                                                   │
  │  ┌───────▼──────────────────────────────────────────────────────────┐   │
  │  │  Backup Targets                                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │   │
  │  │  │ Disk Library │  │  Tape / VTL │  │  Cloud (S3 / Azure Blob)│  │   │
  │  │  │ (Data Domain)│  │             │  │                         │  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────────────────┘  │   │
  │  └──────────────────────────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────────────────────────┘
  Sources: VMware VMs, SQL/Oracle/SAP HANA, Windows/Linux file systems, NAS
```"""

DIAGRAMS['disaster-recovery/netbackup/architecture/index.md'] = """\
## Three-Tier Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                     NetBackup Architecture                               │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Primary Server (Master Server)                                 │    │
  │  │  NetBackup catalogue  Policy DB  Job scheduler  EMM DB          │    │
  │  └──────────────────────────────┬──────────────────────────────────┘    │
  │                                 │  policy / job control                 │
  │         ┌───────────────────────┼────────────────────────┐              │
  │         │                       │                        │              │
  │  ┌──────▼──────┐        ┌───────▼──────┐        ┌───────▼──────┐       │
  │  │  Media Svr 1│        │  Media Svr 2 │        │  Media Svr 3 │       │
  │  │  (Site A)   │        │  (Site B/DR) │        │  (Cloud gate)│       │
  │  └──────┬──────┘        └───────┬──────┘        └───────┬──────┘       │
  │         │  data                 │                       │              │
  │  ┌──────▼──────┐        ┌───────▼──────┐        ┌───────▼──────┐       │
  │  │ Disk / MSDP │        │ Disk / MSDP  │        │  Cloud (S3)  │       │
  │  │ (dedup pool)│        │  (DR copy)   │        │  (long-term) │       │
  │  └─────────────┘        └──────────────┘        └──────────────┘       │
  │                                                                          │
  │  Clients: NBU agents on VMs, DB hosts, NAS NDMP, VMware backup host     │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['disaster-recovery/srm/architecture/index.md'] = """\
## SRM Topology

```
  Site A (Protected)                          Site B (Recovery)
  ──────────────────────────────────          ──────────────────────────────────
  ┌──────────────────────────────┐            ┌──────────────────────────────┐
  │  vCenter A                   │◄──────────►│  vCenter B                   │
  │  SRM A (plugin + server)     │  paired    │  SRM B (plugin + server)     │
  │  Storage Manager A (SRA)     │            │  Storage Manager B (SRA)     │
  └──────────────┬───────────────┘            └───────────────┬──────────────┘
                 │  SRA communicates                          │  SRA communicates
                 │  with storage array                        │  with storage array
  ┌──────────────▼───────────────┐            ┌───────────────▼──────────────┐
  │  Production Storage          │            │  DR Storage                  │
  │  FlashArray / PowerMax       │──replication│  FlashArray / PowerMax (DR)  │
  │  ONTAP / vSAN                │────────────►│  ONTAP / vSAN (DR)           │
  └──────────────────────────────┘            └──────────────────────────────┘
         │  VMs running                               │  VMs recovered here
  ┌──────▼───────────────────┐             ┌──────────▼──────────────────┐
  │  Protection Group        │  SRM plan   │  Recovery Plan              │
  │  (VMs + replication)     │────────────►│  (power-on order, IP remap) │
  └──────────────────────────┘             └────────────────────────────┘
```"""

DIAGRAMS['monitoring/aria-operations/architecture/index.md'] = """\
## Analytics Cluster Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                     Aria Operations Cluster                              │
  │                                                                          │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐   │
  │  │  Primary Node    │  │  Replica Node    │  │  Data Node(s)        │   │
  │  │  UI / scheduler  │  │  failover target │  │  additional capacity  │   │
  │  │  REST API        │  │                  │  │  for large fleets     │   │
  │  └─────────┬────────┘  └─────────┬────────┘  └──────────┬───────────┘   │
  │            └─────────────────────┴───────────────────────┘               │
  │                          cluster bus                                     │
  └───────────────────────────────────┬──────────────────────────────────────┘
                                      │  metrics pull
                    ┌─────────────────┼──────────────────────────┐
                    │                 │                           │
           ┌────────▼────────┐ ┌──────▼──────────┐  ┌───────────▼──────────┐
           │  Remote         │ │  Cloud Proxy     │  │  SNMP / REST         │
           │  Collector A    │ │  (SaaS / cloud)  │  │  Adapters            │
           │  (Site A)       │ │                  │  │  (network, storage)  │
           └────────┬────────┘ └──────────────────┘  └──────────────────────┘
                    │  collect
          ┌─────────▼────────────────────────────────────────────┐
          │  vCenter / ESXi / vSAN / NSX / Physical hosts        │
          │  Applications / Log sources / Storage endpoints       │
          └──────────────────────────────────────────────────────┘
```"""

DIAGRAMS['san/brocade/fabric-os/architecture/index.md'] = """\
## SAN Fabric Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                       Brocade SAN Fabric                                 │
  │                                                                          │
  │  Fabric A (primary)                         Fabric B (secondary)         │
  │  ─────────────────────────────              ─────────────────────────── │
  │  ┌─────────────────────────┐                ┌─────────────────────────┐  │
  │  │  Director A             │                │  Director B             │  │
  │  │  (6510/G720/X7)         │◄──ISL──────────►│  (6510/G720/X7)         │  │
  │  │  Slot 1-4: 48p 32Gb FC  │                │  Slot 1-4: 48p 32Gb FC  │  │
  │  └────┬────────────────────┘                └────┬────────────────────┘  │
  │       │  F_Port (host)                           │  F_Port (host)        │
  │       │  E_Port (ISL)                            │  E_Port (ISL)         │
  │  ┌────▼──────────┐                          ┌────▼──────────┐            │
  │  │  Edge Switch  │                          │  Edge Switch  │            │
  │  │  (G630 etc)   │                          │  (G630 etc)   │            │
  │  └────┬──────────┘                          └────┬──────────┘            │
  │       │  zones per VSAN                          │                       │
  │  ┌────▼────────────────────────────────────────────────────────────┐     │
  │  │  Hosts (HBA0 → Fabric A)   /   Hosts (HBA1 → Fabric B)          │     │
  │  │  Storage (CT0 → Fabric A)  /   Storage (CT1 → Fabric B)         │     │
  │  └──────────────────────────────────────────────────────────────── ┘     │
  │                                                                          │
  │  Zones: one initiator + one or more targets per zone (single-initiator)  │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['san/cisco/mds/architecture/index.md'] = """\
## MDS Fabric Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                         Cisco MDS SAN Fabric                             │
  │                                                                          │
  │  VSAN 10 (Production)                  VSAN 20 (Replication)             │
  │  ──────────────────────────            ─────────────────────────         │
  │  ┌──────────────────────┐              ┌──────────────────────┐          │
  │  │  MDS-9710 A          │◄────ISL─────►│  MDS-9710 B          │          │
  │  │  Slot 1: 48p 32Gb FC │  (PortChannel│  Slot 1: 48p 32Gb FC │          │
  │  │  Slot 2: 48p 32Gb FC │   4x16G)     │  Slot 2: 48p 32Gb FC │          │
  │  └─────────┬────────────┘              └─────────┬────────────┘          │
  │            │  F_Port / NP_Port                   │                       │
  │  ┌─────────▼────────────────────────────────────────────────────┐        │
  │  │  Device Aliases (pWWN → friendly name)                       │        │
  │  │  Zone Sets: prod-fabric-a / prod-fabric-b                    │        │
  │  │  Zones: <host-alias> + <storage-alias>                       │        │
  │  └─────────┬─────────────────────────────────────┬──────────────┘        │
  │            │                                     │                       │
  │  ┌─────────▼───────────┐              ┌──────────▼────────────┐          │
  │  │  Host HBAs (Fab A)  │              │  Storage Ports (Fab A)│          │
  │  │  ESXi / DB / App    │              │  FlashArray CT0        │          │
  │  │                     │              │  PowerMax Dir A        │          │
  │  └─────────────────────┘              └────────────────────── ─┘          │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['security/active-directory/architecture/index.md'] = """\
## Forest and Domain Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                         AD Forest                                        │
  │                                                                          │
  │  ┌────────────────────────────────────────────────────────────────┐     │
  │  │  Forest Root Domain  (corp.example.com)                        │     │
  │  │  ┌────────────────────────────────────────────────────────┐   │     │
  │  │  │  Schema Master  Domain Naming Master  Global Catalogue  │   │     │
  │  │  └────────────────────────────────────────────────────────┘   │     │
  │  │                                                                │     │
  │  │  ┌─────────────────────┐  ┌─────────────────────────────┐    │     │
  │  │  │  DC-01 (Site A PDC) │  │  DC-02 (Site A)             │    │     │
  │  │  │  RID / PDC Emulator │  │  Global Catalogue           │    │     │
  │  │  │  Infra Master       │  │                             │    │     │
  │  │  └────────┬────────────┘  └─────────────────────────────┘    │     │
  │  │           │ AD replication (inter-site: IP / SMTP)            │     │
  │  │  ┌────────▼──────────────────────────────────────────────┐   │     │
  │  │  │  DC-03 (Site B)  DC-04 (Site B)  — replica DCs        │   │     │
  │  │  └────────────────────────────────────────────────────────┘   │     │
  │  └────────────────────────────────────────────────────────────────┘     │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Child Domains (if used)                                        │    │
  │  │  eu.corp.example.com    apac.corp.example.com                   │    │
  │  │  (trust is automatic within forest — transitive two-way)        │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  └──────────────────────────────────────────────────────────────────────────┘
  DNS: every DC is also a DNS server; AD relies entirely on DNS SRV records
```"""

DIAGRAMS['security/certificates/architecture/index.md'] = """\
## PKI Hierarchy

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                        Enterprise PKI                                   │
  │                                                                         │
  │  ┌──────────────────────────────────────────────────────────────────┐  │
  │  │  Root CA  (offline — HSM or dedicated server, air-gapped)        │  │
  │  │  Self-signed, 4096-bit RSA or P-384 EC, 20yr validity            │  │
  │  │  Stored: locked cabinet / HSM — never brought online to issue    │  │
  │  └──────────────────────────┬───────────────────────────────────────┘  │
  │                             │  signed by Root CA                       │
  │  ┌──────────────────────────▼───────────────────────────────────────┐  │
  │  │  Issuing / Intermediate CA  (ADCS — Windows Server online)       │  │
  │  │  Enterprise CA — integrated with AD for auto-enrolment           │  │
  │  │  CRL published to CDP  |  OCSP responder on IIS                  │  │
  │  └───────┬────────────────────────────┬────────────────────────┬────┘  │
  │          │                            │                        │       │
  │  ┌───────▼────────┐  ┌───────────────▼──────┐  ┌─────────────▼──────┐ │
  │  │  Server Certs  │  │  User Certs           │  │  Code Signing      │ │
  │  │  TLS (2yr)     │  │  Smart card / S/MIME  │  │  CI/CD pipeline    │ │
  │  │  HTTPS/LDAPS   │  │  (1yr)                │  │  (1yr)             │ │
  │  └────────────────┘  └───────────────────────┘  └────────────────────┘ │
  └─────────────────────────────────────────────────────────────────────────┘
  Venafi / manual inventory monitors all certs for expiry and policy drift
```"""

DIAGRAMS['security/cyberark/architecture/index.md'] = """\
## PAM Component Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                         CyberArk PAM Platform                           │
  │                                                                          │
  │  ┌────────────────────────────────────────────────────────────────┐     │
  │  │  Digital Vault Server (DVS)                                    │     │
  │  │  Encrypted credential store  |  Hardened OS  |  No network FS  │     │
  │  │  DR Vault (async replication) ◄────────────────────────────    │     │
  │  └───────┬──────────────────────────────────────────┬────────────┘     │
  │          │  Vault API (TCP 1858)                    │                  │
  │  ┌───────▼──────────┐                    ┌──────────▼─────────────┐    │
  │  │  PVWA            │                    │  CPM                   │    │
  │  │  Web UI + REST   │                    │  Password rotation      │    │
  │  │  API gateway     │                    │  Verification & change │    │
  │  │  (IIS on Windows)│                    │  Platform plugins       │    │
  │  └───────┬──────────┘                    └────────────────────────┘    │
  │          │  session launch                                              │
  │  ┌───────▼──────────────────────────────────────────────────────────┐  │
  │  │  PSM  (Privileged Session Manager)                               │  │
  │  │  RDP / SSH proxy  |  Session recording  |  Keystroke logging     │  │
  │  │  No credential reaches end user — PSM injects transparently      │  │
  │  └──────────────────────────────────────────────────────────────────┘  │
  │          │  proxied session to target                                   │
  │  ┌───────▼──────────────────────────────────────────────────────────┐  │
  │  │  Target Systems                                                   │  │
  │  │  Windows servers  Linux / Unix  Network devices  Databases        │  │
  │  └──────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['security/venafi/architecture/index.md'] = """\
## Trust Protection Platform Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                    Venafi Trust Protection Platform (TPP)                │
  │                                                                          │
  │  ┌───────────────────────────────────────────────────────────────────┐  │
  │  │  TPP Server Cluster  (Windows — 2+ nodes for HA)                  │  │
  │  │  Policy Engine  |  Certificate Inventory  |  Workflow Engine      │  │
  │  │  REST API (Aperture)  |  Web Console (Aperture)                   │  │
  │  └───────────┬─────────────────────────────┬──────────────────────── ┘  │
  │              │  CA connector                │  discovery / agent        │
  │   ┌──────────▼──────────────────┐  ┌────────▼──────────────────────┐   │
  │   │  CA Backends                │  │  Discovery & Agents           │   │
  │   │  Microsoft ADCS             │  │  Network scan (port 443)      │   │
  │   │  DigiCert / Entrust         │  │  TPP Agent (on hosts)         │   │
  │   │  Let's Encrypt (ACME)       │  │  Adaptable CA (custom)        │   │
  │   │  HashiCorp Vault            │  │                               │   │
  │   └─────────────────────────────┘  └───────────────────────────────┘   │
  │              │  issue / renew                │  cert found               │
  │   ┌──────────▼──────────────────────────────▼──────────────────────┐   │
  │   │  Certificate Consumers                                          │   │
  │   │  IIS / Apache / Nginx   F5 / NetScaler   vCenter   Kubernetes   │   │
  │   │  Automation: Ansible playbooks  |  ACME clients  |  REST API   │   │
  │   └─────────────────────────────────────────────────────────────── ┘   │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['storage/dell/cloudiq/architecture/index.md'] = """\
## Data Pipeline Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  On-Premises                                                             │
  │                                                                          │
  │  ┌──────────────────────────────────────────────────────────────────┐   │
  │  │  Secure Connect Gateway (SCG) — virtual appliance               │   │
  │  │  Collects telemetry via REST from:                               │   │
  │  │  PowerMax  PowerStore  Unity  PowerScale  PowerFlex  Networking  │   │
  │  └─────────────────────────────────┬────────────────────────────── ┘   │
  │                                    │  HTTPS outbound (port 443)        │
  └────────────────────────────────────┼──────────────────────────────────┘
                                       │
  ┌────────────────────────────────────▼──────────────────────────────────┐
  │  Dell Cloud (CloudIQ SaaS)                                             │
  │                                                                        │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │
  │  │  Telemetry Store │  │  AI / ML Engine  │  │  REST API        │    │
  │  │  (time-series)   │  │  Anomaly detect  │  │  (customer use)  │    │
  │  │                  │  │  Capacity fcst   │  │                  │    │
  │  └──────────────────┘  └──────────────────┘  └──────────────────┘    │
  │                                                                        │
  │  Health Scores  |  Capacity Forecasts  |  Anomaly Alerts               │
  │  Web Dashboard  |  Email / Webhook notifications                       │
  └────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['storage/dell/cod/architecture/index.md'] = """\
## Capacity on Demand Model

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                  PowerMax COD — Capacity Unlock Model                    │
  │                                                                          │
  │  Physical drives installed at factory                                    │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  NVMe Drive Bay (all drives present in chassis)                 │    │
  │  │  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐  │    │
  │  │  │ Drv 1 │ │ Drv 2 │ │ Drv 3 │ │ Drv 4 │ │ Drv 5 │ │ Drv 6 │  │    │
  │  │  │ACTIVE │ │ACTIVE │ │ACTIVE │ │ LOCKED│ │ LOCKED│ │ LOCKED│  │    │
  │  │  │licensed│ │licensed│ │licensed│ │no lic │ │no lic │ │no lic │  │    │
  │  │  └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘  │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  │  Unlock process (no truck roll):                                         │
  │                                                                          │
  │  Purchase COD licence ──► Apply via SYMCLI / Unisphere                   │
  │                       ──► Array controller unlocks capacity instantly    │
  │                       ──► New storage available within minutes           │
  │                                                                          │
  │  symconfigure -cmd "unlock cod -capacity <TB>" commit                    │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['storage/dell/data-domain/architecture/index.md'] = """\
## Deduplication Pipeline

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                  Data Domain (PowerProtect DD) Architecture              │
  │                                                                          │
  │  Ingest                                                                  │
  │  ┌──────────────────────────────────────────────────────────────────┐   │
  │  │  Backup clients / media servers                                  │   │
  │  │  Veeam  NetBackup  CommVault  TSM  Oracle RMAN  NFS / CIFS / VTL│   │
  │  └────────────────────────────────┬─────────────────────────────── ┘   │
  │                                   │  data stream                       │
  │  ┌────────────────────────────────▼─────────────────────────────────┐  │
  │  │  SISL Inline Deduplication Engine                                │  │
  │  │  1. Segment stream into variable-length chunks                   │  │
  │  │  2. Fingerprint each chunk (SHA)                                 │  │
  │  │  3. Lookup FP in dedup index (DRAM + SSD cache)                  │  │
  │  │  4. If match: store reference only (no write to disk)            │  │
  │  │  5. If new: compress + write to active tier                      │  │
  │  └───────────────────────────────┬──────────────────────────────── ┘  │
  │                                  │  deduplicated + compressed data     │
  │  ┌─────────────────────────────── ▼────────────────────────────────┐   │
  │  │  Storage Tiers                                                   │   │
  │  │  ┌──────────────────┐  ┌───────────────────┐  ┌──────────────┐  │   │
  │  │  │  Active Tier     │  │  Retention Tier   │  │  Cloud Tier  │  │   │
  │  │  │  (SSD / NL-SAS)  │  │  (NL-SAS archive) │  │  (S3 / Azure)│  │   │
  │  │  └──────────────────┘  └───────────────────┘  └──────────────┘  │   │
  │  └──────────────────────────────────────────────────────────────────┘  │
  │  Typical dedupe ratio: 20:1 across mixed backup workloads               │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['storage/dell/ecs/architecture/index.md'] = """\
## Scale-Out Object Storage Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                      ECS Scale-Out Architecture                          │
  │                                                                          │
  │  VDC 1 (Site A)                          VDC 2 (Site B)                  │
  │  ─────────────────────────────           ─────────────────────────────── │
  │  ┌─────────────────────────┐             ┌─────────────────────────┐     │
  │  │  ECS Node 1  Node 2     │◄────────────►│  ECS Node 5  Node 6     │     │
  │  │  Node 3      Node 4     │  geo-replic  │  Node 7      Node 8     │     │
  │  │  (x86 commodity)        │             │  (x86 commodity)        │     │
  │  └────────────┬────────────┘             └─────────────────────────┘     │
  │               │                                                          │
  │  ┌────────────▼─────────────────────────────────────────────────────┐   │
  │  │  ECS Data Services                                               │   │
  │  │  S3 API  |  Swift  |  Atmos  |  CAS (content-addressable)       │   │
  │  │  Erasure coding (4+2 / 12+4)  |  Metadata indexing              │   │
  │  └────────────┬─────────────────────────────────────────────────── ┘   │
  │               │  HTTPS / S3                                             │
  │  ┌────────────▼──────────────────────────────────────────────────────┐  │
  │  │  Clients                                                           │  │
  │  │  Backup (Data Domain Cloud Tier)  Analytics  Archive  Media/CDN   │  │
  │  └───────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['storage/dell/powermax/architecture/index.md'] = """\
## Array Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                     PowerMax 8000 Architecture                           │
  │                                                                          │
  │  ┌──────────────────────────────────────────────────────────────────┐   │
  │  │  Director Layer (active-active, all directors share all drives)  │   │
  │  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │   │
  │  │  │  FA Dir A  │  │  FA Dir B  │  │  SRDF Dir  │  │  SRDF Dir  │ │   │
  │  │  │  FC/NVMe   │  │  FC/NVMe   │  │  repl ports│  │  repl ports│ │   │
  │  │  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘ │   │
  │  └─────────┼───────────────┼───────────────┼───────────────┼────────┘   │
  │            └───────────────┴───────────────┴───────────────┘            │
  │                         crossbar fabric                                  │
  │  ┌──────────────────────────────────────────────────────────────────┐   │
  │  │  NVMe Flash (NVMe-SCM / eTLC)  — RAID-5(7+1) / RAID-6(6+2)      │   │
  │  └──────────────────────────────────────────────────────────────────┘   │
  └─────────────────────────┬─────────────────────────┬─────────────────────┘
                            │  FC / NVMe-oF            │  SRDF
            ┌───────────────▼──────────────┐  ┌────────▼─────────────────┐
            │  SAN Fabric (Brocade/MDS)    │  │  Remote PowerMax         │
            │  Hosts: Oracle / SAP / SQL   │  │  (SRDF/S or SRDF/A)      │
            └──────────────────────────────┘  └──────────────────────────┘
```"""

DIAGRAMS['storage/dell/powerpath/architecture/index.md'] = """\
## Host-Side MPIO Stack

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                      Host (Windows / Linux / AIX)                        │
  │                                                                          │
  │  ┌──────────────────────────────────────────────────────────────────┐   │
  │  │  Application (Oracle / SQL Server / File System)                 │   │
  │  └──────────────────────────────────┬───────────────────────────── ┘   │
  │                                     │  I/O                              │
  │  ┌──────────────────────────────────▼───────────────────────────────┐   │
  │  │  PowerPath Virtual Device (pseudo device, single LUN view)       │   │
  │  │  Intelligent load balancing  |  Automatic failover               │   │
  │  │  ALUA-aware path selection   |  Policy: CLAROpt / RoundRobin     │   │
  │  └───────────────┬──────────────────────────┬────────────────────── ┘   │
  │                  │  Active path              │  Standby / secondary path │
  │  ┌───────────────▼──────────┐  ┌────────────▼──────────────────────┐    │
  │  │  HBA0 (Fabric A)         │  │  HBA1 (Fabric B)                  │    │
  │  │  FC / NVMe-oF            │  │  FC / NVMe-oF                     │    │
  │  └───────────────┬──────────┘  └────────────┬──────────────────────┘    │
  └──────────────────┼─────────────────────────┼────────────────────────────┘
                     │  FC / NVMe-oF            │
             ┌───────▼──────────────────────────▼───────┐
             │  PowerMax  (CT0 → Fabric A, CT1 → Fab B)  │
             │  ALUA: preferred port = owning director   │
             └──────────────────────────────────────────┘
```"""

DIAGRAMS['storage/dell/powerscale/architecture/index.md'] = """\
## Scale-Out NAS Cluster

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                  PowerScale (OneFS) Cluster                              │
  │                                                                          │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
  │  │  Node 1  │  │  Node 2  │  │  Node 3  │  │  Node N  │  │  Node N+1│  │
  │  │  F810    │  │  F810    │  │  F810    │  │  H700    │  │  A2000   │  │
  │  │  (flash) │  │  (flash) │  │  (flash) │  │ (hybrid) │  │(archive) │  │
  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
  │       └────────────────────────────────────────────────────────┘        │
  │                       InfiniBand / 25 GbE backend                       │
  │                       (OneFS distributed storage fabric)                │
  │                                                                          │
  │  ┌──────────────────────────────────────────────────────────────────┐   │
  │  │  Frontend network (10/25 GbE)                                    │   │
  │  │  SmartConnect DNS  ──► distributes client connections            │   │
  │  └──────────────────────────────────────────────────────────────────┘   │
  │              │  NFS v3/v4  SMB 2/3  HDFS  S3  FTP                       │
  │  ┌───────────▼─────────────────────────────────────────────────────┐    │
  │  │  Clients  (Linux, Windows, Hadoop, AI/ML GPU nodes)              │    │
  │  └──────────────────────────────────────────────────────────────────┘    │
  │  Single namespace: /ifs  — visible from all nodes simultaneously        │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['storage/dell/unity/architecture/index.md'] = """\
## Dual Storage Processor Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                      Dell Unity XT Chassis                               │
  │                                                                          │
  │  ┌───────────────────────────────────────────────────────────────────┐  │
  │  │                    System Bay                                     │  │
  │  │  ┌───────────────────────┐     ┌───────────────────────┐         │  │
  │  │  │  Storage Processor A  │◄───►│  Storage Processor B  │         │  │
  │  │  │  (active for set A)   │ HA  │  (active for set B)   │         │  │
  │  │  │  FC / iSCSI / NFS     │ peer│  FC / iSCSI / NFS     │         │  │
  │  │  │  SMB ports            │ link│  SMB ports             │         │  │
  │  │  └──────────┬────────────┘     └────────────┬──────────┘         │  │
  │  └─────────────┼────────────────────────────────┼────────────────────┘  │
  │                │  SAS / FC-AL                   │                       │
  │  ┌─────────────▼────────────────────────────────▼────────────────────┐  │
  │  │  Drive Enclosures                                                  │  │
  │  │  SSD (all-flash)  NL-SAS (hybrid)  Tightly coupled to chassis     │  │
  │  └────────────────────────────────────────────────────────────────── ┘  │
  └──────────────────────────────────────────────────────────────────────────┘
  Block: Fibre Channel / iSCSI LUNs  |  File: NFS / SMB (via NAS head)
  Managed via Unisphere for Unity GUI  |  uemcli (CLI)  |  REST API
```"""

DIAGRAMS['storage/dell/vplex/architecture/index.md'] = """\
## Storage Federation Topology

```
  Site A                                          Site B
  ──────────────────────────────────              ──────────────────────────────
  ┌──────────────────────────────┐               ┌──────────────────────────────┐
  │   VPLEX VS2 Cluster (Geo)    │               │   VPLEX VS2 Cluster (Geo)    │
  │   Director Pair 1  Dir Pair 2│◄──WAN/DS3────►│   Director Pair 1  Dir Pair 2│
  │   GeoSynchrony OS            │  synchronous  │   GeoSynchrony OS            │
  └───────┬──────────────────────┘  replication  └──────────┬───────────────────┘
          │  FC (back-end)                                   │  FC (back-end)
  ┌───────▼────────────┐                          ┌──────────▼───────────────┐
  │  Local Arrays      │                          │  Local Arrays (DR site)  │
  │  PowerMax / Unity  │                          │  PowerMax / Unity        │
  │  (physical volumes)│                          │  (mirrored extent)       │
  └────────────────────┘                          └──────────────────────────┘
          │  FC (front-end)                                  │
  ┌───────▼─────────────────────────────────────────────────▼──────────────┐
  │  Hosts — see single virtual volume regardless of which site owns it    │
  │  Active/Active cross-site — no host changes during site migration      │
  └─────────────────────────────────────────────────────────────────────── ┘
```"""

DIAGRAMS['storage/netapp/keystone/architecture/index.md'] = """\
## STaaS Consumption Model

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  Customer Data Centre (or colocation)                                    │
  │                                                                          │
  │  ┌────────────────────────────────────────────────────────────────┐     │
  │  │  NetApp-owned Hardware (managed by NetApp or partner)          │     │
  │  │  AFF (block/file)   FAS (hybrid)   StorageGRID (object)        │     │
  │  │  Installed, monitored, and maintained by NetApp                │     │
  │  └───────────────────────────────────┬──────────────────────────── ┘     │
  │                                      │  HTTPS telemetry                 │
  │  ┌───────────────────────────────────▼─────────────────────────────┐    │
  │  │  Keystone Collector (lightweight agent VM)                      │    │
  │  │  Measures consumed capacity per service tier per hour           │    │
  │  └───────────────────────────────────┬─────────────────────────────┘    │
  └─────────────────────────────────────┼──────────────────────────────────┘
                                        │  usage data
  ┌─────────────────────────────────────▼──────────────────────────────────┐
  │  NetApp Cloud / ActiveIQ                                                │
  │  ┌───────────────────┐  ┌───────────────────┐  ┌─────────────────────┐ │
  │  │  Consumption      │  │  Billing Engine   │  │  Customer Portal    │ │
  │  │  Metering         │  │  Committed + burst│  │  Capacity dashboard │ │
  │  └───────────────────┘  └───────────────────┘  └─────────────────────┘ │
  └────────────────────────────────────────────────────────────────────────┘
  Customer pays for committed reserve + burst overage; no CapEx
```"""

DIAGRAMS['storage/netapp/snapmirror/architecture/index.md'] = """\
## Replication Modes

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                    SnapMirror Architecture                               │
  │                                                                          │
  │  Source Cluster                            Destination Cluster           │
  │  ─────────────────────────────────         ────────────────────────────  │
  │  ┌───────────────────────────────┐         ┌──────────────────────────┐  │
  │  │  SVM / Volume (R/W)           │         │  SVM / Volume (DP/RO)    │  │
  │  │                               │         │                          │  │
  │  │  SnapMirror Async  ───────────┼─────────►  RPO = schedule interval │  │
  │  │  (XDP / SnapVault)            │         │  (hourly / daily)        │  │
  │  │                               │         │                          │  │
  │  │  SnapMirror Sync  ◄───────────┼─────────►  RPO = 0 (synchronous)  │  │
  │  │  (SM-S / SMBC)                │  NVLOG  │  AutomatedFailOver (SAN) │  │
  │  │                               │  mirror │                          │  │
  │  └───────────────────────────────┘         └──────────────────────────┘  │
  │                                                                          │
  │  Relationship management always from destination:                        │
  │  snapmirror create / initialize / update / resync / break / quiesce     │
  │                                                                          │
  │  Mediator (SM-S): third cluster or host — tiebreak for transparent      │
  │  failover when both clusters disagree on primary state                  │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['storage/pure/evergreen-one/architecture/index.md'] = """\
## STaaS Delivery Model

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  Customer Site (or colocation)                                           │
  │                                                                          │
  │  ┌────────────────────────────────────────────────────────────────┐     │
  │  │  Pure-owned FlashArray / FlashBlade hardware                   │     │
  │  │  Installed + monitored + maintained by Pure Storage            │     │
  │  │  Controller refreshes happen non-disruptively at EOG           │     │
  │  └──────────────────────────────┬─────────────────────────────── ┘     │
  │                                 │  phone-home (HTTPS 443)               │
  │  ┌──────────────────────────────▼──────────────────────────────────┐   │
  │  │  Pure1 Cloud (telemetry + AIOps)                                │   │
  │  │  Consumption metering  Health monitoring  Capacity forecasting  │   │
  │  └──────────────────────────────┬───────────────────────────────── ┘   │
  └────────────────────────────────┼────────────────────────────────────── ┘
                                   │  usage data ──► monthly invoice
  ┌────────────────────────────────▼──────────────────────────────────────┐
  │  Pure Storage Billing Portal                                           │
  │  Committed reserve tier + burst + professional services               │
  └────────────────────────────────────────────────────────────────────────┘
  Customer: no CapEx, no hardware ownership, Pure responsible for SLAs
```"""

DIAGRAMS['storage/pure/evergreen/architecture/index.md'] = """\
## Controller Refresh Model

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                  Evergreen — Non-Disruptive Controller Swap              │
  │                                                                          │
  │  Before refresh                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Chassis: Gen 5 CT0 + CT1  │  NVMe Drive Shelf (customer-owned) │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  │  During refresh (hosts stay connected, I/O continues)                   │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Step 1: Pure installs Gen 6 CT0 alongside Gen 5 CT0            │    │
  │  │  Step 2: Ownership migrates non-disruptively                    │    │
  │  │  Step 3: Gen 5 CT0 removed; repeat for CT1                      │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  │  After refresh                                                           │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Chassis: Gen 6 CT0 + CT1  │  Same NVMe Drive Shelf (unchanged) │    │
  │  │  Data unchanged — no migration, no downtime, no host rescan      │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │                                                                          │
  │  Subscription covers: controller hardware, Purity upgrades, support     │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['storage/pure/flashblade/architecture/index.md'] = """\
## Scale-Out Blade Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                     FlashBlade Chassis (17U)                             │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Fabric Management Module (FMM)  /  Blade Mgmt Module (BMM)     │    │
  │  │  NVMe-oF internal fabric  |  Out-of-band management plane       │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
  │  │ Blade 01 │ │ Blade 02 │ │ Blade 03 │ │  ...     │ │ Blade 15 │     │
  │  │ CPU+NVMe │ │ CPU+NVMe │ │ CPU+NVMe │ │          │ │ CPU+NVMe │     │
  │  │ 17 / 52T │ │ 17 / 52T │ │ 17 / 52T │ │          │ │ 17 / 52T │     │
  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
  │       └────────────┴────────────┴─────────────┴────────────┘           │
  │                         internal NVMe-oF fabric                        │
  └──────────────────────────────┬──────────────────────────────────────────┘
                                 │  10 / 25 / 100 GbE
               ┌─────────────────▼───────────────────────┐
               │  Ethernet Fabric (leaf-spine)            │
               │  NFS v3/v4.1  |  S3  |  SMB  |  NFS/S3  │
               └────────────────┬────────────────────────┘
                                │
        ┌───────────────────────▼────────────────────────────┐
        │  Clients                                            │
        │  GPU nodes (AI/ML)  Hadoop  Backup  Analytics       │
        └─────────────────────────────────────────────────────┘
  Scale: 1 to 15 blades per chassis, up to 20 chassis in a cluster
```"""

DIAGRAMS['virtualization/vmware/aria-operations-for-logs/architecture/index.md'] = """\
## Log Pipeline Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                   Aria Operations for Logs Cluster                       │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Master Node                                                    │    │
  │  │  Query engine  |  Index coordinator  |  Web UI  |  REST API    │    │
  │  └──────────────────────────────┬──────────────────────────────── ┘    │
  │                                 │  cluster replication                 │
  │  ┌──────────────────────────────▼──────────────────────────────────┐   │
  │  │  Worker Nodes (2+)                                              │   │
  │  │  Elasticsearch index shards  |  Log storage  |  Query workers  │   │
  │  └─────────────────────────────────────────────────────────────── ┘   │
  └───────────────────────────────────┬──────────────────────────────────── ┘
                                      │  log ingestion
          ┌───────────────────────────┼────────────────────────────┐
          │                           │                            │
  ┌───────▼────────┐         ┌────────▼────────┐          ┌───────▼────────┐
  │  Syslog agent  │         │  Syslog (UDP    │          │  REST API      │
  │  (LI agent on  │         │  514 / TCP 1514)│          │  ingest        │
  │  ESXi / vCenter│         │  Windows events │          │  (third-party) │
  └───────┬────────┘         └─────────────────┘          └────────────────┘
          │
  ┌───────▼─────────────────────────────────────────────────────────────┐
  │  Sources                                                             │
  │  ESXi  vCenter  NSX  vSAN  physical hosts  firewalls  Linux/Windows  │
  └──────────────────────────────────────────────────────────────────── ┘
```"""

DIAGRAMS['virtualization/vmware/aria-suite-lifecycle/architecture/index.md'] = """\
## Product Management Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                  Aria Suite Lifecycle (LCM) Appliance                    │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  LCM Core Services                                              │    │
  │  │  Deployment engine  |  Certificate manager  |  Password manager │    │
  │  │  Inventory / environment registry  |  Upgrade orchestrator      │    │
  │  └──────────────────────────────────────────────────────────────── ┘    │
  │          │  deploy / upgrade / configure                                │
  │  ┌───────┴─────────────────────────────────────────────────────────┐   │
  │  │  Managed Products                                               │   │
  │  │  ┌─────────────────┐  ┌────────────────────┐  ┌──────────────┐  │   │
  │  │  │  Aria Operations│  │  Aria Automation   │  │  Aria Ops    │  │   │
  │  │  │  (vROps)        │  │  (vRA)             │  │  for Logs    │  │   │
  │  │  └─────────────────┘  └────────────────────┘  └──────────────┘  │   │
  │  │  ┌─────────────────┐  ┌────────────────────┐                    │   │
  │  │  │  Identity Mgr   │  │  Other Aria suite  │                    │   │
  │  │  │  (Workspace ONE)│  │  products          │                    │   │
  │  │  └─────────────────┘  └────────────────────┘                    │   │
  │  └─────────────────────────────────────────────────────────────────┘   │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  NFS content library  ←  Binary store / patch bundles           │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['virtualization/vmware/vcenter/architecture/index.md'] = """\
## vSphere Cluster Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                          vSphere Cluster                                 │
  │                                                                          │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
  │  │   ESXi-01    │  │   ESXi-02    │  │   ESXi-03    │  │  ESXi-04   │  │
  │  │  vmnic0/1    │  │  vmnic0/1    │  │  vmnic0/1    │  │  vmnic0/1  │  │
  │  │  vmnic2/3    │  │  vmnic2/3    │  │  vmnic2/3    │  │  vmnic2/3  │  │
  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬─────┘  │
  └─────────┼─────────────────┼─────────────────┼─────────────────┼────────┘
            └─────────────────┴─────────────────┴─────────────────┘
                         vSphere Distributed Switch (VDS)
                         VM / vMotion / Storage / Management VMkernel
                                        │
                    ┌───────────────────▼──────────────────────────┐
                    │  vCenter Server Appliance (VCSA)              │
                    │  Embedded PSC  |  PostgreSQL DB               │
                    │  DRS  HA  vMotion  Lifecycle Manager          │
                    │  vSphere Client  |  REST API  |  MOB          │
                    └───────────────────────────────────────────────┘
                                        │  management
                    ┌───────────────────▼──────────────────────────┐
                    │  Shared Storage                               │
                    │  FlashArray (VMFS / vVols)  |  vSAN (local)  │
                    │  ONTAP NFS datastores                         │
                    └───────────────────────────────────────────────┘
```"""

DIAGRAMS['virtualization/vmware/vmware-cloud-foundation/architecture/index.md'] = """\
## SDDC Stack Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                  VMware Cloud Foundation (VCF)                           │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  SDDC Manager                                                   │    │
  │  │  Lifecycle orchestration  |  Workload domain management         │    │
  │  │  Certificate / password management  |  API / UI                 │    │
  │  └───────────────────────────────────────────────────────────────── ┘    │
  │          │  manages                                                      │
  │  ┌───────┴────────────────────────────────────────────────────────┐     │
  │  │  Workload Domains                                              │     │
  │  │  ┌──────────────────────┐    ┌──────────────────────────────┐  │     │
  │  │  │  Management Domain   │    │  VI Workload Domain(s)       │  │     │
  │  │  │  vCenter (mgmt)      │    │  vCenter (workload)          │  │     │
  │  │  │  NSX Manager cluster │    │  NSX (per domain or shared)  │  │     │
  │  │  │  vSAN (mgmt)         │    │  vSAN / external storage     │  │     │
  │  │  └──────────────────────┘    └──────────────────────────────┘  │     │
  │  └────────────────────────────────────────────────────────────────┘     │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Shared Services (Cloud Builder automates day-0 bring-up)       │    │
  │  │  vCenter  NSX  vSAN  SDDC Manager  Aria Ops  Aria Automation    │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  └──────────────────────────────────────────────────────────────────────────┘
```"""

DIAGRAMS['virtualization/vmware/vsan/architecture/index.md'] = """\
## Cluster Storage Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                     vSAN Cluster                                         │
  │                                                                          │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
  │  │    ESXi-01       │  │    ESXi-02       │  │    ESXi-03       │      │
  │  │  ┌────┐ ┌──────┐ │  │  ┌────┐ ┌──────┐ │  │  ┌────┐ ┌──────┐│      │
  │  │  │NVMe│ │ SSD  │ │  │  │NVMe│ │ SSD  │ │  │  │NVMe│ │ SSD  ││      │
  │  │  │cache│ │ cap  │ │  │  │cache│ │ cap  │ │  │  │cache│ │ cap  ││      │
  │  │  └──┬─┘ └──┬───┘ │  │  └──┬─┘ └──┬───┘ │  │  └──┬─┘ └──┬───┘│      │
  │  │     └──┬───┘     │  │     └──┬───┘     │  │     └──┬───┘     │      │
  │  │   Disk Group 1   │  │   Disk Group 1   │  │   Disk Group 1   │      │
  │  └──────────┬───────┘  └──────────┬───────┘  └──────────┬───────┘      │
  └─────────────┼─────────────────────┼─────────────────────┼──────────────┘
                └─────────────────────┴─────────────────────┘
                     vSAN VMkernel (dedicated 10/25 GbE VLAN)
                     Object components distributed across all hosts

  FTT=1 RAID-1: 2 data replicas + 1 witness  — survives 1 host loss
  FTT=1 RAID-5: 4+ hosts, stripe+parity       — 1.33x overhead
  FTT=2 RAID-6: 6+ hosts                      — survives 2 host failures
```"""

DIAGRAMS['virtualization/vxrail/architecture/index.md'] = """\
## HCI Node Cluster

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                       VxRail Cluster                                     │
  │                                                                          │
  │  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐ │
  │  │   VxRail Node 1    │  │   VxRail Node 2    │  │   VxRail Node N    │ │
  │  │   ESXi             │  │   ESXi             │  │   ESXi             │ │
  │  │   NVMe cache       │  │   NVMe cache       │  │   NVMe cache       │ │
  │  │   SSD / NL-SAS cap │  │   SSD / NL-SAS cap │  │   SSD / NL-SAS cap │ │
  │  │   25 GbE NICs      │  │   25 GbE NICs      │  │   25 GbE NICs      │ │
  │  └─────────┬──────────┘  └─────────┬──────────┘  └─────────┬──────────┘ │
  └────────────┼─────────────────────── ┼────────────────────────┼───────────┘
               └─────────────────────────────────────────────────┘
                        25 GbE ToR switch (leaf-spine)
                        vSAN, vMotion, VM, management traffic

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  VxRail Manager (VM on cluster)                                          │
  │  Lifecycle management  |  Day-0 bring-up  |  vCenter integration        │
  │  HW firmware + ESXi + vSAN coordinated upgrade via VxRail LCM           │
  └──────────────────────────────────────────────────────────────────────────┘
  Part of VCF on VxRail: SDDC Manager orchestrates workload domains
```"""

# ─────────────────────────────────────────────────────────────────────────────
# MOVE operations: extract from index pages, add to architecture pages
# These overwrite destination if it already has the matching section,
# otherwise prepend as a new section.
# ─────────────────────────────────────────────────────────────────────────────

MOVES = [
    # (source_index_path, section_heading, dest_arch_path)
    (
        'storage/pure/flasharray/index.md',
        '## ActiveCluster Topology',
        'storage/pure/flasharray/architecture/index.md',
    ),
    (
        'storage/netapp/ontap/index.md',
        '## HA Pair Topology',
        'storage/netapp/ontap/architecture/index.md',
    ),
    (
        'storage/dell/powermax/index.md',
        '## PowerMax Architecture',
        'storage/dell/powermax/architecture/index.md',
    ),
    (
        'san/brocade/index.md',
        '## SAN Fabric Topology',
        'san/brocade/fabric-os/architecture/index.md',
    ),
    (
        'san/cisco/index.md',
        '## Cisco MDS Fabric Topology',
        'san/cisco/mds/architecture/index.md',
    ),
    (
        'virtualization/vmware/index.md',
        '## vSphere Cluster Topology',
        'virtualization/vmware/vcenter/architecture/index.md',
    ),
    (
        'virtualization/vmware/vsan/index.md',
        '## vSAN Cluster Topology',
        'virtualization/vmware/vsan/architecture/index.md',
    ),
]

def extract_section(content, heading):
    """Extract a ## section from content; return (section_text, content_without_section)."""
    pattern = rf'(?m)^{re.escape(heading)}\n[\s\S]+?(?=^## |\Z)'
    m = re.search(pattern, content)
    if not m:
        return None, content
    section = m.group(0).rstrip()
    # Remove the section from source (also remove leading blank line before it)
    new_content = content[:m.start()].rstrip() + '\n' + content[m.end():]
    return section, new_content.lstrip('\n')

def prepend_section(content, section_md):
    """Add section_md before the first ## heading in content."""
    lines = content.split('\n')
    h2s = [i for i, l in enumerate(lines) if l.startswith('## ')]
    if h2s:
        insert_at = h2s[0]
        result = lines[:insert_at] + [section_md, ''] + lines[insert_at:]
        return '\n'.join(result)
    return section_md + '\n\n' + content

# ─────────────────────────────────────────────────────────────────────────────
# EXECUTE MOVES
# ─────────────────────────────────────────────────────────────────────────────
print('\n=== MOVES ===')
for src_rel, heading, dst_rel in MOVES:
    src = os.path.join(BASE, src_rel)
    dst = os.path.join(BASE, dst_rel)
    src_content = read(src)
    section, stripped = extract_section(src_content, heading)
    if section is None:
        print(f'NOT FOUND: {heading} in {src_rel}')
        continue
    # Write stripped source
    write(src, stripped)
    # Add to destination (prepend before first ## or after title)
    dst_content = read(dst)
    if heading in dst_content:
        print(f'ALREADY IN DEST: {heading} in {dst_rel}')
    else:
        new_dst = prepend_section(dst_content, section)
        write(dst, new_dst)
    print(f'MOVED: {heading}\n  from {src_rel}\n    to {dst_rel}')

# ─────────────────────────────────────────────────────────────────────────────
# EXECUTE ADDITIONS
# ─────────────────────────────────────────────────────────────────────────────
print('\n=== ADDITIONS ===')
for rel_path, section_md in DIAGRAMS.items():
    add_diagram(rel_path, section_md)

print('\nDone.')
