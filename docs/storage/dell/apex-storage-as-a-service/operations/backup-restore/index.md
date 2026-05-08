# APEX Storage as a Service — Backup & Restore

> Part of the [APEX Storage as a Service](../../) reference.

---

Data backup on APEX STaaS is the customer's responsibility using the same backup solutions as for any other storage platform (e.g., PowerProtect Data Manager, Avamar, Networker). Dell manages the hardware and infrastructure layer only.

Key items to document and protect:

- **APEX API credentials**: store client ID and client secret in a secrets vault; cannot be retrieved after creation
- **Subscription records**: retain documentation of subscription ID, committed tier, burst ceiling, contract dates, and SLA tier
- **Monthly usage exports**: export APEX Console billing data monthly and retain for billing reconciliation
