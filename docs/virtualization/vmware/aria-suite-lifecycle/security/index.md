# Aria Suite Lifecycle — Security

```
  LCM Security Layers
┌──────────────────────────────────────────────────────────────┐
│  Identity               Access Control     Encryption         │
│  ┌──────────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │ VIDM (primary)   │   │ LCM Admin    │   │ Locker:      │  │
│  │  SAML/OAuth2     │   │  deploy/     │   │  certs +     │  │
│  │  AD via LDAPS    │   │  upgrade/    │   │  passwords   │  │
│  │                  │   │  Locker      │   │  encrypted   │  │
│  │ admin@local      │   │ Content Dev  │   │  w/ Master PW│  │
│  │  break-glass     │   │  read + CLM  │   │ TLS 1.2+ on  │  │
│  │  only            │   │ Viewer       │   │  all APIs    │  │
│  │                  │   │  read-only   │   │              │  │
│  └──────────────────┘   └──────────────┘   └──────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Workspace ONE Access SSO, identity sources, and local accounts.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>LCM roles, RBAC, and AD group assignment.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Locker certificate management, TLS, and password vault.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
