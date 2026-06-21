#!/usr/bin/env python3
"""Generate FAQ stubs for all products with operations/ directories."""

import os
import xml.etree.ElementTree as ET

BASE = "/Users/chrisanastasiadis/chris-kb/docs"
ASSETS = "/Users/chrisanastasiadis/chris-kb/docs/assets"

# (path_from_docs, tag, product_name, q&a content dict)
PRODUCTS = [
    # automation
    ("automation/ansible/operations", "ansible", "Ansible", {
        "version_check": ("What version of Ansible is recommended for enterprise deployments?",
            "Ansible 2.15+ (the current stable branch) is recommended. Avoid 2.9.x for new deployments; it lacks many modern collection features. Run `ansible --version` to check."),
        "version_cmd": "ansible --version",
        "default_setting": ("What is the default inventory format and when should it be changed?",
            "INI format is the default. Switch to YAML inventory when you need groups-of-groups, host vars inline, or dynamic inventory merging — YAML is easier to read at scale."),
        "enable_feature": ("How do I enable fact caching to speed up large playbooks?",
            "Set `fact_caching = jsonfile` and `fact_caching_connection = /tmp/ansible_facts` in `ansible.cfg`. Facts are cached per host for `fact_caching_timeout` seconds (default 86400)."),
        "rolling_upgrade": ("How do I perform a rolling upgrade without downtime?",
            "Use `serial: 1` (or a percentage like `serial: 20%`) in your play definition. Combined with `max_fail_percentage: 0`, this ensures Ansible aborts on the first host failure before continuing."),
        "add_resource": ("What is the correct procedure to add a new managed host?",
            "Add the hostname to inventory, ensure SSH key is distributed (`ssh-copy-id`), then run `ansible hostname -m ping` to verify connectivity before including it in playbook runs."),
        "warning": ("Ansible shows 'DEPRECATION WARNING: Distribution Ubuntu 20.04 on host X should use /usr/bin/python3'. What does it mean?",
            "The `ansible_python_interpreter` is not set explicitly. Add `ansible_python_interpreter=/usr/bin/python3` to host_vars or inventory group_vars to suppress and ensure correct interpreter."),
        "perf": ("Performance is slow on large inventories — where do I start?",
            "Check `forks` in `ansible.cfg` (default 5, raise to 20-50). Enable pipelining (`pipelining = True`). Enable fact caching. Use `--limit` to scope runs. Profile with `PROFILE_TASKS` callback."),
        "backup_freq": ("How often should I back up Ansible inventory and playbooks?",
            "Store everything in Git. Commit after every change. For AWX/Tower, export job templates and credentials via `awx export` weekly and store in version control."),
        "restore": ("Can I restore a single role without a full repository restore?",
            "Yes — use `git checkout <commit> -- roles/rolename/` to restore a specific role from history without touching other files."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("automation/github-actions/operations", "github-actions", "GitHub Actions", {
        "version_check": ("What runner version is in use and how do I check it?",
            "For GitHub-hosted runners, the version is managed by GitHub. For self-hosted runners, run `./actions-runner/config.sh --version` or check the runner's `_diag/` logs."),
        "version_cmd": "cat /usr/local/share/runner/version",
        "default_setting": ("What is the default workflow trigger and when should it be changed?",
            "`on: push` is most common. Use `on: workflow_dispatch` for manual runs, `on: schedule` for cron jobs, and `on: pull_request` for CI gating. Combine triggers as needed."),
        "enable_feature": ("How do I enable dependency caching to speed up workflows?",
            "Use the `actions/cache` action with a key based on the lockfile hash. For npm: `key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}`."),
        "rolling_upgrade": ("How do I deploy to multiple environments in sequence without downtime?",
            "Use `needs:` to chain jobs sequentially. Use `environment:` with required reviewers for production gates. Use matrix strategy with `max-parallel: 1` for staged rollouts."),
        "add_resource": ("What is the correct procedure to add a new self-hosted runner?",
            "Go to Settings → Actions → Runners → New self-hosted runner. Follow the install steps. Add appropriate labels. Ensure the runner service starts on boot (`./svc.sh install && ./svc.sh start`)."),
        "warning": ("A workflow shows 'Resource not accessible by integration'. What does it mean?",
            "The `GITHUB_TOKEN` lacks permissions for the requested API. Add explicit `permissions:` block to the workflow (e.g., `pull-requests: write`) or grant the token broader scope in repository settings."),
        "perf": ("Workflow queuing time increased — where do I start?",
            "Check runner availability under Settings → Actions → Runners. Confirm self-hosted runners are online. Review concurrent job limits. Consider adding more runner capacity or using GitHub-hosted runners."),
        "backup_freq": ("How often should I back up workflow definitions?",
            "Workflows live in `.github/workflows/` and are version-controlled with the repo. Ensure secrets are documented in a secrets manager (e.g., Vault) since they cannot be read back from GitHub."),
        "restore": ("Can I restore a deleted workflow run's logs?",
            "No — once a run is deleted or expired (default 90 days), logs are gone. Download artifacts and logs during the retention window using the GitHub API or `gh run download`."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("automation/powershell/operations", "powershell", "PowerShell", {
        "version_check": ("What version of PowerShell is recommended for enterprise use?",
            "PowerShell 7.4 LTS is the current recommendation. Windows PowerShell 5.1 is still required for some Windows-specific modules (e.g., Active Directory, Exchange). Run `$PSVersionTable` to check."),
        "version_cmd": "$PSVersionTable.PSVersion",
        "default_setting": ("What is the default execution policy and when should it be changed?",
            "`Restricted` on Windows prevents any scripts from running. Set `RemoteSigned` for enterprise use: `Set-ExecutionPolicy RemoteSigned -Scope LocalMachine`. Never set `Unrestricted` in production."),
        "enable_feature": ("How do I enable PowerShell remoting for remote management?",
            "Run `Enable-PSRemoting -Force` on the target. Ensure WinRM service is running. For non-domain environments, add the host to TrustedHosts: `Set-Item WSMan:\\localhost\\Client\\TrustedHosts -Value 'hostname'`."),
        "rolling_upgrade": ("How do I upgrade PowerShell across many hosts without disruption?",
            "Deploy via SCCM/Intune or DSC. Test on a pilot group first. PowerShell 7 installs side-by-side with 5.1 — no conflict. Use `-Scope AllUsers` for system-wide install."),
        "add_resource": ("What is the correct procedure to add a new PowerShell module to all hosts?",
            "Publish to an internal PSRepository (`Register-PSRepository`), then deploy via DSC or a scheduled task running `Install-Module -Name ModuleName -Repository InternalRepo -Force`."),
        "warning": ("Script shows 'WARNING: The names of some imported commands... include unapproved verbs'. What does it mean?",
            "A module exports functions that don't follow Verb-Noun naming (e.g., `Load-Config` instead of `Import-Config`). It's cosmetic; use `-DisableNameChecking` on `Import-Module` to suppress it."),
        "perf": ("Script runs slowly on remote hosts — where do I start?",
            "Check if implicit remoting is serializing objects unnecessarily. Use `Invoke-Command` with `ThrottleLimit` tuning. Enable JEA for constrained endpoints. Profile with `Measure-Command`."),
        "backup_freq": ("How often should I back up PowerShell scripts and modules?",
            "Store all scripts in Git. For DSC configurations, version-control the `.ps1` and compiled `.mof` files. Module versions should be pinned in a `requirements.psd1`."),
        "restore": ("Can I restore a deleted function from a module without full repo restore?",
            "Yes — `git log -p -- path/to/module.psm1` shows deleted function history. Use `git show <hash>:path/to/module.psm1` to recover a specific version."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("automation/python/operations", "python", "Python", {
        "version_check": ("What Python version is recommended for new infrastructure tooling?",
            "Python 3.11 or 3.12 LTS. Avoid 3.8 (EOL Oct 2024). Check with `python3 --version` or `python3 -c 'import sys; print(sys.version)'`."),
        "version_cmd": "python3 --version",
        "default_setting": ("What is the recommended virtual environment approach?",
            "`venv` (stdlib) for simple projects. `poetry` or `pdm` for dependency management with lockfiles. Avoid `conda` in production infrastructure tooling unless data science libraries require it."),
        "enable_feature": ("How do I enable structured logging in a Python automation script?",
            "Use the `logging` stdlib with `logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)`. For JSON logs, use `python-json-logger`."),
        "rolling_upgrade": ("How do I upgrade a Python automation tool across all hosts without downtime?",
            "Use a blue/green deployment: install new version in a new venv, test, then update the symlink. For cron-driven tools, deploy outside the cron window."),
        "add_resource": ("What is the correct procedure to add a new Python dependency?",
            "Add to `pyproject.toml` or `requirements.in`, regenerate the lockfile (`pip-compile`), test in a fresh venv, then deploy. Never `pip install` directly on production without a lockfile update."),
        "warning": ("Script shows 'DeprecationWarning: datetime.datetime.utcnow()'. What does it mean?",
            "Python 3.12 deprecated `utcnow()`. Replace with `datetime.now(timezone.utc)` which returns a timezone-aware object and is the correct approach going forward."),
        "perf": ("Script is slow processing large data sets — where do I start?",
            "Profile with `cProfile` or `py-spy`. Check for unnecessary loops over large lists (use generators). Consider `multiprocessing.Pool` for CPU-bound work. For I/O-bound, use `asyncio`."),
        "backup_freq": ("How often should I back up Python scripts and configuration?",
            "All code in Git with pinned lockfiles (`requirements.txt` or `poetry.lock`). Configuration in a secrets manager. Commit lockfile changes alongside dependency updates."),
        "restore": ("Can I restore a deleted function without a full repo restore?",
            "Yes — `git log --all -S 'def function_name'` finds the commit where it existed. Use `git show <hash>:path/file.py` to recover it."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("automation/terraform/operations", "terraform", "Terraform", {
        "version_check": ("What version of Terraform is recommended for new deployments?",
            "Terraform 1.7+ (OpenTofu 1.7+ if using the OSS fork). Pin the version in `.terraform-version` or `required_version` in `terraform.tf`. Check with `terraform version`."),
        "version_cmd": "terraform version",
        "default_setting": ("What is the default state backend and when should it change?",
            "Local state (`terraform.tfstate`) is the default but unsuitable for teams. Use remote state immediately: S3+DynamoDB for AWS, Azure Blob for Azure, or Terraform Cloud. Never commit `.tfstate` to Git."),
        "enable_feature": ("How do I enable state locking to prevent concurrent runs?",
            "State locking is automatic with S3+DynamoDB backend (set `dynamodb_table` in the backend config). For Terraform Cloud, locking is built-in. Local state has no locking."),
        "rolling_upgrade": ("How do I upgrade Terraform provider versions without disruption?",
            "Update `required_providers` version constraint, run `terraform init -upgrade`, then `terraform plan` to review changes. Test in dev first. Use `~>` constraints (e.g., `~> 5.0`) to allow patch updates."),
        "add_resource": ("What is the correct procedure to import an existing resource into Terraform state?",
            "Run `terraform import <resource_type>.<name> <provider_id>`. Verify with `terraform plan` — it should show no changes if the config matches. Document the import in a comment."),
        "warning": ("Plan shows 'Warning: Deprecated attribute'. What does it mean?",
            "A provider attribute has been renamed or removed in a newer version. Update the resource block to use the new attribute name. Check the provider changelog for migration guidance."),
        "perf": ("Large plans take too long — where do I start?",
            "Use `-target` to scope applies to specific resources during debugging. Split large monolithic state into smaller workspaces. Use `terraform plan -parallelism=20` (default 10) for faster refreshes."),
        "backup_freq": ("How often should I back up Terraform state?",
            "Remote backends (S3, Azure Blob) support versioning — enable it. For Terraform Cloud, history is kept automatically. Never rely on local state in production."),
        "restore": ("Can I restore a single resource in state without a full restore?",
            "Yes — use `terraform state rm <resource>` to remove a drifted resource, then `terraform import` to re-import the current real-world state. Alternatively, restore a previous state version from S3 versioning."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    # backup
    ("backup/commvault/operations", "commvault", "Commvault", {
        "version_check": ("What Commvault version is recommended for new deployments?",
            "Commvault 11 SP32+ (Feature Release) for new installations. Check the CommServe version under CommCell Console → Help → About or run `qlogin` and check build info."),
        "version_cmd": "qlogin -cs <hostname> -u admin",
        "default_setting": ("What is the default deduplication setting and when should it change?",
            "DDB deduplication is enabled by default for disk libraries. Disable it only for already-compressed data (e.g., encrypted backups, video) where dedup ratio is below 1.1x."),
        "enable_feature": ("How do I enable Commvault Air Gap Protect for immutable backups?",
            "Configure a Cloud Library pointing to an immutable object store (S3 Object Lock or Azure Immutable Blob). Set retention locks in the Storage Policy copy. Contact Commvault support for Air Gap Protect licensing."),
        "rolling_upgrade": ("How do I upgrade Commvault across MediaAgents without disrupting jobs?",
            "Upgrade the CommServe first, then MediaAgents one at a time. Drain running jobs before upgrading each MA. Use the Commvault Update Manager (push upgrades) via CommCell Console → Software → Install/Update Software."),
        "add_resource": ("What is the correct procedure to add a new MediaAgent?",
            "Install the Commvault package on the new server, register it to the CommServe, then configure disk/tape libraries. Verify connectivity with `qping -cs <commserve>` from the new MA."),
        "warning": ("Job shows 'Media Mount Timeout'. What does it mean?",
            "The MediaAgent cannot mount the required media within the timeout period. Check tape library door, drive availability, and scratch pool. For disk, verify the library path is accessible."),
        "perf": ("Backup throughput degraded after adding new clients — where do I start?",
            "Check MA resource utilisation (CPU, disk I/O). Review streams per Storage Policy. Verify network bandwidth between clients and MA. Check DDB store fragmentation — run DDB verification."),
        "backup_freq": ("How often should I back up the CommServe database?",
            "Daily automated DR backups are configured by default. Verify under CommCell Console → CommServe → Disaster Recovery Backup. Store copies off-site. Test restore quarterly."),
        "restore": ("Can I restore a single file without a full job restore?",
            "Yes — use the Browse and Restore wizard in CommCell Console or the Web Console. Select the client, subclient, and point-in-time, then browse to the specific file or folder."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("backup/netbackup/operations", "netbackup", "Veritas NetBackup", {
        "version_check": ("What NetBackup version is recommended for new deployments?",
            "NetBackup 10.3+ for new deployments (supports containerised media servers and REST API v4). Check with `bpgetconfig -g <master> | grep VERSION` or in the Admin Console under Help → About."),
        "version_cmd": "bpgetconfig -g localhost | grep VERSION",
        "default_setting": ("What is the default policy schedule type and when should it change?",
            "Full + Differential Incremental is the default. Switch to Cumulative Incremental when recovery time matters more than storage (fewer tapes/disks to restore). Use `Accelerator` for VMware/NDMP."),
        "enable_feature": ("How do I enable NetBackup Instant Recovery for fast VM restores?",
            "Configure a AdvancedDisk or snapshot-capable storage unit. Enable `Instant Recovery` in the policy. The VM is made available directly from the backup image while data is migrated in the background."),
        "rolling_upgrade": ("How do I upgrade NetBackup master and media servers without disrupting jobs?",
            "Upgrade the master server first. Then upgrade media servers one at a time — drain running jobs first. Clients can be upgraded last; older clients work with newer master up to N-2 versions."),
        "add_resource": ("What is the correct procedure to add a new media server?",
            "Install NetBackup on the new server, then run `bpsetconfig` on the master to add it as a media server. Verify with `bpclntcmd -self` from the new host. Add storage units pointing to the new server."),
        "warning": ("Job fails with 'Status 96: unable to allocate new media for backup'. What does it mean?",
            "The scratch pool is empty. Add new tapes or disk to scratch pool, or check for expired media that hasn't been recycled. Run `vmquery -blist` to see available media."),
        "perf": ("Backup window is being exceeded — where do I start?",
            "Check Media Server utilisation. Increase multiplexing (MPX) on storage units. Add media servers. Review policy schedules — consolidate small clients into fewer larger jobs. Use Accelerator for VMware."),
        "backup_freq": ("How often should I back up the NetBackup catalog?",
            "The catalog auto-backs up after every session. Configure off-host catalog backup (Catalog policy type) to a separate media server. Verify last successful catalog backup daily."),
        "restore": ("Can I restore a single file without restoring the full backup image?",
            "Yes — use `bprestore` with the `-f` flag for specific files, or use the BAR (Backup, Archive, Restore) GUI. For VMware, use Instant Recovery and mount the backup as a datastore."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("backup/veeam/operations", "veeam", "Veeam Backup & Replication", {
        "version_check": ("What Veeam version is recommended for new deployments?",
            "Veeam v12.1+ is the current recommendation. Check under Main Menu → Help → About. Keep the VBR server updated — older agents and proxies continue to work with newer VBR servers."),
        "version_cmd": "Get-VBRVersion  # in Veeam PowerShell console",
        "default_setting": ("What is the difference between SOBR and a simple repository, and when to use each?",
            "Scale-Out Backup Repository (SOBR) spans multiple extents and supports capacity tier offload to object storage. Use SOBR for large environments. Simple repositories suit small setups or dedicated extents within a SOBR."),
        "enable_feature": ("How do I enable immutability on a Linux hardened repository?",
            "During repository configuration, select 'Make recent backups immutable for X days'. The Linux host must run as a non-root single-use account. SSH key auth is required; password auth is blocked for hardened repos."),
        "rolling_upgrade": ("How do I perform a rolling upgrade of Veeam proxies without disrupting jobs?",
            "Upgrade VBR server first. Then upgrade proxies via VBR Console → Backup Infrastructure → right-click proxy → Upgrade. VBR will drain jobs from the proxy before upgrading. Upgrade one proxy at a time."),
        "add_resource": ("What is the correct procedure to add a new backup proxy?",
            "In VBR Console, go to Backup Infrastructure → Backup Proxies → Add VMware Backup Proxy. Provide the server credentials. Set transport mode (Direct SAN, HotAdd, or NBD). Assign to backup jobs."),
        "warning": ("Job shows 'Warning: Backup file is located on the same datastore as the processed VM'. What does it mean?",
            "The target repository is on the same datastore as source VMs. This reduces resilience and can cause storage contention. Move the repository to a separate storage device."),
        "perf": ("Synthetic full backup takes much longer than expected — where do I start?",
            "Check repository disk I/O (synthetic full reads all increments). Consider switching to Active Full if repository IOPS are a bottleneck. Review proxy transport mode — Direct SAN is fastest for synthetic operations."),
        "backup_freq": ("How often should I run SureBackup verification?",
            "Weekly for critical VMs, monthly for non-critical. SureBackup uses an isolated virtual lab — it does not affect production. Results are emailed and logged in VBR reports."),
        "restore": ("Can I restore a single file from a VM backup without restoring the full VM?",
            "Yes — use Instant File-Level Recovery (FLR). In VBR Console, right-click the restore point → Restore Guest Files. Supports Windows, Linux (via helper appliance), and application-aware extracts."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    # cloud
    ("cloud/aws/evs/operations", "aws-evs", "AWS Elastic VMware Service (EVS)", {
        "version_check": ("How do I check which vSphere version is running on my EVS cluster?",
            "In the AWS Console, navigate to EVS → Clusters → select the cluster → Details tab. The vSphere and ESXi versions are shown. You can also run `vim-cmd hostsvc/hostsummary` from an ESXi SSH session."),
        "version_cmd": "vim-cmd hostsvc/hostsummary | grep version",
        "default_setting": ("What is the default SDDC networking model for EVS and when should it change?",
            "EVS uses VMware NSX for overlay networking. The default uses GENEVE encapsulation (requires MTU 1600+). Change the uplink profile MTU if your physical network cannot support jumbo frames."),
        "enable_feature": ("How do I enable stretched clusters across two AWS Availability Zones in EVS?",
            "EVS stretched clusters are available in supported regions. Configure a witness host in a third AZ via the AWS Console. Stretched cluster requires Enterprise Plus licensing and NSX Advanced Edge."),
        "rolling_upgrade": ("How do I upgrade the vSphere components in EVS without downtime?",
            "AWS manages the underlying hardware. vSphere lifecycle upgrades follow the standard VMware vLCM process via the embedded vCenter. Use Maintenance Mode per host; migrate VMs before patching."),
        "add_resource": ("What is the correct procedure to add a new host to an EVS cluster?",
            "In the AWS Console, go to EVS → Clusters → Add Hosts. Select the instance type and count. AWS provisions the hardware and joins it to the cluster. The host appears in vCenter within 30 minutes."),
        "warning": ("vCenter shows 'Host not responding' for an EVS host. What does it mean?",
            "Check the host health in the AWS Console. EVS hosts may be temporarily unreachable during AWS infrastructure maintenance. If persistent, use the AWS Console to reboot the host from the EC2 host management page."),
        "perf": ("VM performance degraded in EVS — where do I start?",
            "Check vCenter performance charts for CPU ready, memory balloon, and storage latency. Review NSX flow logs for network saturation. Check EBS volume performance for the vSAN datastore if applicable."),
        "backup_freq": ("How often should I back up EVS vCenter configuration?",
            "Enable file-based backup in VCSA (Administration → Backup) on a daily schedule. EVS vCenter is a standard VCSA — the same backup procedures apply. Store backups in an S3 bucket."),
        "restore": ("Can I restore a single VM from an EVS backup without restoring the entire vCenter?",
            "Yes — restore via your backup solution (Veeam, AWS Backup for VMware). vCenter itself can be restored from VCSA file-based backup independently of VM workloads."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("cloud/aws/operations", "aws", "AWS", {
        "version_check": ("How do I check which AWS CLI version I am using?",
            "Run `aws --version`. AWS CLI v2 is recommended; v1 is deprecated. Install v2 via the official installer: `curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o awscliv2.zip`."),
        "version_cmd": "aws --version",
        "default_setting": ("What is the default AWS region and how do I change it?",
            "No default is set unless configured. Set with `aws configure set region eu-west-1` or export `AWS_DEFAULT_REGION=eu-west-1`. Always specify region explicitly in scripts to avoid accidental cross-region operations."),
        "enable_feature": ("How do I enable AWS CloudTrail for audit logging?",
            "In the AWS Console, go to CloudTrail → Create Trail. Enable for all regions, log to an S3 bucket with server-side encryption. Enable CloudWatch Logs integration for alerting on suspicious API calls."),
        "rolling_upgrade": ("How do I update EC2 instances in an Auto Scaling Group without downtime?",
            "Use a rolling update: set `UpdatePolicy` in CloudFormation or use Instance Refresh in the ASG console. Configure `MinHealthyPercentage` (e.g., 80%) to maintain capacity during the refresh."),
        "add_resource": ("What is the correct procedure to add a new VPC?",
            "Use the VPC Wizard or IaC (Terraform/CDK). Plan CIDR carefully — avoid overlapping with on-premises or other VPCs you may need to peer. Enable DNS resolution and DNS hostnames. Tag consistently."),
        "warning": ("CloudWatch shows 'ServiceLimitExceeded'. What does it mean?",
            "You have hit a service quota (formerly known as limit). Go to Service Quotas in the console, find the relevant quota, and submit an increase request. Some quotas increase automatically with account age."),
        "perf": ("Application latency increased — where do I start?",
            "Check CloudWatch metrics for the affected service. Review X-Ray traces if instrumented. Check EC2 CPU credit balance (T-class). Review RDS slow query log. Check NAT Gateway bandwidth limits."),
        "backup_freq": ("How often should I back up AWS resources?",
            "Use AWS Backup with daily policies for EC2, RDS, EFS, and DynamoDB. Enable S3 versioning for critical buckets. Test restores quarterly via AWS Backup restore jobs."),
        "restore": ("Can I restore a single RDS table without a full database restore?",
            "Not natively. Restore the RDS snapshot to a temporary instance, export the table using `mysqldump` or `pg_dump`, then import into the production instance. Aurora supports point-in-time restore to a new cluster."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("cloud/azure/operations", "azure", "Microsoft Azure", {
        "version_check": ("How do I check which Azure CLI version I am using?",
            "Run `az --version`. Update with `az upgrade`. The Azure PowerShell module version can be checked with `Get-Module Az -ListAvailable`."),
        "version_cmd": "az --version",
        "default_setting": ("What is the default Azure subscription context and how do I change it?",
            "The default subscription is set during `az login`. Change with `az account set --subscription '<subscription-id>'`. Verify with `az account show`. Use service principals for automation."),
        "enable_feature": ("How do I enable Azure Defender for Servers?",
            "In the Azure Portal, go to Microsoft Defender for Cloud → Environment Settings → select the subscription → enable Defender for Servers Plan 2. This enables vulnerability assessment and JIT VM access."),
        "rolling_upgrade": ("How do I update VMs in an Azure Scale Set without downtime?",
            "Use rolling upgrade policy on the VMSS (Manual, Automatic, or Rolling). For Rolling, set `maxBatchInstancePercent` and `pauseTimeBetweenBatches`. Trigger with `az vmss update-instances` or via ARM template."),
        "add_resource": ("What is the correct procedure to add a new Virtual Network?",
            "Create via Portal, Bicep, or Terraform. Plan address space carefully — Azure reserves 5 IPs per subnet. Enable VNet peering for cross-VNet connectivity. Use Private DNS Zones for private endpoint resolution."),
        "warning": ("Azure Monitor shows 'DTU limit reached' for SQL Database. What does it mean?",
            "The SQL Database tier's DTU cap is being hit consistently. Upgrade to a higher DTU tier or switch to vCore model for more granular scaling. Check `sys.dm_db_resource_stats` for historical usage."),
        "perf": ("Application latency increased in Azure — where do I start?",
            "Check Azure Monitor metrics and Application Insights if instrumented. Review Azure SQL Query Performance Insight. Check App Service Plan CPU/memory. Review ExpressRoute or VPN gateway metrics."),
        "backup_freq": ("How often should I back up Azure resources?",
            "Use Azure Backup for VMs (daily), SQL in VM, and Azure Files. Enable soft delete for Recovery Services Vault. Enable geo-redundant storage (GRS) for the vault. Test restores quarterly."),
        "restore": ("Can I restore a single file from an Azure VM backup without restoring the full VM?",
            "Yes — in Recovery Services Vault, select the restore point, choose 'File Recovery', mount the backup disk as an iSCSI target, and copy the specific files. The mount is available for 12 hours."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    # compute/linux sub-products
    ("compute/linux/mysql/operations", "mysql", "MySQL", {
        "version_check": ("What MySQL version is recommended for new deployments?",
            "MySQL 8.0 LTS or 8.4 LTS (Innovation release). Avoid 5.7 — EOL October 2023. Check with `mysql --version` or `SELECT VERSION();` from the MySQL prompt."),
        "version_cmd": "mysql --version",
        "default_setting": ("What is the default InnoDB buffer pool size and when should it change?",
            "Default is 128 MB — far too small for production. Set to 70-80% of available RAM: `innodb_buffer_pool_size = 12G` in `my.cnf`. Restart MySQL after changing this parameter."),
        "enable_feature": ("How do I enable MySQL binary logging for replication or point-in-time recovery?",
            "Add `log_bin = /var/log/mysql/mysql-bin.log` and `server_id = 1` to `my.cnf`. Restart MySQL. Verify with `SHOW VARIABLES LIKE 'log_bin';`. Required for replication and PITR."),
        "rolling_upgrade": ("How do I perform a MySQL minor version upgrade without downtime?",
            "For replicated setups: upgrade the replica first, promote it, then upgrade the old primary. Use `CHANGE MASTER TO` to re-establish replication. For standalone, schedule a maintenance window."),
        "add_resource": ("What is the correct procedure to add a new MySQL replica?",
            "Take a consistent dump with `mysqldump --single-transaction --master-data=2`, restore to new host, then run `CHANGE MASTER TO` with the binary log position. Verify with `SHOW SLAVE STATUS\\G`."),
        "warning": ("MySQL shows 'Too many connections'. What does it mean?",
            "Active connections hit `max_connections` limit (default 151). Increase: `SET GLOBAL max_connections = 500;`. Also check for connection leaks in the application — use connection pooling (ProxySQL or application-level)."),
        "perf": ("Query performance degraded — where do I start?",
            "Enable the slow query log (`slow_query_log = 1`, `long_query_time = 1`). Use `EXPLAIN` on slow queries. Check `SHOW ENGINE INNODB STATUS` for lock waits. Review index usage with `sys.schema_unused_indexes`."),
        "backup_freq": ("How often should I back up MySQL?",
            "Full dump weekly (`mysqldump` or `xtrabackup`), binary log backups every 15-30 minutes for PITR. Test restores monthly. For critical databases, use MySQL Enterprise Backup or Percona XtraBackup for hot backups."),
        "restore": ("Can I restore a single table without a full database restore?",
            "Yes — with `mysqldump`, restore the specific table: `mysql db_name < table_dump.sql`. With InnoDB transportable tablespaces (`DISCARD TABLESPACE` / `IMPORT TABLESPACE`) for large tables."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("compute/linux/operations", "linux", "Linux", {
        "version_check": ("How do I check the Linux distribution and kernel version?",
            "Run `cat /etc/os-release` for distro info and `uname -r` for kernel version. For RHEL/CentOS: `cat /etc/redhat-release`. For Ubuntu: `lsb_release -a`."),
        "version_cmd": "uname -r && cat /etc/os-release",
        "default_setting": ("What is the default SSH timeout and when should it be changed?",
            "`ClientAliveInterval 0` (no timeout) is the default in most distros. Set `ClientAliveInterval 300` and `ClientAliveCountMax 3` in `/etc/ssh/sshd_config` to disconnect idle sessions after 15 minutes."),
        "enable_feature": ("How do I enable SELinux enforcing mode on RHEL/CentOS?",
            "Check current mode: `getenforce`. To enable: edit `/etc/selinux/config`, set `SELINUX=enforcing`, and reboot. First boot with `permissive` to collect AVC denials before switching to `enforcing`."),
        "rolling_upgrade": ("How do I apply kernel updates across a fleet without downtime?",
            "Use live patching (RHEL: `kpatch`, Ubuntu: `livepatch`) for security patches without reboot. For full kernel upgrades, use rolling reboots — update and reboot one host at a time, verify before proceeding."),
        "add_resource": ("What is the correct procedure to add a new disk to a running Linux system?",
            "Attach the disk, then `lsblk` to identify it. Partition with `fdisk` or `parted`. Create filesystem: `mkfs.xfs /dev/sdb1`. Add to `/etc/fstab` with UUID (`blkid`). Mount: `mount -a`."),
        "warning": ("System logs show 'kernel: EXT4-fs error'. What does it mean?",
            "Filesystem corruption detected. Run `fsck /dev/sdX` from single-user mode or a rescue environment (unmount first). Check `dmesg` and `smartctl -a /dev/sdX` for underlying disk errors."),
        "perf": ("System load is high — where do I start?",
            "Run `top` or `htop` to identify the culprit process. Check I/O wait with `iostat -x 1`. Review memory with `free -h` and `vmstat`. Check for zombie processes. Review `/proc/<pid>/status` for a specific process."),
        "backup_freq": ("How often should I back up Linux system configuration?",
            "Critical config in `/etc` should be in version control (etckeeper or Ansible). Full system backups weekly via Veeam Agent, Commvault, or similar. Log rotation configured in `/etc/logrotate.d/`."),
        "restore": ("Can I restore a single configuration file without a full system restore?",
            "Yes — from Veeam Agent file-level recovery, or from your version-controlled `/etc` repo (`git checkout HEAD -- /etc/nginx/nginx.conf`). Always test changes in a non-production environment first."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("compute/linux/postgresql/operations", "postgresql", "PostgreSQL", {
        "version_check": ("What PostgreSQL version is recommended for new deployments?",
            "PostgreSQL 16 or 17 (latest stable). Avoid versions older than 14 (approaching EOL). Check with `psql --version` or `SELECT version();` from psql."),
        "version_cmd": "psql --version",
        "default_setting": ("What is the default `shared_buffers` size and when should it change?",
            "Default is 128 MB — too small for production. Set to 25% of system RAM: e.g., `shared_buffers = 4GB` in `postgresql.conf`. Also set `effective_cache_size` to 75% of RAM for the query planner."),
        "enable_feature": ("How do I enable logical replication in PostgreSQL?",
            "Set `wal_level = logical` in `postgresql.conf` and restart. Create a publication: `CREATE PUBLICATION mypub FOR TABLE orders;`. On the subscriber, create a subscription pointing to the publisher."),
        "rolling_upgrade": ("How do I upgrade PostgreSQL major versions without extended downtime?",
            "Use `pg_upgrade` for offline upgrade (fastest) or logical replication for near-zero downtime: set up a replica on the new version, replicate, then switch traffic. Test `pg_upgrade --check` first."),
        "add_resource": ("What is the correct procedure to add a streaming replica?",
            "Run `pg_basebackup -h primary -U replicator -D /data/pg16 -Fp -Xs -P`. Configure `recovery.conf` (PG12-) or `standby.signal` (PG12+). Add `primary_conninfo` in `postgresql.conf`. Verify with `pg_stat_replication`."),
        "warning": ("PostgreSQL logs show 'FATAL: sorry, too many clients already'. What does it mean?",
            "`max_connections` limit reached (default 100). Increase in `postgresql.conf` (requires restart). Better solution: use PgBouncer connection pooler in transaction mode to reduce actual backend connections."),
        "perf": ("Queries are slow after data load — where do I start?",
            "Run `ANALYZE` to update statistics. Check `pg_stat_statements` for slow queries. Use `EXPLAIN ANALYZE` on specific queries. Check for missing indexes with `pg_stat_user_indexes`. Review autovacuum settings."),
        "backup_freq": ("How often should I back up PostgreSQL?",
            "Continuous WAL archiving with `pg_basebackup` weekly base backups. Use `pgBackRest` or `Barman` for enterprise backup management. PITR recovery requires both base backup and WAL archive."),
        "restore": ("Can I restore a single table without a full cluster restore?",
            "Yes — `pg_dump -t tablename dbname > table.sql` for export; `psql dbname < table.sql` to restore. For PITR, restore to a separate instance and use `pg_dump` to extract the specific table."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    # compute/windows-server sub-products
    ("compute/windows-server/active-directory/operations", "active-directory", "Active Directory", {
        "version_check": ("How do I check the Active Directory functional level?",
            "Run `Get-ADDomain | Select DomainMode` and `Get-ADForest | Select ForestMode` in PowerShell. Alternatively, in ADUC, right-click the domain → Raise Domain Functional Level to view current level."),
        "version_cmd": "Get-ADDomain | Select DomainMode, PDCEmulator",
        "default_setting": ("What is the default password policy and when should it be changed?",
            "Default Domain Policy sets 7-character minimum, 42-day maximum age. Modern guidance (NIST 800-63B) recommends 12+ character minimum, no regular expiry, and breach detection instead. Use Fine-Grained Password Policies for service accounts."),
        "enable_feature": ("How do I enable AD Recycle Bin?",
            "`Enable-ADOptionalFeature 'Recycle Bin Feature' -Scope ForestOrConfigurationSet -Target (Get-ADForest).Name`. Requires Forest Functional Level 2008 R2+. Objects are recoverable for `msDS-deletedObjectLifetime` days (default 180)."),
        "rolling_upgrade": ("How do I add a new Windows Server 2022 DC and decommission an old one?",
            "Promote the new DC (`dcpromo` or `Install-ADDSDomainController`). Verify replication (`repadmin /replsummary`). Transfer FSMO roles if needed (`Move-ADDirectoryServerOperationMasterRole`). Then demote the old DC (`dcpromo /forceremoval` if needed)."),
        "add_resource": ("What is the correct procedure to add a new OU?",
            "Run `New-ADOrganizationalUnit -Name 'ServerOU' -Path 'DC=corp,DC=local' -ProtectedFromAccidentalDeletion $true`. Apply GPOs to the OU. Verify delegation is correct before moving objects in."),
        "warning": ("Event ID 5805 — 'The session setup from computer X failed'. What does it mean?",
            "The machine account password is out of sync between the computer and the DC. Reset with `Test-ComputerSecureChannel -Repair` from the affected computer (requires domain admin). Alternatively, disjoin and rejoin the domain."),
        "perf": ("AD authentication is slow — where do I start?",
            "Check DC replication status (`repadmin /showrepl`). Review LDAP response times with `nltest /dsgetdc:<domain> /force`. Check DC CPU/memory. Verify DNS resolution is working correctly for all clients."),
        "backup_freq": ("How often should I back up Active Directory?",
            "Daily Windows Server Backup or Veeam backup of all DCs. Ensure System State is included (contains SYSVOL and AD database). Protect at least one DC per site. Test AD restore quarterly using an isolated lab."),
        "restore": ("Can I restore a single deleted user without a full DC restore?",
            "Yes — use AD Recycle Bin: `Get-ADObject -Filter {DisplayName -eq 'John Smith'} -IncludeDeletedObjects | Restore-ADObject`. Without Recycle Bin, use an authoritative restore from backup (`ntdsutil`)."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("compute/windows-server/operations", "windows-server", "Windows Server", {
        "version_check": ("How do I check the Windows Server version and edition?",
            "Run `winver` for GUI, or `(Get-ComputerInfo).WindowsProductName` in PowerShell. For patch level: `(Get-HotFix | Sort InstalledOn)[-1]` shows the most recent update."),
        "version_cmd": "(Get-ComputerInfo).WindowsProductName",
        "default_setting": ("What is the default Windows Update configuration and when should it change?",
            "Default allows automatic updates. For servers, configure WSUS or SCCM/Intune to control update timing. Set maintenance windows to prevent unplanned reboots. Disable automatic restarts for servers in production."),
        "enable_feature": ("How do I enable Windows Defender Credential Guard?",
            "Enable via GPO: Computer Configuration → Administrative Templates → System → Device Guard → Turn On Virtualization Based Security. Requires UEFI, Secure Boot, and Hyper-V. Check with `msinfo32` → Virtualization-based security."),
        "rolling_upgrade": ("How do I apply patches across a Windows Server fleet without downtime?",
            "Use SCCM/WSUS deployment rings. Patch dev → test → prod with 1-week gaps. For clustered workloads, use Cluster-Aware Updating (CAU). Always test patches in a lower environment first."),
        "add_resource": ("What is the correct procedure to add a new data disk to Windows Server?",
            "Attach disk, then in Disk Management: right-click → Online → Initialize → New Simple Volume. For scripting: `Get-Disk | Where PartitionStyle -eq 'RAW' | Initialize-Disk -PartitionStyle GPT | New-Partition -AssignDriveLetter -UseMaximumSize | Format-Volume`."),
        "warning": ("System log shows Event ID 4226 'TCP/IP reached the security limit'. What does it mean?",
            "Half-open TCP connection limit reached (historical limit on older Windows). On modern Windows Server 2016+, this limit is removed. On older systems, check for port exhaustion or SYN flood conditions."),
        "perf": ("Windows Server performance degraded — where do I start?",
            "Open Resource Monitor (`resmon`) or Performance Monitor (`perfmon`). Check CPU, memory, disk, and network. Use `Get-Process | Sort CPU -Descending | Select -First 10` for top CPU consumers. Review event logs for errors."),
        "backup_freq": ("How often should I back up Windows Server?",
            "Daily via Windows Server Backup, Veeam, or Commvault. Include System State for DCs. Test restore monthly. For application servers, follow the application's own backup requirements in addition to OS-level backup."),
        "restore": ("Can I restore a single registry key without a full server restore?",
            "Yes — export the registry key before changes: `reg export HKLM\\SOFTWARE\\MyApp backup.reg`. Restore with `reg import backup.reg`. For full registry restore, boot to WinRE and use System Restore or restore from backup."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("compute/windows-server/sql-server/operations", "sql-server", "Microsoft SQL Server", {
        "version_check": ("What SQL Server version is recommended for new deployments?",
            "SQL Server 2022 (16.x) for new deployments. Check: `SELECT @@VERSION;`. SQL Server 2016 (13.x) is the minimum for modern features; 2012 is EOL. Always apply latest CU (Cumulative Update)."),
        "version_cmd": "SELECT @@VERSION;",
        "default_setting": ("What is the default max memory setting and when should it change?",
            "Default is unlimited — SQL Server will consume all available RAM. Always set `max server memory`: reserve at minimum 4 GB for the OS. Use: `sp_configure 'max server memory (MB)', 12288; RECONFIGURE;`"),
        "enable_feature": ("How do I enable Always On Availability Groups?",
            "Enable the feature in SQL Server Configuration Manager → SQL Server Services → right-click SQL Server → Properties → Always On tab. Create an AG via SSMS wizard or T-SQL. Requires Windows Server Failover Cluster."),
        "rolling_upgrade": ("How do I patch SQL Server without downtime in an AG environment?",
            "Patch secondary replicas first. Failover the AG to a patched secondary. Patch the old primary (now secondary). Use `ALTER AVAILABILITY GROUP [AG] FAILOVER` for manual failover. Verify synchronisation before each step."),
        "add_resource": ("What is the correct procedure to add a new database to an Availability Group?",
            "Ensure full recovery model: `ALTER DATABASE mydb SET RECOVERY FULL`. Take a full backup. In SSMS, right-click the AG → Add Database. Use 'Automatic seeding' or restore to secondary manually with `NORECOVERY`."),
        "warning": ("SQL Agent job fails with 'The job failed. The owner ... does not have server access'. What does it mean?",
            "The job owner's login is disabled or deleted. Change ownership: `EXEC msdb.dbo.sp_update_job @job_name='JobName', @owner_login_name='sa';`. Use a service account as the job owner rather than a personal account."),
        "perf": ("Query performance degraded after a SQL Server upgrade — where do I start?",
            "Check for plan regression: enable Query Store and review forced plans. Run `sp_BlitzCache` (First Responder Kit) to identify top resource consumers. Check compatibility level — lower it if needed for a regression window."),
        "backup_freq": ("How often should I back up SQL Server databases?",
            "Full backup weekly, differential daily, transaction log every 15-30 minutes for PITR. Use Ola Hallengren's backup scripts or SQL Server Agent maintenance plans. Test restores monthly."),
        "restore": ("Can I restore a single table from a SQL Server backup without a full restore?",
            "Not natively. Restore the backup to a separate instance using `RESTORE DATABASE ... WITH NORECOVERY`, then extract the table with BCP or `SELECT INTO`. SQL Server 2022 supports contained availability groups for easier DR."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    # itsm
    ("itsm/confluence/operations", "confluence", "Confluence", {
        "version_check": ("What Confluence version is recommended?",
            "Confluence Data Center 8.x for self-hosted. Cloud is always current. Check version via Admin → System Information. Stay within 2 major versions of latest for security support."),
        "version_cmd": "Admin → System Information → Confluence version",
        "default_setting": ("What is the default attachment storage location and when should it change?",
            "Local filesystem by default. For Data Center, switch to shared NFS/object storage immediately — local storage does not support clustering. Configure in Admin → Attachments."),
        "enable_feature": ("How do I enable Confluence Analytics?",
            "Analytics is built into Confluence Cloud. For Data Center, install the Confluence Analytics (Beta) app from Marketplace. Requires Data Center license. Enable per-space under Space Settings."),
        "rolling_upgrade": ("How do I upgrade Confluence Data Center with minimal downtime?",
            "Put Confluence in read-only mode before upgrade. Back up the home directory and database. Run the installer. For clustered DC, stop all nodes, upgrade one, verify, then start remaining nodes. Rolling upgrades are not supported."),
        "add_resource": ("What is the correct procedure to create a new Space with consistent permissions?",
            "Create via Spaces → Create Space. Apply a Space Permission Template if configured. Add the Space to the relevant group permissions. Set the Space home page and description before announcing to users."),
        "warning": ("Confluence shows 'Your Confluence installation is approaching its user limit'. What does it mean?",
            "The licensed user count is near the cap. Audit inactive users (Admin → User Management → filter by last login) and deactivate dormant accounts. Or purchase additional user licenses from Atlassian."),
        "perf": ("Confluence pages load slowly — where do I start?",
            "Check the Confluence thread dump (Admin → Logging and Profiling → Thread dump). Review JVM heap usage. Check database slow query log. Disable unused plugins (Admin → Manage Apps → filter inactive). Index rebuild may help."),
        "backup_freq": ("How often should I back up Confluence?",
            "Database backup daily (outside backup window). Home directory backup daily (includes attachments). Built-in XML backup is for migration only — not suitable for production backup due to size and restore time."),
        "restore": ("Can I restore a single Space without a full Confluence restore?",
            "For Data Center, use the Space Export/Import feature (Space Settings → Export). This exports pages and attachments for that space. For a full point-in-time restore of a space, you need to restore to a separate instance and re-import."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("itsm/git/operations", "git", "Git", {
        "version_check": ("What Git version is recommended?",
            "Git 2.40+ for new installations. Check with `git --version`. Older versions lack security fixes and features like `git switch`/`git restore`. Update via OS package manager."),
        "version_cmd": "git --version",
        "default_setting": ("What is the default branch name and when should it be changed?",
            "Historically `master`, now `main` is the default in Git 2.28+. Set globally: `git config --global init.defaultBranch main`. Update existing repos with `git branch -m master main`."),
        "enable_feature": ("How do I enable GPG commit signing?",
            "`git config --global commit.gpgsign true` and `git config --global user.signingkey <key-id>`. Verify with `git log --show-signature`. GitHub/GitLab display 'Verified' badge on signed commits."),
        "rolling_upgrade": ("How do I update Git across all servers without disrupting CI pipelines?",
            "Update Git via OS package manager during a low-traffic window. Git is backward compatible — newer Git reads older repos without issue. Test with `git --version` and a basic `git status` after updating."),
        "add_resource": ("What is the correct procedure to add a new remote to an existing repository?",
            "`git remote add <name> <url>`. Verify with `git remote -v`. For mirrors: `git remote add mirror git@internal:repo.git` and push with `git push mirror --all --tags`."),
        "warning": ("Git shows 'warning: LF will be replaced by CRLF'. What does it mean?",
            "Line ending conversion is configured via `core.autocrlf`. On Windows, `autocrlf=true` converts LF to CRLF on checkout. Set `.gitattributes` to enforce consistent line endings across the team."),
        "perf": ("Git operations are slow on large repositories — where do I start?",
            "Enable partial clone (`git clone --filter=blob:none`). Use `git sparse-checkout` for large monorepos. Run `git gc --aggressive` to compact object store. Shallow clones (`--depth=1`) speed up CI pipelines."),
        "backup_freq": ("How often should I back up Git repositories?",
            "Mirror to a secondary Git server (Gitea, internal GitLab) with `git push --mirror`. For GitHub/GitLab SaaS, use the platform's built-in backup features or a third-party tool like Gitprotect."),
        "restore": ("Can I restore a deleted branch without a full repository restore?",
            "Yes — if the commits are still in the reflog: `git reflog | grep 'checkout: moving from branchname'`. Find the commit SHA and `git checkout -b branchname <sha>`. Reflog expires after 90 days by default."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("itsm/jira/operations", "jira", "Jira", {
        "version_check": ("What Jira version is recommended?",
            "Jira Data Center 9.x for self-hosted. Cloud is always current. Check via Administration → System → System Info. Maintain within 2 major versions for Atlassian support."),
        "version_cmd": "Administration → System → System Info",
        "default_setting": ("What is the default issue workflow and when should it change?",
            "Jira ships with a default workflow (To Do → In Progress → Done). Customise workflows per project type. Avoid modifying the default workflow directly — create project-specific workflows and apply via workflow schemes."),
        "enable_feature": ("How do I enable Jira Service Management for an IT helpdesk project?",
            "Go to Project Settings → Project Type → Service Management. Or create a new project using the IT Service Management template. Configure queues, SLAs, and customer portal in the JSM project settings."),
        "rolling_upgrade": ("How do I upgrade Jira Data Center with minimal downtime?",
            "Enable read-only mode before upgrade. Back up the database and Jira home. For clustered DC, stop all nodes, upgrade sequentially. Jira does not support rolling upgrades — all nodes must run the same version."),
        "add_resource": ("What is the correct procedure to create a new project with consistent settings?",
            "Use a project template that matches the desired workflow. Apply the correct Permission Scheme, Notification Scheme, and Issue Type Scheme before the team starts using the project. Audit schemes monthly."),
        "warning": ("Jira shows 'Index recovery in progress'. What does it mean?",
            "The Lucene search index is being rebuilt (common after crash or version upgrade). Jira is still usable but search may be incomplete. Check progress under Administration → System → Indexing."),
        "perf": ("Jira is slow — where do I start?",
            "Check the thread dump (Administration → Logging and Profiling → Thread Dump). Review database slow queries. Check JVM heap (Administration → System → Memory). Disable unused plugins. Review JQL query performance."),
        "backup_freq": ("How often should I back up Jira?",
            "Database daily backup. Jira home directory daily (includes attachments and plugins). Built-in XML backup is for migration only. Test restore quarterly to a staging environment."),
        "restore": ("Can I restore a single project without a full Jira restore?",
            "Not natively with standard restore. You need to restore to a separate Jira instance, then use project export/import or the Jira Cloud Migration Assistant to move just that project's data."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("itsm/servicenow/operations", "servicenow", "ServiceNow", {
        "version_check": ("How do I check which ServiceNow release is running?",
            "Navigate to System Diagnostics → Stats → Build Information, or check the browser URL for the instance version. Release names follow alphabetical convention (Xanadu, Yokohama, etc.). Check Xanadu = Nov 2024."),
        "version_cmd": "System Diagnostics → Stats → Build Information",
        "default_setting": ("What is the default incident assignment rule and when should it change?",
            "By default, incidents are unassigned unless auto-assignment rules are configured. Set up Assignment Rules (System Policy → Rules → Assignment) to route incidents based on category, CMDB CI, or other criteria."),
        "enable_feature": ("How do I enable ServiceNow ITSM with CMDB auto-discovery?",
            "Enable the Discovery plugin (com.snc.discovery). Configure MID Servers for network access. Set up Discovery Schedules to scan IP ranges. Map discovered CIs to CMDB classes via Discovery Patterns."),
        "rolling_upgrade": ("How do I manage a ServiceNow release upgrade?",
            "ServiceNow Cloud upgrades are managed by ServiceNow. Schedule via the Upgrade Centre. Test in sub-production (PDI) first. Review upgrade notes for skipped plugins. Complete upgrade tasks in the Upgrade Monitor post-upgrade."),
        "add_resource": ("What is the correct procedure to add a new CMDB CI class?",
            "Extend an existing CMDB table (e.g., `cmdb_ci_computer`) rather than creating from scratch. Add custom fields as dictionary extensions. Follow CSDM alignment for class placement. Test with Discovery before go-live."),
        "warning": ("ServiceNow shows 'Workflow version out of date'. What does it mean?",
            "A workflow is running against an older checked-out version. Publish the current version under Workflow → Workflow Editor → Publish. Existing running instances continue on the old version; new activations use the published version."),
        "perf": ("ServiceNow portal is slow for users — where do I start?",
            "Check the System Diagnostics → Instance Health page. Review slow transactions in System Logs → Transactions. Check Business Rules for non-conditional scripts running on large tables. Review table indexes."),
        "backup_freq": ("How often does ServiceNow back up data?",
            "ServiceNow SaaS instances are backed up daily by ServiceNow. You can export data via Data Export or use the Table API for custom extracts. Clone production to sub-production environments for additional safety."),
        "restore": ("Can I restore a single record that was accidentally deleted?",
            "If the Audit table captured the deletion, data can be reconstructed. Use the sys_audit table to retrieve field values at the time of deletion. ServiceNow does not have native single-record restore from backup."),
        "ts_link": "../../troubleshooting/index.md",
    }),
]

def make_svg(slug):
    """Generate 820x200px FAQ flow SVG."""
    boxes = ["Identify Question", "Find Answer", "Verify Context", "Apply Solution", "✓ Issue Resolved"]
    w, h = 820, 200
    box_w, box_h = 130, 60
    gap = 15
    total = len(boxes) * box_w + (len(boxes) - 1) * gap
    start_x = (w - total) // 2
    y_center = h // 2

    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width=str(w), height=str(h))
    defs = ET.SubElement(svg, "defs")
    grad = ET.SubElement(defs, "linearGradient", id="hdr", x1="0", y1="0", x2="1", y2="0")
    ET.SubElement(grad, "stop", offset="0%", style="stop-color:#1a2744")
    ET.SubElement(grad, "stop", offset="100%", style="stop-color:#2a3f6f")

    # background
    ET.SubElement(svg, "rect", width=str(w), height=str(h), fill="#f8f9fa")
    # header bar
    ET.SubElement(svg, "rect", width=str(w), height="32", fill="url(#hdr)")
    title = ET.SubElement(svg, "text", x=str(w // 2), y="21",
                           fill="white", **{"font-family": "sans-serif", "font-size": "13",
                                            "font-weight": "bold", "text-anchor": "middle"})
    title.text = "FAQ — Operations Guide"

    colors = ["#1a2744", "#1e3a5f", "#155e75", "#065f46", "#14532d"]
    for i, (label, color) in enumerate(zip(boxes, colors)):
        x = start_x + i * (box_w + gap)
        y = y_center - box_h // 2
        ET.SubElement(svg, "rect", x=str(x), y=str(y), width=str(box_w), height=str(box_h),
                       rx="6", fill=color)
        lines = label.split()
        mid = len(lines) // 2
        for j, word in enumerate(lines):
            dy = (j - mid) * 16 + (8 if len(lines) == 1 else 0)
            t = ET.SubElement(svg, "text",
                               x=str(x + box_w // 2), y=str(y_center + dy),
                               fill="white", **{"font-family": "sans-serif", "font-size": "11",
                                                "text-anchor": "middle"})
            t.text = word
        if i < len(boxes) - 1:
            ax = x + box_w + 2
            ay = y_center
            arr = ET.SubElement(svg, "polygon",
                                  points=f"{ax},{ay-5} {ax+gap-4},{ay} {ax},{ay+5}",
                                  fill="#94a3b8")

    return ET.tostring(svg, encoding="unicode")

def depth_prefix(path_from_docs):
    """Return relative path prefix based on directory depth."""
    parts = path_from_docs.rstrip("/").split("/")
    # parts includes the 'operations' segment
    depth = len(parts)
    return "../" * depth

def slug_from_path(path_from_docs):
    parts = path_from_docs.rstrip("/").split("/")
    return "-".join(parts) + "-faq"

created_files = []
created_svgs = []

for path_from_docs, tag, product_name, qa in PRODUCTS:
    full_dir = os.path.join(BASE, path_from_docs)
    faq_path = os.path.join(full_dir, "faq.md")
    if os.path.exists(faq_path):
        print(f"SKIP (exists): {faq_path}")
        continue

    slug = slug_from_path(path_from_docs)
    prefix = depth_prefix(path_from_docs)
    svg_rel = f"{prefix}assets/{slug}.svg"

    # Build FAQ content
    content = f"""---
tags:
  - {tag}
  - faq
  - operations
---
# {product_name} — Frequently Asked Questions

<div class="kb-summary">
Common questions about {product_name} operations, configuration, and troubleshooting. For step-by-step procedures, see the <a href="index.md">Operations</a> section.
</div>

![{product_name} FAQ]({svg_rel})

## General

**Q: {qa['version_check'][0]}**
A: {qa['version_check'][1]}

**Q: How do I check the current {product_name} version?**
A: `{qa['version_cmd']}`

## Configuration

**Q: {qa['default_setting'][0]}**
A: {qa['default_setting'][1]}

**Q: {qa['enable_feature'][0]}**
A: {qa['enable_feature'][1]}

## Operations

**Q: {qa['rolling_upgrade'][0]}**
A: {qa['rolling_upgrade'][1]}

**Q: {qa['add_resource'][0]}**
A: {qa['add_resource'][1]}

## Troubleshooting

**Q: {qa['warning'][0]}**
A: {qa['warning'][1]}

**Q: {qa['perf'][0]}**
A: {qa['perf'][1]}

## Backup and Recovery

**Q: {qa['backup_freq'][0]}**
A: {qa['backup_freq'][1]}

**Q: {qa['restore'][0]}**
A: {qa['restore'][1]}

## See Also

- [{product_name} Operations](index.md)
- [{product_name} Troubleshooting]({qa['ts_link']})
"""
    os.makedirs(full_dir, exist_ok=True)
    with open(faq_path, "w") as f:
        f.write(content)
    created_files.append(faq_path)

    # SVG
    svg_path = os.path.join(ASSETS, f"{slug}.svg")
    if not os.path.exists(svg_path):
        svg_content = make_svg(slug)
        # validate
        ET.fromstring(svg_content)
        with open(svg_path, "w") as f:
            f.write(svg_content)
        created_svgs.append(svg_path)

print(f"\nCreated {len(created_files)} FAQ files, {len(created_svgs)} SVGs (batch 1 of ~5)")
