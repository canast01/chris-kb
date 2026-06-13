---
tags:
  - aws
---
# EKS


<div class="kb-summary">
EKS reference covering Node Groups, Fargate Profiles, IAM OIDC Provider, Access Entries and Auth Mode, Add-ons and 1 more sections.

*Applies to: AWS*
</div>

```text
┌──────────────────────────────────────────── AWS CLI — EKS ────────────────────────────────────────────┐
│                                                                                                       │
│  EKS CLI commands for cluster management, node groups, add-ons, and kubeconfig.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Cluster Operations              │  │            Node Group Operations            │   │
│   │          create-cluster: provision           │  │               create-nodegroup              │   │
│   │           describe-cluster: status           │  │              describe-nodegroup             │   │
│   │         list-clusters: all in region         │  │           update-nodegroup-config           │   │
│   │       update-cluster-version: upgrade        │  │           update-nodegroup-version          │   │
│   │           delete-cluster: teardown           │  │               delete-nodegroup              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cluster upgraded first; then node groups updated to matching Kubernetes version                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Access and Auth                │  │                   Add-ons                   │   │
│   │           update-kubeconfig: merge           │  │            create-addon: install            │   │
│   │         create-access-entry: IAM map         │  │           describe-addon: version           │   │
│   │           associate-access-policy            │  │            update-addon: upgrade            │   │
│   │             list-access-entries              │  │             delete-addon: remove            │   │
│   │            create-fargate-profile            │  │           describe-addon-versions           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  EKS control plane (AWS-managed) · EC2 worker nodes · VPC · IAM · EBS/EFS storage                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  EKS             = Elastic Kubernetes Service; managed Kubernetes control plane                       │
│  Node group      = Managed group of EC2 worker nodes; auto-scaling enabled                            │
│  update-kubeconfig= Adds EKS cluster to local ~/.kube/config for kubectl access                       │
│  Access entry    = EKS API method mapping IAM principal to Kubernetes RBAC role                       │
│  Associate policy= Binds a predefined EKS access policy to an access entry                            │
│  Add-on          = Managed EKS component: CoreDNS, kube-proxy, VPC CNI, EBS CSI                       │
│  Fargate profile = Runs pods serverlessly without managing EC2 node groups                            │
│  update-cluster-version= Upgrades EKS control plane to next minor version                             │
│  update-nodegroup-version= Replaces node group nodes with new Kubernetes AMI version                  │
│  VPC CNI         = AWS VPC Container Network Interface plugin; assigns pod IPs from VPC               │
│  EBS CSI driver  = Kubernetes CSI driver for provisioning EBS volumes as PVs                          │
│  IRSA            = IAM Roles for Service Accounts; pods assume IAM roles via OIDC                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Fargate Profiles

```bash
# List Fargate profiles
aws eks list-fargate-profiles --cluster-name <cluster>

# Describe a profile
aws eks describe-fargate-profile \
  --cluster-name <cluster> \
  --fargate-profile-name <profile>

# Create a Fargate profile
aws eks create-fargate-profile \
  --cluster-name <cluster> \
  --fargate-profile-name <profile> \
  --pod-execution-role-arn arn:aws:iam::<account_id>:role/<FargatePodExecutionRole> \
  --selectors namespace=<namespace>
```

## IAM OIDC Provider

```bash
# Check if an OIDC provider is already associated
aws eks describe-cluster --name <cluster> \
  --query "cluster.identity.oidc.issuer" --output text

# Associate an IAM OIDC provider with the cluster (requires eksctl)
eksctl utils associate-iam-oidc-provider \
  --cluster <cluster> \
  --region <region> \
  --approve

# List existing OIDC providers in the account
aws iam list-open-id-connect-providers
```

## Access Entries and Auth Mode

```bash
# Get the current authentication mode
aws eks describe-cluster --name <cluster> \
  --query "cluster.accessConfig.authenticationMode" --output text

# Update cluster to use API auth mode (enables access entries)
aws eks update-cluster-config \
  --name <cluster> \
  --access-config authenticationMode=API_AND_CONFIG_MAP

# List access entries
aws eks list-access-entries --cluster-name <cluster>

# Create an access entry for an IAM principal
aws eks create-access-entry \
  --cluster-name <cluster> \
  --principal-arn arn:aws:iam::<account_id>:role/<RoleName>

# Associate an access policy with an entry
aws eks associate-access-policy \
  --cluster-name <cluster> \
  --principal-arn arn:aws:iam::<account_id>:role/<RoleName> \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy \
  --access-scope type=cluster
```

## Add-ons

```bash
# List available add-ons for a cluster version
aws eks describe-addon-versions --kubernetes-version 1.29

# List installed add-ons
aws eks list-addons --cluster-name <cluster>

# Describe an installed add-on
aws eks describe-addon --cluster-name <cluster> --addon-name vpc-cni

# Install an add-on
aws eks create-addon \
  --cluster-name <cluster> \
  --addon-name coredns \
  --resolve-conflicts OVERWRITE

# Update an add-on to a specific version
aws eks update-addon \
  --cluster-name <cluster> \
  --addon-name vpc-cni \
  --addon-version v1.18.0-eksbuild.1 \
  --resolve-conflicts OVERWRITE

# Delete an add-on
aws eks delete-addon --cluster-name <cluster> --addon-name coredns
```

## Pod Identity Associations

```bash
# List pod identity associations for a cluster
aws eks list-pod-identity-associations --cluster-name <cluster>

# Describe a specific association
aws eks describe-pod-identity-association \
  --cluster-name <cluster> \
  --association-id <association_id>

# Create a pod identity association
aws eks create-pod-identity-association \
  --cluster-name <cluster> \
  --namespace <namespace> \
  --service-account <service_account_name> \
  --role-arn arn:aws:iam::<account_id>:role/<RoleName>

# Delete a pod identity association
aws eks delete-pod-identity-association \
  --cluster-name <cluster> \
  --association-id <association_id>
```
