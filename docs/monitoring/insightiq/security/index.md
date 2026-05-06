# InsightIQ Security

InsightIQ access is controlled via local admin accounts or LDAP integration for centralised identity management. HTTPS should be enforced for all web dashboard access; HTTP access should be disabled or redirected. An audit log of admin actions (cluster adds/removes, user changes, configuration modifications) is maintained within the appliance. The PostgreSQL database backup files should be encrypted at rest and stored in a secured backup location. Network access to the InsightIQ management interface should be restricted to the operations management subnet via firewall rules.

- Authentication: local accounts or LDAP integration
- Access: HTTPS-only (disable HTTP)
- Audit log: retained on appliance, export periodically to SIEM
- Database backups: encrypted at rest
- Network restriction: limit access to ops management subnet
- Cluster credentials: dedicated read-only OneFS service account (`svc-insightiq`)
