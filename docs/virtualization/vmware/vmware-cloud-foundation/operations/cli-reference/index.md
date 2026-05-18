# VCF Operations — CLI Reference

```
VCF CLI Tool Map — Where to Run What
┌─────────────────────────────────────────────────────┐
│  SDDC Manager Appliance (SSH: vcf user → sudo)      │
│                                                     │
│  SoS utility                                        │
│  sudo python3 /opt/vmware/sddc-support/sos          │
│    --health-summary      full cross-domain check    │
│    --health-check        per-domain check           │
│    --password-health     credential status          │
│    --certificate-health  cert expiry scan           │
│                                                     │
│  vcf-support-bundle                                 │
│    --type sddc           full SDDC Manager bundle   │
│    --type lcm            LCM-specific bundle        │
│    --type nsx            NSX-related events         │
│                                                     │
│  SDDC Manager REST API  (https://<sddc-mgr>/v1)     │
│    GET  /v1/domains      list all domains           │
│    GET  /v1/clusters     list all clusters          │
│    GET  /v1/hosts        list all hosts             │
│    GET  /v1/credentials  list managed credentials   │
│    PATCH /v1/credentials rotate a credential        │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│  Key Log Paths (SDDC Manager appliance)             │
│  /var/log/vmware/vcf/lcm/lcm-debug.log              │
│  /var/log/vmware/vcf/sddc-manager/sddc-manager.log  │
│  /var/log/vmware/vcf/domainmanager/dm.log           │
└─────────────────────────────────────────────────────┘
```

VCF CLI operations use the SoS (Support and Operations Suite) utility on SDDC Manager, the SDDC Manager REST API, the `vcf-support-bundle` tool, and direct SSH commands on individual components. SoS is the primary health-check and diagnostic tool, run from the SDDC Manager appliance as root.

---

## SoS Health Checks

SoS performs cross-domain health validation across all VCF components. Run from the SDDC Manager appliance.

```bash
# SSH to SDDC Manager
ssh vcf@<sddc-mgr-fqdn>

# Full health summary across all domains
sudo python3 /opt/vmware/sddc-support/sos --health-summary

# Health check for a specific workload domain
sudo python3 /opt/vmware/sddc-support/sos --health-check --domain <domain_name>

# Password validation check
sudo python3 /opt/vmware/sddc-support/sos --password-health

# Certificate validation
sudo python3 /opt/vmware/sddc-support/sos --certificate-health

# List all available SoS flags
sudo python3 /opt/vmware/sddc-support/sos --help
```

---

## Support Bundles

```bash
# Collect LCM-specific support bundle
sudo vcf-support-bundle --type lcm

# Collect full SDDC Manager support bundle
sudo vcf-support-bundle --type sddc

# Collect bundle for a specific component
sudo vcf-support-bundle --type nsx

# List available bundle types
sudo vcf-support-bundle --help
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
