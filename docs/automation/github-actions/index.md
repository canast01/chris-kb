# GitHub Actions


<div class="kb-grid kb-grid-1">

  <div class="kb-card">
    <h3><a href="troubleshooting/">Troubleshooting</a></h3>
    <p>Common issues, diagnostic steps, and resolution guides.</p>
  </div>

</div>
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
