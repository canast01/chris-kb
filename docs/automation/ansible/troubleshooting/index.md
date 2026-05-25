# Ansible — Troubleshooting


```
┌────────────────────────────────────── Ansible — Troubleshooting ──────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Ansible troubleshooting: connectivity, variable resolution, module failures, AWX job issues  │   │
│   │        First check: run with -vvv for full SSH debug output and module argument logging       │   │
│   │    Common root causes: SSH key mismatch, Python missing on host, variable precedence error    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Common Issues                 │  │             Diagnostic Commands             │   │
│   │           UNREACHABLE: SSH timeout           │  │          ansible host -m ping -vvv          │   │
│   │           FAILED: module not found           │  │          ansible-inventory --graph          │   │
│   │         Wrong var value: precedence          │  │         ansible -m debug -a "var=x"         │   │
│   │             Vault decrypt error              │  │         ansible-vault view file.yml         │   │
│   │           AWX job stuck in pending           │  │          kubectl logs -n awx <pod>          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │Variable precedence = 22 levels; host_vars > group_vars > defaults > role defaults (highest win│   │
│   │     UNREACHABLE        = host not reachable via SSH; check firewall, SSH service, key auth    │   │
│   │    Python interpreter = set ansible_python_interpreter if /usr/bin/python3 differs on host    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
