# Ansible — Architecture

<div class="kb-summary">
Agentless IT automation over SSH/WinRM; the control node pushes modules to managed nodes, executes tasks, and removes them; organised via inventory, playbooks, roles, and collections; enterprise scale via AWX/AAP and Execution Environments.
</div>

```
┌─────────────────────────────────────── Ansible — Architecture ────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Ansible architecture: control node runs ansible-playbook; connects outbound via SSH/WinRM   │   │
│   │   No persistent agent on managed nodes; Python must be present on Linux targets (>=2.7/3.5)   │   │
│   │       AWX provides a stateful control plane: job queue, credential store, event logging       │   │
│   │         Execution environments (EE): container images bundling Ansible + dependencies         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 How It Works                 │  │               Design Standards              │   │
│   │       Inventory → play → task → module       │  │             One role per concern            │   │
│   │          SSH multiplexing for speed          │  │      Tag every task for selective runs      │   │
│   │           Facts gathered per host            │  │       Roles in collections, not loose       │   │
│   │        Forks: parallel host execution        │  │           No hardcoded credentials          │   │
│   │        Handlers deferred to play end         │  │         Use check mode in pipelines         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Integrations                 │  │               Execution Model               │   │
│   │        AWX REST API → CI/CD triggers         │  │         Control node → SSH → managed        │   │
│   │         GitHub Actions calls AWX API         │  │          Execution environment (EE)         │   │
│   │         HashiCorp Vault for secrets          │  │         Forks = parallel host limit         │   │
│   │          LDAP/AD → AWX RBAC groups           │  │        Callback plugins: log results        │   │
│   │       Dynamic inventory: AWS, vSphere        │  │          Fact cache: Redis or file          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Physical: control node host (VM or container) + network access to managed nodes on port 22  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
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


