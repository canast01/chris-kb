# System Decommission Procedure

## Overview

This procedure defines steps to safely remove systems from production environments.

## Required Steps

- Confirm system ownership approval
- Verify data retention requirements
- Remove system from monitoring
- Remove backups
- Shut down services
- Update inventory records

## Validation Commands

```bash
shutdown now
systemctl disable service
```

## Completion Criteria

- System powered off
- Records updated
- Access removed
