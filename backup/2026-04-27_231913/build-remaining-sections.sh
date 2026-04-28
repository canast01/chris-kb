#!/usr/bin/env bash

set -e

echo
echo "Running backup first..."
echo

if [ -f "./backup.sh" ]; then
  ./backup.sh
else
  echo "ERROR: backup.sh not found."
  exit 1
fi

echo
echo "Creating remaining section directories and pages..."
echo

mkdir -p docs/ai/{openai,azure-openai,aws-bedrock,local-ai-ollama,gpu-workloads}
mkdir -p docs/automation/{powershell,python,ansible,terraform,github-actions}
mkdir -p docs/disaster-recovery/{recoverpoint,srdf-s,srdf-a,srm,superna-eyeglass,rasr,isolated-recovery-environment-ire,netbackup}
mkdir -p docs/compute/{windows-server,linux}
mkdir -p docs/security/{active-directory,certificates,cyberark,venafi}
mkdir -p docs/monitoring/{aria-operations,cloudiq,pure1,dell-aiops,insightiq,nexus-dashboard}
mkdir -p docs/tools/{servicenow,jira,confluence,git}
mkdir -p docs/project-management/{change-management,incident-management,maintenance-windows,asset-inventory,health-checks}
mkdir -p docs/standards/{naming-conventions,build-standards,configuration-baselines,security-baselines,san-zoning-standard}
mkdir -p docs/protocols/{fibre-channel,iscsi,nfs,smb,dns,dhcp,ntp,snmp,ldap,tls}
mkdir -p docs/certifications/{aws,azure,vmware,storage,san,ai}

create_page() {
  path="$1"
  title="$2"
  cat > "$path/index.md" << PAGE
# $title
PAGE
}

create_page docs/ai/openai "OpenAI"
create_page docs/ai/azure-openai "Azure OpenAI"
create_page docs/ai/aws-bedrock "AWS Bedrock"
create_page docs/ai/local-ai-ollama "Local AI / Ollama"
create_page docs/ai/gpu-workloads "GPU Workloads"

create_page docs/automation/powershell "PowerShell"
create_page docs/automation/python "Python"
create_page docs/automation/ansible "Ansible"
create_page docs/automation/terraform "Terraform"
create_page docs/automation/github-actions "GitHub Actions"

create_page docs/disaster-recovery/recoverpoint "RecoverPoint"
create_page docs/disaster-recovery/srdf-s "SRDF/S"
create_page docs/disaster-recovery/srdf-a "SRDF/A"
create_page docs/disaster-recovery/srm "SRM"
create_page docs/disaster-recovery/superna-eyeglass "Superna Eyeglass"
create_page docs/disaster-recovery/rasr "RASR"
create_page docs/disaster-recovery/isolated-recovery-environment-ire "Isolated Recovery Environment / IRE"
create_page docs/disaster-recovery/netbackup "NetBackup"

create_page docs/compute/windows-server "Windows Server"
create_page docs/compute/linux "Linux"

create_page docs/security/active-directory "Active Directory"
create_page docs/security/certificates "Certificates"
create_page docs/security/cyberark "CyberArk"
create_page docs/security/venafi "Venafi"

create_page docs/monitoring/aria-operations "Aria Operations"
create_page docs/monitoring/cloudiq "CloudIQ"
create_page docs/monitoring/pure1 "Pure1"
create_page docs/monitoring/dell-aiops "Dell AIOps"
create_page docs/monitoring/insightiq "InsightIQ"
create_page docs/monitoring/nexus-dashboard "Nexus Dashboard"

create_page docs/tools/servicenow "ServiceNow"
create_page docs/tools/jira "Jira"
create_page docs/tools/confluence "Confluence"
create_page docs/tools/git "Git"

create_page docs/project-management/change-management "Change Management"
create_page docs/project-management/incident-management "Incident Management"
create_page docs/project-management/maintenance-windows "Maintenance Windows"
create_page docs/project-management/asset-inventory "Asset Inventory"
create_page docs/project-management/health-checks "Health Checks"

create_page docs/standards/naming-conventions "Naming Conventions"
create_page docs/standards/build-standards "Build Standards"
create_page docs/standards/configuration-baselines "Configuration Baselines"
create_page docs/standards/security-baselines "Security Baselines"
create_page docs/standards/san-zoning-standard "SAN Zoning Standard"

create_page docs/protocols/fibre-channel "Fibre Channel"
create_page docs/protocols/iscsi "iSCSI"
create_page docs/protocols/nfs "NFS"
create_page docs/protocols/smb "SMB"
create_page docs/protocols/dns "DNS"
create_page docs/protocols/dhcp "DHCP"
create_page docs/protocols/ntp "NTP"
create_page docs/protocols/snmp "SNMP"
create_page docs/protocols/ldap "LDAP"
create_page docs/protocols/tls "TLS"

create_page docs/certifications/aws "AWS"
create_page docs/certifications/azure "Azure"
create_page docs/certifications/vmware "VMware"
create_page docs/certifications/storage "Storage"
create_page docs/certifications/san "SAN"
create_page docs/certifications/ai "AI"

echo
echo "Creating clean section landing pages..."
echo

cat > docs/ai/index.md << 'PAGE'
# AI

## Areas

- [OpenAI](openai/index.md)
- [Azure OpenAI](azure-openai/index.md)
- [AWS Bedrock](aws-bedrock/index.md)
- [Local AI / Ollama](local-ai-ollama/index.md)
- [GPU Workloads](gpu-workloads/index.md)
PAGE

cat > docs/automation/index.md << 'PAGE'
# Automation

## Tools

- [PowerShell](powershell/index.md)
- [Python](python/index.md)
- [Ansible](ansible/index.md)
- [Terraform](terraform/index.md)
- [GitHub Actions](github-actions/index.md)
PAGE

cat > docs/disaster-recovery/index.md << 'PAGE'
# Disaster Recovery

## Platforms and Technologies

- [RecoverPoint](recoverpoint/index.md)
- [SRDF/S](srdf-s/index.md)
- [SRDF/A](srdf-a/index.md)
- [SRM](srm/index.md)
- [Superna Eyeglass](superna-eyeglass/index.md)
- [RASR](rasr/index.md)
- [Isolated Recovery Environment / IRE](isolated-recovery-environment-ire/index.md)
- [NetBackup](netbackup/index.md)
PAGE

cat > docs/compute/index.md << 'PAGE'
# Compute

## Platforms

- [Windows Server](windows-server/index.md)
- [Linux](linux/index.md)
PAGE

cat > docs/security/index.md << 'PAGE'
# Security

## Areas

- [Active Directory](active-directory/index.md)
- [Certificates](certificates/index.md)
- [CyberArk](cyberark/index.md)
- [Venafi](venafi/index.md)
PAGE

cat > docs/monitoring/index.md << 'PAGE'
# Monitoring

## Platforms

- [Aria Operations](aria-operations/index.md)
- [CloudIQ](cloudiq/index.md)
- [Pure1](pure1/index.md)
- [Dell AIOps](dell-aiops/index.md)
- [InsightIQ](insightiq/index.md)
- [Nexus Dashboard](nexus-dashboard/index.md)
PAGE

cat > docs/tools/index.md << 'PAGE'
# Tools

## Tools

- [ServiceNow](servicenow/index.md)
- [Jira](jira/index.md)
- [Confluence](confluence/index.md)
- [Git](git/index.md)
PAGE

cat > docs/project-management/index.md << 'PAGE'
# Project Management

## Areas

- [Change Management](change-management/index.md)
- [Incident Management](incident-management/index.md)
- [Maintenance Windows](maintenance-windows/index.md)
- [Asset Inventory](asset-inventory/index.md)
- [Health Checks](health-checks/index.md)
PAGE

cat > docs/standards/index.md << 'PAGE'
# Standards

## Standards

- [Naming Conventions](naming-conventions/index.md)
- [Build Standards](build-standards/index.md)
- [Configuration Baselines](configuration-baselines/index.md)
- [Security Baselines](security-baselines/index.md)
- [SAN Zoning Standard](san-zoning-standard/index.md)
PAGE

cat > docs/protocols/index.md << 'PAGE'
# Protocols

## Protocols

- [Fibre Channel](fibre-channel/index.md)
- [iSCSI](iscsi/index.md)
- [NFS](nfs/index.md)
- [SMB](smb/index.md)
- [DNS](dns/index.md)
- [DHCP](dhcp/index.md)
- [NTP](ntp/index.md)
- [SNMP](snmp/index.md)
- [LDAP](ldap/index.md)
- [TLS](tls/index.md)
PAGE

cat > docs/certifications/index.md << 'PAGE'
# Certifications

## Areas

- [AWS](aws/index.md)
- [Azure](azure/index.md)
- [VMware](vmware/index.md)
- [Storage](storage/index.md)
- [SAN](san/index.md)
- [AI](ai/index.md)
PAGE

echo
echo "Done."
echo
echo "Run:"
echo "mkdocs serve --clean"
echo

