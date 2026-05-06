# InsightIQ Integration

The primary integration is with OneFS clusters via the InsightIQ data connector, which polls performance metrics at configurable intervals. Syslog forwarding sends InsightIQ appliance events to the centralised SIEM for audit and security correlation. SNMP traps are forwarded to the enterprise monitoring platform (Aria Operations or Nagios) for availability alerting. Email alert configuration handles threshold breach notifications directly from the InsightIQ appliance. Reports are exported as CSV or PDF for capacity planning meetings and storage review boards.

| Integration | Direction | Purpose |
|---|---|---|
| OneFS Data Connector | Inbound | Performance metrics collection |
| Syslog to SIEM | Outbound | Appliance event forwarding |
| SNMP to Monitoring | Outbound | Availability and threshold alerts |
| Email Alerts | Outbound | Threshold breach notifications |
| CSV / PDF Export | Outbound | Capacity planning report distribution |
