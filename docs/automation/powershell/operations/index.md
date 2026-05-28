# PowerShell — Operations


```
┌─────────────────────────────────────── PowerShell — Operations ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       PowerShell ops: script deployment, module updates, remoting config, DSC management      │   │
│   │  Module mgmt: Install-Module, Update-Module, Get-InstalledModule; -Scope AllUsers for shared  │   │
│   │            Remoting: Enable-PSRemoting; configure WinRM HTTPS; test with Test-WSMan           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Module Operations               │  │             Remoting Operations             │   │
│   │              Find-Module <name>              │  │           Enable-PSRemoting -Force          │   │
│   │       Install-Module -Name <x> -Force        │  │            Test-WSMan <hostname>            │   │
│   │           Update-Module -Name <x>            │  │            Enter-PSSession <host>           │   │
│   │          Get-InstalledModule | sort          │  │           Invoke-Command -Computer          │   │
│   │        Uninstall-Module -AllVersions         │  │          New-PSSession (persistent)         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │Enable-PSRemoting = configures WinRM listener and firewall rule; required before remoting works│   │
│   │  PSRepository      = Register-PSRepository to add internal feed (Nexus, Artifactory, ProGet)  │   │
│   │    -AllowClobber   = Install-Module flag; overrides conflicting commands from other modules   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>PowerShell command reference with syntax and examples.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Daily checks and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Change readiness, maintenance windows, and operational procedures.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install &amp; Upgrade</strong>
  <span>Version management, module installation, and upgrades.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup &amp; Restore</strong>
  <span>Script backup and configuration restore procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for infrastructure operations.</span>
</a>

</div>
