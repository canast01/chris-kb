# Dell VPLEX — Diagnostics

> Diagnostic procedures and log analysis for Dell VPLEX.

## Diagnostic Commands

```bash
# Full system health check
vplexcli -q -e "health-check --full"

# Cluster health indications
vplexcli -q -e "ll /clusters/*/health-indications/"

# Distributed device health and sync state
vplexcli -q -e "ll /distributed-storage/distributed-devices/*/health-indications/"

# Director hardware health across all engines
vplexcli -q -e "ll /engines/*/directors/*/hardware/"

# Witness connectivity (Metro)
vplexcli -q -e "ll /metro-node/*/witness/"

# Consistency group state
vplexcli -q -e "ll /distributed-storage/consistency-groups/"

# Storage view initiator and volume bindings
vplexcli -q -e "ll /clusters/*/exports/storage-views/"

# GeoSynchrony firmware version
vplexcli -q -e "ll /clusters/cluster-1/system-volumes/version/"

# Backend array inventory
vplexcli -q -e "ls /storage-elements/storage-arrays"
```

## Log Locations

| Log | Location | Content |
|---|---|---|
| vplexcli command history | `/var/log/VPlex/cli/vplexcli.log` on VMS | All CLI commands executed |
| VPLEX management log | `/var/log/VPlex/vplexmanagement.log` on VMS | Management events, configuration changes |
| Unisphere web UI log | `/var/log/VPlex/` on VMS | Web UI access and API calls |
| Director system log | Collected via support bundle | Director-level hardware and software events |

## Collecting a Support Bundle

```bash
# From within vplexcli
collect-support-log -f /var/log/support_bundle.tar.gz

# Copy from VMS to a jump host
scp service@<VMS_IP>:/var/log/support_bundle.tar.gz admin@<jump_host>:/tmp/
```

## Before Calling Support

Gather the following before opening a Dell Support case:

- GeoSynchrony version: `vplexcli -q -e "ll /clusters/cluster-1/system-volumes/version/"`
- Full health check output: `vplexcli -q -e "health-check --full"`
- Distributed device health: `vplexcli -q -e "ll /distributed-storage/distributed-devices/*/health-indications/"`
- Consistency group state: `vplexcli -q -e "ll /distributed-storage/consistency-groups/"`
- Support bundle: `collect-support-log -f /var/log/support_bundle.tar.gz`
- Approximate time the issue started
- Description of any recent changes (GeoSynchrony upgrade, backend array changes, zoning changes, host additions)
- Output from hosts: `powermt display dev=all` or `multipath -ll`
