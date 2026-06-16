---
tags:
  - troubleshooting
  - horizon
  - vmware
  - known-issues
---
# VMware Horizon — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Horizon bugs, error codes, and workarounds covering Blast Extreme, PCoIP, Connection Server, and desktop pool issues.

*Applies to: Horizon 8.x (2111+)*
</div>

```text
┌───────────────────────────────────────── VMware Horizon VDI ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Virtual desktop/app delivery — pooled/dedicated VMs, session brokers             │   │
│   │              Protocols: Blast Extreme (TCP/UDP 8443) · PCoIP · RDP · HTTPS (443)              │   │
│   │                  Management: Horizon Console · PowerCLI · REST API · Event DB                 │   │
│   │           User auth -> CS -> UAG -> agent in desktop VM -> display protocol session           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Access           │  │        UAG appliance        │  │         DMZ gateway         │   │
│   │            Broker           │  │      Connection Server      │  │      Session assignment     │   │
│   │           Desktop           │  │       Horizon Agent VM      │  │    Display protocol host    │   │
│   │           Protocol          │  │        Blast / PCoIP        │  │    Display + USB + audio    │   │
│   │           Identity          │  │          AD + vIDM          │  │      Entitlement source     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       UAG        │  Secure gateway  │   HTTPS / Blast   │ Smart card/SAML  │ Replaces SecSrvr │   │
│   │Connection Server │  Session broker  │     HTTPS 443     │   AD Kerberos    │LDAP-backed config│   │
│   │  Horizon Agent   │ Desktop endpoint │    Blast/PCoIP    │       N/A        │In each desktop VM│   │
│   │     App Vol      │   App delivery   │       HTTPS       │     AD group     │VMDK app packages │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: client -> UAG (DMZ) -> Connection Server -> Horizon Agent in desktop VM                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  UAG          = Unified Access Gateway; DMZ reverse proxy replacing Security Server                   │
│  Connection Server = Horizon broker; assigns user to desktop pool/farm                                │
│  Blast Extreme = VMware HTML5/UDP display protocol; preferred over PCoIP                              │
│  PCoIP        = PC-over-IP; Teradici display protocol; still used for thin clients                    │
│  Desktop pool = logical grouping of VMs for user assignment                                           │
│  Entitlement  = mapping of AD group/user to a desktop pool or app                                     │
│  Instant clone = fast VM provisioning; linked to parent snapshot, no customization                    │
│  Full clone   = independent VM copy; slower provision but fully isolated                              │
│  App Volumes  = application delivery via VMDK attached at login                                       │
│  DEM          = Dynamic Environment Manager; user profile and policy config                           │
│  replica      = Horizon CS replica; shared LDAP state, load balances connections                      │
│  vGPU         = GPU passthrough or SR-IOV for graphics-intensive desktops                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Horizon error codes appear in the Horizon Console event log and the Horizon Administrator → Events tab.
- Client-side error codes (e.g., `BLST_*`) are logged in `%APPDATA%\VMware\Horizon Client\logs\`.
- For Blast Extreme issues, collect `vmware-viewagent-*.log` from the desktop VM.

## Connection and Authentication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Error 1306` — Cannot connect to desktop | Horizon 8.x | Blast Extreme port 22443 blocked between client and UAG | Verify port 22443 TCP/UDP open on all firewalls between client and UAG | N/A |
| `Smart card authentication not working` | Horizon 8.x | Card reader driver not present in agent VM or smart card redirection disabled | Enable smart card redirection in pool policy; install middleware on agent | N/A |
| Repeated `Authenticating...` loop with SAML IdP | Horizon 8.x | SAML assertion clock skew >5 minutes | Sync NTP on Connection Server and IdP; ensure clocks match within 5 seconds | N/A |
| `Cannot connect — Connection Server unreachable` for remote clients | Horizon 8.x | UAG not configured or IP pool for Blast routing incorrect | Check UAG external URL configuration; verify Blast External URL matches client-facing address | N/A |

## Display Protocols

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Blast Extreme screen freezes after 30 seconds of inactivity | Horizon 2111 | Blast display timeout misconfiguration | Set `BlastReconnectInterval` in `blast.conf` on agent; or adjust GPO | 2203 |
| PCoIP session drops every 10 minutes | Horizon 8.x | PCoIP session timeout policy too aggressive | Increase `pcoip.disconnected_session_timeout_seconds` in group policy | N/A |
| USB redirection not working | Horizon 8.x | USB arbitrator service not running on agent | Start `VMware USB Arbitration Service` on agent VM | N/A |
| H.264 hardware decode not used on client | Horizon 8.x | Client GPU driver outdated or `H264.Enabled` policy not set | Update client GPU drivers; enable H.264 in Blast policy | N/A |

## Desktop Pools and Provisioning

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Instant clone pool fails provisioning: `CustomizationError` | Horizon 8.x | Sysprep timeout on slow storage | Increase customization timeout in pool advanced settings | N/A |
| `Agent unreachable` on newly provisioned instant clone | Horizon 8.x | DNS not resolving desktop FQDN | Ensure DHCP registers desktop hostname in DNS; verify DNS suffix | N/A |
| Desktop stuck in `Deleting` state | Horizon 8.x | vCenter task hung during VM deletion | Manually cancel vCenter task; run Connection Server refresh pools | N/A |

## Connection Server

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Connection Server event database fills disk | Horizon 8.x | Event archiving not configured | Enable event archiving to external DB; purge `event_data` table | N/A |
| JMS cluster split after network partition | Horizon 8.x | JMS (port 4001/4002) blocked between Connection Servers | Restore JMS connectivity; restart `VMware Horizon View Connection Server` service | N/A |

## See also

- [VMware Horizon — Common Issues](common-issues.md)
- [VMware vCenter — Known Issues](../../vcenter/troubleshooting/known-issues/)
