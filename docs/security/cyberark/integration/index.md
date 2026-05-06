# CyberArk Integration

CyberArk integrates with the enterprise identity, ticketing, automation, and monitoring stack to enforce privileged access controls across all platforms. LDAP/AD integration allows CyberArk users to authenticate with their domain credentials, and AD group membership drives safe access entitlements without requiring manual PVWA user management. MFA is enforced at PVWA logon via RADIUS integration with RSA SecurID or Duo Security.

| Integration | Method | Notes |
|---|---|---|
| Active Directory (LDAP) | LDAP bind from PVWA | User authentication and group-based safe membership |
| MFA (RSA / Duo) | RADIUS from PVWA | Enforced at logon; configured in PVWA Authentication settings |
| Syslog / SIEM (Splunk) | Syslog from Vault and PVWA | Vault audit events forwarded to Splunk; CIM-compliant event format |
| ServiceNow | REST API (ticket validation) | Dual-control access requests validated against open ServiceNow change/ticket number |
| Ansible | CyberArk Ansible modules (`cyberark.pas`) | Retrieve credentials from Vault at playbook runtime; no secrets in code |
| Terraform | CyberArk Terraform provider | Manage safes, accounts, and platforms as code |
| PSMP (SSH Proxy) | SSH through PSMP to target | Linux privileged access without exposing root credentials; sessions recorded |
| CyberArk EPM | Agent on endpoints | Least-privilege enforcement for workstations integrated with PAM |
