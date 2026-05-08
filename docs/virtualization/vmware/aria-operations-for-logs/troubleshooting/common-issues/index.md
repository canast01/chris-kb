# Aria Ops for Logs — Common Issues

## Common Search Examples

| Use Case | Search Term |
|---|---|
| Login failures | `Failed to authenticate` |
| Host disconnects | `lost connectivity` or `not responding` |
| Certificate errors | `certificate` or `SSL` or `handshake` |
| vMotion errors | `vmotion` and `error` |
| NTP issues | `NTP` or `time` and `drift` |
| Storage errors | `SCSI` or `datastore` and `error` |
| Service restarts | `hostd restarted` or `vpxa restarted` |

## Searching ESXi Host Logs

Search for a specific host by name or IP and filter by log source:

- `hostd` — VM and host operations
- `vpxa` — vCenter agent on the host
- `vmkernel` — kernel-level events
- `vobd` — hardware and storage events

## Searching vCenter Events

Use the vCenter log source and filter by event type or keyword:

- Login events: search `SessionManager`
- Task failures: search `TaskManager` or `error`
- Certificate events: search `certificate` or `STS`
