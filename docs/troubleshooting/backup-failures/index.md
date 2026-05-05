# Backup Failures Troubleshooting

## Overview

Backup failures increase risk of data loss and recovery delays during outages.

## Symptoms

- Failed backup jobs
- Missing restore points
- Repository errors
- Network timeouts

## Health Commands

```bash
Get-VBRJob
bpdbjobs
qlist job
```

## Troubleshooting Workflow

1. Identify failed job
2. Review error logs
3. Validate storage capacity
4. Confirm network connectivity
5. Retry backup job
