# Database Performance Troubleshooting

## Overview

This runbook identifies performance bottlenecks affecting database workloads.

## Pre-Checks

- Confirm affected queries
- Check system resource usage
- Review recent configuration changes

## Commands

```bash
top
iostat -x 1
vmstat 1
```

## Validation

1. Confirm resource utilization stabilized
2. Confirm query response time improved
3. Document root cause
