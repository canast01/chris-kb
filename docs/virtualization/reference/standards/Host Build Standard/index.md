# Host Standards

```
┌───────────────────────────────────── ESXi — Host Build Standard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Baseline configuration applied to every ESXi host via host profile — enforced in vCenter   │   │
│   │       NTP: 2+ NTP servers; drift < 250ms; required for vSAN, vMotion, and Kerberos auth       │   │
│   │         Syslog: forwarded to centralised SIEM; retention 90 days minimum at SIEM level        │   │
│   │     Lockdown: Normal mode on all production hosts; exception list for LCM service accounts    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Build standard items enforced via host profile; non-compliant hosts flagged in vCenter             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Time & DNS         │  │           Security          │  │          Networking         │   │
│   │        NTP servers x2       │  │       Lockdown: Normal      │  │        VDS uplinks x2       │   │
│   │       DNS primary/sec       │  │        SSH: disabled        │  │          MTU: 9000          │   │
│   │       DNS suffix list       │  │       ESXi Shell: off       │  │       LACP / failover       │   │
│   │        Syslog target        │  │       VIB: PartnerSupp      │  │         VMkernel IPs        │   │
│   │        Drift < 250ms        │  │         Host profile        │  │          iDRAC VLAN         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Host profile compliance checked after every LCM patch; non-compliant hosts remediated              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Item       │  Required value  │    Enforced by    │      Check       │   Remediation    │   │
│   │  Lockdown mode   │      Normal      │    Host profile   │    vCenter UI    │  Profile apply   │   │
│   │   SSH service    │   Stopped/off    │    Host profile   │   esxcli check   │  Profile apply   │   │
│   │    NTP drift     │     < 250ms      │     NTP daemon    │     ntpq -p      │ Sync NTP servers │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: management NIC on VLAN 10; iDRAC on OOB VLAN; vSAN NIC on VLAN 30                        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Host profile  = vCenter template enforcing consistent config across all cluster hosts              │
│    Lockdown mode = ESXi state blocking direct SSH; all management routed through vCenter              │
│    Exception list = Accounts permitted direct host access in lockdown (VxRail Mgr SVC acct)           │
│    VIB acceptance = Host policy for VIB package signing: VMwareCertified > PartnerSupported           │
│    NTP drift     = Clock offset tolerance; >250ms breaks vSAN resync and Kerberos tickets             │
│    ESXi Shell    = TSM service; disabled in production to reduce attack surface                       │
│    SSH service   = TSM-SSH service; disabled in production; enabled only for troubleshooting          │
│    Syslog target = Remote syslog server (SIEM) receiving all ESXi log events                          │
│    LACP          = Link Aggregation Control Protocol; bonds uplinks for bandwidth and failover        │
│    PartnerSupp   = VIB acceptance level allowing Dell, NetApp, and VMware-signed VIBs                 │
│    VMkernel IP   = Per-VLAN ESXi virtual NIC IP: management, vMotion, vSAN, iSCSI/NFS                 │
│    iDRAC VLAN    = OOB management VLAN for iDRAC; isolated from ESXi and VM traffic                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
- Consistent ESXi version per cluster
- Consistent firmware and drivers
- Correct DNS and NTP
- Standard VMkernel layout
- Standard syslog configuration
- Management access restricted
- Lockdown mode where required
- Hardware health monitored
