# SRDF/A Security

SRDF link encryption is available via the SRDF/E option, which encrypts data in-flight over FCIP using AES-256. Solutions Enabler RBAC restricts SRDF operations to authorised roles; automation accounts running SYMCLI commands should follow the least-privilege principle, holding only the `StorageAdmin` role scoped to relevant SRDF groups. All failover events are recorded in the array audit log, which should be forwarded to a central SIEM.

- **SRDF/E encryption**: AES-256 in-flight encryption over FCIP; verify with `symcfg list -rdfg -v` for encryption status.
- **Solutions Enabler RBAC**: Define separate roles for read-only monitoring vs. failover execution.
- **Automation accounts**: Dedicated service account per automation system; rotate credentials quarterly.
- **Network ACLs**: Restrict SRDF FCIP (TCP 3260/custom) and iSCSI ports to known array management IPs only.
- **Audit logging**: Array audit logs retained for ≥90 days; forward to SIEM for failover event alerting.
