# Security — Operations

<div class="kb-summary">
Security day-to-day operations — certificate lifecycle, PAM account management, and hardening reviews.
</div>

```text
┌──────────────────────────────────────── Security — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   Day-to-day security operations: certificate lifecycle, PAM rotation, log retention, correlation     │
│   Three sub-sections: Runbooks (procedures), Log Retention (policy + sizing), Event Correlation       │
│   Recurring tasks: weekly firewall review, monthly access recertification, daily SIEM triage          │
│   Change-driven tasks: certificate renewal, PAM rotation, hardening baseline review                   │
│                                                                                                       │
│   Runbooks                                                                                            │
│   Certificate renewal  Expiry scan (openssl) → CSR → CA submission → deploy → verify                  │
│   PAM rotation         CyberArk CPM rotation check; verify Last Modified matches expected interval    │
│   Access recertification Monthly; compare AD group members against HR offboarding list                │
│   Firewall rule review Weekly; flag any/any rules and zero-hit rules from last 90 days                │
│                                                                                                       │
│   Hardening check schedule                                                                            │
│   Daily    Privileged account login review — SIEM / CyberArk audit trail                              │
│   Weekly   Failed auth events exceeding threshold — SIEM alert                                        │
│   Monthly  CIS benchmark scan — Lynis (Linux) or CIS-CAT (Windows)                                    │
│   Quarterly Penetration test (internal red team)                                                      │
│   Annually  Full security audit — external assessor                                                   │
│                                                                                                       │
│   Key terms:                                                                                          │
│   CPM               = CyberArk Central Policy Manager; automates credential rotation                  │
│   PAM               = Privileged Access Management; controls and audits high-privilege accounts       │
│   Lynis             = open-source Unix security auditing and hardening tool                           │
│   CIS-CAT           = CIS Configuration Assessment Tool; scores against CIS Benchmarks                │
│   SIEM              = Security Information and Event Management; aggregates and correlates logs       │
│   event correlation = linking related events across sources to identify root cause or attack pattern  │
│   log retention     = policy defining how long logs are kept; drives storage sizing                   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="runbooks/"><strong>Runbooks</strong><span>Operational runbooks for security procedures.</span></a>

<a class="kb-card" href="log-retention/"><strong>Log Retention</strong><span>Log retention policies, storage sizing, archiving strategy, and compliance requirements.</span></a>

<a class="kb-card" href="event-correlation/"><strong>Event Correlation</strong><span>Correlating events across layers — log, metric, and topology-based root cause identification.</span></a>

</div>
