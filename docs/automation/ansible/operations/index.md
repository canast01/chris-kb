# Operations

> Part of the [Ansible](../) reference.

---

## Daily Checks

- [ ] Review scheduled playbook run results in AWX/Tower job history or cron logs
- [ ] Check AWX/Tower dashboard for job failures and review failure output
- [ ] Validate dynamic inventory sources are returning the expected host count
- [ ] Review Vault-encrypted variable files for secrets nearing expiry
- [ ] Confirm Galaxy roles and collections are current and not deprecated
- [ ] Verify control node SSH key access to all critical host groups
- [ ] Check for playbooks pinned to deprecated module names or legacy syntax
- [ ] Confirm Python version on target hosts meets minimum Ansible requirements

## Health Check

- [ ] Control node can reach all target hosts via SSH
- [ ] `ansible --version` reports expected Ansible core version
- [ ] Inventory returns the correct host count for all groups
- [ ] Vault password/file is accessible to the control node
- [ ] Galaxy collections are installed and at expected versions
- [ ] A `--check` run against a representative playbook completes without errors
- [ ] AWX/Tower API is reachable and job templates are visible
- [ ] Become/sudo access works on a representative target host

```bash
# Ansible version
ansible --version

# Ping all hosts in inventory
ansible all -m ping -i inventory/

# List hosts in a group
ansible <group> --list-hosts -i inventory/

# Syntax check a playbook
ansible-playbook site.yml --syntax-check -i inventory/

# Dry-run (check mode) against a group
ansible-playbook site.yml --check --limit <group> -i inventory/

# List installed collections
ansible-galaxy collection list
```

## Change Readiness

- [ ] Playbook tested in staging environment or validated with `--check` mode
- [ ] Inventory validated — `--list-hosts` confirms correct target scope
- [ ] Vault secrets are accessible (vault password file or prompt configured)
- [ ] `--limit` flag set to scope the run to the correct host group or pattern
- [ ] Rollback playbook or manual revert procedure documented
- [ ] `--tags` or `--skip-tags` configured if running a subset of tasks
- [ ] Syntax check passes: `ansible-playbook site.yml --syntax-check`

| Item | Status | Notes |
|---|---|---|
| Staging / check-mode run | | Pass / Fail |
| Inventory scope (`--limit`) | | Host group or pattern |
| Vault access confirmed | | Yes / No |
| Rollback procedure | | Link to runbook |
| Syntax check | | Pass / Fail |

## Incident Triage

- [ ] Re-run the playbook with `-v` (verbose) or `-vvv` (very verbose) to capture detailed output
- [ ] Test SSH connectivity to the failing target host manually
- [ ] Validate `become`/sudo access on the target host
- [ ] Check the inventory source — confirm the failing host is listed and reachable
- [ ] Confirm the correct Python interpreter is available on the target
- [ ] Review Ansible log file if logging is configured (`log_path` in ansible.cfg)
- [ ] Check if a Vault-encrypted variable file failed to decrypt
- [ ] Confirm no module or collection version mismatch between control node and requirements

| Question | Answer |
|---|---|
| Is the target host reachable via SSH? | `ssh -i <key> user@host` |
| Does become/sudo work? | `ansible <host> -m shell -a "id" --become` |
| Is the Vault password accessible? | Check vault password file/env var |
| Is the inventory returning the host? | `ansible <group> --list-hosts` |
| Is the correct Python available? | `ansible_python_interpreter` set? |

## Maintenance Window

1. Disable AWX/Tower scheduled jobs or comment out cron entries for the affected playbooks during the window.
2. Notify team of the maintenance window and the scope of playbook changes.
3. Take a snapshot or backup of configuration files on target hosts if the playbook makes destructive changes.
4. Run the playbook with `--check` immediately before the window to confirm expected task list.
5. Execute the playbook with `--limit` scoped to the target group; monitor output.
6. If a failure occurs mid-run, stop and execute the rollback playbook or manual revert.
7. Re-enable AWX/Tower scheduled jobs or cron entries after successful completion.
8. Confirm idempotency with a follow-up `--check` run.

## Post-Change Validation

- [ ] Re-run the playbook in `--check` mode — confirm zero tasks report changes (idempotent)
- [ ] Full re-run produces no unexpected changes on any host
- [ ] Target service or application is healthy and responding
- [ ] AWX/Tower scheduled jobs re-enabled and showing green on next run
- [ ] Ansible log or AWX job output shows no errors or warnings
- [ ] Inventory still returns the expected host count for all groups
- [ ] Vault-encrypted variables still decrypt successfully
