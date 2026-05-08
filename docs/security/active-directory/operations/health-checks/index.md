# Active Directory — Health Checks

Daily operations centre on replication health and authentication event monitoring across all Domain Controllers. Run `repadmin /replsummary` and `dcdiag /test:replications` each morning to surface any replication failures before they impact authentication or Group Policy delivery. Review Windows Event Log on all DCs for Event ID 4625 (logon failures) and Event ID 4740 (account lockouts), and confirm SYSVOL share accessibility and DNS zone health before declaring a DC healthy.

**Daily checks:**

- `repadmin /replsummary` — replication health across all DCs
- `dcdiag /test:replications` — per-DC replication diagnostics
- Review Event IDs 4625, 4740, 4776 on all DCs
- Verify `\\domain\SYSVOL` and `\\domain\NETLOGON` are accessible
- Check DNS forward and reverse lookup zones for SOA and NS record integrity
- Confirm time synchronisation (PDC Emulator → reliable NTP source, all DCs within 5 minutes)

**Weekly checks:**

- `repadmin /showrepl` — full replication partner detail
- Review FSMO role holders with `netdom query fsmo`
- Confirm DC OS patch levels are current
