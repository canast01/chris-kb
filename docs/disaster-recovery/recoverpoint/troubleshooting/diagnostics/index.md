# RecoverPoint — Diagnostics

> Part of the [RecoverPoint](../../) > [Troubleshooting](../) reference.

---

## Log Locations

| Log | Location |
|---|---|
| RPA system logs | Accessible via `boxmgmt` → `Support` → `Collect support bundle` |
| RPMA audit log | RecoverPoint Management Application → Reports → Audit Log |
| Splitter logs (ESXi) | `/var/log/vmkernel.log` on ESXi host |

---

## Support Bundle Collection

```bash
# Via boxmgmt
boxmgmt support collect_bundle
```

Upload bundle to Dell Support case via https://www.dell.com/support.
