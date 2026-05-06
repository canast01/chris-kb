# VMware Cloud Foundation Security

VCF credential rotation is managed centrally through SDDC Manager's Password Management feature, which rotates passwords for ESXi, vCenter, NSX, and SDDC Manager service accounts on a configurable schedule (recommended: 90-day maximum). SDDC Manager RBAC provides three built-in roles — `ADMIN`, `OPERATOR`, and `VIEWER` — which should be mapped to AD groups rather than local accounts; local accounts should be reserved for break-glass access only and their passwords stored in an enterprise vault. All audit events for SDDC Manager operations are logged to `/var/log/vmware/vcf/sddc-manager/` and should be forwarded to a SIEM via syslog for retention and alerting.

**Security hardening checklist:**
- [ ] All default passwords rotated via SDDC Manager Password Management at first use
- [ ] Password rotation schedule set to 90 days or per organisation policy
- [ ] SDDC Manager RBAC roles mapped to AD groups; local `admin` account locked post-setup
- [ ] TLS 1.2 minimum enforced on all VCF component endpoints (verify via SDDC Manager UI)
- [ ] Certificate replacement for all VCF components performed via SDDC Manager Certificate Management
- [ ] Syslog forwarding to SIEM configured: SDDC Manager > Administration > Syslog
- [ ] Network access to SDDC Manager UI (443) restricted to management jump-host CIDR
- [ ] vSAN data-at-rest encryption enabled for workload domains containing sensitive workloads
- [ ] Review SDDC Manager audit logs monthly for privilege escalation or unexpected API calls
