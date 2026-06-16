"""
Known-issues page diagram functions.
Auto-registered via @kb_diagram decorator at import time.

All functions follow the same fixed layout (validated by the storage_dell
"good examples" already in the repo): W2=103, IV box 3-99, three Layer/
Component/Notes boxes at (3,33)/(36,66)/(69,99), a 5-column sections table
at dividers (22,41,61,80), a physical-infra line, and a 12-entry glossary.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

W2 = 103
IV_L, IV_R = 3, 99
B1_L, B1_R = 3, 33
B2_L, B2_R = 36, 66
B3_L, B3_R = 69, 99
M1, M2, M3 = 18, 51, 84
PD1, PD2, PD3, PD4 = 22, 41, 61, 80


# ── Automation ────────────────────────────────────────────────────────────────

@kb_diagram(
    'ki-ansible',
    'docs/automation/ansible/troubleshooting/known-issues.md',
    'Ansible Automation Platform known issues — Controller, Receptor mesh, execution environments',
)
def ki_ansible():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Ansible Automation Platform'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AAP — Controller, Execution Environments, Receptor mesh, Event-Driven Ansible')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: SSH · WinRM · Receptor (TCP 27199) · REST API')))
    lines.append(R(bMid(IV_L, IV_R, 'Management: Automation Controller UI / awx-manage CLI')))
    lines.append(R(bMid(IV_L, IV_R, 'Inventory -> Playbook execution -> Receptor mesh -> Execution node -> Target host')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Layer'), bMid(B2_L, B2_R, 'Component'), bMid(B3_L, B3_R, 'Notes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Control plane'), bMid(B2_L, B2_R, 'Automation Controller'), bMid(B3_L, B3_R, 'Job sched. + RBAC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Execution'), bMid(B2_L, B2_R, 'Execution Environment'), bMid(B3_L, B3_R, 'Container, ansible-runner'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Mesh'), bMid(B2_L, B2_R, 'Receptor'), bMid(B3_L, B3_R, 'Node routing, TCP 27199'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Inventory'), bMid(B2_L, B2_R, 'Dynamic / static'), bMid(B3_L, B3_R, 'AWX inventory plugins'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Credentials'), bMid(B2_L, B2_R, 'Credential store'), bMid(B3_L, B3_R, 'Vault-backed, encrypted'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Component', 'Purpose', 'Protocol', 'Auth', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Controller', 'Job orchestration', 'HTTPS', 'OAuth2/LDAP', 'Cluster-aware'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Execution node', 'Runs playbooks', 'Receptor/SSH', 'Cert (mesh)', 'Isolated EE'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Receptor mesh', 'Node-to-node route', 'TCP 27199', 'mTLS', 'Mesh topology'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Automation Hub', 'Content/collection', 'HTTPS', 'Token', 'Private + Galaxy'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('Physical: Controller HA cluster - execution nodes - PostgreSQL DB - target hosts (SSH/WinRM)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AAP            = Ansible Automation Platform; Red Hat enterprise suite (Controller+Hub+EDA)'))
    lines.append(txt_row('Controller     = formerly AWX/Tower; orchestrates job templates, schedules, and RBAC'))
    lines.append(txt_row('Exec. Env.     = container bundling Ansible + collections + Python deps for a job run'))
    lines.append(txt_row('Receptor       = mesh networking layer routing work to execution/hop nodes; TCP 27199'))
    lines.append(txt_row('Playbook       = YAML automation script defining tasks and target hosts'))
    lines.append(txt_row('Become         = privilege escalation (sudo/su) used to run tasks as another user'))
    lines.append(txt_row('Inventory      = list of managed hosts; static file or dynamic plugin (cloud, CMDB)'))
    lines.append(txt_row('Credential     = encrypted secret (SSH key, vault pw, API key) stored in Controller'))
    lines.append(txt_row('Job template   = reusable definition: playbook + inventory + credentials + survey'))
    lines.append(txt_row('Automation Hub = private content repository for certified/validated collections'))
    lines.append(txt_row('EDA            = Event-Driven Ansible; reacts to webhooks/alerts, triggers rulebooks'))
    lines.append(txt_row('ansible-vault  = encrypts sensitive variables/files at rest inside playbooks'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ki-github-actions',
    'docs/automation/github-actions/troubleshooting/known-issues.md',
    'GitHub Actions known issues — self-hosted runners, secrets, workflow triggers',
)
def ki_github_actions():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'GitHub Actions'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CI/CD platform — cloud-hosted or self-hosted runners executing workflow YAML')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: HTTPS (TCP 443) to github.com · webhook callbacks')))
    lines.append(R(bMid(IV_L, IV_R, 'Management: Settings -> Actions (repo/org/enterprise level)')))
    lines.append(R(bMid(IV_L, IV_R, 'Trigger -> Runner pickup -> Job steps -> Artifacts/Logs -> Status check')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Layer'), bMid(B2_L, B2_R, 'Component'), bMid(B3_L, B3_R, 'Notes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Trigger'), bMid(B2_L, B2_R, 'Workflow YAML'), bMid(B3_L, B3_R, 'on: push/PR/schedule'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Compute'), bMid(B2_L, B2_R, 'Hosted / self-hosted runner'), bMid(B3_L, B3_R, 'Labels match runs-on'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identity'), bMid(B2_L, B2_R, 'GITHUB_TOKEN / OIDC'), bMid(B3_L, B3_R, 'Scoped per job'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Secrets'), bMid(B2_L, B2_R, 'Repo/org/env secrets'), bMid(B3_L, B3_R, 'Masked in logs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Artifacts'), bMid(B2_L, B2_R, 'actions/upload-artifact'), bMid(B3_L, B3_R, '90-day default retention'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Component', 'Purpose', 'Protocol', 'Auth', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Hosted runner', 'Ephemeral VM/job', 'HTTPS', 'GITHUB_TOKEN', 'GitHub-managed'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Self-hosted runner', 'Customer compute', 'HTTPS out (443)', 'Runner token', 'Long-lived process'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['OIDC', 'Cloud federation', 'HTTPS', 'JWT claims', 'No static keys'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Environments', 'Deploy gating', 'N/A', 'Reviewers', 'Protection rules'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('Physical: GitHub-hosted VM fleet (cloud) or customer-owned self-hosted runner hosts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Workflow       = YAML file in .github/workflows defining triggers, jobs, and steps'))
    lines.append(txt_row('Runner         = the machine (hosted or self-hosted) that executes a job'))
    lines.append(txt_row('runs-on        = label selecting which runner picks up a job (e.g. ubuntu-latest)'))
    lines.append(txt_row('GITHUB_TOKEN   = auto-generated per-job token scoped to the triggering repository'))
    lines.append(txt_row('OIDC           = OpenID Connect; lets workflows get short-lived cloud creds, no secrets'))
    lines.append(txt_row('Secret         = encrypted value set at repo/org/environment scope, masked in logs'))
    lines.append(txt_row('Environment    = named deployment target with optional required reviewers/wait timer'))
    lines.append(txt_row('Artifact       = file(s) uploaded by a job for later jobs or download, time-limited'))
    lines.append(txt_row('Matrix build   = one job definition fanned out across a grid of input variables'))
    lines.append(txt_row('Self-hosted    = customer-managed runner; needs outbound 443 to github.com, no inbound'))
    lines.append(txt_row('Concurrency    = group key limiting/cancelling overlapping workflow runs'))
    lines.append(txt_row('Reusable wflow = workflow called by another workflow via workflow_call'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ki-powershell',
    'docs/automation/powershell/troubleshooting/known-issues.md',
    'PowerShell / WinRM known issues — remoting, execution policy, module loading',
)
def ki_powershell():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'PowerShell / WinRM'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerShell 5.1 (Windows-only) and 7.x (cross-platform) scripting and remoting')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: WinRM (HTTP 5985 / HTTPS 5986) · SSH (PS 7.x remoting)')))
    lines.append(R(bMid(IV_L, IV_R, 'Management: PowerShell console / ISE / VS Code extension')))
    lines.append(R(bMid(IV_L, IV_R, 'Script -> Execution policy check -> Module import -> Remoting session -> Target')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Layer'), bMid(B2_L, B2_R, 'Component'), bMid(B3_L, B3_R, 'Notes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Engine'), bMid(B2_L, B2_R, 'PS 5.1 / PS 7.x (Core)'), bMid(B3_L, B3_R, '.NET Framework / .NET'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Remoting'), bMid(B2_L, B2_R, 'WinRM listener'), bMid(B3_L, B3_R, 'HTTP 5985 / HTTPS 5986'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Security'), bMid(B2_L, B2_R, 'Execution policy'), bMid(B3_L, B3_R, 'Restricted/RemoteSigned'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Modules'), bMid(B2_L, B2_R, 'PSGallery / PSRepository'), bMid(B3_L, B3_R, 'Per-user or system scope'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Delegation'), bMid(B2_L, B2_R, 'CredSSP / Kerberos'), bMid(B3_L, B3_R, 'Double-hop auth'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Component', 'Purpose', 'Protocol', 'Auth', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Enter-PSSession', 'Interactive remote', 'WinRM', 'Kerberos/NTLM', 'Single host'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Invoke-Command', 'Batch remoting', 'WinRM', 'Kerberos/NTLM', 'Fan-out to many'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CredSSP', 'Cred. delegation', 'WinRM', 'Delegated creds', 'Double-hop fix'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['PSGallery', 'Module source', 'HTTPS', 'API key (publish)', 'Public repo'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('Physical: Windows hosts (WinRM listener) - Linux/macOS hosts (PS 7.x + SSH remoting)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('WinRM          = Windows Remote Management; SOAP-based remoting over HTTP/HTTPS'))
    lines.append(txt_row('Execution pol. = local script-running policy: Restricted/AllSigned/RemoteSigned/etc.'))
    lines.append(txt_row('TrustedHosts   = client allow-list of remote hosts permitted without Kerberos'))
    lines.append(txt_row('CredSSP        = Credential Security Support Provider; enables credential delegation'))
    lines.append(txt_row('Double-hop     = a remote session needing to authenticate onward to a third host'))
    lines.append(txt_row('PSGallery      = Microsoft-hosted public PowerShell module repository'))
    lines.append(txt_row('Zone.Identifier= NTFS alternate stream marking a file as downloaded from the internet'))
    lines.append(txt_row('Unblock-File   = removes the Zone.Identifier stream so a script will run'))
    lines.append(txt_row('PSSession      = a persistent remoting connection reusable across multiple commands'))
    lines.append(txt_row('Desired State Config. = DSC; declarative configuration management built into PS'))
    lines.append(txt_row('$PSVersionTable= built-in variable reporting PS edition, version, and OS platform'))
    lines.append(txt_row('Constrained EP = endpoint exposing only a restricted command set for remoting'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ki-python-automation',
    'docs/automation/python/troubleshooting/known-issues.md',
    'Python automation scripts known issues — venvs, SSL trust, REST API integration',
)
def ki_python_automation():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Python Automation Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Python 3.10/3.12 scripts for infrastructure automation and REST API integration')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: HTTPS (requests/urllib3) · SSH (paramiko/fabric) · SNMP (pysnmp)')))
    lines.append(R(bMid(IV_L, IV_R, 'Management: venv per project / pip / requirements.txt or pyproject.toml')))
    lines.append(R(bMid(IV_L, IV_R, 'venv activate -> pip install -> script run -> API/SSH call -> target system')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Layer'), bMid(B2_L, B2_R, 'Component'), bMid(B3_L, B3_R, 'Notes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Isolation'), bMid(B2_L, B2_R, 'venv / virtualenv'), bMid(B3_L, B3_R, 'Per-project deps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Packages'), bMid(B2_L, B2_R, 'pip / PyPI'), bMid(B3_L, B3_R, 'requirements.txt pin'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Trust'), bMid(B2_L, B2_R, 'CA bundle / certifi'), bMid(B3_L, B3_R, 'Internal CA often missing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HTTP client'), bMid(B2_L, B2_R, 'requests / httpx'), bMid(B3_L, B3_R, 'Timeout, retries'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Remote exec'), bMid(B2_L, B2_R, 'paramiko / fabric'), bMid(B3_L, B3_R, 'SSH key or password'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Component', 'Purpose', 'Protocol', 'Auth', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['requests', 'REST API calls', 'HTTPS', 'Bearer/Basic/cert', 'Uses OS trust'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['paramiko', 'SSH automation', 'SSH', 'Key/password', 'Pure-Python SSH2'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['venv', 'Dep. isolation', 'N/A', 'N/A', 'One per project'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['pip', 'Package install', 'HTTPS to PyPI', 'Token (priv idx)', 'Pin versions'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('Physical: automation/jump host running scripts - target APIs/SSH endpoints over network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('venv           = isolated Python environment with its own interpreter + package set'))
    lines.append(txt_row('pip            = Python package installer; reads requirements.txt or pyproject.toml'))
    lines.append(txt_row('certifi        = Python package bundling Mozilla CA certs used as a trust fallback'))
    lines.append(txt_row('SSLCertVerif.  = error raised when a server cert chain is not in the trust store'))
    lines.append(txt_row('requests       = most common Python HTTP client library for REST automation'))
    lines.append(txt_row('paramiko       = pure-Python SSHv2 library used for remote command execution'))
    lines.append(txt_row('Timeout        = max wait for a connect/read; unset defaults can hang indefinitely'))
    lines.append(txt_row('update-ca-trust= RHEL command to add a CA cert to the OS-wide trust store'))
    lines.append(txt_row('site-packages  = directory where pip installs packages for an interpreter/venv'))
    lines.append(txt_row('JSONDecodeError= raised when a response body is not valid JSON (often an HTML error page)'))
    lines.append(txt_row('Distributed Seg. Proc. = backup-specific DSP; unrelated term seen in some integration logs'))
    lines.append(txt_row('Idempotency    = property where re-running a script produces the same end state safely'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ki-terraform',
    'docs/automation/terraform/troubleshooting/known-issues.md',
    'Terraform / OpenTofu known issues — state locking, providers, Terraform Enterprise',
)
def ki_terraform():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Terraform / OpenTofu'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Infrastructure-as-code: declarative state-driven provisioning via providers')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: HTTPS to provider APIs · HTTPS to remote state backend (S3/TFE)')))
    lines.append(R(bMid(IV_L, IV_R, 'Management: terraform CLI / Terraform Enterprise (TFE) UI')))
    lines.append(R(bMid(IV_L, IV_R, 'plan -> diff against state -> apply -> provider API calls -> state updated')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Layer'), bMid(B2_L, B2_R, 'Component'), bMid(B3_L, B3_R, 'Notes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'State'), bMid(B2_L, B2_R, 'State file + lock'), bMid(B3_L, B3_R, 'S3/TFE/Consul backend'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Providers'), bMid(B2_L, B2_R, 'AWS/Azure/vSphere etc.'), bMid(B3_L, B3_R, 'Plugin binaries'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Execution'), bMid(B2_L, B2_R, 'CLI / TFE agent'), bMid(B3_L, B3_R, 'Local or remote runs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Modules'), bMid(B2_L, B2_R, 'Registry / Git source'), bMid(B3_L, B3_R, 'Reusable IaC units'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Workspace'), bMid(B2_L, B2_R, 'TFE workspace'), bMid(B3_L, B3_R, 'Per-environment state'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Component', 'Purpose', 'Protocol', 'Auth', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['State backend', 'Stores tfstate', 'HTTPS', 'IAM/Token', 'Lock vs. races'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Provider plugin', 'API translation', 'Provider-specific', 'Cloud creds', 'Versioned, cached'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['TFE agent', 'Remote execution', 'HTTPS to TFE', 'Agent token', 'On-prem access'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Module registry', 'Shared IaC modules', 'HTTPS/Git', 'Token (priv reg)', 'Public + private'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('Physical: CLI/agent host running terraform - state backend - target cloud/on-prem APIs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('State file     = JSON record mapping resources to real infrastructure IDs'))
    lines.append(txt_row('State lock     = prevents two concurrent applies from corrupting the same state'))
    lines.append(txt_row('Provider       = plugin translating HCL resources into API calls for a platform'))
    lines.append(txt_row('Plan           = dry-run diff between desired config and current state'))
    lines.append(txt_row('Apply          = executes the plan, calling provider APIs to reach desired state'))
    lines.append(txt_row('Drift          = real infrastructure diverges from what state file records'))
    lines.append(txt_row('Module         = reusable bundle of resources with input variables and outputs'))
    lines.append(txt_row('TFE            = Terraform Enterprise; self-hosted remote run/state platform'))
    lines.append(txt_row('Workspace      = isolated state + variable set, typically one per environment'))
    lines.append(txt_row('Agent pool     = group of self-hosted runners executing TFE runs in private networks'))
    lines.append(txt_row('Parallelism    = max concurrent resource operations per apply (default 10)'))
    lines.append(txt_row('force-unlock   = manually clears a stuck state lock after confirming no other run'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
