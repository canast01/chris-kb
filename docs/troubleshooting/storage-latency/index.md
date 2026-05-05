# Storage Latency Troubleshooting

## Overview

Storage latency impacts application response times, database performance, and VM operations.

## Symptoms

- Slow disk operations
- VM performance degradation
- Database timeouts
- Increased I/O wait

## Health Commands

```bash
iostat -x 5
vmstat 5
esxtop
symstat
```

## Troubleshooting Workflow

1. Confirm latency metrics
2. Identify impacted volumes or LUNs
3. Check host connectivity
4. Review storage alerts
5. Validate replication or snapshot activity
