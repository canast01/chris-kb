# Linux — Troubleshooting

```text
┌──────────────────────────────────────────────────────┐
│            Linux Triage Decision Tree                │
└──────────────────────┬───────────────────────────────┘
                       ▼
         ┌─────────────────────────┐
         │  System unreachable?    │
         └──────┬──────────────────┘
        Yes ◄───┤──► No
        ▼               ▼
┌──────────────┐  ┌───────────────────────────────────┐
│  Boot issues │  │  Identify symptom                  │
│  GRUB/initrd │  ├───────────┬──────────┬────────────┤
│  journalctl  │  │  Service  │ Network  │  Disk/Perf  │
│  -b -1       │  │  failed   │ no route │  no space   │
└──────────────┘  └─────┬─────┴────┬─────┴─────┬──────┘
                        ▼          ▼           ▼ 
               ┌──────────────┐ ┌──────────┐ ┌──────────────┐
               │ systemctl    │ │ ip/ss/   │ │ df/iostat/   │
               │ status <svc> │ │ tcpdump  │ │ top/vmstat   │
               └──────┬───────┘ └────┬─────┘ └──────┬───────┘
                      └──────────────┴───────────────┘
                                     ▼
                         ┌───────────────────────┐
                         │  Logs: journalctl -xe │
                         │  /var/log/messages    │
                         └───────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
