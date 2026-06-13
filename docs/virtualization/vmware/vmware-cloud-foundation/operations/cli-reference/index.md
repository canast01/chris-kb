---
tags:
  - operations
  - vcf
  - vmware
---
# VCF Operations — CLI Reference


<div class="kb-summary">
CLI Reference reference covering Support Bundles, SDDC Manager REST API, Password Management, Service Status & Logs.

*Applies to: VCF 4.x / 5.x*
</div>

VCF CLI Tool Map — Where to Run What
```text
┌─────────────────────────────── VMware Cloud Foundation — CLI Reference ───────────────────────────────┐
│                                                                                                       │
│  VCF is primarily managed via SDDC Manager UI and REST API; PowerVCF and lcm-cli                      │
│  provide CLI automation for lifecycle, password, and certificate operations.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              PowerVCF Commands               │  │            SDDC Manager REST API            │   │
│   │           Connect-VCFManager -fqdn           │  │             GET /v1/sddcs (list)            │   │
│   │         Get-VCFDomain (list domains)         │  │               GET /v1/domains               │   │
│   │         Get-VCFHost (host inventory)         │  │                GET /v1/hosts                │   │
│   │          Start-VCFUpgrade (trigger)          │  │              POST /v1/upgrades              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  PowerVCF wraps SDDC Manager REST API; all ops require SDDC Manager admin credentials.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Password & Cert CLI              │  │            LCM CLI (on appliance)           │   │
│   │           Request-VCFToken (auth)            │  │                  lcm status                 │   │
│   │           Get-VCFCredential (list)           │  │             lcm bundle-download             │   │
│   │          Set-VCFCredential (rotate)          │  │              lcm upgrade-status             │   │
│   │         Get-VCFCertificate (status)          │  │                lcm remediate                │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  PowerVCF connects over HTTPS to SDDC Manager; lcm-cli runs on SDDC Manager appliance                 │
│  shell accessed via SSH on port 22.                                                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PowerVCF     = PowerShell module for SDDC Manager REST API automation                                │
│  SDDC Manager = VCF control plane; REST API on port 443                                               │
│  Request-VCFToken= obtain bearer token for API auth                                                   │
│  lcm-cli      = Lifecycle Manager CLI on SDDC Manager appliance                                       │
│  lcm bundle   = upgrade package downloaded from VMware depot                                          │
│  Get-VCFCredential= list all managed passwords (rotated by SDDC Mgr)                                  │
│  Set-VCFCredential= trigger password rotation for a component                                         │
│  Get-VCFDomain = list all workload and management domains                                             │
│  Get-VCFHost  = list all hosts; free pool or assigned to domain                                       │
│  Bearer token = JWT token; obtained via API; expires after 24h                                        │
│  lcm remediate= fix failed upgrade tasks; retry individual steps                                      │
│  upgrade-status= show current upgrade state across all components                                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
---

## SDDC Manager REST API

The SDDC Manager API runs at `https://<sddc-mgr>/v1`. Authenticate with the `vcf` admin account.

```bash
# Authenticate and get token
curl -k -X POST https://<sddc-mgr>/v1/tokens \
  -H "Content-Type: application/json" \
  -d '{"username":"administrator@vsphere.local","password":"<pass>"}'

# List all domains
curl -k -X GET https://<sddc-mgr>/v1/domains \
  -H "Authorization: Bearer <token>"

# List all clusters
curl -k -X GET https://<sddc-mgr>/v1/clusters \
  -H "Authorization: Bearer <token>"

# List managed credentials
curl -k -X GET https://<sddc-mgr>/v1/credentials \
  -H "Authorization: Bearer <token>"

# List hosts
curl -k -X GET https://<sddc-mgr>/v1/hosts \
  -H "Authorization: Bearer <token>"

# List workload domains
curl -k -X GET https://<sddc-mgr>/v1/domains \
  -H "Authorization: Bearer <token>"
```

---

## Password Management

```bash
# List all managed credentials via API
curl -k -X GET https://<sddc-mgr>/v1/credentials \
  -H "Authorization: Bearer <token>"

# Rotate a credential
curl -k -X PATCH https://<sddc-mgr>/v1/credentials \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"operationType":"ROTATE","elements":[{"resourceName":"<name>","resourceType":"<type>","credentials":[{"credentialType":"<type>","username":"<user>"}]}]}'
```

---

## Service Status & Logs

```bash
# Check SDDC Manager service
systemctl status sddc-manager

# Follow LCM debug log
tail -f /var/log/vmware/vcf/lcm/lcm-debug.log

# Follow SDDC Manager application log
tail -f /var/log/vmware/vcf/sddc-manager/sddc-manager.log

# View recent system events
journalctl -u sddc-manager --since "2 hours ago"
```
