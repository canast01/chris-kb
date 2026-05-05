# Directory Integration

## Overview

Directory integration allows systems to authenticate users using centralized identity services.

## Daily Checks

- Verify directory connectivity
- Check authentication logs
- Confirm group membership synchronization

## Health Commands

```bash
ldapsearch -x -h directory-server
id username
getent passwd username
```

## Troubleshooting Workflow

1. Confirm directory service reachable
2. Validate credentials
3. Review authentication logs
4. Restart authentication service
