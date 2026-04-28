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
echo "Creating cleaner vendor landing pages..."
echo

cat > docs/storage/pure/index.md << 'PAGE'
# Pure

## Platforms

- [FlashArray](flasharray/)
- [FlashBlade](flashblade/)
- [Evergreen](evergreen/)
- [Evergreen One](evergreen-one/)
PAGE

cat > docs/storage/dell/index.md << 'PAGE'
# Dell

## Platforms

- [PowerMax](powermax/)
- [VMAX](vmax/)
- [PowerScale](powerscale/)
- [ECS](ecs/)
- [Data Domain](data-domain/)
- [Unity](unity/)
- [VPLEX](vplex/)
- [PowerPath](powerpath/)
- [APEX Storage as a Service](apex-storage-as-a-service/)
- [COD](cod/)
- [FOD](fod/)
- [Secure Connect Gateway](secure-connect-gateway/)
PAGE

cat > docs/storage/netapp/index.md << 'PAGE'
# NetApp

## Platforms

- [ONTAP](ontap/)
- [SnapMirror](snapmirror/)
- [SnapCenter](snapcenter/)
- [Keystone](keystone/)
PAGE

cat > docs/virtualization/vmware/index.md << 'PAGE'
# VMware

## Platforms

- [VMware Cloud Foundation](vmware-cloud-foundation/)
- [vCenter](vcenter/)
- [ESXi](esxi/)
- [vSAN](vsan/)
- [NSX](nsx/)
- [VxRail](vxrail/)
- [VxRail Manager](vxrail-manager/)
- [Aria Operations](aria-operations/)
- [Aria Operations for Logs](aria-operations-for-logs/)
- [Aria Automation](aria-automation/)
- [Aria Suite Lifecycle](aria-suite-lifecycle/)
PAGE

cat > docs/cloud/aws/index.md << 'PAGE'
# AWS

## Services

- [EC2](ec2/)
- [EBS](ebs/)
- [S3](s3/)
- [VPC](vpc/)
- [IAM](iam/)
- [RDS](rds/)
- [Lambda](lambda/)
- [CloudWatch](cloudwatch/)
- [CloudTrail](cloudtrail/)
- [Route 53](route-53/)
- [Elastic Load Balancer](elastic-load-balancer/)
- [Auto Scaling](auto-scaling/)
- [Systems Manager](systems-manager/)
- [AWS Backup](aws-backup/)
- [KMS](kms/)
- [Secrets Manager](secrets-manager/)
- [AWS Config](aws-config/)
- [AWS Organizations](aws-organizations/)
- [Cost Explorer / Billing](cost-explorer-billing/)
PAGE

cat > docs/cloud/azure/index.md << 'PAGE'
# Azure

## Services

- [Virtual Machines](virtual-machines/)
- [Managed Disks](managed-disks/)
- [Storage Accounts](storage-accounts/)
- [Virtual Network](virtual-network/)
- [Network Security Groups](network-security-groups/)
- [Load Balancer](load-balancer/)
- [Application Gateway](application-gateway/)
- [VPN Gateway](vpn-gateway/)
- [ExpressRoute](expressroute/)
- [Entra ID](entra-id/)
- [Azure Backup](azure-backup/)
- [Azure Site Recovery](azure-site-recovery/)
- [Azure Monitor](azure-monitor/)
- [Log Analytics](log-analytics/)
- [Key Vault](key-vault/)
- [Azure Automation](azure-automation/)
- [Azure Policy](azure-policy/)
- [Cost Management / Billing](cost-management-billing/)
PAGE

cat > docs/san/cisco/index.md << 'PAGE'
# Cisco

## Platforms

- [MDS](mds/)
- [Cisco DCNM](cisco-dcnm/)
- [Nexus Dashboard](nexus-dashboard/)
PAGE

cat > docs/san/brocade/index.md << 'PAGE'
# Brocade

## Platforms

- [Fabric OS](fabric-os/)
- [SANnav](sannav/)
PAGE

echo
echo "Updating mkdocs.yml with cleaner nav..."
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
      - VMware: virtualization/vmware/index.md

  - Storage:
      - Dell: storage/dell/index.md
      - Pure: storage/pure/index.md
      - NetApp: storage/netapp/index.md

  - Cloud:
      - AWS: cloud/aws/index.md
      - Azure: cloud/azure/index.md

  - SAN:
      - Cisco: san/cisco/index.md
      - Brocade: san/brocade/index.md

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
echo "Run: mkdocs serve --clean"
echo
