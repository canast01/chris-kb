# Virtualization Troubleshooting

Common virtualization troubleshooting workflows.

## Troubleshooting Flow

Start by defining the scope, then work down through the stack.

1. **Define scope** — one VM, one host, one cluster, or full vCenter outage?
2. **Check vCenter health** — can you log in? Are services running? Any critical alarms?
3. **Check host health** — are all hosts connected? Any in warning or not responding?
4. **Check storage and vSAN** — are datastores accessible? Is vSAN Skyline Health green?
5. **Check network** — are VM and management networks reachable? Any vMotion failures?
6. **Review recent tasks and events** — what changed in the last 24 hours?
7. **Check logs** — hostd, vpxa, vmkernel, vCenter events, Aria for Logs
8. **Escalate** — open a Dell or VMware support case if the root cause is unclear

