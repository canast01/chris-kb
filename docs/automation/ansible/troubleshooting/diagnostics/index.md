# Ansible — Diagnostics

> Part of the [Ansible Troubleshooting](../) reference.

---

## Ansible Diagnostic Workflow

```mermaid
graph LR
    issue["Issue Reported\nor Failure Detected"]
    listTasks["--list-tasks\nWhat tasks will run?"]
    listHosts["--list-hosts\nWhich hosts are targeted?"]
    syntaxCheck["--syntax-check\nAny YAML errors?"]
    checkMode["--check --diff\nDry run: what would change?"]
    verboseRun["-vvv\nFull connection\n& task detail"]
    retryFailed["--limit @site.retry\nRetry failed hosts only"]
    debugTask["ansible.builtin.debug\nvar: my_variable"]
    resolved["Issue Identified\n& Resolved"]

    issue --> listTasks
    issue --> listHosts
    listTasks --> syntaxCheck
    listHosts --> syntaxCheck
    syntaxCheck --> checkMode
    checkMode --> verboseRun
    verboseRun --> debugTask
    verboseRun --> retryFailed
    debugTask --> resolved
    retryFailed --> resolved
```

## Useful Diagnostic Commands

```bash
# List tasks without running them
ansible-playbook site.yml --list-tasks

# List hosts that would be targeted
ansible-playbook site.yml --list-hosts

# Syntax check only
ansible-playbook site.yml --syntax-check

# Step through tasks interactively
ansible-playbook site.yml --step

# Retry failed hosts from last run
ansible-playbook site.yml --limit @site.retry
```

Content to be added.
