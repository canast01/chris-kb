---
tags:
  - troubleshooting
  - ansible
  - automation
  - known-issues
---
# Ansible / AAP — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Ansible Automation Platform bugs, error codes, and workarounds covering inventory, playbook execution, and Receptor mesh.

*Applies to: Ansible Automation Platform 2.x*
</div>

```text
┌───────────────────────────────────── Ansible Automation Platform ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         AAP — Controller, Execution Environments, Receptor mesh, Event-Driven Ansible         │   │
│   │                    Protocols: SSH · WinRM · Receptor (TCP 27199) · REST API                   │   │
│   │                     Management: Automation Controller UI / awx-manage CLI                     │   │
│   │       Inventory -> Playbook execution -> Receptor mesh -> Execution node -> Target host       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │        Control plane        │  │    Automation Controller    │  │      Job sched. + RBAC      │   │
│   │          Execution          │  │    Execution Environment    │  │  Container, ansible-runner  │   │
│   │             Mesh            │  │           Receptor          │  │   Node routing, TCP 27199   │   │
│   │          Inventory          │  │       Dynamic / static      │  │    AWX inventory plugins    │   │
│   │         Credentials         │  │       Credential store      │  │   Vault-backed, encrypted   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    Controller    │Job orchestration │       HTTPS       │   OAuth2/LDAP    │  Cluster-aware   │   │
│   │  Execution node  │  Runs playbooks  │    Receptor/SSH   │   Cert (mesh)    │   Isolated EE    │   │
│   │  Receptor mesh   │Node-to-node route│     TCP 27199     │       mTLS       │  Mesh topology   │   │
│   │  Automation Hub  │Content/collection│       HTTPS       │      Token       │ Private + Galaxy │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: Controller HA cluster - execution nodes - PostgreSQL DB - target hosts (SSH/WinRM)         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AAP            = Ansible Automation Platform; Red Hat enterprise suite (Controller+Hub+EDA)          │
│  Controller     = formerly AWX/Tower; orchestrates job templates, schedules, and RBAC                 │
│  Exec. Env.     = container bundling Ansible + collections + Python deps for a job run                │
│  Receptor       = mesh networking layer routing work to execution/hop nodes; TCP 27199                │
│  Playbook       = YAML automation script defining tasks and target hosts                              │
│  Become         = privilege escalation (sudo/su) used to run tasks as another user                    │
│  Inventory      = list of managed hosts; static file or dynamic plugin (cloud, CMDB)                  │
│  Credential     = encrypted secret (SSH key, vault pw, API key) stored in Controller                  │
│  Job template   = reusable definition: playbook + inventory + credentials + survey                    │
│  Automation Hub = private content repository for certified/validated collections                      │
│  EDA            = Event-Driven Ansible; reacts to webhooks/alerts, triggers rulebooks                 │
│  ansible-vault  = encrypts sensitive variables/files at rest inside playbooks                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- AAP job errors appear in Automation Controller → Jobs — click the failed job for detailed output.
- Most playbook failures are SSH connectivity, become (sudo) config, or Python interpreter issues on targets.
- Verbose mode: run playbooks with `-vvv` to see connection details.

## SSH Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Permission denied (publickey)` | AAP 2.x | SSH key not deployed to target or wrong user | Verify machine credential in AAP has correct SSH private key; test: `ssh -i <key> user@host` | N/A |
| `ssh: connect to host port 22: Connection refused` | AAP 2.x | SSH not running on target or port blocked | Check SSH service on target; verify TCP 22 from AAP execution node to target | N/A |
| `UNREACHABLE: Failed to connect to the host via ssh: Host key verification failed` | AAP 2.x | SSH host key changed; known_hosts mismatch | Set `host_key_checking = False` in `ansible.cfg` (lab only); or update known_hosts | N/A |

## Become / Sudo

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `sudo: a password is required` | AAP 2.x | Target requires sudo password; not in credential | Add sudo password to machine credential in AAP; or configure passwordless sudo | N/A |
| `Timeout waiting for privilege escalation` | AAP 2.x | Sudo prompt not matched; or become_method mismatch | Set `become_method: sudo`; increase `timeout` in `ansible.cfg` | N/A |

## Execution Nodes (Receptor)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Execution node `Unavailable` | AAP 2.x | Receptor mesh port 27199 blocked | Verify TCP 27199 between controller and execution nodes | N/A |
| Jobs queued but not starting | AAP 2.x | No healthy execution nodes in instance group | Check execution node health in AAP → Topology; restart receptor: `systemctl restart receptor` | N/A |

## WinRM (Windows)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `winrm or requests is not installed` | AAP 2.x | Python `pywinrm` not installed on execution node | Install: `pip install pywinrm` on execution node | N/A |
| `AuthenticationError: 401 Unauthorized` | AAP 2.x | Windows credential type mismatch (basic vs Kerberos) | Configure WinRM for Basic or NTLM auth; or set up Kerberos properly | N/A |

## See also

- [Ansible — Common Issues](common-issues.md)
- [Terraform — Known Issues](../../terraform/troubleshooting/known-issues/)
