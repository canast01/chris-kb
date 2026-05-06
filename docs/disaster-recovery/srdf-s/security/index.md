# SRDF/S Security

Solutions Enabler RBAC controls which users and service accounts can execute SRDF operations; failover and resync commands should be restricted to a dedicated DR-operator role, separate from read-only monitoring accounts. SRDF/S port security is enforced via FCIP encryption (AES-256) and hard zoning on the FC fabric to prevent unauthorised array-to-array communication. All failover events generate entries in the array audit log, which must be retained for compliance purposes and forwarded to the SIEM.

- **RBAC roles**: `StorageAdmin` (failover), `StorageMonitor` (read-only); never use root/admin for automation.
- **FCIP encryption**: Enabled per SRDF group; verify with `symcfg list -rdfg -v | grep Encrypt`.
- **Fabric zoning**: Hard zoning by WWPN between SRDF director ports; no soft-zone aliases for SRDF ports.
- **Management access**: Solutions Enabler API gated by certificate-based auth; rotate service account credentials every 90 days.
- **Audit log forwarding**: Array event log → syslog → SIEM; alert on `SRDF Failover` and `SRDF Split` event types.
