# Aria Automation — Operations

```
┌──────────────────────────────────── Aria Automation — Operations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Blueprint lifecycle management; request monitoring for failed deployments; catalog item health│   │
│   │  Subscription and event broker management; pipeline status monitoring; ABX function execution │   │
│   │ Daily: review failed requests, check cloud account connectivity, verify ABX timeout thresholds│   │
│   │    Lifecycle: Automation upgrade with pre-upgrade snapshot; embedded vRO and plugin updates   │   │
│   │        Automation: vRA REST API, ABX Python/Node, Terraform integration, vRO workflows        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch request failures · lifecycle keeps Automation current · automation scales delivery │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │      Request monitoring     │  │      Automation upgrade     │  │         vRA REST API        │   │
│   │        Failed deploys       │  │       Pre-upg snapshot      │  │       ABX: Python/Node      │   │
│   │        Catalog health       │  │         Embedded vRO        │  │        Terraform intg       │   │
│   │         Sub. events         │  │       ABX FaaS update       │  │        vRO workflows        │   │
│   │       Pipeline status       │  │        Plugin updates       │  │        PowerShell ABX       │   │
│   │       ABX timeout chk       │  │        API compat chk       │  │         API Explorer        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops monitor request health · lifecycle upgrades safely with snapshot                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │   vRA REST API   │   Requests: ok   │   Blueprint ver   │   Pre-upg snap   │  Config export   │   │
│   │   ABX function   │  Catalog: items  │    Deploy test    │  Automation upg  │  Policy backup   │   │
│   │  Terraform CLI   │  Cloud accts ok  │      ABX test     │    API compat    │  Blueprint bkp   │   │
│   │   API Explorer   │  Pipelines: ok   │    Entitlement    │   Post-upg val   │  Restore redep   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VM (Automation appliance) · RAM DIMMs · Network NICs · Cloud provider connectivity               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Blueprint     = IaC template; versioned in Aria Automation; deploy, update, and destroy lifecycle    │
│  Request       = User-initiated catalog item deployment; tracked in Service Broker with status and    │
│  Catalog item  = Published blueprint or workflow in Service Broker; versioned and                     │
│  ABX action    = FaaS function (Python/Node/PowerShell) triggered by events or directly from blueprint│
│  Subscription  = Event broker rule mapping a lifecycle event to an ABX action or Orchestrator workflow│
│  Event broker  = Aria Automation event bus; publishes compute/network/storage events to subscriptions │
│  Cloud account = Aria connection to vCenter/AWS/Azure/GCP; health check ensures connectivity          │
│  Approval policy = Required sign-off before request fulfillment; configurable per catalog item        │
│  Orchestrator workflow = vRO workflow embedded in Aria Automation; runs complex multi-step tasks      │
│  vRA REST API  = Primary Aria Automation programmatic interface; used for requests, blueprints,       │
│  Terraform provider = Aria Automation Terraform provider for IaC-driven provisioning workflows        │
│  Entitlement   = Service Broker policy granting project members access to specific catalog items      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Commands, syntax, and quick reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Routine checks, service validation, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Day-to-day operational tasks and how-to guides.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Installation, upgrade, patching, and decommission.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup configuration, restore procedures, and validation.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and reusable code.</span>
</a>

</div>
