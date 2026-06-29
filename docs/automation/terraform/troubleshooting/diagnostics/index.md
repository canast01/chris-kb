---
tags:
  - terraform
  - troubleshooting
search:
  boost: 1.5
---
# Terraform — Diagnostics

<div class="kb-summary">
Terraform diagnostic commands: enable TF_LOG trace logging, inspect plan output as JSON, audit state with terraform state commands, debug provider authentication, diagnose backend connectivity, and safely recover from state lock incidents.

*Applies to: Terraform 1.x / OpenTofu 1.x*
</div>

```d2
direction: right

A: "Terraform Error" {shape: rectangle}
B: "terraform validate\nSyntax check" {shape: rectangle}
C: "C" {shape: rectangle}
D: "Fix HCL syntax\nterraform fmt -recursive" {shape: rectangle}
E: "TF_LOG=DEBUG tf plan\nCapture full trace" {shape: rectangle}
F: "F" {shape: rectangle}
G: "Check env vars\nterraform providers" {shape: rectangle}
H: "terraform state list\nInspect state" {shape: rectangle}
I: "terraform init -reconfigure\nRe-init backend" {shape: rectangle}
J: "terraform refresh\nResync state to reality" {shape: rectangle}
K: "K" {shape: rectangle}
L: "Check: AWS_ACCESS_KEY_ID\nAZURE_CLIENT_SECRET etc" {shape: rectangle}
M: "Check: ~/.aws/credentials\nor tf login status" {shape: rectangle}
N: "terraform state show\ncompare to cloud console" {shape: rectangle}
O: "Re-run terraform plan" {shape: rectangle}

A -> B
C -> D
C -> E
F -> G
F -> H
F -> I
F -> J
K -> L
K -> M
H -> N
D -> O
I -> O
J -> O
L -> O
M -> O
N -> O
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_validate_and_format: "Step 1 — Validate and format" {shape: rectangle}
step_2_enable_debug_logging: "Step 2 — Enable debug logging" {shape: rectangle}
step_3_debug_provider_authentication: "Step 3 — Debug provider authentication" {shape: rectangle}
step_4_inspect_and_audit_state: "Step 4 — Inspect and audit state" {shape: rectangle}
step_5_diagnose_backend_connectivity: "Step 5 — Diagnose backend connectivity" {shape: rectangle}
step_6_state_lock_recovery_caution: "Step 6 — State lock recovery (caution)" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_validate_and_format: investigate
symptom -> step_2_enable_debug_logging: investigate
symptom -> step_3_debug_provider_authentication: investigate
symptom -> step_4_inspect_and_audit_state: investigate
symptom -> step_5_diagnose_backend_connectivity: investigate
symptom -> step_6_state_lock_recovery_caution: investigate
step_1_validate_and_format -> resolution
step_2_enable_debug_logging -> resolution
step_3_debug_provider_authentication -> resolution
step_4_inspect_and_audit_state -> resolution
step_5_diagnose_backend_connectivity -> resolution
step_6_state_lock_recovery_caution -> resolution
```

## Before you begin

- **Access:** Provider credentials configured (env vars, credential file, or `terraform login`); read access to the backend (S3 bucket, Azure container, Terraform Cloud workspace)
- **Gather first:** the exact error message from `terraform plan` or `terraform apply`, the provider name and version, and whether a state lock is present
- **Never edit `.tfstate` directly:** the JSON structure has checksums; manual edits corrupt state and may require full re-import
- **State backups:** `terraform state pull > backup-$(date +%F).tfstate` before any state manipulation command
- **force-unlock caution:** only use `terraform force-unlock` after confirming the process that set the lock is truly gone — removing an active lock allows concurrent applies, which corrupts state

---

## Step 1 — Validate and format

```bash
# Check configuration syntax without calling any provider APIs
terraform validate
# Expected: "Success! The configuration is valid."
# If error: the output includes file path and line number

# Check and fix formatting (catches common style issues that can cause parse errors)
terraform fmt -check -recursive
terraform fmt -recursive   # auto-fix formatting

# Verify provider versions in use
terraform version
# Shows: Terraform version + all provider plugins with versions

# List all providers declared and their source addresses
terraform providers
# Output: dependency tree of modules → providers
```


```text title="Expected output"
Success! The configuration is valid.

Terraform has been successfully initialized!

Terraform v1.5.7
on linux_amd64
+ provider registry.terraform.io/hashicorp/aws v5.31.0
+ provider registry.terraform.io/hashicorp/azurerm v3.85.0
+ provider registry.terraform.io/hashicorp/null v3.2.2

Providers required by configuration:
.
├── provider[registry.terraform.io/hashicorp/aws] (v5.31.0)
├── provider[registry.terraform.io/hashicorp/azurerm] (v3.85.0)
└── provider[registry.terraform.io/hashicorp/null] (v3.2.2)

module.networking
├── provider[registry.terraform.io/hashicorp/aws] (v5.31.0)
└── provider[registry.terraform.io/hashicorp/null] (v3.2.2)
```

!!! warning "Common errors"
    **`Error: Invalid or unsupported block type on main.tf line 42, in resource "aws_instance" "web"`** — Review the resource block syntax and ensure the resource type matches the provider schema.
    **`Error: Unsupported argument on variables.tf line 15, in variable "instance_count"`** — Remove or correct the argument name; check the Terraform documentation for valid variable block arguments.
    **`Error: Failed to query available provider versions on registry.terraform.io`** — Verify internet connectivity and that the provider registry is accessible, or configure a custom registry mirror.
---

## Step 2 — Enable debug logging

```bash
# Enable trace-level logging (most verbose — includes all provider API calls)
export TF_LOG=TRACE
export TF_LOG_PATH=./terraform-debug-$(date +%F-%H%M).log
terraform plan 2>&1 | tee /tmp/tf-plan-output.txt

# Provider-only trace (reduces noise if only provider API calls are needed)
export TF_LOG_PROVIDER=DEBUG
export TF_LOG=INFO
terraform plan 2>&1 | tee /tmp/tf-plan-output.txt

# After diagnosis — unset to avoid trace log overhead
unset TF_LOG TF_LOG_PROVIDER TF_LOG_PATH

# Search the trace log for the root cause
grep -i "error\|fail\|denied\|unauthorized" terraform-debug-*.log | head -50

# Find provider API calls and their response codes
grep -E "HTTP.*[45][0-9][0-9]" terraform-debug-*.log | head -20
```


```text title="Expected output"
terraform-debug-2025-01-15-1423.log

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # aws_instance.web[0] will be updated in-place
  ~ resource "aws_instance" "web" {
      ~ tags = {
          ~ "Environment" = "staging" -> "production"
        }
    }

Plan: 0 to add, 1 to change, 0 to destroy.

2025-01-15T14:23:47.823Z [DEBUG] provider.terraform-provider-aws: {"jsonrpc":"2.0","id":42,"method":"ApplyResourceChange","params":{"typeName":"aws_instance","priorState":{"values":{"ami":"ami-0c55b159cbfafe1f0"}}}}
2025-01-15T14:23:48.156Z [DEBUG] provider.terraform-provider-aws: HTTP 200 OK - DescribeInstances completed successfully
2025-01-15T14:23:49.234Z [WARN] provider.terraform-provider-aws: Rate limit approaching - 45 requests remaining in current window

terraform-debug-2025-01-15-1423.log:2025-01-15T14:23:50.891Z [ERROR] provider.terraform-provider-aws: AccessDenied: User: arn:aws:iam::123456789012:user/terraform is not authorized to perform: ec2:ModifyInstanceAttribute on resource: arn:aws:ec2:us-east-1:123456789012:instance/i-0abcd1234efgh5678
terraform-debug-2025-01-15-1423.log:2025-01-15T14:23:51.102Z [ERROR] Terraform encountered an error: failed to update resource

terraform-debug-2025-01-15-1423.log:2025-01-15T14:23:48.445Z [DEBUG] provider.terraform-provider-aws: HTTP 403 Forbidden - ModifyInstanceAttribute denied
terraform-debug-2025-01-15-1423.log:2025-01-15T14:23:49.667Z [DEBUG] provider.terraform-provider-aws: HTTP 401 Unauthorized - Invalid AWS credentials
```

!!! warning "Common errors"
    **`AccessDenied: User: arn:aws:iam::123456789012:user/terraform is not authorized to perform: ec2:ModifyInstanceAttribute`** — Add the required IAM policy action `ec2:ModifyInstanceAttribute` to the Terraform user's IAM role or policy.
    **`HTTP 403 Forbidden`** — Verify AWS credentials are correct and the IAM user/role has permissions for the resource being modified; check credential expiration with `aws sts get-caller-identity`.
    **`HTTP 401 Unauthorized - Invalid AWS credentials`** — Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are set correctly or update your AWS credentials file at `~/.aws/credentials`.
---

## Step 3 — Debug provider authentication

```bash
# List provider plugins installed in the working directory
terraform providers

# Check which credentials are configured in environment variables
# AWS:
env | grep -E "AWS_ACCESS_KEY|AWS_SECRET|AWS_SESSION_TOKEN|AWS_PROFILE|AWS_REGION"
aws sts get-caller-identity    # Verify the identity Terraform will use

# Azure:
env | grep -E "ARM_CLIENT|ARM_TENANT|ARM_SUBSCRIPTION|ARM_USE_MSI"
az account show                # Verify Azure identity

# GCP:
env | grep GOOGLE_CREDENTIALS
gcloud auth application-default print-access-token | head -c 50

# vSphere (govmomi-based providers):
env | grep -E "VSPHERE_USER|VSPHERE_PASSWORD|VSPHERE_SERVER"
govc about -u "https://${VSPHERE_USER}:${VSPHERE_PASSWORD}@${VSPHERE_SERVER}"

# For profile-based AWS auth (multiple accounts):
aws configure list
cat ~/.aws/credentials | grep -A3 "\[<profile-name>\]"
# To use a specific profile in Terraform:
export AWS_PROFILE=<profile-name>

# For Terraform Cloud authentication:
terraform login
# Verify: ~/.terraform.d/credentials.tfrc.json exists and contains token for app.terraform.io
```


```text title="Expected output"
Providers required by configuration:
.
└── provider[registry.terraform.io/hashicorp/aws]

AWS_ACCESS_KEY_ID=AKIA2EXAMPLE1234567
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG+39POPBGQ8ExampleKey
AWS_REGION=us-east-1
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/terraform-admin"
}

ARM_CLIENT_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890
ARM_TENANT_ID=f1e2d3c4-b5a6-7890-1234-567890abcdef
ARM_SUBSCRIPTION_ID=12345678-1234-1234-1234-123456789012
{
  "id": "12345678-1234-1234-1234-123456789012",
  "name": "Production",
  "state": "Enabled"
}

GOOGLE_CREDENTIALS=/home/user/.config/gcloud/application_default_credentials.json
eyJhbGciOiJSUzI1NiIsImtpZCI6IjEyMzQ1Njc4OTBhYmNkZWY...

          User: terraform@vsphere.local
       vCenter: vcenter.example.com
        Logged in as: terraform@vsphere.local
     API Version: 7.0.2

     Access key Id                      AKIA2EXAMPLE1234567
     Secret access key                  ****
     MFA serial number                  arn:aws:iam::123456789012:mfa/user
     role ARN                           arn:aws:iam::123456789012:role/terraform-role
     role session name                  terraform-session
     source profile                     default

[prod-account]
aws_access_key_id = AKIA3EXAMPLE9876543
aws_secret_access_key = aBc1XyZ9DefGhIjKlMnOpQrStUvWxYz2Example

Terraform will be configured to use the Terraform Cloud/Enterprise credentials in:
  /home/user/.terraform.d/credentials.tfrc.json

Success! Terraform has obtained and saved an API token.
```

!!! warning "Common errors"
    **`Error: Failed to query available provider packages could not query provider registry for registry.terraform.io/hashicorp/aws: no credentials found`** — Ensure at least one credential environment variable (AWS_ACCESS_KEY_ID, ARM_CLIENT_ID, GOOGLE_CREDENTIALS, or VSPHERE_USER) is properly set before running Terraform.
    **`error: VSPHERE_PASSWORD: command not found`** — Wrap the govc command in quotes or escape special characters, or use a credentials file instead of environment variables for vSphere authentication.
    **`Error: Failed to retrieve caller identity: InvalidClientId.NotFound`** — Verify the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are correct and the IAM user has not been deleted or disabled.
---

## Step 4 — Inspect and audit state

```bash
# Safe state inspection commands (read-only, no changes)

# List all resources tracked in state
terraform state list
# Each line: resource_type.resource_name (e.g., aws_instance.web01)

# Show all attributes for a specific resource
terraform state show aws_instance.web01
# Compare these values to what the cloud console shows
# Discrepancies = drift; resolve with terraform refresh or targeted import

# Pull remote state as JSON for offline inspection
terraform state pull | jq '.' > /tmp/state-$(date +%F).json
# Count resources in state
terraform state pull | jq '.resources | length'
# Find a specific resource by attribute value
terraform state pull | jq '.resources[] | select(.type == "aws_s3_bucket") | {name, instances}'

# Check backend configuration
cat .terraform/terraform.tfstate          # local; shows which workspace is active
# For S3 backend: also check DynamoDB for an active lock entry
aws dynamodb scan --table-name <lock-table-name> --filter-expression "attribute_exists(LockID)"
```


```text title="Expected output"
aws_instance.web01
aws_instance.web02
aws_s3_bucket.logs
aws_iam_role.lambda_exec
aws_dynamodb_table.sessions
...

# resource "aws_instance" "web01":
resource "aws_instance" "web01" {
  id                   = "i-0a7f2c9e1b4d5f8a2"
  ami                  = "ami-0c55b159cbfafe1f0"
  instance_type        = "t3.medium"
  private_ip           = "10.0.1.42"
  public_ip            = "203.0.113.87"
  availability_zone    = "us-east-1a"
  vpc_security_group_ids = ["sg-0f1a2b3c4d5e6f7a8"]
  tags = {
    Name = "web01"
    Environment = "production"
  }
}

5

{
  "name": "prod-logs",
  "instances": [
    {
      "index_key": null,
      "attributes": {
        "bucket": "prod-logs-2024",
        "region": "us-east-1"
      }
    }
  ]
}

{
  "version": 4,
  "terraform_version": "1.6.2",
  "serial": 247,
  "lineage": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "outputs": {},
  "resources": [...]
}

Item: {LockID: {S: "prod/terraform.tfstate"}, Digest: {S: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"}, Operation: {S: "OperationTypeApply"}, Info: {S: "user@admin-laptop"}, Path: {S: "prod"}, Created: {N: "1704067200"}}
```

!!! warning "Common errors"
    **`Error: error reading state: state file not found`** — Ensure you are in the correct Terraform working directory and have initialized the backend with `terraform init`.
    **`Error: error reading the S3 bucket in the current account: AccessDenied`** — Verify your AWS credentials have `s3:GetObject` and `dynamodb:Scan` permissions for the state bucket and lock table.
---

## Step 5 — Diagnose backend connectivity

```bash
# Re-initialize the backend (safe — does not change state)
terraform init -reconfigure
# If this fails, the backend endpoint is unreachable or credentials lack access

# For S3 backend — test directly
aws s3 ls s3://<state-bucket>/<state-prefix>/
# Expected: lists state file(s); if AccessDenied = IAM permission issue

# For Azure blob backend
az storage blob list \
  --account-name <storage-account> \
  --container-name <container> \
  --prefix <workspace-key> \
  --auth-mode login

# For Terraform Cloud
curl -s -H "Authorization: Bearer $(cat ~/.terraform.d/credentials.tfrc.json | jq -r '.credentials."app.terraform.io".token')" \
  "https://app.terraform.io/api/v2/organizations" | jq '.data[].attributes.name'
# Expected: your organization name

# Diagnose state lock (S3 + DynamoDB backend)
# Check if a lock exists in DynamoDB
aws dynamodb get-item \
  --table-name <dynamodb-lock-table> \
  --key '{"LockID": {"S": "<s3-bucket>/<state-prefix>/terraform.tfstate-md5"}}' \
  --query 'Item'
# If output is non-empty, a lock is active; note the LockID for force-unlock
```


```text title="Expected output"
Initializing the backend...
Successfully configured the backend "s3"!

Terraform has been successfully initialized!

2024-01-15T09:42:33Z        0 2024-01-15T08:12:44Z PRD/terraform.tfstate
2024-01-15T09:42:33Z        0 2024-01-15T08:12:44Z PRD/terraform.tfstate.backup

{
  "name": "my-org",
  "created-at": "2023-11-20T14:22:15.000Z",
  "email": "ops@example.com"
}

{
    "Item": {
        "LockID": {
            "S": "terraform-state-prod/terraform.tfstate-md5"
        },
        "Digest": {
            "S": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
        },
        "Operation": {
            "S": "OperationTypeApply"
        },
        "Info": {
            "S": "user@hostname"
        },
        "Who": {
            "S": "terraform@prod-runner"
        },
        "Version": {
            "S": "1.6.2"
        },
        "Created": {
            "N": "1705318953"
        }
    }
}
```

!!! warning "Common errors"
    **`An error occurred (AccessDenied) when calling the ListBucket operation: Access Denied`** — Verify the IAM role/user has `s3:ListBucket` and `s3:GetObject` permissions on the state bucket.
    **`Error: error reading the backend configuration: unsupported attribute "region"`** — Remove or correct the region attribute in the backend block; use `aws_region` environment variable instead.
    **`error: Item not found`** — No lock exists; if Terraform is hanging, check for network connectivity to DynamoDB or verify the lock table name matches your backend configuration.
---

## Step 6 — State lock recovery (caution)

```bash
# SAFE: Back up state before any lock operation
terraform state pull > /tmp/state-backup-$(date +%F-%H%M).tfstate

# Check the lock info (Terraform includes lock ID in the error message)
# Error looks like: "Error: Error locking state: Error acquiring the state lock"
# Note the Lock ID from the error message

# Verify the locking process is truly gone before unlocking
# For CI/CD runners: check if the pipeline run that acquired the lock has terminated
# For local workstations: check if another terminal session is running terraform

# Unlock only when you are certain no other process holds the lock
terraform force-unlock <lock-id>
# This is irreversible; if a legitimate apply was in progress, it will continue writing to
# a state that is now also unlocked — resulting in corrupted state

# After force-unlock: immediately run plan to verify state consistency
terraform plan
```


```text title="Expected output"
state-backup-2024-01-15-143022.tfstate
(no output — command completes silently)

Acquiring state lock. This may take a few moments...
Acquiring state lock. This may take a few moments...

Terraform will perform the following actions:

  # aws_instance.web will be updated in-place
  ~ resource "aws_instance" "web" {
      ~ tags = {
          ~ "Environment" = "staging" -> "production"
        }
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

!!! warning "Common errors"
    **`Error: Error locking state: Error acquiring the state lock: ConditionalCheckFailedException: The conditional request failed`** — Run `terraform force-unlock <lock-id>` only after confirming no active terraform process holds the lock by checking CI/CD pipeline status or other terminal sessions.
    **`Error: error reading state: failed to read state from backend: AccessDenied: User is not authorized to perform: dynamodb:GetItem`** — Verify your AWS credentials have DynamoDB read/write permissions for the state lock table (typically `terraform-locks`).
---

## Plan inspection

```bash
# Save a plan in binary format, then inspect
terraform plan -out=tfplan
terraform show tfplan                 # Human-readable

# Machine-readable JSON plan
terraform show -json tfplan | jq '.' > /tmp/plan.json

# Find all resources that will change
terraform show -json tfplan | jq '.resource_changes[] | select(.change.actions[] != "no-op") | {address, actions: .change.actions}'

# Find resources that will be destroyed
terraform show -json tfplan | jq '.resource_changes[] | select(.change.actions[] == "delete") | .address'

# Visualise resource dependency graph
terraform graph | dot -Tsvg > /tmp/tf-graph.svg
# Open in a browser or SVG viewer to trace dependency cycles
```


```text title="Expected output"
Terraform used the following default actions for this workspace: apply

Terraform will perform the following actions:

  # aws_instance.web[0] will be created
  + resource "aws_instance" "web" {
      + ami           = "ami-0c55b159cbfafe1f0"
      + instance_type = "t3.micro"
      + tags          = {
          + "Name" = "web-server-01"
        }
    }

  # aws_security_group.allow_http will be updated in-place
  ~ resource "aws_security_group" "allow_http" {
      ~ ingress {
          + cidr_blocks = [
              + "0.0.0.0/0",
            ]
          + from_port   = 80
          + protocol    = "tcp"
          + to_port     = 80
        }
    }

  # aws_rds_instance.primary will be destroyed
  - resource "aws_rds_instance" "primary" {
      - allocated_storage    = 20
      - engine               = "postgres"
      - identifier           = "prod-db-01"
    }

Plan: 2 to add, 1 to change, 1 to destroy.

────────────────────────────────────────────────────────────────────────────────

Saved the plan to: tfplan

To perform exactly these actions, run the command below
to apply:
    terraform apply tfplan

digraph {
	compound = true
	newrank = true
	subgraph "root" {
		"[root] aws_instance.web[0]" [label = "aws_instance.web[0]", shape = "box"]
		"[root] aws_security_group.allow_http" [label = "aws_security_group.allow_http", shape = "box"]
		"[root] aws_instance.web[0]" -> "[root] aws_security_group.allow_http"
	}
}
```

!!! warning "Common errors"
    **`Error: No configuration files found in working directory.`** — Run `terraform init` first to initialize the working directory and download required providers.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure the plan file exists and is valid by running `terraform plan -out=tfplan` before attempting to parse it with `jq`.
    **`Error: Graphviz not found in PATH`** — Install Graphviz with `apt-get install graphviz` (Ubuntu/Debian) or `brew install graphviz` (macOS) to convert the graph to SVG format.
---

## See also

- [Terraform — Common Issues](../common-issues/)
- [Terraform — Escalation](../escalation/)
- [Terraform — Health Checks](../../operations/health-checks/)

## Verify resolution

- `terraform validate` returns `"The configuration is valid."`
- `terraform plan` shows the expected set of changes (or `No changes.`) with no errors
- `terraform state list` matches the expected set of managed resources
- For backend issues: `terraform init` completes without error and state is accessible
- After any state manipulation: run `terraform plan` and confirm no unexpected changes appear
