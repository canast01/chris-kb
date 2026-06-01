# Ansible — How It Works


<div class="kb-summary">
Ansible is an agentless IT automation engine that automates provisioning, configuration management, application deployment, orchestration, and many other IT processes.
</div>

 It uses SSH (or WinRM for Windows) to communicate with managed nodes, pushing small programs called modules to execute tasks, then removing them when complete. No agent daemon is required on any managed node.

---

## The Agentless Model

| Property | Agentless (Ansible) | Agent-Based (Puppet/Chef) |
|---|---|---|
| Node prerequisite | SSH + Python (or WinRM) | Agent installed and running |
| Control plane overhead | Minimal | Agent check-ins + CA infrastructure |
| Network exposure | Outbound SSH from control node | Inbound from nodes to master |
| Bootstrapping | Works on fresh OS installs immediately | Agent must be provisioned first |
| Update surface | Only the control node | Every single managed node |
| Latency per task | SSH handshake per batch | Persistent connection |

```mermaid
flowchart LR
    CN[Control Node\nAnsible installed] -->|SSH| MN1[Linux Host]
    CN -->|SSH| MN2[Network Device\nCisco / Juniper]
    CN -->|WinRM or SSH| MN3[Windows Host]
    CN -->|HTTPS API| MN4[Cloud API\nAWS / Azure / vSphere]
    CN -->|SSH| MN5[Linux Host]
```
┌─────────────────────────────────────── Ansible — How It Works ────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Execution flow: ansible-playbook reads inventory + playbook → connects to hosts → runs tasks │   │
│   │      Each task calls a module; module code is transferred to the remote host and executed     │   │
│   │  Results returned as JSON; Ansible evaluates changed/ok/failed; handlers notified on changed  │   │
│   │       AWX wraps this: stores credentials, queues jobs, streams events to UI in real time      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Step 1: Parse        │  │       Step 2: Connect       │  │       Step 3: Execute       │   │
│   │        Load inventory       │  │        SSH/WinRM open       │  │     Module runs on host     │   │
│   │     Parse playbook YAML     │  │     Gather facts (setup)    │  │     JSON result returned    │   │
│   │      Resolve variables      │  │     Multiplexed SSH conn    │  │    changed / ok / failed    │   │
│   │     Apply filters/limits    │  │    Fork N hosts parallel    │  │      Handlers triggered     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Gather facts     = module: setup; collects OS, IP, memory, disk, fqdn for use in templates  │   │
│   │        Check mode    = --check flag; simulates without applying; modules report changes       │   │
│   │    Diff mode        = --diff flag; shows before/after for file edits; combine with --check    │   │
│   │  Fork             = max parallel host connections; default 5; increase for large inventories  │   │
│   │ Serial           = limit hosts per batch in rolling update; e.g. serial: 1 for canary deploys │   │
│   │       delegate_to      = run task on a different host (e.g. register DNS on a jump host)      │   │
│   │        when             = conditional expression; task skipped when condition is False        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## Playbooks

Playbooks are YAML files that define ordered sets of plays. Each play maps a set of hosts to a list of tasks.

```yaml
- name: Configure web tier
  hosts: webservers
  become: true
  roles:
    - common
    - nginx

- name: Configure database tier
  hosts: databases
  become: true
  roles:
    - common
    - postgresql
```

---

## Module Execution

Ansible transfers a Python script (or PowerShell for Windows) to the managed node, executes it, collects the JSON output, and removes it.

```mermaid
sequenceDiagram
    participant CN as Control Node
    participant MN as Managed Node
    CN->>MN: SSH connect
    CN->>MN: Transfer module (Python + args JSON)
    MN->>MN: Execute module
    MN-->>CN: Return JSON result {changed, rc, stdout}
    CN->>MN: Remove module temp files
    CN->>MN: SSH disconnect
```

---

## Roles

Roles provide a structured, reusable packaging format bundling tasks, handlers, variables, templates, and files.

```text
roles/
└── nginx/
    ├── defaults/main.yml
    ├── vars/main.yml
    ├── tasks/main.yml
    ├── handlers/main.yml
    ├── templates/
    ├── files/
    ├── meta/main.yml
    └── molecule/
```

---

## Collections

| Collection | Purpose |
|---|---|
| `ansible.builtin` | Core modules shipped with ansible-core |
| `community.general` | Broad community module library |
| `ansible.posix` | POSIX-specific modules |
| `community.vmware` | VMware vSphere automation |
| `amazon.aws` | AWS resource management |
| `azure.azcollection` | Azure resource management |
| `kubernetes.core` | Kubernetes / OpenShift automation |

---

## Execution Flow

```mermaid
flowchart TD
    A[ansible-playbook site.yml -i inventory/] --> B[Parse Inventory\nResolve hosts and groups]
    B --> C[Load Variables\ngroup_vars host_vars extra_vars]
    C --> D[Gather Facts\nsetup module on each host]
    D --> E[Execute Play 1\nhosts: webservers]
    E --> F[Task: Install nginx]
    F --> G{Changed?}
    G -->|Yes| H[Notify handler: restart nginx]
    G -->|No| I[Task: Deploy config file]
    I --> J[Task: Ensure service running]
    J --> K[Run notified handlers once]
    K --> L[Execute Play 2\nhosts: databases]
    L --> M[Playbook complete]
```

---

## Ansible CLI vs AWX vs AAP

| Feature | Ansible CLI | AWX (open source) | AAP (Red Hat) |
|---|---|---|---|
| Interface | CLI only | Web UI + REST API | Web UI + REST API |
| RBAC | None | Yes | Yes — enterprise LDAP/SAML |
| Scheduling | External cron | Built-in scheduler | Built-in scheduler |
| Credential storage | Ansible Vault files | Encrypted database | Encrypted DB + EE isolation |
| Audit log | Local stdout/log | Activity stream | Activity stream + SIEM integration |
| Execution Environments | Via ansible-navigator | Yes (AWX 21+) | First-class EE support |
| Certified content | No | No | Red Hat certified collections |

---

## Execution Environments

Since Ansible Automation Platform 2.0, Ansible runs inside container images called Execution Environments (EEs). EEs bundle ansible-core, Python dependencies, and collection dependencies into an immutable image.

```bash
ansible-navigator run site.yml \
  --eei registry.redhat.io/ansible-automation-platform-24/ee-supported-rhel9:latest \
  --mode stdout

ansible-builder build \
  --file execution-environment.yml \
  --tag my-org/custom-ee:1.0
```
