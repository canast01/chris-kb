# PowerShell — Security



<div class="kb-summary">
PowerShell — Security reference.
</div>

```
┌──────────────────────────────────────── PowerShell — Security ────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  PowerShell security: execution policy, code signing, AMSI integration, script block logging  │   │
│   │      Enable: ScriptBlockLogging + ModuleLogging + Protected Event Logging in Group Policy     │   │
│   │    JEA: Just Enough Administration — constrained PS endpoints with minimal allowed commands   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Execution Controls     │  │           Logging           │  │          Delegation         │   │
│   │  ExecutionPolicy: AllSigned │  │     ScriptBlock logging     │  │        JEA endpoints        │   │
│   │     Code signing (cert)     │  │        Module logging       │  │         RBAC via JEA        │   │
│   │      AMSI: malware scan     │  │     Protected Event Log     │  │    Constrained lang mode    │   │
│   │    Constrained lang mode    │  │       SIEM forwarding       │  │     No interactive admin    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    ScriptBlock logging = logs every command block executed; enables forensics post-incident   │   │
│   │     Constrained lang   = restricts allowed .NET types in PS; limits attacker capabilities     │   │
│   │  JEA                = session config with VisibleCmdlets list; operators use PS without admin │   │
│   │      Protected Event Log= encrypts event log entries so only authorised users can decrypt     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────── PowerShell — Security ────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  PowerShell security: execution policy, code signing, AMSI integration, script block logging  │   │
│   │      Enable: ScriptBlockLogging + ModuleLogging + Protected Event Logging in Group Policy     │   │
│   │    JEA: Just Enough Administration — constrained PS endpoints with minimal allowed commands   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Execution Controls     │  │           Logging           │  │          Delegation         │   │
│   │  ExecutionPolicy: AllSigned │  │     ScriptBlock logging     │  │        JEA endpoints        │   │
│   │     Code signing (cert)     │  │        Module logging       │  │         RBAC via JEA        │   │
│   │      AMSI: malware scan     │  │     Protected Event Log     │  │    Constrained lang mode    │   │
│   │    Constrained lang mode    │  │       SIEM forwarding       │  │     No interactive admin    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    ScriptBlock logging = logs every command block executed; enables forensics post-incident   │   │
│   │     Constrained lang   = restricts allowed .NET types in PS; limits attacker capabilities     │   │
│   │  JEA                = session config with VisibleCmdlets list; operators use PS without admin │   │
│   │      Protected Event Log= encrypts event log entries so only authorised users can decrypt     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Credential management and authentication methods.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Execution policy, roles, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>SecureString, credential encryption, and secure communication.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and PowerShell hardening configuration.</span>
</a>

</div>
