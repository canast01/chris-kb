# Account Unlock Runbook


<div class="kb-summary">
| Field | Value | |---|---| | Risk | Low | | Approval | Verify requester identity — no change ticket required for standard user accounts | | Estimated time | 5–15 minutes | | Impact | User regains access; no service disruption |
</div>

| Field | Value |
|---|---|
| Risk | Low |
| Approval | Verify requester identity — no change ticket required for standard user accounts |
| Estimated time | 5–15 minutes |
| Impact | User regains access; no service disruption |

## Process Flow

```text
  Ticket received: account locked
           │
           ▼
  Confirm requester identity ────── Cannot confirm? ──► Escalate to manager
           │ Confirmed
           ▼
  Service account?  ─────────────── Yes ──────────────► Require owner approval
           │ No (standard user)
           ▼
  Find lockout source (Event ID 4740 on PDC)
           │
           ▼
  Identify root cause (stale creds / task / device)
           │
           ▼
  Fix root cause first ──── Cannot fix now? ──► Unlock and document — user re-locks risk
           │
           ▼
  Unlock account + confirm authentication
           │
           ▼
  Update ticket with lockout source
```
┌────────────────────────────────────── Runbook — Account Unlock ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Unlock AD account; identify lockout source; prevent re-lock before fix            │   │
│   │          Pre-check: confirm account is locked; find lockout source DC and application         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Identify Lockout Source            │  │                 Unlock Steps                │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │       Check Security Event Log (4740)        │  │          ADUC: right-click → Unlock         │   │
│   │          Use LockoutStatus.exe tool          │  │         PowerShell: Unlock-ADAccount        │   │
│   │         Find PDC emulator for events         │  │          Reset password if unknown          │   │
│   │         Caller workstation in event          │  │         Clear cached creds on device        │   │
│   │       Service account = check services       │  │           Update service/app creds          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                # PowerShell — unlock and check                                │   │
│   │         Get-ADUser <user> -Properties LockedOut,BadLogonCount | Select Name,LockedOut         │   │
│   │                               Unlock-ADAccount -Identity <user>                               │   │
│   │              Search-ADAccount -LockedOut | Select Name,LockedOut,PasswordExpired              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Step       │      Action      │    Command/tool   │      Verify      │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   Confirm lock   │   Check state    │     Get-ADUser    │  LockedOut=True  │  Before unlock   │   │
│   │   Find source    │    Event 4740    │   LockoutStatus   │   Caller found   │   PDC emulator   │   │
│   │      Unlock      │   Unlock acct    │  Unlock-ADAccount │ LockedOut=False  │   Sync all DCs   │   │
│   │    Fix cause     │   Clear creds    │   Device/service  │    No re-lock    │    Test login    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Event 4740     = Windows Security Event: account was locked out; caller and workstation noted      │
│    PDC emulator   = FSMO role; receives lockout events fastest; check Security log here first         │
│    LockoutStatus  = Microsoft tool; shows bad password count and lockout status per DC                │
│    Cached creds   = Windows stores last-used credentials; stale cached cred causes re-lock            │
│    Service account= Non-interactive account; lockout = service failing; update credential source      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────────── Runbook — Account Unlock ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Unlock AD account; identify lockout source; prevent re-lock before fix            │   │
│   │          Pre-check: confirm account is locked; find lockout source DC and application         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Identify Lockout Source            │  │                 Unlock Steps                │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │       Check Security Event Log (4740)        │  │          ADUC: right-click → Unlock         │   │
│   │          Use LockoutStatus.exe tool          │  │         PowerShell: Unlock-ADAccount        │   │
│   │         Find PDC emulator for events         │  │          Reset password if unknown          │   │
│   │         Caller workstation in event          │  │         Clear cached creds on device        │   │
│   │       Service account = check services       │  │           Update service/app creds          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                # PowerShell — unlock and check                                │   │
│   │         Get-ADUser <user> -Properties LockedOut,BadLogonCount | Select Name,LockedOut         │   │
│   │                               Unlock-ADAccount -Identity <user>                               │   │
│   │              Search-ADAccount -LockedOut | Select Name,LockedOut,PasswordExpired              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Step       │      Action      │    Command/tool   │      Verify      │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   Confirm lock   │   Check state    │     Get-ADUser    │  LockedOut=True  │  Before unlock   │   │
│   │   Find source    │    Event 4740    │   LockoutStatus   │   Caller found   │   PDC emulator   │   │
│   │      Unlock      │   Unlock acct    │  Unlock-ADAccount │ LockedOut=False  │   Sync all DCs   │   │
│   │    Fix cause     │   Clear creds    │   Device/service  │    No re-lock    │    Test login    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Event 4740     = Windows Security Event: account was locked out; caller and workstation noted      │
│    PDC emulator   = FSMO role; receives lockout events fastest; check Security log here first         │
│    LockoutStatus  = Microsoft tool; shows bad password count and lockout status per DC                │
│    Cached creds   = Windows stores last-used credentials; stale cached cred causes re-lock            │
│    Service account= Non-interactive account; lockout = service failing; update credential source      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Key fields in Event ID 4740:

| Field | Meaning |
|---|---|
| Caller Computer Name | Machine generating bad password attempts |
| Account Name | Locked account |
| Failure Reason | Usually "bad password" |

## Step 3 — Fix Root Cause

| Cause | Where to look | Fix |
|---|---|---|
| Stale cached credentials | Mobile device, Remote Desktop saved creds | Clear saved credentials on device |
| Scheduled task | Task Scheduler on caller machine | Update task credentials |
| Service with old password | Services console / `sc qc <svc>` | Update service account password |
| Mapped drive | `net use` output | Remove and re-add drive mapping |
| Repeated MFA failure | Azure AD Sign-In logs | Investigate for unauthorised attempts |

## Step 4 — Unlock the Account

```powershell
# Unlock single account
Unlock-ADAccount -Identity <username>

# Confirm unlocked
Get-ADUser -Identity <username> -Properties LockedOut | Select-Object Name, LockedOut
```

**Reset password and unlock (if password is also compromised):**
```powershell
Set-ADAccountPassword -Identity <username> -Reset `
    -NewPassword (ConvertTo-SecureString "<NewPass>" -AsPlainText -Force)
Unlock-ADAccount -Identity <username>
```

## Step 5 — Validate Authentication

```powershell
Get-ADUser -Identity <username> -Properties LockedOut, BadLogonCount |
    Select-Object Name, LockedOut, BadLogonCount
# LockedOut should be False; BadLogonCount should be 0
```

## Linux / SSSD (if applicable)

```bash
# Check lock state (RHEL 7 / pam_tally2)
pam_tally2 --user <username>
pam_tally2 --user <username> --reset

# RHEL 8+ (faillock)
faillock --user <username>
faillock --user <username> --reset
```

## Checklist

- [ ] Requester identity confirmed
- [ ] Account ownership verified (not an unattended service account)
- [ ] Lockout source identified and documented
- [ ] Root cause fixed or noted if deferred
- [ ] Account unlocked
- [ ] User confirmed able to authenticate
- [ ] Ticket updated with lockout source and fix applied
