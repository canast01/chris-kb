# Protocols

<div class="kb-summary">
Reference coverage for the networking and storage protocols used in enterprise infrastructure — Fibre Channel, iSCSI, NFS, SMB, NTP, SNMP, TLS, DNS, DHCP, and LDAP.
</div>
```text
┌───────────────────────────────────────── Protocol Landscape ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │   Block Storage Proto.      │  │      File Protocols         │  │   Management Protocols      │   │
│   │  FC: 8/16/32/64G block      │  │  NFS: TCP 2049 (file)       │  │  SNMP: UDP 161/162 trap     │   │
│   │  iSCSI: TCP 3260 (IP)       │  │  SMB: TCP 445 (Windows)     │  │  NTP: UDP 123 time sync     │   │
│   │  WWPN/WWNN addressing       │  │  iSCSI also serves file     │  │  DNS: UDP/TCP 53 naming     │   │
│   │  Zoning: hard/soft/WWN      │  │  NFS: Unix ACLs + Kerb      │  │  DHCP: UDP 67/68 IP         │   │
│   │  Multipath: ALUA failovr    │  │  SMB3: encrypt+multichan    │  │  SNMP v3: auth+encrypt      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                 ▼                                ▼                                ▼                   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │    TLS / Certificates       │  │     LDAP / LDAPS            │  │  Logging & Integration      │   │
│   │  TLS 1.2+ (TCP 443/8443)    │  │  LDAP: TCP 389 (plain)      │  │  Syslog: UDP 514 / TLS      │   │
│   │  Certificate: CA-signed     │  │  LDAPS: TCP 636 (TLS)       │  │  SMTP: TCP 25/587 relay     │   │
│   │  SNI: multi-tenant TLS      │  │  StartTLS on port 389       │  │  API: HTTPS REST / JSON     │   │
│   │  mTLS: client certs         │  │  Bind: simple/SASL/Kerb     │  │  Webhooks: HTTP POST        │   │
│   │  OCSP/CRL revocation        │  │  Search: filter + attrs     │  │  Service hooks: REST        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Proto   │  Port(s)    │  Transport  │  Layer  │  Primary use in enterprise infrastructure     │   │
│   ├───────────────────────────────────────────────────────────────────────────────────────────────┤   │
│   │ FC      │  N/A (SAN)  │  Fibre Ch.  │  L2/L3  │  Block storage to hosts via SAN fabric        │   │
│   │ iSCSI   │  3260       │  TCP/IP     │  L4-7   │  Block storage over IP network                │   │
│   │ NFS     │  2049       │  TCP/IP     │  L4-7   │  Unix/Linux file mounts from NAS              │   │
│   │ SMB     │  445        │  TCP/IP     │  L4-7   │  Windows file shares and DFS namespaces       │   │
│   │ TLS     │  443/8443   │  TCP/IP     │  L4-7   │  Encryption wrapper for HTTPS, LDAPS          │   │
│   │ LDAP    │  389/636    │  TCP/IP     │  L4-7   │  Directory queries and authentication         │   │
│   │ SNMP    │  161/162    │  UDP        │  L4-7   │  Device monitoring, polling, and traps        │   │
│   │ NTP     │  123        │  UDP        │  L4-7   │  Time synchronization across all devices      │   │
│   │ DNS     │  53         │  UDP/TCP    │  L4-7   │  Name resolution for all infrastructure       │   │
│   │ DHCP    │  67/68      │  UDP        │  L4     │  Dynamic IP address assignment to hosts       │   │
│   │ Syslog  │  514/6514   │  UDP/TCP    │  L4-7   │  Centralised log collection and forwarding    │   │
│   │ SMTP    │  25/587     │  TCP        │  L4-7   │  Email relay for alerts and notifications     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SAN switches (FC) · 10/25/100 GbE NICs · DNS/NTP servers · Log collectors                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  WWPN    = World Wide Port Name; unique 8-byte FC HBA port identifier                                 │
│  FLOGI   = Fabric Login; process by which an FC HBA registers with the fabric                         │
│  Zoning  = FC fabric access control; restricts initiator-to-target visibility                         │
│  IQN     = iSCSI Qualified Name; unique identifier for iSCSI initiators and targets                   │
│  CHAP    = Challenge Handshake Auth; authenticates iSCSI initiators to targets                        │
│  NFS v4  = Stateful NFS with built-in Kerberos auth, ACLs, and file delegations                       │
│  SMB3    = SMB version 3.0+; adds multichannel, encryption, and cluster witness                       │
│  LDAPS   = LDAP over TLS on port 636; preferred over StartTLS for security                            │
│  Syslog  = UDP/TCP log forwarding; RFC 5424 structured format preferred                               │
│  SNMP v3 = SNMPv3; adds authentication (MD5/SHA) and encryption (DES/AES)                             │
│  SMTP    = Simple Mail Transfer Protocol; used for alert routing from infra tools                     │
│  TLS     = Transport Layer Security; cryptographic protocol protecting data in transit                │
│  DHCP    = Dynamic Host Configuration Protocol; assigns IP, mask, gateway, DNS                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="dhcp/">
  <strong>DHCP</strong>
  <span>IP address lease management, scope configuration, reservations, and relay agent troubleshooting.</span>
</a>

<a class="kb-card" href="dns/">
  <strong>DNS</strong>
  <span>Name resolution, zone management, record types, TTL, and DNS troubleshooting.</span>
</a>

<a class="kb-card" href="fibre-channel/">
  <strong>Fibre Channel</strong>
  <span>FC protocol fundamentals, WWN addressing, zoning, and login (FLOGI/PLOGI/PRLI) troubleshooting.</span>
</a>

<a class="kb-card" href="iscsi/">
  <strong>iSCSI</strong>
  <span>Block storage over IP: initiator/target configuration, IQN naming, CHAP auth, and path management.</span>
</a>

<a class="kb-card" href="ldap/">
  <strong>LDAP</strong>
  <span>Directory service query protocol for authentication and attribute lookup, with bind and search operations.</span>
</a>

<a class="kb-card" href="nfs/">
  <strong>NFS</strong>
  <span>Network File System exports, mount options, version differences (v3 vs v4.1), and permission mapping.</span>
</a>

<a class="kb-card" href="ntp/">
  <strong>NTP</strong>
  <span>Network time synchronization, stratum hierarchy, server configuration, and drift troubleshooting.</span>
</a>

<a class="kb-card" href="smb/">
  <strong>SMB</strong>
  <span>Windows file sharing protocol including SMB versions, share permissions, signing, and diagnostics.</span>
</a>

<a class="kb-card" href="snmp/">
  <strong>SNMP</strong>
  <span>Network device monitoring via SNMP v2c/v3, OID references, trap configuration, and community strings.</span>
</a>

<a class="kb-card" href="tls/">
  <strong>TLS</strong>
  <span>TLS 1.2/1.3 handshake, certificate chain validation, cipher suite review, and expiry monitoring.</span>
</a>

<a class="kb-card" href="syslog/">
  <strong>Syslog</strong>
  <span>Centralised logging architecture, syslog forwarding configuration, filtering, and SIEM integration.</span>
</a>

<a class="kb-card" href="api-connectivity/">
  <strong>API Connectivity</strong>
  <span>REST and API integration patterns, authentication, and connectivity standards.</span>
</a>

<a class="kb-card" href="email-relay/">
  <strong>Email Relay (SMTP)</strong>
  <span>SMTP relay configuration, mail flow, authentication, and relay troubleshooting.</span>
</a>

<a class="kb-card" href="service-integrations/"><strong>Service Integrations</strong><span>Cross-platform service integration patterns and connection standards.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Protocol-level diagnostics — connectivity failures, handshake errors, and port troubleshooting.</span></a>
</div>
