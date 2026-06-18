---
tags:
  - vcf
  - operations
---
# VCF Cheat Sheet

<div class="kb-summary">
Top-10 VCF commands for SDDC Manager operations, workload domains, LCM upgrades, and password management via REST API and CLI.
</div>

```text
┌──────────────────────────────────────── VCF Cheat Sheet ──────────────────────────────────────────────┐
│  CLI: vcf-password-ops  ·  REST API: https://sddc-mgr/v1  ·  LCM: lifecycle management                │
│  Categories: Domains · Hosts · LCM · Passwords · Bundles · Health                                     │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## SDDC Manager REST API

```bash
BASE="https://sddc-mgr"
# Get bearer token
TOKEN=$(curl -sk -X POST $BASE/v1/tokens \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"VMware1!"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['accessToken'])")

AUTH="Authorization: Bearer $TOKEN"

# Workload domains
curl -sk -H "$AUTH" $BASE/v1/domains | python3 -m json.tool          # list domains
curl -sk -H "$AUTH" $BASE/v1/domains/<id> | python3 -m json.tool     # domain detail

# Hosts
curl -sk -H "$AUTH" $BASE/v1/hosts | python3 -m json.tool            # commissioned hosts
curl -sk -H "$AUTH" $BASE/v1/hosts?status=UNASSIGNED | python3 -m json.tool  # free hosts

# LCM bundles and upgrades
curl -sk -H "$AUTH" $BASE/v1/bundles | python3 -m json.tool          # available bundles
curl -sk -H "$AUTH" $BASE/v1/upgrades | python3 -m json.tool         # upgrade history

# Cluster operations
curl -sk -H "$AUTH" $BASE/v1/clusters | python3 -m json.tool         # all clusters
```

## Password management (SDDC Manager appliance SSH)

```bash
vcf-password-ops --getpassword --component VCENTER --account root
vcf-password-ops --rotatepassword --component VCENTER --account root
```

## See also

- [VCF Operations](../../virtualization/vmware/vmware-cloud-foundation/operations/procedures/)
- [VCF Troubleshooting](../../virtualization/vmware/vmware-cloud-foundation/troubleshooting/common-issues/)
