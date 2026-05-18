# NetBackup

<div class="kb-summary">
Veritas NetBackup enterprise backup — three-tier architecture with Primary Server catalog, Media Servers for data movement, and MSDP deduplication with AIR image replication.
</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                    NetBackup Architecture                            │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │              Master / Primary Server                         │    │
│  │   Policy catalog · job scheduling · device management        │    │
│  └──────────────────────────────┬───────────────────────────────┘    │
│                                 │ job dispatch                       │
│  ┌──────────────────────────────▼───────────────────────────────┐    │
│  │              Media Server(s)                                 │    │
│  │   Data mover · MSDP deduplication · multiplexing             │    │
│  └─────────┬─────────────────────────────────┬──────────────────┘    │
│            │ agent backup                    │ data write            │
│  ┌─────────▼──────────────────┐   ┌──────────▼───────────────────┐   │
│  │  Client Agents             │   │  Storage Units               │   │
│  │  Linux · Windows · Oracle  │   │  Disk (MSDP pool)            │   │
│  │  SQL · VMware proxy        │   │  Tape (robot library)        │   │
│  └────────────────────────────┘   │  Cloud (S3 / Blob)           │   │
│                                   └──────────────────────────────┘   │
│                                                                      │
│  AIR (Auto Image Replication): MSDP ──► remote MSDP (DR site)        │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Three-tier topology, Primary Server catalog, Media Servers, MSDP dedup, and key processes.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
