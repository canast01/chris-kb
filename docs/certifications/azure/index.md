---
tags:
  - azure
  - certifications
description: "Azure Certification reference covering Overview, Core Certification Paths, Daily Study Focus, Useful Commands, Renewal Notes."
---
# Azure Certification

<div class="kb-summary">
Azure Certification reference covering Overview, Core Certification Paths, Daily Study Focus, Useful Commands, Renewal Notes.
</div>

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="exam-tracking/">
  <strong>Exam Tracking</strong>
  <span>Exam scheduling, scores, and certification tracking.</span>
</a>

<a class="kb-card" href="practice-notes/">
  <strong>Practice Notes</strong>
  <span>Practice exam notes and study materials.</span>
</a>

<a class="kb-card" href="review-plan/">
  <strong>Review Plan</strong>
  <span>Study plan and review schedule.</span>
</a>

<a class="kb-card" href="weak-areas/"><strong>Weak Areas</strong><span>Topics needing additional study and focus.</span></a>
<a class="kb-card" href="services/"><strong>Services</strong><span>Per-service study notes — Entra ID, VMs, VNet, Blob Storage, AKS, and more.</span></a>

</div>

## Overview

Azure certifications validate skills in managing Microsoft Azure infrastructure, networking, storage, and identity services.

## Core Certification Paths

- AZ-900 Fundamentals
- AZ-104 Administrator
- AZ-305 Architect
- AZ-500 Security

## Daily Study Focus

- Review Azure resource management
- Practice virtual networking scenarios
- Study identity and access management
- Review monitoring and backup services

## Useful Commands

```bash
az login
az vm list
az network vnet list
az storage account list
```


```text title="Expected output"
You have logged in. Welcome to Azure CLI 2.54.0!

Name                ResourceGroup      PowerState    PublicIps      Fqdns
------------------  -----------------  -----------   -----------    -----
prod-web-vm-01      prod-rg            VM running    52.168.45.12   prod-web-01.eastus.cloudapp.azure.com
prod-db-vm-02       prod-rg            VM running    52.168.45.13   prod-db-02.eastus.cloudapp.azure.com
dev-test-vm-03      dev-rg             VM deallocated
staging-app-vm-04   staging-rg         VM running    20.45.123.89   staging-app.eastus.cloudapp.azure.com

Name                   ResourceGroup      Location    NumSubnets    ProvisioningState
---------------------  -----------------  ----------  -----------   -----------------
prod-vnet-eastus       prod-rg            eastus      3             Succeeded
dev-vnet-eastus        dev-rg             eastus      2             Succeeded
staging-vnet-eastus    staging-rg         eastus      1             Succeeded

Name                      ResourceGroup      Location    SkuName      ProvisioningState
-------------------------  -----------------  ----------  -----------  -----------------
prodstg001               prod-rg            eastus      Standard_LRS  Succeeded
devstg002                dev-rg             eastus      Standard_GRS  Succeeded
stagingstg003            staging-rg         eastus      Premium_LRS   Succeeded
```

!!! warning "Common errors"
    **`ERROR: Please run 'az login' first.`** — Run `az login` to authenticate before executing other Azure CLI commands.
    **`ERROR: The subscription of <subscription-id> doesn't have authorization to perform action 'Microsoft.Compute/virtualMachines/read' on resource '<resource-id>'.`** — Ensure your Azure account has the required Reader or Contributor role assigned to the subscription via Azure Portal IAM settings.
## Renewal Notes

Azure certifications typically require renewal annually through online assessment.
