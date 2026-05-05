# Authentication Failures Troubleshooting

## Overview

Authentication failures may occur due to directory service issues, credential problems, certificate errors, or network connectivity problems.

## Symptoms

- Login failures
- Account lockouts
- Expired passwords
- Kerberos errors

## Health Commands

```powershell
Get-EventLog -LogName Security -Newest 20
nltest /dsgetdc:domain
klist
```

## Troubleshooting Workflow

1. Confirm user credentials
2. Verify domain controller availability
3. Check time synchronization
4. Review security logs
5. Reset credentials if required
