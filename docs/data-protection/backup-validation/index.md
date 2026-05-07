# Backup Validation

## Overview

Backup validation ensures recovery capability and data integrity.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Verify successful backup jobs |  |  |
| Confirm restore points exist |  |  |
| Check repository capacity |  |  |

## Health Commands

```bash
Get-VBRJob
bpdbjobs
qlist job
```

## Workflow

1. Identify backup set
2. Perform test restore
3. Validate recovered data
4. Document results
