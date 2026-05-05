# GitHub Actions

## Overview

GitHub Actions runs CI/CD workflows for validation, builds, publishing, automation, and scheduled operations.

## Daily Checks

- Review failed workflows
- Check secrets and variables
- Validate runner availability
- Review deployment history
- Confirm branch protection rules

## Health Commands

```bash
gh workflow list
gh run list
gh run view RUN_ID
gh secret list
```

## Upgrade Workflow

1. Review workflow changes
2. Validate action versions
3. Update pinned actions carefully
4. Run workflow on test branch
5. Confirm deployment output
