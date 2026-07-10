# Site Map

<div class="kb-summary">
Full KB site index: links to all infrastructure, resilience, security, automation, and cloud sections. Use Ctrl+F to locate any product or topic quickly.
</div>

```d2
direction: down

infrastructure: "Infrastructure" {shape: rectangle}
resilience_recovery: "Resilience & Recovery" {shape: rectangle}
security_compliance: "Security & Compliance" {shape: rectangle}
automation_tooling: "Automation & Tooling" {shape: rectangle}

infrastructure -> resilience_recovery: uses
resilience_recovery -> security_compliance: uses
security_compliance -> automation_tooling: uses
```

## Infrastructure

| Section | Sub-sections |
|---|---|
| [Virtualization](virtualization/index.md) | [VMware](virtualization/vmware/index.md) · [OpenShift](virtualization/openshift/index.md) · [VxRail](virtualization/vmware/products/vxrail/index.md) · [Operations](virtualization/vmware/operations/index.md) · [Reference](virtualization/vmware/reference/index.md) |
| [Storage](storage/index.md) | [Dell](storage/products/dell/index.md) · [Pure Storage](storage/products/pure/index.md) · [NetApp](storage/products/netapp/index.md) · [Ceph](storage/products/ceph/index.md) · [Storage Design](storage/storage-design/index.md) · [Runbooks](storage/runbooks/index.md) |
| [SAN](san/index.md) | [Cisco MDS](san/cisco/index.md) · [Brocade](san/brocade/index.md) |
| [Compute](compute/index.md) | [Windows Server](compute/windows-server/index.md) · [Linux](compute/linux/index.md) · [Local AI & GPU](compute/local-ai/index.md) · [High CPU](compute/linux/troubleshooting/high-cpu/index.md) |
| [Certifications](certifications/index.md) | [SAN](certifications/san/index.md) · [Storage](certifications/storage/index.md) · [VMware](certifications/vmware/index.md) · [AWS](certifications/aws/index.md) · [Azure](certifications/azure/index.md) · [Cloud AI](certifications/ai/index.md) |
| [Cloud](cloud/index.md) | [AWS](cloud/aws/index.md) · [Azure](cloud/azure/index.md) · [Cloud AI](cloud/ai/index.md) |
| [Networking](networking/index.md) | [Switching & Routing](networking/switching-routing/index.md) · [Network Services](networking/services/index.md) · [Network Security](networking/security/index.md) · [External Connectivity](networking/external-connectivity/index.md) · [Network Design](networking/network-design/index.md) · [Troubleshooting](networking/troubleshooting/index.md) · [Protocols](networking/protocols/index.md) |

### VMware Products

| Product | Sub-sections |
|---|---|
| [vCenter](virtualization/vmware/products/vcenter/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [ESXi](virtualization/vmware/products/esxi/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [vSAN](virtualization/vmware/products/vsan/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [NSX](virtualization/vmware/products/nsx/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [VMware Cloud Foundation](virtualization/vmware/products/vmware-cloud-foundation/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [VxRail (VMware)](virtualization/vmware/products/vxrail/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Aria Operations](virtualization/vmware/products/aria-operations/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Aria Operations for Logs](virtualization/vmware/products/aria-operations-for-logs/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Aria Operations for Networks](virtualization/vmware/products/aria-operations-for-networks/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Aria Automation](virtualization/vmware/products/aria-automation/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Aria Suite Lifecycle](virtualization/vmware/products/aria-suite-lifecycle/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Horizon](virtualization/vmware/products/horizon/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [SRM](virtualization/vmware/products/srm/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [vSphere Replication](virtualization/vmware/products/vsphere-replication/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Tanzu](virtualization/vmware/products/tanzu/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [PowerCLI](virtualization/vmware/products/powercli/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [VMware Topics](virtualization/vmware/topics/index.md) | Learning Path · Scenarios |
| [VMware Internals](virtualization/vmware/internals/index.md) | Cluster Services · Networking · Permissions · Resource Management · Security · Storage |

### Dell Storage Products

| Product | Sub-sections |
|---|---|
| [PowerMax](storage/products/dell/powermax/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [PowerScale](storage/products/dell/powerscale/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [PowerStore](storage/products/dell/powerstore/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Unity XT](storage/products/dell/unity/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [VPLEX](storage/products/dell/vplex/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Data Domain](storage/products/dell/data-domain/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [ECS](storage/products/dell/ecs/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [PowerPath](storage/products/dell/powerpath/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [RecoverPoint](storage/products/dell/recoverpoint/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [SRDF/A](storage/products/dell/srdf-a/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [SRDF/S](storage/products/dell/srdf-s/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Dell AIOps](storage/products/dell/dell-aiops/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Apex STaaS](storage/products/dell/apex-storage-as-a-service/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [CloudIQ](storage/products/dell/cloudiq/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [CoD](storage/products/dell/cod/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [FoD](storage/products/dell/fod/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Secure Connect Gateway](storage/products/dell/secure-connect-gateway/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |

### NetApp & Pure Storage Products

| Product | Sub-sections |
|---|---|
| [ONTAP](storage/products/netapp/ontap/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [SnapMirror](storage/products/netapp/snapmirror/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [SnapCenter](storage/products/netapp/snapcenter/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Keystone](storage/products/netapp/keystone/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [InsightIQ](storage/products/netapp/insightiq/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Superna Eyeglass](storage/products/netapp/superna-eyeglass/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [FlashArray](storage/products/pure/flasharray/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [FlashBlade](storage/products/pure/flashblade/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Evergreen](storage/products/pure/evergreen/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Evergreen One](storage/products/pure/evergreen-one/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |
| [Pure1](storage/products/pure/pure1/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting |

### Compute Sub-sections

| Section | Sub-sections |
|---|---|
| [Windows Server](compute/windows-server/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting · [Active Directory](compute/windows-server/active-directory/index.md) · [SQL Server](compute/windows-server/sql-server/index.md) |
| [Linux](compute/linux/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting · [High CPU](compute/linux/troubleshooting/high-cpu/index.md) · [MySQL/MariaDB](compute/linux/mysql/index.md) · [PostgreSQL](compute/linux/postgresql/index.md) · [Directory Integration](compute/linux/directory-integration/index.md) |
| [Local AI & GPU](compute/local-ai/index.md) | [Ollama](compute/local-ai/ollama/index.md) · [GPU Workloads](compute/local-ai/gpu/index.md) |

### Cloud Sub-sections

| Section | Sub-sections |
|---|---|
| [AWS](cloud/aws/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting · Identity · Networking · Compute · Storage · Monitoring · Backup · Cost · Governance · CLI Reference · [Amazon EVS](cloud/aws/evs/index.md) |
| [Azure](cloud/azure/index.md) | Architecture · Deploy · Operations · Security · Troubleshooting · Identity · Networking · Compute · Storage · Monitoring · Backup/DR · Cost · Governance · CLI Reference |
| [Cloud AI](cloud/ai/index.md) | [AWS Bedrock](cloud/ai/aws-bedrock/index.md) · [Azure OpenAI](cloud/ai/azure-openai/index.md) · [OpenAI API](cloud/ai/openai/index.md) |

## Resilience & Recovery

| Section | Sub-sections |
|---|---|
| [Backup & DR](backup/index.md) | [Veeam](backup/products/veeam/index.md) · [Commvault](backup/products/commvault/index.md) · [NetBackup](backup/products/netbackup/index.md) · [DR Operations](backup/dr-operations/index.md) · [DR Design](backup/dr-operations/dr-design/index.md) · [Runbooks](backup/dr-operations/runbooks/index.md) · [Recovery Testing](backup/dr-operations/recovery-testing/index.md) · [IRE](backup/dr-operations/ire/index.md) · [Backup Validation](backup/dr-operations/backup-validation/index.md) · [Health Checks](backup/dr-operations/health-checks/index.md) · [Failure Testing](backup/dr-operations/failure-testing/index.md) · [Reliability Engineering](backup/dr-operations/reliability-engineering/index.md) · [Service Availability](backup/dr-operations/service-availability/index.md) · [SLOs](backup/dr-operations/service-level-objectives/index.md) · [Troubleshooting](backup/dr-operations/troubleshooting/index.md) |

## Security & Compliance

| Section | Sub-sections |
|---|---|
| [Security](security/index.md) | [CyberArk](security/products/cyberark/index.md) · [Venafi](security/products/venafi/index.md) · [Certificates](security/certificates/index.md) · [Certificates — Deploy](security/certificates/deploy/index.md) · [MFA](security/mfa/index.md) · [LDAP Integration](security/ldap-integration/index.md) · [SAML Configuration](security/saml-configuration/index.md) · [Access Review](security/access-review/index.md) · [Compliance Standards](security/compliance-standards/index.md) · [Vulnerability Management](security/vulnerability-management/index.md) · [Security Monitoring](security/security-monitoring/index.md) · [Security Audit](security/security-audit/index.md) · [Patch Compliance](security/patch-compliance/index.md) · [Incident Handling](security/incident-handling/index.md) · [Data Protection](security/data-protection/index.md) |

## Automation & Tooling

| Section | Sub-sections |
|---|---|
| [Automation](automation/index.md) | [Ansible](automation/ansible/index.md) · [PowerShell](automation/powershell/index.md) · [Python](automation/python/index.md) · [Terraform](automation/terraform/index.md) · [GitHub Actions](automation/github-actions/index.md) |
| [ITSM](itsm/index.md) | [ServiceNow](itsm/servicenow/index.md) · [Jira](itsm/jira/index.md) · [Confluence](itsm/confluence/index.md) · [Git](itsm/git/index.md) |
