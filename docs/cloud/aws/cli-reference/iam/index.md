---
title: AWS CLI — IAM
---

# AWS CLI — IAM


<div class="kb-summary">
AWS CLI — IAM reference.
</div>

```text
IAM CLI: Users · Roles · Policies · STS
──────────────────────────────────────────────────────────────

  sts get-caller-identity (always run first)
          │
          ▼
  ┌─────────────┐   ┌─────────────┐   ┌─────────────────┐
  │  IAM Users  │   │  IAM Roles  │   │  IAM Policies   │
  │             │   │             │   │                 │
  │ list-users  │   │ list-roles  │   │ attach-role-    │
  │ create-user │   │ create-role │   │   policy        │
  │ delete-user │   │ get-role    │   │ attach-user-    │
  │             │   │             │   │   policy        │
  │ list-access │   │             │   │                 │
  │   -keys     │   │             │   │                 │
  └──────┬──────┘   └──────┬──────┘   └─────────────────┘
         │                 │
         │                 ▼ sts assume-role
         │          ┌─────────────────────────┐
         │          │  Temporary Credentials  │
         │          │  (STS token, 1-12h)     │
         │          │  AccessKeyId            │
         │          │  SecretAccessKey        │
         │          │  SessionToken           │
         └─────────►└─────────────────────────┘
```
┌──────────────────────────────────────────── AWS CLI — IAM ────────────────────────────────────────────┐
│                                                                                                       │
│  IAM CLI commands for users, roles, policies, MFA, and access key management.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               User Management                │  │               Role Management               │   │
│   │          create-user: new IAM user           │  │        create-role: with trust policy       │   │
│   │            list-users: all users             │  │            list-roles: all roles            │   │
│   │            get-user: user details            │  │         assume-role: get credentials        │   │
│   │             delete-user: remove              │  │          update-assume-role-policy          │   │
│   │         update-login-profile: passwd         │  │         list-attached-role-policies         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Users for human access; roles for service and cross-account access                                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Policy and Key Management           │  │               MFA and Security              │   │
│   │          create-policy: new managed          │  │          enable-mfa-device: attach          │   │
│   │          attach-user-policy: assign          │  │            deactivate-mfa-device            │   │
│   │          create-access-key: new key          │  │            get-credential-report            │   │
│   │          update-access-key: disable          │  │          generate-credential-report         │   │
│   │          delete-access-key: remove           │  │          get-account-summary: stats         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  IAM service (global) · AWS STS (assume-role) · CloudTrail (API logging)                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  assume-role     = Requests temporary credentials for a role via STS                                  │
│  Trust policy    = JSON policy on a role defining who can assume it                                   │
│  Managed policy  = Standalone IAM policy; attached to multiple users/roles                            │
│  Inline policy   = Policy embedded directly in user/role; not reusable                                │
│  Access key      = Long-term programmatic credentials; rotate every 90 days                           │
│  update-access-key= Disables or activates an access key without deleting                              │
│  Credential report= CSV of all IAM users with last-used dates and MFA status                          │
│  enable-mfa-device= Registers a virtual or hardware MFA token for a user                              │
│  STS             = Security Token Service; issues temporary credentials                               │
│  get-account-summary= Returns counts of users, roles, policies, groups                                │
│  Permission boundary= IAM policy limiting max permissions a principal can have                        │
│  update-login-profile= Changes console password for an IAM user                                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
