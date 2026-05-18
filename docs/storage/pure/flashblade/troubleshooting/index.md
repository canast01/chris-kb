# FlashBlade — Troubleshooting

```
FlashBlade Triage Entry Points
  Alert type ──► purefb alert list
       │
       ├── Hardware ──► purefb blade list / purefb hardware list
       │                └── Open Pure support case if blade failed
       │
       ├── NFS/SMB ──► check export policy / share ACL
       │               └── check AD/LDAP connectivity
       │
       ├── S3 ──── check bucket ACL / access key validity
       │
       ├── Replication ──► purefb replication list
       │                   └── check network BW + lag vs RPO
       │
       ├── Performance ──► purefb array list (throughput/IOPS)
       │
       └── Escalate ──► Pure1 ──► support case + diagnostic upload
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
