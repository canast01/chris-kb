# Nexus Dashboard Scripts

Automation scripts interact with the Nexus Dashboard REST API, NDFC API, and ACI APIC REST API using Python. Scripts are stored in the team repository under `scripts/nexus-dashboard/`.

| Script | Purpose |
|---|---|
| `nd_health_check.py` | Query ND REST API for cluster node health and service status, alert on failures |
| `fabric_fault_export.py` | Export active fabric faults to CSV, filtered by severity and fabric |
| `ndfc_compliance_report.py` | Generate policy compliance report for all NDFC-managed fabrics |
| `alert_to_servicenow.py` | Forward P1/P2 fabric faults to ServiceNow via REST API to create incidents |
| `apic_fault_summary.py` | Query ACI APIC REST API for current fault counts by severity and category |

Scripts authenticate to ND using OAuth2 client credentials. ACI APIC scripts use cookie-based authentication via the APIC REST API `/api/aaaLogin.json` endpoint.
