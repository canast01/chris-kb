---
tags:
  - aws
description: "EKS reference covering Node Groups, Fargate Profiles, IAM OIDC Provider, Access Entries and Auth Mode, Add-ons and 1 more sections."
---
# EKS

<div class="kb-summary">
EKS reference covering Node Groups, Fargate Profiles, IAM OIDC Provider, Access Entries and Auth Mode, Add-ons and 1 more sections.

*Applies to: AWS*
</div>

```d2
direction: down

fargate_profiles: "Fargate Profiles" {shape: rectangle}
iam_oidc_provider: "IAM OIDC Provider" {shape: rectangle}
access_entries_and_auth_mode: "Access Entries and Auth Mode" {shape: rectangle}
addons: "Add-ons" {shape: rectangle}
pod_identity_associations: "Pod Identity Associations" {shape: rectangle}

fargate_profiles -> iam_oidc_provider: uses
iam_oidc_provider -> access_entries_and_auth_mode: uses
access_entries_and_auth_mode -> addons: uses
addons -> pod_identity_associations: uses
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


```text title="Expected output"
{
    "fargateProfileNames": [
        "default",
        "production-apps",
        "monitoring"
    ]
}
{
    "fargateProfile": {
        "fargateProfileName": "production-apps",
        "fargateProfileArn": "arn:aws:eks:us-east-1:123456789012:fargateprofile/my-cluster/production-apps/12a3b4c5-d6e7-8f9g-0h1i-2j3k4l5m6n7o",
        "clusterName": "my-cluster",
        "createdAt": "2024-01-15T10:23:45.123000+00:00",
        "podExecutionRoleArn": "arn:aws:iam::123456789012:role/eks-fargate-pod-execution-role",
        "selectors": [
            {
                "namespace": "production",
                "labels": {}
            }
        ],
        "status": "ACTIVE",
        "tags": {}
    }
}
{
    "fargateProfile": {
        "fargateProfileName": "staging-apps",
        "fargateProfileArn": "arn:aws:eks:us-east-1:123456789012:fargateprofile/my-cluster/staging-apps/9x8y7z6w-5v4u-3t2s-1r0q-9p8o7n6m5l4k",
        "clusterName": "my-cluster",
        "createdAt": "2024-01-15T11:47:32.456000+00:00",
        "podExecutionRoleArn": "arn:aws:iam::123456789012:role/eks-fargate-pod-execution-role",
        "selectors": [
            {
                "namespace": "staging",
                "labels": {}
            }
        ],
        "status": "CREATING",
        "tags": {}
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the ListFargateProfiles operation: No cluster found in us-east-1: <cluster>` | Verify the cluster name is correct and exists in the specified region with `aws eks describe-cluster --name <cluster> --region <region>`. |
    | `An error occurred (InvalidParameterException) when calling the CreateFargateProfile operation: Invalid ARN: arn:aws:iam::<account_id>:role/<FargatePodExecutionRole>` | Replace `<account_id>` and `<FargatePodExecutionRole>` with actual values, and confirm the IAM role exists with `aws iam get-role --role-name <FargatePodExecutionRole>`. |
    | `An error occurred (InvalidParameterException) when calling the CreateFargateProfile operation: Fargate profile with name <profile> already exists` | Use a unique profile name or delete the existing profile with `aws eks delete-fargate-profile --cluster-name <cluster> --fargate-profile-name <profile>` first. |
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


```text title="Expected output"
https://oidc.eks.us-east-1.amazonaws.com/id/EXAMPLEABCD1234567890ABCD

2024-11-15 14:32:18 [ℹ]  eksctl version 0.187.0
2024-11-15 14:32:18 [ℹ]  using region us-east-1
2024-11-15 14:32:19 [ℹ]  IAM Open ID Connect provider is already associated with cluster "prod-cluster"
2024-11-15 14:32:19 [✔]  associated IAM OIDC provider with cluster "prod-cluster"

OpenIdConnectProviderList:
- Arn: arn:aws:iam::123456789012:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/EXAMPLEABCD1234567890ABCD
  CreateDate: '2024-10-20T09:15:33+00:00'
  Url: https://oidc.eks.us-east-1.amazonaws.com/id/EXAMPLEABCD1234567890ABCD
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceInUseException) when calling the AssociateOpenIDConnectProvider operation: OIDC provider already exists` | Run the describe-cluster command first to verify the provider exists, then skip the associate step. |
    | `error: cluster not found: "prod-cluster"` | Verify the cluster name matches exactly and confirm you are querying the correct region with `--region`. |
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


```text title="Expected output"
CONFIG_MAP
Updating cluster configuration...
{
    "update": {
        "id": "8f4c9e2a-1b7d-4k3m-9p2q-5r6s7t8u9v0w",
        "status": "InProgress",
        "type": "ConfigServiceResourceUpdate",
        "params": [
            {
                "type": "AccessConfig",
                "value": "{\"authenticationMode\":\"API_AND_CONFIG_MAP\"}"
            }
        ],
        "createdAt": "2024-01-15T14:32:18.456000+00:00",
        "errors": []
    }
}
{
    "accessEntries": [
        {
            "clusterName": "prod-eks-cluster",
            "principalArn": "arn:aws:iam::123456789012:role/eks-admin-role",
            "kubernetesGroups": [],
            "accessEntryArn": "arn:aws:eks:us-east-1:123456789012:access-entry/prod-eks-cluster/role/eks-admin-role",
            "createdAt": "2024-01-15T14:33:02.123000+00:00",
            "modifiedAt": "2024-01-15T14:33:02.123000+00:00",
            "tags": {}
        }
    ]
}
{
    "accessPolicy": {
        "arn": "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy",
        "name": "AmazonEKSClusterAdminPolicy"
    },
    "accessScope": {
        "type": "cluster"
    },
    "associatedAt": "2024-01-15T14:33:45.789000+00:00",
    "modifiedAt": "2024-01-15T14:33:45.789000+00:00"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the DescribeCluster operation: No cluster found for name: <cluster>` | Replace `<cluster>` with the actual EKS cluster name and verify the cluster exists in the current AWS region. |
    | `An error occurred (InvalidParameterException) when calling the UpdateClusterConfig operation: Invalid authentication mode. Valid values are: CONFIG_MAP, API, API_AND_CONFIG_MAP` | Ensure the authenticationMode value is spelled correctly and is one of the three valid options. |
    | `An error occurred (InvalidParameterException) when calling the CreateAccessEntry operation: Invalid principal ARN format` | Verify the IAM principal ARN follows the correct format (e.g., `arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME`) and that the role exists. |
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


```text title="Expected output"
{
    "addons": [
        {
            "addonName": "vpc-cni",
            "type": "networking",
            "addonVersions": [
                {
                    "addonVersion": "v1.18.0-eksbuild.1",
                    "created": "2024-01-15T10:22:33.000000+00:00",
                    "modified": "2024-01-15T10:22:33.000000+00:00",
                    "serviceAccount": "aws-node"
                },
                {
                    "addonVersion": "v1.17.1-eksbuild.2",
                    "created": "2023-12-10T08:15:22.000000+00:00",
                    "modified": "2023-12-10T08:15:22.000000+00:00"
                }
            ]
        },
        {
            "addonName": "coredns",
            "type": "networking",
            "addonVersions": [
                {
                    "addonVersion": "v1.10.1-eksbuild.2",
                    "created": "2024-01-20T14:33:11.000000+00:00",
                    "modified": "2024-01-20T14:33:11.000000+00:00"
                }
            ]
        }
    ]
}
{
    "addons": [
        "vpc-cni",
        "coredns",
        "kube-proxy"
    ]
}
{
    "addon": {
        "addonName": "vpc-cni",
        "clusterName": "prod-eks-cluster",
        "addonVersion": "v1.18.0-eksbuild.1",
        "createdAt": "2024-02-01T09:45:22.123456+00:00",
        "modifiedAt": "2024-02-01T09:45:22.123456+00:00",
        "serviceAccountRoleArn": "arn:aws:iam::123456789012:role/eks-vpc-cni-role",
        "status": "ACTIVE",
        "health": {
            "issues": []
        }
    }
}
{
    "addon": {
        "addonName": "coredns",
        "clusterName": "prod-eks-cluster",
        "addonVersion": "v1.10.1-eksbuild.2",
        "createdAt": "2024-02-05T11:22:15.654321+00:00",
        "modifiedAt": "2024-02-05T11:22:15.654321+00:00",
        "status": "ACTIVE",
        "health": {
            "issues": []
        }
    }
}
{
    "addon": {
        "addonName": "vpc-cni",
        "clusterName": "prod-eks-cluster",
        "addonVersion": "v1.18.0-eksbuild.1",
        "createdAt": "2024-02-10T13:55:44.987654+00:00",
        "modifiedAt": "2024-
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


```text title="Expected output"
{
    "associations": [
        {
            "clusterName": "prod-eks-cluster",
            "namespace": "kube-system",
            "serviceAccount": "aws-load-balancer-controller",
            "roleArn": "arn:aws:iam::123456789012:role/AWSLoadBalancerControllerRole",
            "associationArn": "arn:aws:eks:us-east-1:123456789012:podidentityassociation/prod-eks-cluster/a-1a2b3c4d5e6f7g8h9",
            "associationId": "a-1a2b3c4d5e6f7g8h9",
            "createdAt": "2024-01-15T10:32:45.123000+00:00",
            "modifiedAt": "2024-01-15T10:32:45.123000+00:00",
            "tags": {}
        },
        {
            "clusterName": "prod-eks-cluster",
            "namespace": "monitoring",
            "serviceAccount": "prometheus",
            "roleArn": "arn:aws:iam::123456789012:role/PrometheusRole",
            "associationArn": "arn:aws:eks:us-east-1:123456789012:podidentityassociation/prod-eks-cluster/a-2b3c4d5e6f7g8h9i0",
            "associationId": "a-2b3c4d5e6f7g8h9i0",
            "createdAt": "2024-01-14T14:22:10.456000+00:00",
            "modifiedAt": "2024-01-14T14:22:10.456000+00:00",
            "tags": {}
        }
    ]
}
{
    "association": {
        "clusterName": "prod-eks-cluster",
        "namespace": "kube-system",
        "serviceAccount": "aws-load-balancer-controller",
        "roleArn": "arn:aws:iam::123456789012:role/AWSLoadBalancerControllerRole",
        "associationArn": "arn:aws:eks:us-east-1:123456789012:podidentityassociation/prod-eks-cluster/a-1a2b3c4d5e6f7g8h9",
        "associationId": "a-1a2b3c4d5e6f7g8h9",
        "createdAt": "2024-01-15T10:32:45.123000+00:00",
        "modifiedAt": "2024-01-15T10:32:45.123000+00:00"
    }
}
{
    "association": {
        "clusterName": "prod-eks-cluster",
        "namespace": "default",
        "serviceAccount": "my-app-sa",
        "roleArn": "arn:aws:iam::123456789012:role/MyAppRole",
        "associationArn": "arn:aws:eks:us-east-1:123456789012:podidentityassociation/prod-eks
```
## See also

- [AWS CLI Reference](../index.md)
- [AWS Compute](../../compute/index.md)
- [AWS Networking](../../networking/index.md)
