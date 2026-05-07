# Certificates

Certificates operational notes and deep-dive references.

<div class="kb-grid kb-grid-2">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>certutil, openssl, PowerShell certificate store commands, and TLS verification.</span>
</a>

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Architecture overview, components, and design patterns.</span>
</a>

<a class="kb-card" href="integration/">
  <strong>Integration</strong>
  <span>Integration with other systems and platforms.</span>
</a>

<a class="kb-card" href="lifecycle/">
  <strong>Lifecycle</strong>
  <span>Installation, upgrades, patching, and decommission.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Day-to-day operational tasks, checks, and procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for common tasks and reporting.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Security configuration, hardening, and access control.</span>
</a>

<a class="kb-card" href="standards/">
  <strong>Standards</strong>
  <span>Configuration standards, naming conventions, and baselines.</span>
</a>

<a class="kb-card" href="vendor-support/">
  <strong>Vendor Support</strong>
  <span>Support bundles, case management, and escalation paths.</span>
</a>
</div>

<a class="kb-card" href="inventory/">
  <strong>Inventory</strong>
  <span>Inventory notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="expiration/">
  <strong>Expiration</strong>
  <span>Expiration notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="renewal/">
  <strong>Renewal</strong>
  <span>Renewal notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="chains/">
  <strong>Chains</strong>
  <span>Chains notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="tls-validation/">
  <strong>TLS Validation</strong>
  <span>TLS Validation notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Troubleshooting notes, checks, commands, troubleshooting, and validation.</span>
</a>

</div>

## Certificate Lifecycle

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    Certificate Lifecycle States                         │
  │                                                                         │
  │  Generate CSR  ──►  Submit to CA  ──►  CA signs cert  ──►  Deploy      │
  │  (private key)      (CSR + proof)      (DV/OV/EV)          (server/app) │
  │                                                                         │
  │                 ┌─────────────────────────────────────────┐            │
  │  Monitor expiry │  Valid → Warning (30d) → Critical (7d)  │ ◄── alerts │
  │                 └─────────────────────────────────────────┘            │
  │                                                                         │
  │  Renew / Rotate  ──►  Test new cert  ──►  Hot-swap  ──►  Revoke old    │
  │  (before expiry)       (staging)          (zero downtime)   (CRL/OCSP) │
  └─────────────────────────────────────────────────────────────────────────┘
```

## SAML SSO Authentication Flow

```
  User (Browser)          Service Provider (SP)          Identity Provider (IdP)
         │                          │                              │
         │── Access resource ──────►│                              │
         │                          │── No session — redirect ────►│
         │◄── 302 to IdP (SAML req) │   (AuthnRequest, signed)     │
         │                          │                              │
         │── GET IdP login page ───────────────────────────────►  │
         │◄── Login form ──────────────────────────────────────── │
         │                          │                              │
         │── Username + Password ──────────────────────────────►  │
         │   (+ MFA if enforced)    │                              │
         │◄── SAML Response (POST) ────────────────────────────── │
         │    (assertion, signed by IdP)                           │
         │                          │                              │
         │── POST to SP ACS URL ───►│                              │
         │   (SAML assertion)       │── Verify signature ─────────►│
         │                          │◄── Valid / Invalid ──────────│
         │                          │── Create session             │
         │◄── Set cookie + redirect─│                              │
         │                          │                              │
         │── Access resource ──────►│                              │
         │◄── 200 OK (content) ─────│                              │
```
