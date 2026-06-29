---
tags:
  - servicenow
---
# System Decommission Procedure

<div class="kb-summary">
Safely removes a server, VM, or cloud instance from production — preventing orphaned monitoring alerts, failed backup jobs, billing waste, and security exposure from unmanaged systems.

*Applies to: ServiceNow*
</div>

## Decommission Workflow

```d2
direction: right

A: "Decommission\nrequest raised" {shape: rectangle}
B: "Owner approval\nand data sign-off" {shape: rectangle}
C: "Dependency check\nand notification" {shape: rectangle}
D: "Data retention\nreview" {shape: rectangle}
E: "Remove from\nmonitoring + backup" {shape: rectangle}
F: "Revoke access\nand credentials" {shape: rectangle}
G: "Shut down\nand archive" {shape: rectangle}
H: "Reclaim resources\nor delete VM" {shape: rectangle}
I: "CMDB and\ndocumentation update" {shape: rectangle}

A -> B
B -> C
C -> D
D -> E
E -> F
F -> G
G -> H
H -> I
```

| Data Category | Decision | Signed Off |
|---|---|---|
| Application data | Archive / Delete | ☐ |
| Log files | Archive / Delete | ☐ |
| Database data | Archive / Migrate | ☐ |
| SSL certificates | Revoke | ☐ |
| SSH keys | Rotate on dependents | ☐ |

## 4. Remove from Monitoring

```bash
# Prometheus — remove from scrape targets
# Edit prometheus/targets/linux_hosts.yml — delete host entry

# Verify no active alerts for this host
curl -s "http://prometheus:9090/api/v1/alerts" | \
  python3 -c "import sys,json; [print(a) for a in json.load(sys.stdin)['data']['alerts'] if '<hostname>' in str(a)]"

# Zabbix — disable host via API
curl -s -X POST http://zabbix.example.com/api_jsonrpc.php \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"host.update","params":{"hostid":"<id>","status":1},"auth":"<token>","id":1}'
```


```text title="Expected output"
[
  {
    "labels": {
      "alertname": "HighCPUUsage",
      "instance": "web-prod-04:9100",
      "severity": "warning"
    },
    "state": "firing",
    "value": "1"
  },
  {
    "labels": {
      "alertname": "DiskSpaceWarning",
      "instance": "web-prod-04:9100",
      "severity": "critical"
    },
    "state": "firing",
    "value": "1"
  }
]
{"jsonrpc":"2.0","result":{"hostids":["10084"]},"id":1}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to prometheus:9090: Connection refused`** — Verify Prometheus is running with `docker ps` or `systemctl status prometheus` and check the correct hostname/port in your environment.
    **`"error":{"code":-32602,"message":"Invalid params.","data":"No permissions to referred object or it does not exist."}`** — Confirm the `<id>` (hostid) is correct by querying `host.get` method first, and verify the auth token has admin privileges.
## 5. Remove from Backup

```bash
# Veeam — remove from backup job
$job = Get-VBRJob -Name "Production VMs"
$vm = Get-VBRJobObject -Job $job | Where-Object Name -eq "<hostname>"
Remove-VBRJobObject -Job $job -Objects $vm

# Delete backup data (only after retention period confirmed)
# Veeam UI: Home → Backups → Disk → <hostname> → Delete from Disk

# Commvault — retire client
# CommCell Console: Client Computers → <hostname> → Retire Client
```


```text title="Expected output"
Get-VBRJob -Name "Production VMs" | Select-Object Name, ID, JobType

Name              ID                                   JobType
----              --                                   -------
Production VMs    xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx Backup

Get-VBRJobObject -Job $job | Where-Object Name -eq "web-prod-01"

Name          ObjectType VirtualMachine
----          ---------- --------------
web-prod-01   VM         web-prod-01

Remove-VBRJobObject -Job $job -Objects $vm
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Get-VBRJob : The term 'Get-VBRJob' is not recognized as the name of a cmdlet, function, script file, or operable program.`** — Load the Veeam PowerShell snapin with `Add-PSSnapin VeeamPSSnapin` before running these commands.
    **`Remove-VBRJobObject : Cannot remove object. Job must contain at least one object.`** — Verify the VM object exists in the job using `Get-VBRJobObject -Job $job | Format-Table Name` before attempting removal.
## 6. Revoke Access and Credentials

```bash
# Remove SSH authorized keys
ssh root@<hostname> "rm -f /home/ansible/.ssh/authorized_keys"

# CyberArk — remove managed account
# CyberArk UI: Accounts → search <hostname> → Delete

# Venafi — revoke SSL certificate
# Venafi TLS Protect: Certificates → <hostname> → Revoke and Delete

# Active Directory — disable computer account (disable first, delete after 30 days)
Disable-ADComputer -Identity "<HOSTNAME>" -Confirm:$false

# Remove DNS records
nsupdate <<EOF
server dns.example.com
update delete <hostname>.example.com A
update delete <reverse-ip>.in-addr.arpa. PTR
send
EOF

# Verify removal
nslookup <hostname>.example.com
```


```text title="Expected output"
Connection to 192.168.45.12 closed.
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
> server dns.example.com
> update delete web-prod-01.example.com A
> update delete 45.168.192.in-addr.arpa. PTR
> send
(no output — DNS update sent)

Server:		dns.example.com
Address:	192.168.1.53#53

** server can't find web-prod-01.example.com: NXDOMAIN
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Verify the root account has SSH key access to the target hostname and the key is loaded in your SSH agent.
    **`Update failed: NOTAUTH`** — Ensure your nsupdate command includes proper TSIG authentication (key-file parameter) or that the DNS server allows unsigned updates from your source IP.
    **`Disable-ADComputer : Cannot find an object with identity "<HOSTNAME>" under: "DC=example,DC=com".`** — Verify the exact hostname spelling matches the AD computer object name and confirm you are connected to the correct Active Directory domain.
## 7. Shutdown and Delete

### Virtual Machine

```powershell
!!! danger "Permanently deletes VM and all disk files — no recovery"
    `Remove-VM -DeletePermanently` deletes the VM configuration and all VMDKs from the datastore immediately. Ensure the decommission checklist is complete: data backed up, application decommissioned, CMDB updated, and approval obtained in ServiceNow before running.

# VMware — power off and delete
Stop-VM -VM "<hostname>" -Confirm:$false
Remove-VM -VM "<hostname>" -DeletePermanently -Confirm:$false

# Verify datastore space reclaimed
Get-Datastore -Name "Datastore-01" | Select-Object Name, FreeSpaceGB
```

### Physical Server

```bash
shutdown -h now
# DRAC: racadm serveraction powerdown
# iLO:  ilorest set PowerState=Off

# After physical removal:
# → Coordinate rack removal with data centre team
# → Complete hardware disposal form (WEEE compliance)
# → Update asset management with disposal method
```

### Cloud Instance

```bash
# AWS
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
aws ec2 release-address --allocation-id eipalloc-12345678

# Azure
az vm delete --resource-group prod-rg --name <hostname> --yes
az disk delete --resource-group prod-rg --name <hostname>-osDisk --yes

# GCP
gcloud compute instances delete <hostname> --zone=europe-west1-b
```


```text title="Expected output"
# AWS
An error occurred (InvalidInstanceID.NotFound) when calling the TerminateInstances operation: The instance ID 'i-1234567890abcdef0' does not exist
(no output — command completes silently)

# Azure
Command group 'vm delete' is deprecated and will be removed in a future release. Use 'az vm delete' from 'azure-cli-core' instead.
Are you sure you want to perform this operation? (y/N): y
- Running ..
Finished operation: vm delete
(no output — command completes silently)

# GCP
ERROR: (gcloud.compute.instances.delete) Could not fetch resource:
 - The resource 'projects/my-project/zones/europe-west1-b/instances/<hostname>' was not found
```

!!! warning "Common errors"
    **`An error occurred (InvalidInstanceID.NotFound) when calling the TerminateInstances operation: The instance ID 'i-1234567890abcdef0' does not exist`** — Verify the instance ID is correct and still running with `aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"`.
    **`ERROR: (gcloud.compute.instances.delete) Could not fetch resource: The resource 'projects/my-project/zones/europe-west1-b/instances/<hostname>' was not found`** — Confirm the hostname and zone match the actual instance with `gcloud compute instances list --zones=europe-west1-b`.
    **`ResourceNotFoundError: The Resource 'Microsoft.Compute/disks/<hostname>-osDisk' under resource group 'prod-rg' was not found`** — Ensure the disk name and resource group are correct by listing disks with `az disk list --resource-group prod-rg`.
## 8. CMDB and Ansible Cleanup

```bash
# Ansible — remove from inventory
git rm -r inventory/production/host_vars/<hostname>.example.com/
# Remove host entry from hosts.yml
git commit -m "Decommission <hostname> — CHG-XXXX"
git push

# CMDB entry: Status → Retired, Decommission date → YYYY-MM-DD
```


```text title="Expected output"
rm 'inventory/production/host_vars/db-prod-03.example.com/'
[main 7a2f4c9] Decommission db-prod-03 — CHG-0047821
 1 file changed, 47 deletions(-)
 delete mode 100644 inventory/production/host_vars/db-prod-03.example.com/ansible-vault.yml
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using 5 objects.
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 1.24 KiB | 1.24 MiB/s, done.
Total 5 (delta 3), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (3/3), done.
To git.company.internal:infrastructure/ansible-inventory.git
   4f8e1a2..7a2f4c9  main -> main
```

!!! warning "Common errors"
    **`fatal: pathspec 'inventory/production/host_vars/<hostname>.example.com/' did not match any files`** — Replace `<hostname>` with the actual hostname (e.g., `db-prod-03`) before running the command.
    **`error: pathspec 'inventory/production/host_vars/db-prod-03.example.com/' did not match any files`** — Verify the directory exists and the path is correct; check for typos or confirm the host_vars structure matches your inventory layout.
    **`[main (root-commit) ...] fatal: your current branch 'main' does not have any commits yet`** — Ensure you are in the correct git repository directory and that the branch has been initialized with at least one commit.
## Decommission Checklist

| Step | Done |
|---|---|
| Owner sign-off obtained | ☐ |
| Change ticket approved | ☐ |
| All dependents notified | ☐ |
| Data retention review complete | ☐ |
| Archive transferred (if required) | ☐ |
| Removed from monitoring | ☐ |
| Removed from backup jobs | ☐ |
| SSH keys removed | ☐ |
| PAM accounts removed | ☐ |
| SSL certificates revoked | ☐ |
| AD computer account disabled | ☐ |
| DNS records removed | ☐ |
| Powered off | ☐ |
| VM deleted / hardware reclaimed | ☐ |
| CMDB status set to Retired | ☐ |
| Ansible inventory updated | ☐ |
| Change ticket closed | ☐ |
