---
tags:
  - architecture
  - aws
---
# Amazon EVS — Architecture

<!-- diagram:evs-architecture -->

<div class="kb-summary">
EVS architecture: bare-metal EC2 instances running VCF, VPC-native networking, vSAN HCI storage, NSX-T overlay, and on-premises connectivity via Direct Connect or HCX.

*Applies to: Amazon EVS*
</div>

![Amazon EVS — Architecture — Diagram](../../../../assets/cloud-aws-evs-architecture-diagram.svg)


![Amazon EVS Architecture Overview](../../../../assets/evs-architecture-overview.svg)

<div class="kb-grid">
  <a class="kb-card" href="how-it-works/">
    <span class="kb-card-title">How It Works</span>
    <span class="kb-card-desc">Bare-metal host model, VPC integration, vSAN datastore, NSX-T overlay</span>
  </a>
  <a class="kb-card" href="design-standards/">
    <span class="kb-card-title">Design Standards</span>
    <span class="kb-card-desc">Cluster sizing, AZ placement, CIDR planning, Direct Connect bandwidth</span>
  </a>
  <a class="kb-card" href="integrations/">
    <span class="kb-card-title">Integrations</span>
    <span class="kb-card-desc">HCX migration, Direct Connect, AWS native services, IAM</span>
  </a>
</div>
