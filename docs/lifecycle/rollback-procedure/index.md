# Rollback Procedure

## Overview

This procedure restores systems to a previous stable state when changes fail.

## Rollback Steps

1. Identify failure point
2. Restore backup or snapshot
3. Restart services
4. Validate system stability
5. Notify stakeholders

## Validation Commands

```bash
restore backup-file
systemctl restart service
```

## Completion Criteria

- System restored
- Services stable
- Incident documented
