---
tags:
  - ansible
  - architecture
---
# Ansible — Architecture

<div class="kb-summary">
Agentless IT automation over SSH/WinRM; the control node pushes modules to managed nodes, executes tasks, and removes them; organised via inventory, playbooks, roles, and collections; enterprise scale via AWX/AAP and Execution Environments.

*Applies to: Ansible 2.x*
</div>

```text
┌───────────────────────────── Ansible Architecture — Agentless Automation ─────────────────────────────┐
│                                                                                                       │
│  Agentless model: control node pushes Python modules over SSH/WinRM to managed                        │
│  nodes, executes tasks, then removes them; no daemon installed on targets.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Control Plane                 │  │                Managed Nodes                │   │
│   │        Control node: any Linux/macOS         │  │         No agent installed on target        │   │
│   │        Inventory: hosts + group vars         │  │         Linux: SSH + Python required        │   │
│   │          Playbooks: YAML task lists          │  │           Windows: WinRM 5985/5986          │   │
│   │        Roles: reusable task structure        │  │         Network: httpapi connection         │   │
│   │        Collections: packaged modules         │  │         Temp module: /tmp/ansible-*         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Control node connects to each host, copies module, runs it, collects stdout/rc.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Enterprise Scale (AWX/AAP)          │  │            Execution Environments           │   │
│   │        AWX: open-source web UI + API         │  │        Container with Ansible + deps        │   │
│   │        AAP: Red Hat supported product        │  │           Isolated runtime per job          │   │
│   │        RBAC: teams, orgs, credentials        │  │          Build: ansible-builder CLI         │   │
│   │           Schedules + survey forms           │  │         Registry: private or quay.io        │   │
│   │         Webhook: trigger on Git push         │  │        Replaces virtualenv isolation        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Control node (Linux VM/container); SSH/WinRM access to all managed hosts;                            │
│  AWX/AAP: PostgreSQL backend + Redis + web/task containers.                                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Control node  = machine running ansible-playbook; not a target                                       │
│  Managed node  = target host; SSH or WinRM connection; Python required                                │
│  Inventory     = list of hosts and groups with variables                                              │
│  Playbook      = YAML file; ordered list of plays and tasks                                           │
│  Role          = reusable structure: tasks/handlers/vars/templates                                    │
│  Collection    = packaged roles/modules/plugins; Galaxy or private                                    │
│  Module        = unit of work; pushed as temp Python; idempotent                                      │
│  AWX           = open-source web UI for Ansible; upstream of AAP                                      │
│  AAP           = Ansible Automation Platform; Red Hat enterprise product                              │
│  EE            = Execution Environment; container with Ansible + collections                          │
│  WinRM         = Windows Remote Management; port 5985 HTTP, 5986 HTTPS                                │
│  Idempotent    = safe to re-run; same end state regardless of start state                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Ansible Architecture](../../../assets/ansible-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Agentless model, inventory, playbooks, modules, roles, collections, and execution flow.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## Core Components

| Component | Purpose |
|---|---|
| Control Node | Ansible installed here; all automation initiated; no agent on managed nodes |
| Managed Node | Target host or device; requires only SSH + Python (or WinRM for Windows) |
| Inventory | Source of truth for hosts and group membership (static INI/YAML or dynamic plugins) |
| Playbook | YAML file defining ordered plays; maps host groups to task lists |
| Module | Unit of work; transferred to managed node, executed, result returned as JSON |
| Role | Structured, reusable bundle of tasks, handlers, vars, templates, and files |
| Collection | Distribution format for modules, roles, plugins, namespaced under `<ns>.<name>` |
| AWX / AAP | Web UI + REST API + RBAC + scheduling layer on top of Ansible CLI |

## Agentless Execution Model

