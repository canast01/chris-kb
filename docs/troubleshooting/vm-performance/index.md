# VM Performance Troubleshooting

## Overview

Virtual machine performance issues may be caused by CPU contention, memory pressure, storage latency, or network congestion.

## Symptoms

- Slow application response
- High CPU ready time
- Memory swapping
- Disk latency alerts

## Health Commands

```bash
esxtop
vmstat
top
free -m
```

## Troubleshooting Workflow

1. Check CPU and memory utilization
2. Review storage latency
3. Confirm network connectivity
4. Review recent changes
5. Adjust resource allocation if needed
