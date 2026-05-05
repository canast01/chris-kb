# Account Unlock Runbook

## Overview

This runbook provides a standard process for handling locked user or service accounts.

## Pre-Checks

- Confirm requester identity
- Check lockout source
- Validate account ownership
- Review failed login pattern

## Commands

```powershell
Search-ADAccount -LockedOut
Unlock-ADAccount -Identity username
Get-ADUser username -Properties LockedOut
```

## Validation

1. Confirm account unlocked
2. Confirm user can authenticate
3. Review lockout source if issue repeats
