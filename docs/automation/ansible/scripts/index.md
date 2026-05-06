# Scripts

> Part of the [Ansible](../) reference.

---

## Infrastructure Health Check Playbook

A general-purpose health-check playbook targeting Linux server and network device groups. Reports disk usage, load average, failed services, and reboot time per host, with block/rescue error handling and a delegated summary at the end.

~~~yaml
---
# infra-health-check.yml
# Usage: ansible-playbook infra-health-check.yml -i inventory/hosts.yml

- name: Linux Server Health Check
  hosts: linux_servers
  gather_facts: true
  become: true

  vars:
    disk_warn_pct: 85
    load_warn: 4

  tasks:
    - name: Check disk usage
      block:
        - name: Get disk usage facts
          command: df -h --output=source,pcent,target
          register: df_output
          changed_when: false

        - name: Parse and flag high disk usage
          set_fact:
            high_disk_mounts: >-
              {{
                df_output.stdout_lines[1:] |
                map('split') |
                selectattr(1, 'regex', '^([89][0-9]|100)%$') |
                list
              }}

        - name: Warn on high disk usage
          debug:
            msg: "WARNING: High disk usage on {{ inventory_hostname }}: {{ high_disk_mounts }}"
          when: high_disk_mounts | length > 0

      rescue:
        - name: Record disk check failure
          set_fact:
            disk_check_failed: true
          delegate_to: localhost

    - name: Check load average
      block:
        - name: Read load average
          command: cat /proc/loadavg
          register: load_raw
          changed_when: false

        - name: Parse 1-minute load average
          set_fact:
            load_1m: "{{ load_raw.stdout.split()[0] | float }}"

        - name: Warn on high load
          debug:
            msg: "WARNING: High load on {{ inventory_hostname }}: {{ load_1m }}"
          when: load_1m | float > load_warn

      rescue:
        - name: Record load check failure
          set_fact:
            load_check_failed: true
          delegate_to: localhost

    - name: Check for failed systemd services
      block:
        - name: List failed services
          command: systemctl list-units --state=failed --no-legend --no-pager
          register: failed_services
          changed_when: false
          failed_when: false

        - name: Report failed services
          debug:
            msg: "FAILED SERVICES on {{ inventory_hostname }}: {{ failed_services.stdout_lines }}"
          when: failed_services.stdout_lines | length > 0

      rescue:
        - name: Record service check failure
          set_fact:
            service_check_failed: true
          delegate_to: localhost

    - name: Get last reboot time
      command: who -b
      register: last_reboot
      changed_when: false
      failed_when: false

    - name: Aggregate host health to controller
      set_fact:
        host_health_summary:
          host: "{{ inventory_hostname }}"
          load_1m: "{{ load_1m | default('N/A') }}"
          high_disk: "{{ high_disk_mounts | default([]) | length }}"
          failed_services: "{{ failed_services.stdout_lines | default([]) | length }}"
          last_reboot: "{{ last_reboot.stdout | default('unknown') | trim }}"
      delegate_to: localhost
      delegate_facts: true

  post_tasks:
    - name: Print health summary for this host
      debug:
        msg:
          - "Host           : {{ inventory_hostname }}"
          - "Load (1m)      : {{ load_1m | default('N/A') }}"
          - "High disk mts  : {{ high_disk_mounts | default([]) | length }}"
          - "Failed services: {{ failed_services.stdout_lines | default([]) | length }}"
          - "Last reboot    : {{ last_reboot.stdout | default('unknown') | trim }}"


- name: Network Device Reachability Check
  hosts: network_devices
  gather_facts: false

  tasks:
    - name: Ping network devices from controller
      command: "ping -c 3 -W 2 {{ ansible_host }}"
      register: ping_result
      changed_when: false
      failed_when: false
      delegate_to: localhost

    - name: Report unreachable devices
      debug:
        msg: "UNREACHABLE: {{ inventory_hostname }} ({{ ansible_host }})"
      when: ping_result.rc != 0


- name: Health Report Aggregation
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Print overall summary header
      debug:
        msg: "=== Infrastructure Health Summary ==="

    - name: Print per-host summaries
      debug:
        msg: "{{ hostvars[item].host_health_summary | default({'host': item, 'status': 'no data'}) }}"
      loop: "{{ groups['linux_servers'] | default([]) }}"
~~~

---

## Rolling Update Playbook

Update a web application fleet one host at a time without downtime: drain from the load balancer, stop, update, start, health-check, and re-add. Stops immediately on first failure.

~~~yaml
---
# rolling-update.yml
# Usage: ansible-playbook rolling-update.yml -i inventory/hosts.yml
#        -e "app_package=myapp app_version=2.3.1 lb_api_url=http://lb.example.com/api lb_token=TOKEN"

- name: Rolling Application Update
  hosts: web_servers
  serial: 1
  max_fail_percentage: 0
  gather_facts: true

  vars:
    app_package:      "{{ app_package }}"
    app_version:      "{{ app_version }}"
    app_service:      "myapp"
    health_check_url: "http://{{ ansible_host }}:8080/health"
    health_check_retries: 10
    health_check_delay:   5
    lb_api_url:       "{{ lb_api_url }}"
    lb_token:         "{{ lb_token }}"
    drain_timeout:    30

  tasks:

    - name: Drain host from load balancer
      uri:
        url: "{{ lb_api_url }}/backends/{{ inventory_hostname }}/drain"
        method: POST
        headers:
          Authorization: "Bearer {{ lb_token }}"
          Content-Type: "application/json"
        body_format: json
        body:
          state: "drain"
        status_code: [200, 202]
      delegate_to: localhost
      register: drain_result

    - name: Wait for active connections to drop
      uri:
        url: "{{ lb_api_url }}/backends/{{ inventory_hostname }}/connections"
        method: GET
        headers:
          Authorization: "Bearer {{ lb_token }}"
        return_content: true
      register: conn_check
      until: (conn_check.json.active_connections | int) == 0
      retries: "{{ (drain_timeout / 5) | int }}"
      delay: 5
      delegate_to: localhost
      ignore_errors: true

    - name: Stop application service
      systemd:
        name: "{{ app_service }}"
        state: stopped
      become: true

    - name: Update application package
      package:
        name: "{{ app_package }}={{ app_version }}"
        state: present
      become: true
      register: package_update

    - name: Start application service
      systemd:
        name: "{{ app_service }}"
        state: started
        enabled: true
      become: true

    - name: Health check application endpoint
      uri:
        url: "{{ health_check_url }}"
        method: GET
        status_code: 200
        return_content: true
      register: health_check
      until: health_check.status == 200
      retries: "{{ health_check_retries }}"
      delay: "{{ health_check_delay }}"
      delegate_to: localhost

    - name: Re-add host to load balancer
      uri:
        url: "{{ lb_api_url }}/backends/{{ inventory_hostname }}/drain"
        method: POST
        headers:
          Authorization: "Bearer {{ lb_token }}"
          Content-Type: "application/json"
        body_format: json
        body:
          state: "active"
        status_code: [200, 202]
      delegate_to: localhost

    - name: Report update result for this host
      debug:
        msg: "{{ inventory_hostname }}: updated to {{ app_version }}, health OK, back in LB."
~~~

---

## Inventory Validation Playbook

Verify that every inventory host meets baseline configuration requirements: SSH access, Python, sudoers, required packages, hostname, NTP sync, and DNS resolution.

~~~yaml
---
# inventory-validate.yml
# Usage: ansible-playbook inventory-validate.yml -i inventory/hosts.yml

- name: Inventory Validation
  hosts: all
  gather_facts: true
  become: true

  vars:
    required_packages:
      - python3
      - curl
      - rsync
      - sudo
    ntp_service: "chronyd"   # or "ntp" depending on distro

  tasks:

    - name: Verify SSH connection
      ping:
      register: ssh_check

    - name: Verify Python is installed
      command: python3 --version
      register: python_check
      changed_when: false
      failed_when: false

    - name: Verify sudo access
      command: sudo -n true
      register: sudo_check
      changed_when: false
      failed_when: false

    - name: Check required packages
      package_facts:
        manager: auto

    - name: Flag missing packages
      set_fact:
        missing_packages: >-
          {{
            required_packages |
            reject('in', ansible_facts.packages.keys()) |
            list
          }}

    - name: Verify hostname matches inventory name
      set_fact:
        hostname_match: "{{ ansible_hostname == inventory_hostname.split('.')[0] }}"

    - name: Check NTP synchronisation
      command: "timedatectl show --property=NTPSynchronized --value"
      register: ntp_sync
      changed_when: false
      failed_when: false

    - name: Verify DNS resolution
      command: "getent hosts {{ inventory_hostname }}"
      register: dns_check
      changed_when: false
      failed_when: false
      delegate_to: localhost

    # Build per-host result
    - name: Compile validation results
      set_fact:
        validation_result:
          host:              "{{ inventory_hostname }}"
          ssh:               "{{ 'PASS' if ssh_check is defined else 'FAIL' }}"
          python:            "{{ 'PASS' if python_check.rc == 0 else 'FAIL' }}"
          sudo:              "{{ 'PASS' if sudo_check.rc == 0 else 'FAIL' }}"
          required_packages: "{{ 'PASS' if missing_packages | length == 0 else 'FAIL: missing ' + missing_packages | join(',') }}"
          hostname_match:    "{{ 'PASS' if hostname_match else 'FAIL (got ' + ansible_hostname + ')' }}"
          ntp_sync:          "{{ 'PASS' if ntp_sync.stdout == 'yes' else 'FAIL' }}"
          dns:               "{{ 'PASS' if dns_check.rc == 0 else 'FAIL' }}"

    - name: Print per-host validation table
      debug:
        msg:
          - "Host      : {{ validation_result.host }}"
          - "SSH       : {{ validation_result.ssh }}"
          - "Python    : {{ validation_result.python }}"
          - "Sudo      : {{ validation_result.sudo }}"
          - "Packages  : {{ validation_result.required_packages }}"
          - "Hostname  : {{ validation_result.hostname_match }}"
          - "NTP       : {{ validation_result.ntp_sync }}"
          - "DNS       : {{ validation_result.dns }}"

    - name: Persist results to controller
      set_fact:
        validation_result: "{{ validation_result }}"
      delegate_to: localhost
      delegate_facts: true


- name: Validation Summary
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Identify non-compliant hosts
      set_fact:
        non_compliant: >-
          {{
            groups['all'] |
            map('extract', hostvars) |
            selectattr('validation_result', 'defined') |
            selectattr('validation_result.ssh', 'ne', 'PASS') |
            map(attribute='validation_result.host') |
            list
          }}

    - name: Print non-compliant summary
      debug:
        msg: "Non-compliant hosts: {{ non_compliant }}"

    - name: Fail if any non-compliant hosts
      fail:
        msg: "Validation failed for: {{ non_compliant | join(', ') }}"
      when: non_compliant | length > 0
~~~

---

## Secret Rotation with Vault (Bash + Ansible)

Bash wrapper that generates a new database password, encrypts it into an Ansible Vault file, runs the playbook to push it to the database and app servers, and rolls back if the playbook fails.

~~~bash
#!/usr/bin/env bash
# rotate-db-secret.sh
# Usage: VAULT_PASSWORD_FILE=<path> DB_VARS_FILE=<path> ./rotate-db-secret.sh
#
# Requires: ansible, ansible-vault, openssl, python3

set -euo pipefail

VAULT_PASSWORD_FILE="${VAULT_PASSWORD_FILE:?VAULT_PASSWORD_FILE is required}"
DB_VARS_FILE="${DB_VARS_FILE:-vars/db_secrets.yml}"
PLAYBOOK="${PLAYBOOK:-playbooks/push-db-secret.yml}"
INVENTORY="${INVENTORY:-inventory/hosts.yml}"
BACKUP_FILE="/tmp/db_secrets_backup_$(date +%Y%m%d%H%M%S).yml"
LOGFILE="/var/log/secret-rotation-$(date +%Y%m%d-%H%M%S).log"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

log "=== Database Secret Rotation ==="
log "Vars file : ${DB_VARS_FILE}"
log "Playbook  : ${PLAYBOOK}"

# --- Step 1: Backup current vault file ---
log "Step 1: Backing up current vars file to ${BACKUP_FILE}..."
cp "${DB_VARS_FILE}" "${BACKUP_FILE}"

# --- Step 2: Generate new password ---
log "Step 2: Generating new database password..."
NEW_PASSWORD=$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-24)
log "New password generated (not logged)."

# --- Step 3: Encrypt new password with Ansible Vault ---
log "Step 3: Encrypting new password with Ansible Vault..."
ENCRYPTED_VALUE=$(ansible-vault encrypt_string \
    --vault-password-file "${VAULT_PASSWORD_FILE}" \
    --stdin-name "db_password" <<< "${NEW_PASSWORD}")

# Update the vars file: replace the db_password line with new encrypted value.
# The vars file is expected to contain a line starting with "db_password:"
python3 - <<EOF
import re, sys

with open('${DB_VARS_FILE}', 'r') as f:
    content = f.read()

# Remove old db_password block (multi-line vault value)
new_content = re.sub(
    r'^db_password:.*?(?=^\w|\Z)',
    '',
    content,
    flags=re.MULTILINE | re.DOTALL
)

# Append new encrypted value
new_content = new_content.rstrip('\n') + '\n' + '''${ENCRYPTED_VALUE}''' + '\n'

with open('${DB_VARS_FILE}', 'w') as f:
    f.write(new_content)

print("Vars file updated.")
EOF

log "Vars file updated with new encrypted password."

# --- Step 4: Run Ansible playbook to push new password ---
log "Step 4: Running Ansible playbook to push new password..."
if ansible-playbook \
    --vault-password-file "${VAULT_PASSWORD_FILE}" \
    -i "${INVENTORY}" \
    -e "db_password=${NEW_PASSWORD}" \
    "${PLAYBOOK}" 2>&1 | tee -a "${LOGFILE}"; then
    log "Playbook succeeded. Secret rotation complete."
    log "Backup of old vars: ${BACKUP_FILE}"
else
    # --- Step 5: Rollback on failure ---
    log "ERROR: Playbook failed. Rolling back vars file from backup..."
    cp "${BACKUP_FILE}" "${DB_VARS_FILE}"
    log "Rollback complete. Old vars file restored."
    log "MANUAL ACTION REQUIRED: The database password was NOT successfully rotated."
    log "  Review playbook errors above and investigate before retrying."
    exit 1
fi
~~~
