# Ansible

<div class="kb-summary">
Ansible automation knowledge base covering agentless architecture, inventory and playbook design, role and collection management, AWX/AAP deployment, and troubleshooting for Linux, Windows, network, and cloud targets.
</div>

```text
┌──────────────────────────── Ansible — Agentless Configuration Management ─────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Ansible: open-source agentless automation using SSH (Linux) or WinRM (Windows) transport   │   │
│   │     Control node pushes tasks to managed nodes; no agent installation required on targets     │   │
│   │       YAML playbooks describe desired state; modules execute tasks; idempotent by design      │   │
│   │    AWX / AAP adds RBAC, scheduling, credential vault, and REST API over the Ansible engine    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      Control node + SSH     │  │     Inventory management    │  │        Vault secrets        │   │
│   │   Inventory static/dynamic  │  │      Playbook execution     │  │         SSH key auth        │   │
│   │    Roles and collections    │  │      AWX job templates      │  │         RBAC via AWX        │   │
│   │    AWX/AAP control plane    │  │      Health and upgrade     │  │       Credential store      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Playbook      = ordered list of plays; each play maps a set of hosts to a set of tasks    │   │
│   │     Role          = reusable unit: tasks, handlers, vars, files, templates, defaults, meta    │   │
│   │Collection    = distribution format for roles + modules + plugins; installed via ansible-galaxy│   │
│   │     Inventory     = list of managed nodes; static (INI/YAML) or dynamic (scripts, plugins)    │   │
│   │     Module        = unit of work called by a task; e.g. apt, yum, copy, template, service     │   │
│   │  Handler       = task triggered only when notified by another task; used for service restarts │   │
│   │         Vault         = Ansible encryption for secrets; ansible-vault encrypt/decrypt         │   │
│   │            AWX           = Ansible Tower upstream; web UI + API + RBAC + scheduling           │   │
│   │     AAP           = Ansible Automation Platform; Red Hat enterprise product; includes AWX     │   │
│   │          Galaxy        = community hub for roles and collections; galaxy.ansible.com          │   │
│   │       host_vars     = variables scoped to a single host; stored in host_vars/<hostname>/      │   │
│   │         group_vars    = variables scoped to a group; stored in group_vars/<groupname>/        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Day-to-day operational tasks, health checks, procedures, and automation scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation procedures.</span>
</a>

</div>
