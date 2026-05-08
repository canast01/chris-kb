# CloudIQ — Backup & Restore

> Part of the [CloudIQ](../../) reference.

---

CloudIQ is a SaaS platform — there is no customer-managed backup of the CloudIQ service itself. Dell manages data retention and service continuity on the back end.

Key items to back up on the customer side:

- **API credential records**: store client ID and client secret securely in a secrets vault (CyberArk, HashiCorp Vault, or AWS Secrets Manager). These cannot be retrieved from CloudIQ after creation.
- **Notification rule configuration**: export or document notification rules (recipients, severity filters, webhook URLs) so they can be recreated if the CloudIQ account is reset.
- **SCG registration records**: maintain a record of which arrays are registered to which SCG appliance. Re-registration after an SCG rebuild requires this information.
- **Audit log exports**: export the CloudIQ audit log periodically (Admin > Audit Log > Export as CSV) and retain for at least 90 days per your security policy.
