# Aria Operations for Logs — Troubleshooting Guide
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

## Time-Based Filtering

Always set a time range before searching — searching all time is slow and returns too many results. Start with the last 1 hour during an active incident, then expand if needed.

## Correlating Events Across Systems

When troubleshooting, search the same time window across multiple log sources:

1. Start with vCenter events to find the first symptom
2. Match the timestamp to ESXi host logs for the affected host
3. Check storage or network logs if the issue involves those layers
4. Cross-reference with Aria Operations alerts at the same time

## Exporting Evidence

Use the export function to save log query results as CSV or text for change tickets, RCAs, or support cases.
