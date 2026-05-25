# EKS

```text
EKS CLI: Cluster → Nodes → Workloads
──────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────┐
  │  EKS Control Plane (AWS managed)                    │
  │  describe-cluster / list-clusters                   │
  │  update-kubeconfig ──► ~/.kube/config               │
  └────────────────────────┬────────────────────────────┘
                           │ kubectl now works
                           ▼
  ┌─────────────────────────────────────────────────────┐
  │  Node Groups / Fargate Profiles                     │
  │  list-nodegroups                                    │
  │  describe-nodegroup                                 │
  │  update-nodegroup-config (scale min/max/desired)    │
  └────────────────────────┬────────────────────────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
         ┌────────┐   ┌─────────┐   ┌────────────┐
         │Add-ons │   │  OIDC   │   │Pod Identity│
         │coredns │   │provider │   │Associations│
         │vpc-cni │   │(IRSA)   │   │            │
         │kube-   │   │         │   │            │
         │proxy   │   │         │   │            │
         └────────┘   └─────────┘   └────────────┘
```

> Part of the AWS CLI Reference.

---

## Clusters

```bash
# List and inspect clusters
aws eks list-clusters
aws eks describe-cluster --name <cluster>

# Update local kubeconfig
aws eks update-kubeconfig --name <cluster> --region <region>
```

## Node Groups

```bash
# List and inspect managed node groups
aws eks list-nodegroups --cluster-name <cluster>
aws eks describe-nodegroup --cluster-name <cluster> --nodegroup-name <ng>

# Scale a managed node group
aws eks update-nodegroup-config \
  --cluster-name <cluster> \
  --nodegroup-name <ng> \
  --scaling-config minSize=2,maxSize=10,desiredSize=4
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
