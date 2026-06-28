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
![VCF Operations — CLI Reference](../../../../assets/virtualization-vmware-vmware-cloud-foundation-operations-cli.svg)


VCF CLI Tool Map — Where to Run What

---

```d2
direction: right

hub: "VMware Cloud Foundation\nOperations" {shape: hexagon}
sddc_manager_rest_api: "SDDC Manager REST API" {shape: rectangle}
password_management: "Password Management" {shape: rectangle}
service_status_logs: "Service Status & Logs" {shape: rectangle}
verify: "Verify" {shape: rectangle}

hub -> sddc_manager_rest_api
hub -> password_management
hub -> service_status_logs
hub -> verify
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

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

---

## See also

- [VCF — Procedures](procedures/)
- [VMware Cloud Foundation — Operational Scripts](scripts/)
- [VCF — Health Checks](health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
