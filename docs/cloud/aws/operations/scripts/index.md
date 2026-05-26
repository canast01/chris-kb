# AWS — Scripts

> Part of the [Operations](../index.md) section.

---

## AWS Account Health Check

Prints a formatted section-by-section health report for EC2 instances, RDS databases, and load balancers. Exits non-zero if any instances are found in a stopped state.

~~~bash
#!/bin/bash
set -euo pipefail

AWS_PROFILE="${AWS_PROFILE:-default}"
AWS_REGION="${AWS_REGION:-us-east-1}"

export AWS_PROFILE AWS_REGION

BOLD="\033[1m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
GREEN="\033[0;32m"
RESET="\033[0m"

STOPPED_COUNT=0

echo -e "${BOLD}=== AWS Account Health Check ===${RESET}"
echo "Profile : ${AWS_PROFILE}"
echo "Region  : ${AWS_REGION}"
echo "Time    : $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

# --- Identity ---
echo -e "${BOLD}--- Caller Identity ---${RESET}"
aws sts get-caller-identity
echo

# --- EC2 Instances ---
echo -e "${BOLD}--- EC2 Instances ---${RESET}"
INSTANCE_TABLE=$(aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,Tags[?Key==`Name`].Value|[0]]' \
  --output table)
echo "${INSTANCE_TABLE}"

STOPPED_COUNT=$(aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=stopped" \
  --query 'length(Reservations[*].Instances[*])' \
  --output text)

if [[ "${STOPPED_COUNT}" -gt 0 ]]; then
  echo -e "${RED}WARNING: ${STOPPED_COUNT} stopped instance(s) found.${RESET}"
else
  echo -e "${GREEN}All instances running.${RESET}"
fi
echo

# --- RDS ---
echo -e "${BOLD}--- RDS Instances ---${RESET}"
aws rds describe-db-instances \
  --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus,Engine,DBInstanceClass]' \
  --output table
echo

# --- Load Balancers ---
echo -e "${BOLD}--- Load Balancers (ELBv2) ---${RESET}"
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[*].[LoadBalancerName,State.Code,Type,DNSName]' \
  --output table
echo

# --- Exit code ---
if [[ "${STOPPED_COUNT}" -gt 0 ]]; then
  echo -e "${RED}Health check FAILED: stopped instances detected.${RESET}"
  exit 1
fi

echo -e "${GREEN}Health check PASSED.${RESET}"
~~~

### How to run this script — step by step

**Before you start — what you need**
- AWS CLI installed (download from https://aws.amazon.com/cli/)
- An AWS account with credentials configured via `aws configure`
- Git for Windows installed so you have Git Bash (download from https://gitforwindows.org)

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files** (important — prevents Notepad adding .txt)
5. Name it `aws-health-check.sh` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `AWS_PROFILE` | Your AWS CLI profile name | Run `aws configure list-profiles` to see your profiles |
| `AWS_REGION` | Your AWS region, e.g. `eu-west-1` | AWS Console → top-right region selector |

**Step 3 — Open the right terminal**

- **For .sh (Bash):** Install Git for Windows (gitforwindows.org) → open Git Bash

**Step 4 — Run it**

```bash
cd ~/Desktop
bash aws-health-check.sh
```

**What you should see**

A table of your EC2 instances with their state (running/stopped), a list of RDS databases, and load balancers. If any EC2 instances are stopped you will see a red WARNING line and the script exits with an error code.

---

## EC2 Instance Audit

Connects to all regions (or a configurable list), lists every EC2 instance with metadata, flags instances with common compliance issues, and exports a CSV report.

~~~python
#!/usr/bin/env python3
"""EC2 Instance Audit — flags stopped, untagged, default-VPC, and public-IP instances."""

import boto3
import csv
import sys
import datetime
from typing import Optional

# --- Configuration ---
REGIONS: list[str] = []          # Empty = all enabled regions
OUTPUT_FILE = "ec2_audit.csv"
STOPPED_DAYS_THRESHOLD = 7       # Flag instances stopped longer than this

# ---------------------

def get_regions(session: boto3.Session) -> list[str]:
    if REGIONS:
        return REGIONS
    ec2 = session.client("ec2", region_name="us-east-1")
    return [r["RegionName"] for r in ec2.describe_regions(Filters=[{"Name": "opt-in-status", "Values": ["opt-in-not-required", "opted-in"]}])["Regions"]]

def get_tag(tags: list, key: str) -> Optional[str]:
    if not tags:
        return None
    for t in tags:
        if t["Key"] == key:
            return t["Value"]
    return None

def get_default_vpc(ec2_client) -> Optional[str]:
    vpcs = ec2_client.describe_vpcs(Filters=[{"Name": "isDefault", "Values": ["true"]}])["Vpcs"]
    return vpcs[0]["VpcId"] if vpcs else None

def days_since(dt: Optional[datetime.datetime]) -> Optional[int]:
    if dt is None:
        return None
    return (datetime.datetime.now(datetime.timezone.utc) - dt).days

def audit_region(session: boto3.Session, region: str, rows: list) -> None:
    ec2 = session.client("ec2", region_name=region)
    default_vpc = get_default_vpc(ec2)

    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for inst in reservation["Instances"]:
                iid        = inst["InstanceId"]
                itype      = inst["InstanceType"]
                state      = inst["State"]["Name"]
                launch     = inst.get("LaunchTime")
                vpc_id     = inst.get("VpcId", "")
                subnet_id  = inst.get("SubnetId", "")
                key_name   = inst.get("KeyName", "")
                public_ip  = inst.get("PublicIpAddress", "")
                profile    = (inst.get("IamInstanceProfile") or {}).get("Arn", "")
                tags       = inst.get("Tags", [])
                name       = get_tag(tags, "Name") or ""
                sgs        = ",".join(sg["GroupId"] for sg in inst.get("SecurityGroups", []))

                # --- Flags ---
                flags = []

                if state == "stopped":
                    # Approximate stopped time via launch time (not perfect but useful)
                    if launch and days_since(launch) and days_since(launch) > STOPPED_DAYS_THRESHOLD:
                        flags.append(f"STOPPED>{STOPPED_DAYS_THRESHOLD}d")

                if not name:
                    flags.append("NO_NAME_TAG")

                if vpc_id and vpc_id == default_vpc:
                    flags.append("DEFAULT_VPC")

                if not profile:
                    flags.append("NO_IAM_ROLE")

                justification = get_tag(tags, "PublicIPJustification")
                if public_ip and not justification:
                    flags.append("PUBLIC_IP_NO_JUSTIFICATION")

                rows.append({
                    "Region":        region,
                    "InstanceId":    iid,
                    "Name":          name,
                    "Type":          itype,
                    "State":         state,
                    "LaunchTime":    launch.isoformat() if launch else "",
                    "VpcId":         vpc_id,
                    "SubnetId":      subnet_id,
                    "KeyPair":       key_name,
                    "PublicIP":      public_ip,
                    "SecurityGroups": sgs,
                    "IAMProfile":    profile,
                    "Flags":         "|".join(flags),
                })

def main() -> None:
    session = boto3.Session()
    regions = get_regions(session)
    print(f"Auditing {len(regions)} region(s)...")

    rows: list[dict] = []
    for region in regions:
        try:
            audit_region(session, region, rows)
            print(f"  {region}: {len([r for r in rows if r['Region'] == region])} instances")
        except Exception as exc:
            print(f"  {region}: ERROR — {exc}", file=sys.stderr)

    if not rows:
        print("No instances found.")
        return

    fields = ["Region", "InstanceId", "Name", "Type", "State", "LaunchTime",
              "VpcId", "SubnetId", "KeyPair", "PublicIP", "SecurityGroups", "IAMProfile", "Flags"]

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    flagged = [r for r in rows if r["Flags"]]
    print(f"\nTotal instances : {len(rows)}")
    print(f"Flagged         : {len(flagged)}")
    print(f"Report written  : {OUTPUT_FILE}")

    if flagged:
        print("\nFlagged instances:")
        for r in flagged:
            print(f"  {r['Region']:20s}  {r['InstanceId']:20s}  {r['Name']:30s}  {r['Flags']}")

if __name__ == "__main__":
    main()
~~~

### How to run this script — step by step

**Before you start — what you need**
- Python installed (download from https://python.org — tick "Add Python to PATH" during install)
- AWS CLI installed and configured (`aws configure` run at least once)
- The `boto3` package installed

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `ec2_audit.py` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `REGIONS` | Leave empty for all regions, or add specific ones like `["us-east-1", "eu-west-1"]` | AWS Console → region names |
| `OUTPUT_FILE` | Where to save the CSV report | Default is `ec2_audit.csv` in the same folder |
| `STOPPED_DAYS_THRESHOLD` | Number of days stopped before flagging | Default is `7` |

**Step 3 — Open the right terminal**

- **For .py (Python):** Open Command Prompt. Install Python from python.org if not installed yet.

**Step 4 — Install the required package and run**

```bash
cd C:\Users\YourName\Desktop
pip install boto3
python ec2_audit.py
```

**What you should see**

Lines like `us-east-1: 12 instances` as it scans each region, then a summary showing total and flagged instances. A file called `ec2_audit.csv` will appear on your Desktop — open it in Excel to review flagged instances.

---

## S3 Bucket Security Audit

Lists all S3 buckets and checks public access blocks, ACL grants, bucket policy wildcards, versioning, encryption, logging, and lifecycle rules. Flags any bucket with public access enabled.

~~~python
#!/usr/bin/env python3
"""S3 Bucket Security Audit — checks public access, ACLs, policies, versioning, encryption."""

import json
import boto3
from botocore.exceptions import ClientError

s3  = boto3.client("s3")
s3r = boto3.resource("s3")

HEADER = f"{'Bucket':<45} {'PubBlock':>8} {'PubACL':>7} {'PubPolicy':>9} {'Versioning':>10} {'SSE':>5} {'Logging':>8} {'Lifecycle':>10} {'Flags'}"
SEP    = "-" * len(HEADER)

findings: list[dict] = []

def check_public_access_block(bucket: str) -> bool:
    """Returns True when ALL four block settings are enabled."""
    try:
        r = s3.get_public_access_block(Bucket=bucket)
        cfg = r["PublicAccessBlockConfiguration"]
        return all([
            cfg.get("BlockPublicAcls",       False),
            cfg.get("IgnorePublicAcls",      False),
            cfg.get("BlockPublicPolicy",     False),
            cfg.get("RestrictPublicBuckets", False),
        ])
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchPublicAccessBlockConfiguration":
            return False
        raise

def check_public_acl(bucket: str) -> bool:
    """Returns True if any ACL grant gives access to AllUsers or AuthenticatedUsers."""
    PUBLIC_GRANTEES = {
        "http://acs.amazonaws.com/groups/global/AllUsers",
        "http://acs.amazonaws.com/groups/global/AuthenticatedUsers",
    }
    try:
        acl = s3.get_bucket_acl(Bucket=bucket)
        for grant in acl.get("Grants", []):
            uri = grant.get("Grantee", {}).get("URI", "")
            if uri in PUBLIC_GRANTEES:
                return True
    except ClientError:
        pass
    return False

def check_public_policy(bucket: str) -> bool:
    """Returns True if the bucket policy has any Allow with Principal '*'."""
    try:
        policy = json.loads(s3.get_bucket_policy(Bucket=bucket)["Policy"])
        for stmt in policy.get("Statement", []):
            if stmt.get("Effect") == "Allow":
                principal = stmt.get("Principal", "")
                if principal == "*" or (isinstance(principal, dict) and "*" in principal.get("AWS", [])):
                    return True
    except ClientError as e:
        if e.response["Error"]["Code"] in ("NoSuchBucketPolicy", "AccessDenied"):
            return False
        raise
    return False

def check_versioning(bucket: str) -> str:
    try:
        status = s3.get_bucket_versioning(Bucket=bucket).get("Status", "Disabled")
        return status or "Disabled"
    except ClientError:
        return "Unknown"

def check_encryption(bucket: str) -> bool:
    try:
        s3.get_bucket_encryption(Bucket=bucket)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
            return False
        raise

def check_logging(bucket: str) -> bool:
    try:
        cfg = s3.get_bucket_logging(Bucket=bucket)
        return "LoggingEnabled" in cfg
    except ClientError:
        return False

def check_lifecycle(bucket: str) -> bool:
    try:
        rules = s3.get_bucket_lifecycle_configuration(Bucket=bucket).get("Rules", [])
        return len(rules) > 0
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchLifecycleConfiguration":
            return False
        raise

def main() -> None:
    buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    print(f"Auditing {len(buckets)} buckets...\n")
    print(HEADER)
    print(SEP)

    public_count = 0

    for name in buckets:
        pub_block   = check_public_access_block(name)
        pub_acl     = check_public_acl(name)
        pub_policy  = check_public_policy(name)
        versioning  = check_versioning(name)
        sse         = check_encryption(name)
        logging_on  = check_logging(name)
        lifecycle   = check_lifecycle(name)

        flags = []
        if not pub_block:  flags.append("NO_PUB_BLOCK")
        if pub_acl:        flags.append("PUBLIC_ACL")
        if pub_policy:     flags.append("PUBLIC_POLICY")
        if not sse:        flags.append("NO_SSE")
        if not logging_on: flags.append("NO_LOGGING")
        if versioning == "Disabled": flags.append("NO_VERSIONING")

        is_public = pub_acl or pub_policy or not pub_block
        if is_public:
            public_count += 1

        flag_str = "|".join(flags) if flags else "OK"

        print(
            f"{name:<45} "
            f"{'YES' if pub_block   else 'NO':>8} "
            f"{'YES' if pub_acl    else 'no':>7} "
            f"{'YES' if pub_policy else 'no':>9} "
            f"{versioning:>10} "
            f"{'Y' if sse         else 'N':>5} "
            f"{'Y' if logging_on  else 'N':>8} "
            f"{'Y' if lifecycle   else 'N':>10}  "
            f"{flag_str}"
        )

    print(SEP)
    print(f"\nTotal buckets  : {len(buckets)}")
    print(f"Public buckets : {public_count}")

    if public_count:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
~~~

### How to run this script — step by step

**Before you start — what you need**
- Python installed (download from https://python.org)
- AWS CLI installed and configured with credentials that have S3 read access
- The `boto3` package installed

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `s3_audit.py` and save to your Desktop

**Step 2 — Fill in your details**

This script uses your default AWS credentials automatically — no variables to change. Make sure `aws configure` has been run first.

| Variable | What to enter | Where to find it |
|---|---|---|
| AWS credentials | Set up via `aws configure` before running | AWS Console → IAM → your user → Security credentials |

**Step 3 — Open the right terminal**

- **For .py (Python):** Open Command Prompt.

**Step 4 — Install the required package and run**

```bash
cd C:\Users\YourName\Desktop
pip install boto3
python s3_audit.py
```

**What you should see**

A table with one row per S3 bucket. Each row shows YES/NO for public access blocks, ACL, policy, versioning, encryption, logging, and lifecycle. Buckets with problems show flags like `NO_PUB_BLOCK` or `PUBLIC_ACL`. The script exits with an error if any publicly accessible buckets are found.

---

## Cost and Usage Report

Queries Cost Explorer for the past N months (default 3), formats a top-10 services table, and highlights services with a cost increase greater than 20% versus the prior month.

~~~bash
#!/bin/bash
set -euo pipefail

AWS_PROFILE="${AWS_PROFILE:-default}"
MONTHS_BACK="${MONTHS_BACK:-3}"

export AWS_PROFILE

BOLD="\033[1m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
GREEN="\033[0;32m"
RESET="\033[0m"

# Build date range: first day of (today - MONTHS_BACK) to today
START_DATE=$(date -v "-${MONTHS_BACK}m" +"%Y-%m-01" 2>/dev/null || date -d "${MONTHS_BACK} months ago" +"%Y-%m-01")
END_DATE=$(date +"%Y-%m-%d")

echo -e "${BOLD}=== AWS Cost and Usage Report ===${RESET}"
echo "Profile     : ${AWS_PROFILE}"
echo "Period      : ${START_DATE} → ${END_DATE}"
echo "Months back : ${MONTHS_BACK}"
echo

RAW_JSON=$(aws ce get-cost-and-usage \
  --time-period "Start=${START_DATE},End=${END_DATE}" \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by "Type=DIMENSION,Key=SERVICE" \
  --output json)

export RAW_JSON
python3 - <<'PYEOF'
import json, os
from collections import defaultdict

data = json.loads(os.environ["RAW_JSON"])

service_months = defaultdict(dict)
month_labels   = []

for result in data["ResultsByTime"]:
    start = result["TimePeriod"]["Start"][:7]
    month_labels.append(start)
    for group in result["Groups"]:
        svc  = group["Keys"][0]
        cost = float(group["Metrics"]["BlendedCost"]["Amount"])
        service_months[svc][start] = cost

months     = sorted(set(month_labels))
prev_month = months[-2] if len(months) >= 2 else months[-1]
curr_month = months[-1]

ranked = sorted(service_months.items(), key=lambda x: x[1].get(curr_month, 0), reverse=True)
top10  = ranked[:10]

print(f"\n{'Service':<50} {prev_month:>12} {curr_month:>12} {'Change':>8}")
print("-" * 86)

for svc, mc in top10:
    prev = mc.get(prev_month, 0)
    curr = mc.get(curr_month, 0)
    pct  = (curr - prev) / prev * 100 if prev > 0 else 0.0
    flag = "  *** >20% INCREASE ***" if pct > 20 else ""
    print(f"{svc:<50} ${prev:>11.2f} ${curr:>11.2f} {pct:>+7.1f}%{flag}")
PYEOF
~~~

### How to run this script — step by step

**Before you start — what you need**
- AWS CLI installed and configured
- Cost Explorer enabled in your AWS account (it is on by default but may need enabling in Billing settings)
- Git Bash installed (from https://gitforwindows.org) to run `.sh` scripts
- Your AWS user must have the `ce:GetCostAndUsage` permission

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `aws-cost-report.sh` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `AWS_PROFILE` | Your AWS CLI profile name | Run `aws configure list-profiles` |
| `MONTHS_BACK` | How many months of history to pull | Default is `3` |

**Step 3 — Open the right terminal**

- **For .sh (Bash):** Install Git for Windows (gitforwindows.org) → open Git Bash

**Step 4 — Run it**

```bash
cd ~/Desktop
bash aws-cost-report.sh
```

**What you should see**

A table of your top 10 most expensive AWS services for the past 3 months, with a dollar amount per month and a percentage change column. Services with more than 20% cost increase are marked with `*** >20% INCREASE ***`.

---

## EC2 DR Failover Playbook (Ansible)

Copies AMIs from the source region to the DR region, launches replacement EC2 instances, waits for them to be running, and prints a summary of new instance IDs and IPs.

~~~yaml
---
# ec2_dr_failover.yml
# Requires: amazon.aws, community.aws collections
# ansible-galaxy collection install amazon.aws community.aws

- name: EC2 DR Failover
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
    source_region:  "us-east-1"
    dr_region:      "us-west-2"
    source_ami_ids: []         # e.g. ["ami-0abc123", "ami-0def456"]
    instance_type:  "t3.medium"
    dr_subnet_id:   "subnet-xxxxxxxx"
    dr_sg_ids:      []         # e.g. ["sg-xxxxxxxx"]
    key_name:       "my-dr-key"
    wait_timeout:   600

  tasks:

    - name: Get latest snapshot/AMI details from source region
      amazon.aws.ec2_ami_info:
        region:   "{{ source_region }}"
        image_ids: "{{ source_ami_ids }}"
      register: source_amis

    - name: Copy each AMI to DR region
      community.aws.ec2_ami_copy:
        region:        "{{ dr_region }}"
        source_region: "{{ source_region }}"
        source_image_id: "{{ item.image_id }}"
        name:          "DR-{{ item.name }}-{{ ansible_date_time.date }}"
        wait:          true
        wait_timeout:  "{{ wait_timeout }}"
        tags:
          Purpose:     "DR"
          SourceAMI:   "{{ item.image_id }}"
          CopiedDate:  "{{ ansible_date_time.iso8601 }}"
      loop: "{{ source_amis.images }}"
      register: dr_amis

    - name: Launch EC2 instances in DR region
      amazon.aws.ec2_instance:
        region:        "{{ dr_region }}"
        image_id:      "{{ item.image_id }}"
        instance_type: "{{ instance_type }}"
        subnet_id:     "{{ dr_subnet_id }}"
        security_groups: "{{ dr_sg_ids }}"
        key_name:      "{{ key_name }}"
        wait:          true
        wait_timeout:  "{{ wait_timeout }}"
        state:         running
        tags:
          Name:        "DR-{{ item.name }}"
          Role:        "dr-failover"
          LaunchedBy:  "ansible-dr-playbook"
      loop: "{{ dr_amis.results }}"
      register: launched_instances

    - name: Wait for instances to reach running state
      amazon.aws.ec2_instance_info:
        region:      "{{ dr_region }}"
        instance_ids: "{{ item.instances | map(attribute='instance_id') | list }}"
      loop: "{{ launched_instances.results }}"
      register: instance_info
      until: >
        instance_info.instances | map(attribute='state.name') | list | difference(['running']) | length == 0
      retries: 30
      delay:   20

    - name: Register with target groups (when target_group_arns is defined)
      community.aws.elb_target:
        region:          "{{ dr_region }}"
        target_group_arn: "{{ item.1 }}"
        target_id:       "{{ item.0.instance_id }}"
        state:           present
      loop: "{{ launched_instances.results
               | map(attribute='instances') | flatten
               | product(target_group_arns | default([]))
               | list }}"
      when: target_group_arns is defined and target_group_arns | length > 0

    - name: Print DR failover summary
      ansible.builtin.debug:
        msg: >-
          DR instance {{ item.instance_id }} launched in {{ dr_region }}
          — private IP: {{ item.private_ip_address }}
          — public IP: {{ item.public_ip_address | default('none') }}
      loop: "{{ launched_instances.results | map(attribute='instances') | flatten }}"
~~~

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed (this runs on Linux or WSL — Ansible does not run natively on Windows)
- AWS collections installed: run `ansible-galaxy collection install amazon.aws community.aws`
- AWS credentials configured (via `aws configure` or environment variables)
- At least one AMI ID in your source region to copy

**Step 1 — Save the file**

1. Open your WSL terminal (Windows key → type `wsl`)
2. Navigate to your home directory: `cd ~`
3. Create the file: `nano ec2_dr_failover.yml`
4. Paste the code, then press `Ctrl+X`, then `Y`, then `Enter` to save

**Step 2 — Fill in your details**

Open the saved file and update these values in the `vars:` section:

| Variable | What to enter | Where to find it |
|---|---|---|
| `source_region` | Your main AWS region | AWS Console → top-right region selector |
| `dr_region` | Your DR/backup AWS region | Choose a different region from your main one |
| `source_ami_ids` | List of AMI IDs to copy and launch | AWS Console → EC2 → AMIs |
| `dr_subnet_id` | Subnet ID in your DR region | AWS Console → VPC → Subnets |
| `dr_sg_ids` | Security group IDs in DR region | AWS Console → EC2 → Security Groups |
| `key_name` | EC2 key pair name for SSH access | AWS Console → EC2 → Key Pairs |

**Step 3 — Open the right terminal**

- **For .yml (Ansible):** Needs Linux or WSL. Open your WSL terminal.

**Step 4 — Run it**

```bash
cd ~
ansible-playbook ec2_dr_failover.yml
```

**What you should see**

Ansible prints each task as it runs. You will see it copying AMIs (this can take several minutes), then launching instances, then waiting for them to reach the running state. At the end it prints a summary with the new instance IDs and IP addresses.

---

## IAM Access Key Age Audit

Lists all IAM users and access keys, flags keys that are unused, overdue for rotation, or older than one year, and optionally deactivates stale keys with a confirmation prompt.

~~~python
#!/usr/bin/env python3
"""IAM Access Key Age Audit — flags stale, unused, and overdue-for-rotation keys."""

import argparse
import datetime
import sys
import boto3

# Thresholds (days)
UNUSED_THRESHOLD       = 90
LAST_USED_THRESHOLD    = 60
AGE_CRITICAL_THRESHOLD = 365

NOW = datetime.datetime.now(datetime.timezone.utc)

def key_age_days(create_date: datetime.datetime) -> int:
    return (NOW - create_date).days

def days_since_used(last_used: datetime.datetime | None) -> int | None:
    if last_used is None:
        return None
    return (NOW - last_used).days

def audit_keys(iam) -> list[dict]:
    rows: list[dict] = []
    paginator = iam.get_paginator("list_users")
    for page in paginator.paginate():
        for user in page["Users"]:
            username = user["UserName"]
            keys = iam.list_access_keys(UserName=username)["AccessKeyMetadata"]
            for key in keys:
                key_id     = key["AccessKeyId"]
                status     = key["Status"]
                created    = key["CreateDate"]
                age        = key_age_days(created)

                try:
                    lu_data    = iam.get_access_key_last_used(AccessKeyId=key_id)["AccessKeyLastUsed"]
                    last_used  = lu_data.get("LastUsedDate")
                    last_svc   = lu_data.get("ServiceName", "")
                    last_region= lu_data.get("Region", "")
                except Exception:
                    last_used  = None
                    last_svc   = ""
                    last_region= ""

                d_since = days_since_used(last_used)

                flags = []
                if d_since is None and age > UNUSED_THRESHOLD:
                    flags.append(f"NEVER_USED>{UNUSED_THRESHOLD}d")
                if d_since is not None and d_since > LAST_USED_THRESHOLD and status == "Active":
                    flags.append(f"LAST_USED>{LAST_USED_THRESHOLD}d")
                if age > AGE_CRITICAL_THRESHOLD:
                    flags.append(f"AGE>{AGE_CRITICAL_THRESHOLD}d")

                rows.append({
                    "User":       username,
                    "KeyId":      key_id,
                    "Status":     status,
                    "AgeDays":    age,
                    "LastUsedDays": d_since if d_since is not None else "never",
                    "LastService": last_svc,
                    "LastRegion":  last_region,
                    "Flags":      "|".join(flags),
                })

    return sorted(rows, key=lambda r: r["AgeDays"], reverse=True)

def deactivate_key(iam, username: str, key_id: str) -> None:
    iam.update_access_key(UserName=username, AccessKeyId=key_id, Status="Inactive")
    print(f"  Deactivated: {key_id} (user: {username})")

def main() -> None:
    parser = argparse.ArgumentParser(description="IAM Access Key Age Audit")
    parser.add_argument("--deactivate", action="store_true",
                        help="Interactively deactivate keys older than AGE_CRITICAL_THRESHOLD days")
    parser.add_argument("--max-age", type=int, default=AGE_CRITICAL_THRESHOLD,
                        help="Max key age in days before deactivation (used with --deactivate)")
    args = parser.parse_args()

    iam  = boto3.client("iam")
    rows = audit_keys(iam)

    print(f"\n{'User':<30} {'KeyId':<22} {'Status':<10} {'Age(d)':>7} {'LastUsed(d)':>12} {'Flags'}")
    print("-" * 105)
    for r in rows:
        print(
            f"{r['User']:<30} {r['KeyId']:<22} {r['Status']:<10} "
            f"{r['AgeDays']:>7} {str(r['LastUsedDays']):>12}  {r['Flags']}"
        )

    flagged = [r for r in rows if r["Flags"]]
    print(f"\nTotal keys : {len(rows)}")
    print(f"Flagged    : {len(flagged)}")

    if args.deactivate:
        stale = [r for r in rows if r["AgeDays"] >= args.max_age and r["Status"] == "Active"]
        if not stale:
            print("\nNo keys old enough to deactivate.")
            return
        print(f"\nThe following {len(stale)} key(s) are >= {args.max_age} days old and Active:")
        for r in stale:
            print(f"  {r['User']} / {r['KeyId']}  ({r['AgeDays']} days)")
        confirm = input("\nType YES to deactivate all listed keys: ")
        if confirm.strip() == "YES":
            for r in stale:
                deactivate_key(iam, r["User"], r["KeyId"])
        else:
            print("Aborted.")

if __name__ == "__main__":
    main()
~~~

### How to run this script — step by step

**Before you start — what you need**
- Python installed
- AWS CLI configured with credentials that have IAM read access (`iam:ListUsers`, `iam:ListAccessKeys`, `iam:GetAccessKeyLastUsed`)
- The `boto3` package installed

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `iam_key_audit.py` and save to your Desktop

**Step 2 — Fill in your details**

The thresholds near the top can be adjusted:

| Variable | What to enter | Where to find it |
|---|---|---|
| `UNUSED_THRESHOLD` | Days before a never-used key is flagged | Default: `90` |
| `LAST_USED_THRESHOLD` | Days since last use before flagging | Default: `60` |
| `AGE_CRITICAL_THRESHOLD` | Key age in days before flagging as critical | Default: `365` |

**Step 3 — Open the right terminal**

- **For .py (Python):** Open Command Prompt.

**Step 4 — Run it**

```bash
cd C:\Users\YourName\Desktop
pip install boto3
python iam_key_audit.py
```

To also deactivate stale keys (use with caution):

```bash
python iam_key_audit.py --deactivate
```

**What you should see**

A table with one row per access key showing the user, key ID, status, age in days, last used days ago, and any flags. Flags like `AGE>365d` or `NEVER_USED>90d` highlight keys that need attention.

---

## CloudWatch Alarm Status Check

Lists all CloudWatch alarms, filters for those in ALARM state, prints a formatted table of alarm name, metric, threshold, and reason, and exits non-zero if any alarms are firing.

~~~bash
#!/bin/bash
set -euo pipefail

AWS_PROFILE="${AWS_PROFILE:-default}"
AWS_REGION="${AWS_REGION:-us-east-1}"

export AWS_PROFILE AWS_REGION

BOLD="\033[1m"
RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"

echo -e "${BOLD}=== CloudWatch Alarm Status ===${RESET}"
echo "Profile : ${AWS_PROFILE}"
echo "Region  : ${AWS_REGION}"
echo

ALL_JSON=$(aws cloudwatch describe-alarms --output json)
export ALL_JSON

python3 - <<'PYEOF'
import json, os, sys

data   = json.loads(os.environ["ALL_JSON"])
alarms = data.get("MetricAlarms", []) + data.get("CompositeAlarms", [])

counts = {}
for a in alarms:
    state = a.get("StateValue", "UNKNOWN")
    counts[state] = counts.get(state, 0) + 1

print(f"{'State':<20} {'Count':>6}")
print("-" * 28)
for state, cnt in counts.items():
    print(f"{state:<20} {cnt:>6}")

firing = [a for a in alarms if a.get("StateValue") == "ALARM"]
if not firing:
    print("\nNo alarms in ALARM state.")
    sys.exit(0)

print(f"\n{'AlarmName':<45} {'Namespace':<25} {'Metric':<30} {'Threshold':>10} {'Reason'}")
print("-" * 140)
for a in firing:
    name      = a.get("AlarmName", "")[:44]
    ns        = a.get("Namespace", "")[:24]
    metric    = a.get("MetricName", "")[:29]
    threshold = a.get("Threshold", "")
    reason    = (a.get("StateReason") or "")[:80]
    print(f"{name:<45} {ns:<25} {metric:<30} {str(threshold):>10}  {reason}")

sys.exit(1)
PYEOF
~~~

### How to run this script — step by step

**Before you start — what you need**
- AWS CLI installed and configured
- Your AWS user needs `cloudwatch:DescribeAlarms` permission
- Git Bash installed (from https://gitforwindows.org)

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `cloudwatch-check.sh` and save to your Desktop

**Step 2 — Fill in your details**

| Variable | What to enter | Where to find it |
|---|---|---|
| `AWS_PROFILE` | Your AWS CLI profile name | Run `aws configure list-profiles` |
| `AWS_REGION` | Your AWS region | AWS Console → top-right |

**Step 3 — Open the right terminal**

- **For .sh (Bash):** Install Git for Windows (gitforwindows.org) → open Git Bash

**Step 4 — Run it**

```bash
cd ~/Desktop
bash cloudwatch-check.sh
```

**What you should see**

A count table showing how many alarms are in OK, ALARM, and INSUFFICIENT_DATA state. If any alarms are currently firing, a second detailed table appears showing the alarm name, metric, threshold value, and the reason text from AWS. The script exits with an error code if any alarms are firing.

---

## Ansible AWS Infrastructure Health Playbook

Checks EC2 instance states, RDS status, ELB health, S3 bucket replication, and Route 53 health check results for a given environment tag, then prints a pass/fail summary.

~~~yaml
---
# aws_infra_health.yml
# Requires: amazon.aws, community.aws collections
# ansible-galaxy collection install amazon.aws community.aws

- name: AWS Infrastructure Health Check
  hosts: localhost
  connection: local
  gather_facts: true

  vars:
    aws_region:      "us-east-1"
    environment_tag: "production"

  tasks:

    - name: Get EC2 instance facts for environment tag
      amazon.aws.ec2_instance_info:
        region: "{{ aws_region }}"
        filters:
          "tag:Environment": "{{ environment_tag }}"
      register: ec2_facts

    - name: Assert all EC2 instances are running
      ansible.builtin.assert:
        that: >
          ec2_facts.instances | map(attribute='state.name') | list | difference(['running']) | length == 0
        fail_msg: >-
          Non-running EC2 instances detected:
          {{ ec2_facts.instances | selectattr('state.name', '!=', 'running') | map(attribute='instance_id') | list }}
        success_msg: "All {{ ec2_facts.instances | length }} EC2 instance(s) running."

    - name: Get RDS instance facts
      community.aws.rds_instance_info:
        region: "{{ aws_region }}"
      register: rds_facts

    - name: Assert all RDS instances are available
      ansible.builtin.assert:
        that: >
          rds_facts.instances | map(attribute='db_instance_status') | list | difference(['available']) | length == 0
        fail_msg: "RDS instances not in 'available' state: {{ rds_facts.instances | map(attribute='db_instance_identifier') | list }}"
        success_msg: "All {{ rds_facts.instances | length }} RDS instance(s) available."

    - name: Get ELBv2 load balancer facts
      community.aws.elb_application_lb_info:
        region: "{{ aws_region }}"
      register: elb_facts

    - name: Assert all load balancers are active
      ansible.builtin.assert:
        that: >
          elb_facts.load_balancers | map(attribute='state.code') | list | difference(['active']) | length == 0
        fail_msg: "Load balancers not active: {{ elb_facts.load_balancers | map(attribute='load_balancer_name') | list }}"
        success_msg: "All {{ elb_facts.load_balancers | length }} load balancer(s) active."

    - name: Get S3 bucket replication config for tagged buckets
      amazon.aws.s3_bucket_info:
        region: "{{ aws_region }}"
      register: s3_facts

    - name: Report S3 buckets with replication enabled
      ansible.builtin.debug:
        msg: >-
          Bucket {{ item.name }}: replication
          {{ 'ENABLED' if item.replication | default({}) else 'DISABLED' }}
      loop: "{{ s3_facts.buckets }}"

    - name: Get Route 53 health check statuses
      amazon.aws.route53_info:
        query: health_check
        health_check_method: status
      register: r53_health

    - name: Flag unhealthy Route 53 health checks
      ansible.builtin.debug:
        msg: "UNHEALTHY: {{ item.Id }}"
      loop: "{{ r53_health.HealthChecks | default([]) }}"
      when: item.HealthCheckConfig is defined

    - name: Print health summary
      ansible.builtin.debug:
        msg:
          - "===== AWS Infrastructure Health Summary ====="
          - "Environment : {{ environment_tag }}"
          - "Region      : {{ aws_region }}"
          - "EC2 instances checked  : {{ ec2_facts.instances | length }}"
          - "RDS instances checked  : {{ rds_facts.instances | length }}"
          - "Load balancers checked : {{ elb_facts.load_balancers | length }}"
          - "S3 buckets found       : {{ s3_facts.buckets | length }}"
          - "Result: PASSED (assertions above would have failed otherwise)"
~~~

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on Linux or WSL (Ansible does not run natively on Windows)
- AWS Ansible collections: run `ansible-galaxy collection install amazon.aws community.aws`
- AWS credentials configured via `aws configure` or environment variables

**Step 1 — Save the file**

1. Open your WSL terminal (Windows key → type `wsl`)
2. Create the file: `nano aws_infra_health.yml`
3. Paste the code, then press `Ctrl+X`, `Y`, `Enter` to save

**Step 2 — Fill in your details**

| Variable | What to enter | Where to find it |
|---|---|---|
| `aws_region` | Your AWS region, e.g. `eu-west-1` | AWS Console → top-right region selector |
| `environment_tag` | The value of the `Environment` tag on your resources | Check your EC2/RDS tags in the AWS Console |

**Step 3 — Open the right terminal**

- **For .yml (Ansible):** Needs Linux or WSL. Open your WSL terminal.

**Step 4 — Run it**

```bash
cd ~
ansible-playbook aws_infra_health.yml
```

**What you should see**

Ansible runs through each check in order — EC2, RDS, ELB, S3, Route53. Each `assert` task either shows `ok` (green) with a success message or `failed` (red) with a list of the problem resources. At the end it prints a summary block showing how many resources were checked.

---

## Windows: AWS Health Check via AWS CLI (CMD Batch)

Check your AWS EC2 instances, ELB health, CloudWatch alarms, and RDS databases directly from Windows using the AWS CLI. No Linux needed.

~~~batch
@echo off
REM aws-health-check.bat
REM Requires: AWS CLI for Windows (download from https://aws.amazon.com/cli/)
REM Run "aws configure" first to set your credentials.

set AWS_PROFILE=default
set AWS_REGION=us-east-1
set LB_NAME=my-load-balancer

echo === AWS Account Health Check ===
echo Profile : %AWS_PROFILE%
echo Region  : %AWS_REGION%
echo.

echo --- Caller Identity ---
aws sts get-caller-identity --output table
echo.

echo --- EC2 Instance Status ---
aws ec2 describe-instance-status --output table
echo.

echo --- ELB Instance Health ---
aws elb describe-instance-health --load-balancer-name %LB_NAME% --output table
echo.

echo --- CloudWatch Alarms in ALARM State ---
aws cloudwatch describe-alarms --state-value ALARM --output table
echo.

echo --- RDS Instances ---
aws rds describe-db-instances --query "DBInstances[*].{ID:DBInstanceIdentifier,Status:DBInstanceStatus}" --output table
echo.

echo Health check complete.
pause
~~~

### How to run this script — step by step

**Before you start — what you need**
- AWS CLI for Windows installed (download the MSI installer from https://aws.amazon.com/cli/)
- AWS credentials configured — open Command Prompt and run `aws configure` once to enter your access key, secret key, and region

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files** (important — prevents Notepad adding .txt)
5. Name it `aws-health-check.bat` and save to your Desktop

**Step 2 — Fill in your details**

| Variable | What to enter | Where to find it |
|---|---|---|
| `AWS_PROFILE` | Your AWS CLI profile name, usually `default` | Run `aws configure list-profiles` in Command Prompt |
| `AWS_REGION` | Your AWS region code, e.g. `eu-west-1` | AWS Console → top-right region selector |
| `LB_NAME` | Your Classic Load Balancer name | AWS Console → EC2 → Load Balancers |

**Step 3 — Open the right terminal**

- **For .bat / .cmd:** Open Command Prompt or just double-click the file

**Step 4 — Run it**

```bash
cd C:\Users\YourName\Desktop
aws-health-check.bat
```

Or just double-click the file from your Desktop.

**What you should see**

Tables printed in your Command Prompt window showing EC2 instance statuses, ELB health, any CloudWatch alarms currently in ALARM state, and your RDS database statuses. The window stays open (due to `pause`) so you can read the output before it closes.

---

## Windows: AWS S3 Bucket Inventory (PowerShell with AWS Tools)

List all your S3 buckets and check versioning, logging, and encryption settings using the AWS Tools for PowerShell module.

~~~powershell
# aws-s3-inventory.ps1
# Requires: AWS Tools for PowerShell
# Install with: Install-Module -Name AWS.Tools.S3 -Scope CurrentUser

param(
    [string]$AwsAccessKey = "YOUR_ACCESS_KEY",
    [string]$AwsSecretKey = "YOUR_SECRET_KEY",
    [string]$AwsRegion    = "us-east-1"
)

# Install module if not present
if (-not (Get-Module -ListAvailable -Name AWS.Tools.S3)) {
    Write-Host "Installing AWS.Tools.S3 module..." -ForegroundColor Yellow
    Install-Module -Name AWS.Tools.S3 -Scope CurrentUser -Force
}

Import-Module AWS.Tools.S3

# Set credentials
Initialize-AWSDefaultConfiguration -AccessKey $AwsAccessKey -SecretKey $AwsSecretKey -Region $AwsRegion

Write-Host "`n=== AWS S3 Bucket Inventory ===" -ForegroundColor Cyan
Write-Host "Region : $AwsRegion"
Write-Host "Time   : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"

$buckets = Get-S3Bucket

$results = foreach ($bucket in $buckets) {
    $name = $bucket.BucketName

    try {
        $versioning = (Get-S3BucketVersioning -BucketName $name).Status
        $versioningStatus = if ($versioning) { $versioning } else { "Disabled" }
    } catch {
        $versioningStatus = "Error"
    }

    try {
        $logging = Get-S3BucketLogging -BucketName $name
        $loggingEnabled = if ($logging.LoggingConfig.TargetBucketName) { "Yes" } else { "No" }
    } catch {
        $loggingEnabled = "Error"
    }

    try {
        $encryption = Get-S3BucketEncryption -BucketName $name
        $encryptionType = $encryption.ServerSideEncryptionConfiguration.Rules[0].ServerSideEncryptionByDefault.ServerSideEncryptionAlgorithm
    } catch {
        $encryptionType = "None"
    }

    $flags = @()
    if ($versioningStatus -eq "Disabled") { $flags += "NO_VERSIONING" }
    if ($loggingEnabled -eq "No")         { $flags += "NO_LOGGING" }
    if ($encryptionType -eq "None")       { $flags += "NO_ENCRYPTION" }

    [PSCustomObject]@{
        BucketName  = $name
        Versioning  = $versioningStatus
        Logging     = $loggingEnabled
        Encryption  = $encryptionType
        Flags       = if ($flags) { $flags -join "|" } else { "OK" }
    }
}

$results | Format-Table -AutoSize

$flagged = $results | Where-Object { $_.Flags -ne "OK" }
Write-Host "Total buckets : $($results.Count)"
Write-Host "Flagged       : $($flagged.Count)"

if ($flagged.Count -gt 0) {
    Write-Host "`nBuckets needing attention:" -ForegroundColor Yellow
    $flagged | ForEach-Object {
        Write-Host "  $($_.BucketName) — $($_.Flags)" -ForegroundColor Yellow
    }
}
~~~

### How to run this script — step by step

**Before you start — what you need**
- Windows PowerShell 5.1 or PowerShell 7 (already installed on most Windows 10/11 machines)
- An AWS access key and secret key (create one in AWS Console → IAM → your user → Security credentials)
- Internet access so PowerShell can download the AWS module

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files** (important — prevents Notepad adding .txt)
5. Name it `aws-s3-inventory.ps1` and save to your Desktop

**Step 2 — Fill in your details**

| Variable | What to enter | Where to find it |
|---|---|---|
| `$AwsAccessKey` | Your AWS access key ID | AWS Console → IAM → Users → your user → Security credentials |
| `$AwsSecretKey` | Your AWS secret access key | Same place — only shown once when created |
| `$AwsRegion` | Your AWS region, e.g. `eu-west-1` | AWS Console → top-right region selector |

**Step 3 — Open the right terminal**

- **For .ps1 (PowerShell):** Windows key → `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time per session)**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run it**

```bash
cd C:\Users\YourName\Desktop
.\aws-s3-inventory.ps1
```

**What you should see**

The first time it runs, it will install the `AWS.Tools.S3` PowerShell module automatically (this takes a minute). Then it prints a table with one row per S3 bucket showing versioning status, whether logging is on, and the encryption type. Buckets missing any of these will be flagged at the bottom.
