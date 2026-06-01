# Ansible — Operations



<div class="kb-summary">
Ansible — Operations reference: Health Checks, Procedures, CLI Reference, Install & Upgrade, and 2 more.
</div>

```
┌──────────────────────────────────────── Ansible — Operations ─────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Ansible operations: running playbooks, managing inventory, AWX job templates, upgrades    │   │
│   │ Day-to-day: add/remove hosts from inventory, update group_vars, trigger jobs via AWX UI or API│   │
│   │   Health checks: AWX service status, job success rate, credential expiry, EE image currency   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        CLI Operations       │  │        AWX Operations       │  │         Maintenance         │   │
│   │     ansible-playbook run    │  │     Job template launch     │  │         Upgrade AWX         │   │
│   │   ansible-inventory --list  │  │        Inventory sync       │  │       Update EE images      │   │
│   │     ansible -m ping all     │  │     Credential rotation     │  │      Rotate Vault keys      │   │
│   │     ansible-vault rekey     │  │     RBAC team assignment    │  │      Purge old job data     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Job template    = saved configuration: playbook + inventory + credentials + extra vars in AWX │   │
│   │     Inventory sync  = pull current host list from dynamic source (cloud, Netbox) into AWX     │   │
│   │EE              = Execution Environment; OCI container with Ansible + collections + Python deps│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────── Ansible — Operations ─────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Ansible operations: running playbooks, managing inventory, AWX job templates, upgrades    │   │
│   │ Day-to-day: add/remove hosts from inventory, update group_vars, trigger jobs via AWX UI or API│   │
│   │   Health checks: AWX service status, job success rate, credential expiry, EE image currency   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        CLI Operations       │  │        AWX Operations       │  │         Maintenance         │   │
│   │     ansible-playbook run    │  │     Job template launch     │  │         Upgrade AWX         │   │
│   │   ansible-inventory --list  │  │        Inventory sync       │  │       Update EE images      │   │
│   │     ansible -m ping all     │  │     Credential rotation     │  │      Rotate Vault keys      │   │
│   │     ansible-vault rekey     │  │     RBAC team assignment    │  │      Purge old job data     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Job template    = saved configuration: playbook + inventory + credentials + extra vars in AWX │   │
│   │     Inventory sync  = pull current host list from dynamic source (cloud, Netbox) into AWX     │   │
│   │EE              = Execution Environment; OCI container with Ansible + collections + Python deps│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
</div>
