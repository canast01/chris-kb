# SRM Security

SRM access is controlled via vCenter RBAC; a dedicated `DR-Operator` role should be defined with permissions scoped to SRM actions only, preventing DR operators from having broad vCenter administrative access. Site pair credentials are stored encrypted within SRM and should use a dedicated service account with the minimum required permissions on each vCenter. Recovery plan execution is logged in both SRM and vCenter audit logs, which must be retained and forwarded to SIEM.

- **vCenter RBAC**: Define `DR-Operator` role with `Site Recovery` privilege set; assign at the SRM inventory root.
- **Site pair credentials**: Use dedicated `svc-srm-pair@domain` account; restrict account to SRM-required permissions only.
- **Test failover isolation**: Test recovery always runs in a network bubble (isolated port group); confirm no routing to production exists.
- **Certificate management**: SRM and vCenter use TLS certificates for mutual authentication; replace default self-signed certs with CA-signed certs in production.
- **Audit logging**: SRM logs every recovery plan start, test, stop, and cleanup; forward to SIEM; alert on unscheduled plan executions.
