# Scripts

> Part of the [Terraform](../) reference.

---

## State Drift Detection (Bash)

Wrapper around `terraform plan` that detects configuration drift in a given workspace, parses the change summary, and alerts if drift is found. Suitable for scheduled execution.

~~~bash
#!/usr/bin/env bash
# tf-drift-detect.sh
# Usage: TF_DIR=<path> TF_WORKSPACE=<workspace> ./tf-drift-detect.sh
#
# Exit codes: 0=no drift, 1=drift detected or error

set -euo pipefail

TF_DIR="${TF_DIR:?TF_DIR is required}"
TF_WORKSPACE="${TF_WORKSPACE:-default}"
PLANFILE="/tmp/tfplan-$(date +%Y%m%d%H%M%S).out"
ALERT_WEBHOOK="${ALERT_WEBHOOK:-}"   # Optional: Slack/Teams webhook URL
LOGFILE="/var/log/tf-drift-$(date +%Y%m%d-%H%M%S).log"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

cleanup() { rm -f "${PLANFILE}" "${PLANFILE}.json"; }
trap cleanup EXIT

log "=== Terraform Drift Detection ==="
log "Directory : ${TF_DIR}"
log "Workspace : ${TF_WORKSPACE}"

cd "${TF_DIR}"

# --- Step 1: Select workspace ---
log "Step 1: Selecting workspace '${TF_WORKSPACE}'..."
terraform workspace select "${TF_WORKSPACE}" 2>&1 | tee -a "${LOGFILE}"

# --- Step 2: Init ---
log "Step 2: Running terraform init -reconfigure..."
terraform init -reconfigure -input=false 2>&1 | tee -a "${LOGFILE}"

# --- Step 3: Plan with detailed exit code ---
log "Step 3: Running terraform plan..."
set +e
terraform plan -detailed-exitcode -input=false -out="${PLANFILE}" 2>&1 | tee -a "${LOGFILE}"
PLAN_RC=$?
set -e

# --- Step 4: Interpret exit code ---
case "${PLAN_RC}" in
    0)
        log "RESULT: No changes. Infrastructure matches configuration."
        exit 0
        ;;
    1)
        log "RESULT: ERROR — terraform plan encountered an error."
        exit 1
        ;;
    2)
        log "RESULT: DRIFT DETECTED — configuration changes exist."
        ;;
    *)
        log "RESULT: Unexpected plan exit code: ${PLAN_RC}"
        exit 1
        ;;
esac

# --- Step 5: Parse change summary ---
log "Step 5: Parsing resource change summary..."
terraform show -json "${PLANFILE}" > "${PLANFILE}.json"

SUMMARY=$(python3 - <<EOF
import json, sys

with open('${PLANFILE}.json') as f:
    plan = json.load(f)

changes = plan.get('resource_changes', [])
to_add     = [c['address'] for c in changes if 'create' in c.get('change', {}).get('actions', [])]
to_change  = [c['address'] for c in changes if 'update' in c.get('change', {}).get('actions', [])]
to_destroy = [c['address'] for c in changes if 'delete' in c.get('change', {}).get('actions', [])]

print(f"Add: {len(to_add)}, Change: {len(to_change)}, Destroy: {len(to_destroy)}")
print()
for r in to_add:
    print(f"  + {r}")
for r in to_change:
    print(f"  ~ {r}")
for r in to_destroy:
    print(f"  - {r}")
EOF
)

log "Change summary:"
echo "${SUMMARY}" | while IFS= read -r line; do log "  ${line}"; done

# --- Step 6: Send alert if webhook configured ---
if [[ -n "${ALERT_WEBHOOK}" ]]; then
    log "Step 6: Sending drift alert..."
    PAYLOAD=$(python3 -c "
import json
msg = 'Terraform drift detected in workspace ${TF_WORKSPACE} (${TF_DIR}):\n${SUMMARY}'
print(json.dumps({'text': msg}))
")
    curl -s -X POST -H "Content-Type: application/json" \
        -d "${PAYLOAD}" "${ALERT_WEBHOOK}" > /dev/null
    log "Alert sent to webhook."
fi

log "Log: ${LOGFILE}"
exit 1
~~~

---

## Multi-Workspace Deploy Script (Bash)

Deploy Terraform across dev, staging, and prod workspaces in sequence. Prompts for approval before each workspace (unless auto-approve is configured for dev). Stops and alerts on any workspace failure.

~~~bash
#!/usr/bin/env bash
# tf-multi-workspace-deploy.sh
# Usage: TF_DIR=<path> ./tf-multi-workspace-deploy.sh [--destroy]
#
# Set AUTO_APPROVE_DEV=true to skip approval for dev workspace.

set -euo pipefail

TF_DIR="${TF_DIR:?TF_DIR is required}"
WORKSPACES=("dev" "staging" "prod")
AUTO_APPROVE_DEV="${AUTO_APPROVE_DEV:-false}"
DESTROY=false
LOGFILE="/var/log/tf-deploy-$(date +%Y%m%d-%H%M%S).log"

for arg in "$@"; do
    [[ "$arg" == "--destroy" ]] && DESTROY=true
done

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

alert_failure() {
    local ws="$1"
    log "ALERT: Deployment failed in workspace '${ws}'. Stopping pipeline."
    log "Review errors above and check state with: terraform workspace select ${ws} && terraform plan"
}

cd "${TF_DIR}"

log "=== Terraform Multi-Workspace Deploy ==="
log "Directory   : ${TF_DIR}"
log "Workspaces  : ${WORKSPACES[*]}"
${DESTROY} && log "MODE: DESTROY" || log "MODE: APPLY"

for WS in "${WORKSPACES[@]}"; do
    log ""
    log "--- Workspace: ${WS} ---"

    # Select workspace
    log "Selecting workspace '${WS}'..."
    terraform workspace select "${WS}" 2>&1 | tee -a "${LOGFILE}"

    # Init
    log "Running terraform init..."
    terraform init -reconfigure -input=false 2>&1 | tee -a "${LOGFILE}"

    # Plan
    PLANFILE="/tmp/tfplan-${WS}-$(date +%Y%m%d%H%M%S).out"
    if ${DESTROY}; then
        log "Planning destroy for workspace '${WS}'..."
        terraform plan -destroy -detailed-exitcode -input=false -out="${PLANFILE}" 2>&1 | tee -a "${LOGFILE}" || true
    else
        log "Planning for workspace '${WS}'..."
        terraform plan -detailed-exitcode -input=false -out="${PLANFILE}" 2>&1 | tee -a "${LOGFILE}" || true
    fi

    # Approval
    AUTO_APPROVE=false
    if [[ "${WS}" == "dev" ]] && [[ "${AUTO_APPROVE_DEV}" == "true" ]]; then
        AUTO_APPROVE=true
        log "Auto-approve enabled for dev workspace."
    fi

    if ! ${AUTO_APPROVE}; then
        echo ""
        read -r -p "Apply changes for workspace '${WS}'? [yes/no]: " CONFIRM
        if [[ "${CONFIRM}" != "yes" ]]; then
            log "Skipped workspace '${WS}' by operator choice."
            rm -f "${PLANFILE}"
            continue
        fi
    fi

    # Apply or Destroy
    if ${DESTROY}; then
        log "Running terraform destroy for workspace '${WS}'..."
        if ! terraform apply -destroy -auto-approve -input=false "${PLANFILE}" 2>&1 | tee -a "${LOGFILE}"; then
            alert_failure "${WS}"
            exit 1
        fi
    else
        log "Running terraform apply for workspace '${WS}'..."
        if ! terraform apply -auto-approve -input=false "${PLANFILE}" 2>&1 | tee -a "${LOGFILE}"; then
            alert_failure "${WS}"
            exit 1
        fi
    fi

    rm -f "${PLANFILE}"
    log "Workspace '${WS}': SUCCESS"
done

log ""
log "=== All workspaces processed successfully. ==="
log "Log: ${LOGFILE}"
~~~

---

## DR Infrastructure Provision (HCL + Bash)

Terraform templates for provisioning DR infrastructure on AWS (EC2 from AMI, RDS from snapshot, ALB) plus a Bash wrapper that runs the apply and outputs DR endpoints.

**`variables.tf`**

~~~hcl
# variables.tf — DR Infrastructure

variable "dr_region" {
  description = "AWS region for DR infrastructure"
  type        = string
  default     = "us-west-2"
}

variable "dr_ami_id" {
  description = "AMI ID to launch DR EC2 instances from"
  type        = string
}

variable "dr_instance_type" {
  description = "EC2 instance type for DR app servers"
  type        = string
  default     = "t3.large"
}

variable "dr_instance_count" {
  description = "Number of DR app server instances"
  type        = number
  default     = 2
}

variable "rds_snapshot_identifier" {
  description = "RDS snapshot ARN/identifier to restore from"
  type        = string
}

variable "rds_instance_class" {
  description = "RDS instance class for DR database"
  type        = string
  default     = "db.t3.medium"
}

variable "vpc_id" {
  description = "VPC ID for DR resources"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for DR resources (at least 2 AZs)"
  type        = list(string)
}

variable "environment" {
  description = "Environment tag value"
  type        = string
  default     = "dr"
}

variable "app_name" {
  description = "Application name for tagging"
  type        = string
}
~~~

**`main.tf`**

~~~hcl
# main.tf — DR Infrastructure

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.dr_region
}

# --- Security Group for app servers ---
resource "aws_security_group" "dr_app" {
  name        = "${var.app_name}-dr-app-sg"
  description = "DR app server security group"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.app_name}-dr-app-sg"
    Environment = var.environment
    Application = var.app_name
    Owner       = "infra"
    CostCenter  = "dr"
  }
}

# --- EC2 Instances from AMI ---
resource "aws_instance" "dr_app" {
  count         = var.dr_instance_count
  ami           = var.dr_ami_id
  instance_type = var.dr_instance_type
  subnet_id     = element(var.subnet_ids, count.index % length(var.subnet_ids))

  vpc_security_group_ids = [aws_security_group.dr_app.id]

  # Start stopped — operator activates during DR event
  # Remove this if instances should be running continuously
  # monitoring = true

  tags = {
    Name        = "${var.app_name}-dr-app-${count.index + 1}"
    Environment = var.environment
    Application = var.app_name
    Owner       = "infra"
    CostCenter  = "dr"
  }
}

# --- RDS restored from snapshot ---
resource "aws_db_instance" "dr_db" {
  identifier              = "${var.app_name}-dr-db"
  snapshot_identifier     = var.rds_snapshot_identifier
  instance_class          = var.rds_instance_class
  skip_final_snapshot     = true
  publicly_accessible     = false
  vpc_security_group_ids  = [aws_security_group.dr_app.id]
  db_subnet_group_name    = aws_db_subnet_group.dr.name
  apply_immediately       = true

  tags = {
    Name        = "${var.app_name}-dr-db"
    Environment = var.environment
    Application = var.app_name
    Owner       = "infra"
    CostCenter  = "dr"
  }
}

resource "aws_db_subnet_group" "dr" {
  name       = "${var.app_name}-dr-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Environment = var.environment
    Application = var.app_name
    Owner       = "infra"
    CostCenter  = "dr"
  }
}

# --- Application Load Balancer ---
resource "aws_lb" "dr_alb" {
  name               = "${var.app_name}-dr-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.dr_app.id]
  subnets            = var.subnet_ids

  tags = {
    Name        = "${var.app_name}-dr-alb"
    Environment = var.environment
    Application = var.app_name
    Owner       = "infra"
    CostCenter  = "dr"
  }
}

resource "aws_lb_target_group" "dr_app" {
  name     = "${var.app_name}-dr-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/health"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "dr_https" {
  load_balancer_arn = aws_lb.dr_alb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  # certificate_arn = "<your-ACM-cert-ARN>"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.dr_app.arn
  }
}

resource "aws_lb_target_group_attachment" "dr_app" {
  count            = var.dr_instance_count
  target_group_arn = aws_lb_target_group.dr_app.arn
  target_id        = aws_instance.dr_app[count.index].id
  port             = 80
}
~~~

**`outputs.tf`**

~~~hcl
# outputs.tf — DR Infrastructure

output "dr_alb_dns_name" {
  description = "DNS name of the DR Application Load Balancer"
  value       = aws_lb.dr_alb.dns_name
}

output "dr_app_instance_ids" {
  description = "EC2 instance IDs of DR app servers"
  value       = aws_instance.dr_app[*].id
}

output "dr_db_endpoint" {
  description = "RDS endpoint for the DR database"
  value       = aws_db_instance.dr_db.endpoint
}

output "dr_db_port" {
  description = "RDS port for the DR database"
  value       = aws_db_instance.dr_db.port
}
~~~

**Bash wrapper**

~~~bash
#!/usr/bin/env bash
# tf-dr-provision.sh
# Usage: TF_DIR=<path> ./tf-dr-provision.sh
# Expects terraform.tfvars or env vars for variable values.

set -euo pipefail

TF_DIR="${TF_DIR:?TF_DIR is required}"
LOGFILE="/var/log/tf-dr-provision-$(date +%Y%m%d-%H%M%S).log"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

log "=== DR Infrastructure Provision ==="
log "Directory: ${TF_DIR}"
cd "${TF_DIR}"

log "Running terraform init..."
terraform init -reconfigure -input=false 2>&1 | tee -a "${LOGFILE}"

log "Running terraform apply..."
terraform apply -auto-approve -input=false 2>&1 | tee -a "${LOGFILE}"

log ""
log "=== DR Endpoints ==="
ALB_DNS=$(terraform output -raw dr_alb_dns_name 2>/dev/null || echo "not available")
DB_ENDPOINT=$(terraform output -raw dr_db_endpoint 2>/dev/null || echo "not available")

log "ALB DNS    : ${ALB_DNS}"
log "DB Endpoint: ${DB_ENDPOINT}"
log ""
log "Provision complete. Log: ${LOGFILE}"

echo ""
echo "DR_ALB_ENDPOINT=${ALB_DNS}"
echo "DR_DB_ENDPOINT=${DB_ENDPOINT}"
~~~

---

## Resource Tagging Compliance Check (Python)

Parse `terraform show -json` output from the current state file and verify that every resource carries the required tags: Owner, Environment, CostCenter, Application.

~~~python
#!/usr/bin/env python3
# tf-tag-compliance.py
# Usage: python3 tf-tag-compliance.py [--state terraform.tfstate]
#        Or pipe: terraform show -json terraform.tfstate | python3 tf-tag-compliance.py
#
# Can be used as a pre-commit hook or CI gate.
# Exit codes: 0=all compliant, 1=violations found

import json
import sys
import subprocess
import argparse

REQUIRED_TAGS = {"Owner", "Environment", "CostCenter", "Application"}


def load_state(state_file: str | None) -> dict:
    if state_file:
        result = subprocess.run(
            ["terraform", "show", "-json", state_file],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    else:
        # Read from stdin if piped
        if not sys.stdin.isatty():
            return json.load(sys.stdin)
        # Default: use current workspace state
        result = subprocess.run(
            ["terraform", "show", "-json"],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)


def get_resource_tags(resource: dict) -> dict:
    values = resource.get("values", {})
    return values.get("tags", {}) or {}


def check_resources(state: dict) -> list[dict]:
    results = []
    resources = state.get("values", {}).get("root_module", {}).get("resources", [])

    # Also check child modules
    child_modules = state.get("values", {}).get("root_module", {}).get("child_modules", [])
    for module in child_modules:
        resources.extend(module.get("resources", []))

    for resource in resources:
        res_type    = resource.get("type", "")
        res_name    = resource.get("name", "")
        res_address = resource.get("address", f"{res_type}.{res_name}")
        mode        = resource.get("mode", "managed")

        # Only check managed resources
        if mode != "managed":
            continue

        # Data sources and some resource types don't support tags
        if res_type.startswith("aws_iam_policy_document") or res_type.startswith("random_"):
            continue

        tags         = get_resource_tags(resource)
        missing_tags = REQUIRED_TAGS - set(tags.keys())
        compliant    = len(missing_tags) == 0

        results.append({
            "address":     res_address,
            "type":        res_type,
            "compliant":   compliant,
            "present_tags": list(tags.keys()),
            "missing_tags": sorted(missing_tags),
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Terraform tag compliance checker")
    parser.add_argument("--state", default=None, help="Path to terraform state file")
    args = parser.parse_args()

    try:
        state = load_state(args.state)
    except subprocess.CalledProcessError as e:
        sys.exit(f"ERROR: Failed to read Terraform state: {e.stderr}")
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: Invalid JSON from terraform show: {e}")

    results = check_resources(state)

    if not results:
        print("No managed resources found in state.")
        sys.exit(0)

    print()
    print("=== Terraform Resource Tagging Compliance ===")
    print(f"Required tags: {', '.join(sorted(REQUIRED_TAGS))}")
    print()
    print(f"{'Resource':<55} {'Compliant':<10} {'Missing Tags'}")
    print("-" * 90)

    violations = []
    for r in results:
        status  = "PASS" if r["compliant"] else "FAIL"
        missing = ", ".join(r["missing_tags"]) if r["missing_tags"] else ""
        flag    = "  <-- NON-COMPLIANT" if not r["compliant"] else ""
        print(f"{r['address']:<55} {status:<10} {missing}{flag}")
        if not r["compliant"]:
            violations.append(r)

    print()
    print(f"Total resources checked : {len(results)}")
    print(f"Compliant               : {len(results) - len(violations)}")
    print(f"Non-compliant           : {len(violations)}")

    if violations:
        print()
        print("Non-compliant resources:")
        for v in violations:
            print(f"  {v['address']}")
            print(f"    Missing: {', '.join(v['missing_tags'])}")
        sys.exit(1)
    else:
        print()
        print("RESULT: All resources are tag-compliant.")
        sys.exit(0)


if __name__ == "__main__":
    main()
~~~
