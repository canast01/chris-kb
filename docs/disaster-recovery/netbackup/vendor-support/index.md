# NetBackup Vendor Support

Veritas support is accessed via the Veritas Support Portal at support.veritas.com using your MyVeritas account linked to your maintenance contract. When opening a case, classify severity accurately: Sev 1 for production backup failure with no workaround, Sev 2 for significant degradation, Sev 3 for non-urgent issues or questions. Collect the `nbsupport` diagnostic bundle from the master server before opening a case — it captures version info, configuration, and recent logs in a single archive.

**Collecting the diagnostic bundle**

```bash
/usr/openv/netbackup/bin/support/nbsupport
# Output archive is written to /tmp/nbsupport_<hostname>_<timestamp>.tar.gz
```

**Required information for a support case**

- NetBackup master server version (`bpgetconfig -L`)
- Master and media server OS version and patch level
- Job ID(s) of failing jobs (`bpdbjobs -jobid <id> -report`)
- Policy and schedule configuration (`bppllist -allpolicies -L`)
- Storage unit type and version (Data Domain firmware, Cloud provider region)
- Relevant logs from `/usr/openv/netbackup/logs/`

**Support tiers**

| Tier | Response SLA | Availability |
|---|---|---|
| Essential | 4 business hours (Sev 2) | Business hours |
| Standard | 2 hours (Sev 1) | 24x7 |
| Mission Critical | 1 hour (Sev 1) | 24x7 + TAM |
