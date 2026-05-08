# ESXi — Authentication

## Local Accounts

Minimise local accounts to root and one named break-glass account. Do not create shared service accounts with local ESXi access.

```bash
# Set root password
passwd root
```

**Root account:** Set a strong, unique root password per host. Rotate passwords at least annually or after any personnel change. Use a password manager or secrets vault.

## Active Directory Authentication

All administrative access should go through vCenter with Active Directory authentication. Configure vCenter to use AD as the identity source. AD users and groups are assigned roles in vCenter, not directly on ESXi hosts.

## Password Policy

Enforce complexity and history via host profile settings:

- Minimum length: 12 characters
- Complexity: upper, lower, digit, special
- History: last 5 passwords
- Lockout: 5 failed attempts, 15-minute lockout
