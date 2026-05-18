# Windows Server — Security

```
┌───────────────────────────────────────────────────────┐
│             Windows Server Security Layers            │
├───────────────────────────────────────────────────────┤
│  Identity & Access                                    │
│  AD DS → Kerberos/NTLM → RBAC (AD groups)             │
│  GPO User Rights Assignments │ JEA (PS remoting)      │
├───────────────────────────────────────────────────────┤
│  Policy Enforcement                                   │
│  GPO ──► Computer Config ──► Security Settings        │
│          Account Policy │ Audit Policy │ Sec Options  │
├───────────────────────────────────────────────────────┤
│  Endpoint Protection                                  │
│  Windows Defender AV │ ASR rules │ Credential Guard   │
│  BitLocker (disk) │ Windows Firewall                  │
├───────────────────────────────────────────────────────┤
│  Audit & Monitoring                                   │
│  auditpol → Security Event Log → SIEM forwarding      │
└───────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Active Directory, local accounts, and authentication configuration.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC, local groups, file permissions, and GPO-based access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>BitLocker, TLS, and encrypted communication.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, CIS benchmarks, and compliance.</span>
</a>

</div>
