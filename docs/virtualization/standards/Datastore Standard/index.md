# Datastore Standards

- Clear datastore names
- Avoid running production datastores near full capacity
- Monitor thin provisioning risk
- Use storage policies where appropriate
- Remove stale ISOs and old templates
- Review snapshots regularly
- Document datastore ownership and purpose

## Capacity Thresholds

| Threshold | Action |
|---|---|
| 80% used | Review growth trends |
| 85% used | Plan cleanup or expansion |
| 90% used | Open action ticket |
| 95% used | Treat as urgent — immediate action required |

## Expansion and Decommission

- Expansion requires change approval
- Emergency expansion process should be documented in the runbook
- Decommission process: confirm no active VMs, remove from datastores, coordinate with storage team
