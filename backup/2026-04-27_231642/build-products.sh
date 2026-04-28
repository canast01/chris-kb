#!/usr/bin/env bash

set -e

echo
echo "Running backup first..."
echo

if [ -f "./backup.sh" ]; then
  ./backup.sh
else
  echo "ERROR: backup.sh not found. Create backup.sh first."
  exit 1
fi

echo
echo "Creating product/platform directories..."
echo

mkdir -p docs/virtualization/vmware/{vmware-cloud-foundation,vcenter,esxi,vsan,nsx,vxrail,vxrail-manager,aria-operations,aria-operations-for-logs,aria-automation,aria-suite-lifecycle}

mkdir -p docs/storage/dell/{powermax,vmax,powerscale,ecs,data-domain,unity,vplex,powerpath,apex-storage-as-a-service,cod,fod,secure-connect-gateway}
mkdir -p docs/storage/pure/{flasharray,flashblade,evergreen,evergreen-one}
mkdir -p docs/storage/netapp/{ontap,snapmirror,snapcenter,keystone}

mkdir -p docs/cloud/aws/{ec2,ebs,s3,vpc,iam,rds,lambda,cloudwatch,cloudtrail,route-53,elastic-load-balancer,auto-scaling,systems-manager,aws-backup,kms,secrets-manager,aws-config,aws-organizations,cost-explorer-billing}
mkdir -p docs/cloud/azure/{virtual-machines,managed-disks,storage-accounts,virtual-network,network-security-groups,load-balancer,application-gateway,vpn-gateway,expressroute,entra-id,azure-backup,azure-site-recovery,azure-monitor,log-analytics,key-vault,azure-automation,azure-policy,cost-management-billing}

mkdir -p docs/san/cisco/{mds,cisco-dcnm,nexus-dashboard}
mkdir -p docs/san/brocade/{fabric-os,sannav}

echo "Creating product/platform pages..."
echo

create_page() {
  path="$1"
  title="$2"

  cat > "$path/index.md" << PAGE
# $title
PAGE
}

create_page docs/virtualization/vmware/vmware-cloud-foundation "VMware Cloud Foundation"
create_page docs/virtualization/vmware/vcenter "vCenter"
create_page docs/virtualization/vmware/esxi "ESXi"
create_page docs/virtualization/vmware/vsan "vSAN"
create_page docs/virtualization/vmware/nsx "NSX"
create_page docs/virtualization/vmware/vxrail "VxRail"
create_page docs/virtualization/vmware/vxrail-manager "VxRail Manager"
create_page docs/virtualization/vmware/aria-operations "Aria Operations"
create_page docs/virtualization/vmware/aria-operations-for-logs "Aria Operations for Logs"
create_page docs/virtualization/vmware/aria-automation "Aria Automation"
create_page docs/virtualization/vmware/aria-suite-lifecycle "Aria Suite Lifecycle"

create_page docs/storage/dell/powermax "PowerMax"
create_page docs/storage/dell/vmax "VMAX"
create_page docs/storage/dell/powerscale "PowerScale"
create_page docs/storage/dell/ecs "ECS"
create_page docs/storage/dell/data-domain "Data Domain"
create_page docs/storage/dell/unity "Unity"
create_page docs/storage/dell/vplex "VPLEX"
create_page docs/storage/dell/powerpath "PowerPath"
create_page docs/storage/dell/apex-storage-as-a-service "APEX Storage as a Service"
create_page docs/storage/dell/cod "COD"
create_page docs/storage/dell/fod "FOD"
create_page docs/storage/dell/secure-connect-gateway "Secure Connect Gateway"

create_page docs/storage/pure/flasharray "FlashArray"
create_page docs/storage/pure/flashblade "FlashBlade"
create_page docs/storage/pure/evergreen "Evergreen"
create_page docs/storage/pure/evergreen-one "Evergreen One"

create_page docs/storage/netapp/ontap "ONTAP"
create_page docs/storage/netapp/snapmirror "SnapMirror"
create_page docs/storage/netapp/snapcenter "SnapCenter"
create_page docs/storage/netapp/keystone "Keystone"

create_page docs/cloud/aws/ec2 "EC2"
create_page docs/cloud/aws/ebs "EBS"
create_page docs/cloud/aws/s3 "S3"
create_page docs/cloud/aws/vpc "VPC"
create_page docs/cloud/aws/iam "IAM"
create_page docs/cloud/aws/rds "RDS"
create_page docs/cloud/aws/lambda "Lambda"
create_page docs/cloud/aws/cloudwatch "CloudWatch"
create_page docs/cloud/aws/cloudtrail "CloudTrail"
create_page docs/cloud/aws/route-53 "Route 53"
create_page docs/cloud/aws/elastic-load-balancer "Elastic Load Balancer"
create_page docs/cloud/aws/auto-scaling "Auto Scaling"
create_page docs/cloud/aws/systems-manager "Systems Manager"
create_page docs/cloud/aws/aws-backup "AWS Backup"
create_page docs/cloud/aws/kms "KMS"
create_page docs/cloud/aws/secrets-manager "Secrets Manager"
create_page docs/cloud/aws/aws-config "AWS Config"
create_page docs/cloud/aws/aws-organizations "AWS Organizations"
create_page docs/cloud/aws/cost-explorer-billing "Cost Explorer / Billing"

create_page docs/cloud/azure/virtual-machines "Virtual Machines"
create_page docs/cloud/azure/managed-disks "Managed Disks"
create_page docs/cloud/azure/storage-accounts "Storage Accounts"
create_page docs/cloud/azure/virtual-network "Virtual Network"
create_page docs/cloud/azure/network-security-groups "Network Security Groups"
create_page docs/cloud/azure/load-balancer "Load Balancer"
create_page docs/cloud/azure/application-gateway "Application Gateway"
create_page docs/cloud/azure/vpn-gateway "VPN Gateway"
create_page docs/cloud/azure/expressroute "ExpressRoute"
create_page docs/cloud/azure/entra-id "Entra ID"
create_page docs/cloud/azure/azure-backup "Azure Backup"
create_page docs/cloud/azure/azure-site-recovery "Azure Site Recovery"
create_page docs/cloud/azure/azure-monitor "Azure Monitor"
create_page docs/cloud/azure/log-analytics "Log Analytics"
create_page docs/cloud/azure/key-vault "Key Vault"
create_page docs/cloud/azure/azure-automation "Azure Automation"
create_page docs/cloud/azure/azure-policy "Azure Policy"
create_page docs/cloud/azure/cost-management-billing "Cost Management / Billing"

create_page docs/san/cisco/mds "MDS"
create_page docs/san/cisco/cisco-dcnm "Cisco DCNM"
create_page docs/san/cisco/nexus-dashboard "Nexus Dashboard"

create_page docs/san/brocade/fabric-os "Fabric OS"
create_page docs/san/brocade/sannav "SANnav"

echo
echo "Updating mkdocs.yml..."
echo

cat > mkdocs.yml << 'YAML'
site_name: Chris KB
site_description: Infrastructure engineering knowledge base covering virtualization, storage, cloud, automation, and operations.

theme:
  name: material
  features:
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.highlight
    - search.suggest
    - content.code.copy

extra_css:
  - stylesheets/extra.css

nav:
  - Home: index.md

  - Virtualization:
      - VMware:
          - VMware Cloud Foundation: virtualization/vmware/vmware-cloud-foundation/index.md
          - vCenter: virtualization/vmware/vcenter/index.md
          - ESXi: virtualization/vmware/esxi/index.md
          - vSAN: virtualization/vmware/vsan/index.md
          - NSX: virtualization/vmware/nsx/index.md
          - VxRail: virtualization/vmware/vxrail/index.md
          - VxRail Manager: virtualization/vmware/vxrail-manager/index.md
          - Aria Operations: virtualization/vmware/aria-operations/index.md
          - Aria Operations for Logs: virtualization/vmware/aria-operations-for-logs/index.md
          - Aria Automation: virtualization/vmware/aria-automation/index.md
          - Aria Suite Lifecycle: virtualization/vmware/aria-suite-lifecycle/index.md

  - Storage:
      - Dell:
          - PowerMax: storage/dell/powermax/index.md
          - VMAX: storage/dell/vmax/index.md
          - PowerScale: storage/dell/powerscale/index.md
          - ECS: storage/dell/ecs/index.md
          - Data Domain: storage/dell/data-domain/index.md
          - Unity: storage/dell/unity/index.md
          - VPLEX: storage/dell/vplex/index.md
          - PowerPath: storage/dell/powerpath/index.md
          - APEX Storage as a Service: storage/dell/apex-storage-as-a-service/index.md
          - COD: storage/dell/cod/index.md
          - FOD: storage/dell/fod/index.md
          - Secure Connect Gateway: storage/dell/secure-connect-gateway/index.md
      - Pure:
          - FlashArray: storage/pure/flasharray/index.md
          - FlashBlade: storage/pure/flashblade/index.md
          - Evergreen: storage/pure/evergreen/index.md
          - Evergreen One: storage/pure/evergreen-one/index.md
      - NetApp:
          - ONTAP: storage/netapp/ontap/index.md
          - SnapMirror: storage/netapp/snapmirror/index.md
          - SnapCenter: storage/netapp/snapcenter/index.md
          - Keystone: storage/netapp/keystone/index.md

  - Cloud:
      - AWS:
          - EC2: cloud/aws/ec2/index.md
          - EBS: cloud/aws/ebs/index.md
          - S3: cloud/aws/s3/index.md
          - VPC: cloud/aws/vpc/index.md
          - IAM: cloud/aws/iam/index.md
          - RDS: cloud/aws/rds/index.md
          - Lambda: cloud/aws/lambda/index.md
          - CloudWatch: cloud/aws/cloudwatch/index.md
          - CloudTrail: cloud/aws/cloudtrail/index.md
          - Route 53: cloud/aws/route-53/index.md
          - Elastic Load Balancer: cloud/aws/elastic-load-balancer/index.md
          - Auto Scaling: cloud/aws/auto-scaling/index.md
          - Systems Manager: cloud/aws/systems-manager/index.md
          - AWS Backup: cloud/aws/aws-backup/index.md
          - KMS: cloud/aws/kms/index.md
          - Secrets Manager: cloud/aws/secrets-manager/index.md
          - AWS Config: cloud/aws/aws-config/index.md
          - AWS Organizations: cloud/aws/aws-organizations/index.md
          - Cost Explorer / Billing: cloud/aws/cost-explorer-billing/index.md
      - Azure:
          - Virtual Machines: cloud/azure/virtual-machines/index.md
          - Managed Disks: cloud/azure/managed-disks/index.md
          - Storage Accounts: cloud/azure/storage-accounts/index.md
          - Virtual Network: cloud/azure/virtual-network/index.md
          - Network Security Groups: cloud/azure/network-security-groups/index.md
          - Load Balancer: cloud/azure/load-balancer/index.md
          - Application Gateway: cloud/azure/application-gateway/index.md
          - VPN Gateway: cloud/azure/vpn-gateway/index.md
          - ExpressRoute: cloud/azure/expressroute/index.md
          - Entra ID: cloud/azure/entra-id/index.md
          - Azure Backup: cloud/azure/azure-backup/index.md
          - Azure Site Recovery: cloud/azure/azure-site-recovery/index.md
          - Azure Monitor: cloud/azure/azure-monitor/index.md
          - Log Analytics: cloud/azure/log-analytics/index.md
          - Key Vault: cloud/azure/key-vault/index.md
          - Azure Automation: cloud/azure/azure-automation/index.md
          - Azure Policy: cloud/azure/azure-policy/index.md
          - Cost Management / Billing: cloud/azure/cost-management-billing/index.md

  - SAN:
      - Cisco:
          - MDS: san/cisco/mds/index.md
          - Cisco DCNM: san/cisco/cisco-dcnm/index.md
          - Nexus Dashboard: san/cisco/nexus-dashboard/index.md
      - Brocade:
          - Fabric OS: san/brocade/fabric-os/index.md
          - SANnav: san/brocade/sannav/index.md

  - AI: ai/index.md
  - Automation: automation/index.md
  - Disaster Recovery: disaster-recovery/index.md
  - Compute: compute/index.md
  - Security: security/index.md
  - Monitoring: monitoring/index.md
  - Tools: tools/index.md
  - Project Management: project-management/index.md
  - Standards: standards/index.md
  - Protocols: protocols/index.md
  - Certifications: certifications/index.md

markdown_extensions:
  - admonition
  - toc:
      permalink: true
  - tables
  - fenced_code
YAML

echo
echo "Done."
echo
echo "Run this next:"
echo "mkdocs serve --clean"
echo

