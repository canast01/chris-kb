# Protocols

<div class="kb-summary">
Reference coverage for the networking and storage protocols used in enterprise infrastructure — Fibre Channel, iSCSI, NFS, SMB, NTP, SNMP, TLS, DNS, DHCP, and LDAP.
</div>

                        PROTOCOL LANDSCAPE
```text
┌───────────────────────────────────────────────────────────────┐
│  STORAGE PROTOCOLS          MANAGEMENT PROTOCOLS                                                      │
│  ┌──────────┐  ┌───────┐   ┌──────┐ ┌─────┐ ┌─────┐ ┌─────┐                                           │
│  │    FC    │  │ iSCSI │   │ SNMP │ │ NTP │ │ DNS │ │DHCP │                                           │
│  │ 8/16/32G │  │TCP3260│   │161/  │ │UDP  │ │UDP/ │ │UDP  │                                           │
│  │ (block)  │  │(block)│   │162udp│ │ 123 │ │TCP53│ │67/68│                                           │
│  └──────────┘  └───────┘   └──────┘ └─────┘ └─────┘ └─────┘                                           │
│  ┌──────────┐  ┌───────┐   ┌──────────────────────────────┐                                           │
│  │   NFS    │  │  SMB  │   │ SECURITY / DIRECTORY         │                                           │
│  │ TCP 2049 │  │TCP 445│   │ ┌─────┐        ┌──────┐      │                                           │
│  │  (file)  │  │ (file)│   │ │ TLS │        │ LDAP │      │                                           │
│  └──────────┘  └───────┘   │ │443+ │        │389/  │      │                                           │
│                             │ └─────┘        │ 636  │      │                                          │
│                             └────────────────┴──────┘──────┘                                          │
└───────────────────────────────────────────────────────────────┘
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

<a class="kb-card" href="service-integrations/">
  <strong>Service Integrations</strong>
  <span>Cross-platform service integration patterns and connection standards.</span>
</a>
</div>
