# vCenter Upgrade Readiness Checklist

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                   vCenter Upgrade Flow                                   │
│                                                                          │
│  1. File-based backup (VAMI) ──► verify backup exists + accessible       │
│          │                                                               │
│          ▼                                                               │
│  2. Pre-checks: disk space │ certs │ all hosts Connected │ 0 red alarms  │
│          │                                                               │
│          ▼                                                               │
│  3. Launch installer → deploy new appliance → run pre-check wizard       │
│          │                                                               │
│          ▼                                                               │
│  4. Data migration → new VCSA takes over → old VCSA suspended            │
│          │                                                               │
│          ▼                                                               │
│  5. Post-upgrade: login OK │ all services running │ hosts Connected      │
│     plugins OK │ vSAN green │ NSX connected │ Aria adapters OK           │
│          │                                                               │
│          ▼                                                               │
│  6. Keep old VCSA 48h → validate → delete old appliance                  │
└──────────────────────────────────────────────────────────────────────────┘
```

## Current State

- Confirm current vCenter version and build number
- Confirm current ESXi versions and ensure they are compatible with the target vCenter

## Target Version

- Confirm target vCenter version and supported upgrade path
- Review VMware upgrade path tool: supported paths only

## Pre-Upgrade Checks

- vCenter file-based backup completed
- SSO domain health confirmed
- Certificate health confirmed — no expiring certs during the window
- All disk partitions have sufficient free space
- All hosts are Connected
- No critical active alarms
- Plugin compatibility confirmed (backup, monitoring, etc.)
- vCenter and PSC in the same SSO domain are upgraded together

## Post-Upgrade Validation

- Confirm vSphere Client is accessible on the new version
- Confirm all hosts are still Connected
- Confirm vSAN health is green if applicable
- Confirm NSX is functioning if applicable
- Confirm Aria integrations are working
- Confirm backup and monitoring plugins are working
- Capture new version and build number for records
