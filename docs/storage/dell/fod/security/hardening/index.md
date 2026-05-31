# FOD — Hardening

```text
┌──────────────────────────────────────── Dell FoD — Hardening ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     FoD hardening: secure the portal account, vault, array management, and audit workflow     │   │
│   │        Portal hardening: enforce MFA, IP allowlist, session timeout, and account review       │   │
│   │         Vault hardening: short-lived leases, MFA auth, LDAP backend, access log review        │   │
│   │         Array hardening: disable unused protocols, enforce LDAP auth, SSH key-only CLI        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Harden portal account → harden vault → harden array → audit controls → quarterly review            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Portal Hardening      │  │       Vault Hardening       │  │       Array Hardening       │   │
│   │         Enforce MFA         │  │       Short TTL lease       │  │         SSH key-only        │   │
│   │         IP allowlist        │  │          MFA + LDAP         │  │         Disable HTTP        │   │
│   │       Session timeout       │  │       Audit log review      │  │          LDAP auth          │   │
│   │        Account review       │  │         Sealed vault        │  │          Mgmt VLAN          │   │
│   │         Offboard SOP        │  │        Policy-as-code       │  │         FW restrict         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Vault sealed when not in use; unseal requires quorum of key shares; reduces breach window          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Control      │      Setting      │     Standard     │      Owner       │   │
│   │   Dell portal    │   Enforce MFA    │      Org-wide     │   NIST 800-63    │   Storage lead   │   │
│   │      Vault       │    Short TTL     │    1h lease max   │  CIS benchmark   │     Sec team     │   │
│   │      Array       │   SSH key-only   │   Disable pw SSH  │      CIS L1      │    Infra team    │   │
│   │     Network      │    Mgmt VLAN     │   Isolated VLAN   │    Sec policy    │   Network team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: array management interface on isolated VLAN; only jumphost or VPN can reach it           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Portal MFA     = Enforce MFA for all Dell portal accounts; disable accounts that bypass it         │
│    IP allowlist   = Restrict portal login to corporate egress IPs; block personal/home access         │
│    Session timeout = Portal logs out after 30 min idle; vault lease expires in 1h                     │
│    Sealed vault   = HashiCorp Vault sealed state; no secrets accessible until quorum unseal           │
│    Short TTL      = Vault leases expire in 1 hour; limits window of access after key retrieval        │
│    Policy-as-code = Vault ACL policies in HCL files under version control; reviewed each quarter      │
│    SSH key-only   = Disable password-based SSH on array; only pre-approved public keys allowed        │
│    Disable HTTP   = Array management only on HTTPS 443; no plaintext HTTP redirect                    │
│    LDAP auth      = Array and vault use corporate AD/LDAP; no local service accounts for FoD          │
│    Mgmt VLAN      = Array management IPs on isolated VLAN; not reachable from user workstations       │
│    FW restrict    = Firewall allows only jumphost IP to reach array management VLAN                   │
│    CIS L1         = Center for Internet Security Level 1 baseline applied to array OS                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Flex on Demand](../../index.md) reference.

---

## Hardening Checklist

| Control | Standard | Action |
|---|---|---|
| **SCG software version** | Current GA release | Update the SCG appliance whenever Dell releases a new version. Outdated SCG versions may break telemetry delivery, causing metering gaps that require manual correction. Check the SCG admin console for available updates at least monthly. |
| **SCG redundancy** | Two SCG appliances per site | Deploy two SCG appliances and register each monitored array to both. A single SCG is a metering single point of failure. Both appliances should be on separate physical hosts. |
| **SCG network isolation** | Management VLAN only | Place SCG appliances on the storage management VLAN. Block access from general server VLANs. The SCG needs outbound HTTPS (443) to Dell cloud endpoints only — no inbound connections are required. |
| **SCG outbound allowlist** | Dell cloud endpoints only | Permit SCG outbound TCP 443 to `esrs.dell.com`, `cloudiq.dell.com`, and `api.dell.com` (or the regional equivalents listed in the SCG deployment guide). Deny all other outbound destinations at the perimeter. |
| **API service accounts** | One per integration | Create a dedicated APEX API service account for each consuming system. Assign the Viewer role unless write access is explicitly required. Document any account with elevated permissions and justify quarterly. |
| **API credential rotation** | Every 90 days | Rotate all API client secrets on a 90-day cycle. Automate rotation where possible. Store credentials in a secrets vault — never in config files or version control. |
| **APEX Console MFA** | Enforced for all human users | Enable MFA on the APEX Console account. This is configured under account identity settings and applies to all users in the tenancy. |
| **APEX Console IP allowlisting** | Corporate egress IPs only | If the APEX Console supports IP allowlisting for the account (check under account security settings), restrict access to known corporate egress IP ranges or VPN exit nodes. |
| **Least-privilege Unisphere accounts** | Named accounts, Viewer role for automation | Automation scripts querying FOD capacity metrics do not require StorageAdmin write access. Use Unisphere Monitor or Viewer roles for all read-only integrations. |
| **Audit log review** | Monthly | Review the CloudIQ audit log monthly for unexpected API access patterns, failed authentication attempts, and unscheduled gateway registration or deregistration events. |
| **Default credential changes** | At deployment | Change all default passwords on SCG appliances and associated service accounts immediately after deployment. Document that this step was completed in the CMDB entry for each SCG. |
| **Certificate validation** | SCG certificate pinning enabled | Do not deploy a TLS-inspecting proxy between the SCG and Dell cloud endpoints. Certificate pinning on the SCG will reject inspected connections, silently breaking telemetry delivery. |

## Network Requirements Summary

| Destination | Port | Direction | Purpose |
|---|---|---|---|
| `esrs.dell.com` | TCP 443 | Outbound from SCG | Secure Connect Gateway telemetry upload |
| `cloudiq.dell.com` | TCP 443 | Outbound from SCG | CloudIQ metric ingestion |
| `api.dell.com` | TCP 443 | Outbound from management hosts | APEX API access |
| Array management interface | TCP 443 / 8443 | SCG to array | Array registration and metric collection |

All other inbound connections to the SCG should be denied by default.
