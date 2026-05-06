# Aria Suite Lifecycle Operations

Daily operational checks should begin with the LCM dashboard's Environment Health view, which aggregates product health status across all managed environments and surfaces certificate expiry warnings, failed services, and sync errors. Disk usage on the LCM appliance must be monitored — the `/data` partition (NFS-backed binary repo) and `/` (OS) should stay below 80% utilisation; a full `/data` partition will prevent bundle downloads and upgrades. Certificate expiry alerts are visible under Locker > Certificates and should be reviewed weekly, with renewals initiated at least 30 days before expiry.

**Daily checks:**
- LCM dashboard: verify all environment cards show green health
- Locker > Certificates: check for entries expiring within 30 days
- LCM appliance: `df -h` — confirm `/`, `/data`, `/tmp` below 80%
- Review LCM sync schedule (Settings > System Details) — confirm last sync succeeded
- Check LCM service status: `systemctl status lcm`
- Review `/var/log/lcm/lcm-app.log` for ERROR or WARN entries from the past 24 h
