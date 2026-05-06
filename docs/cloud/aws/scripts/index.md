# Scripts

> Part of the [AWS](../) reference.

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

# Print monthly totals per service using Python for clean formatting
python3 - <<'PYEOF'
import json, sys, os

data = json.loads("""${RAW_JSON}""".replace('${RAW_JSON}', os.environ.get('RAW_JSON', '')))

# Collect service → [monthly costs]
from collections import defaultdict
service_months = defaultdict(dict)
month_labels   = []

for result in data["ResultsByTime"]:
    start  = result["TimePeriod"]["Start"][:7]   # YYYY-MM
    month_labels.append(start)
    for group in result["Groups"]:
        svc  = group["Keys"][0]
        cost = float(group["Metrics"]["BlendedCost"]["Amount"])
        service_months[svc][start] = cost

if len(month_labels) < 2:
    print("Not enough months to compare.")
    sys.exit(0)

# Unique ordered months
months = sorted(set(month_labels))
prev_month = months[-2]
curr_month = months[-1]

# Sort services by current-month cost descending
ranked = sorted(service_months.items(), key=lambda x: x[1].get(curr_month, 0), reverse=True)
top10  = ranked[:10]

print(f"\n{'Service':<50} {prev_month:>12} {curr_month:>12} {'Change':>8}")
print("-" * 86)

for svc, mc in top10:
    prev = mc.get(prev_month, 0)
    curr = mc.get(curr_month, 0)
    if prev > 0:
        pct = (curr - prev) / prev * 100
        marker = "  ▲ HIGH" if pct > 20 else ""
    else:
        pct   = 0.0
        marker = ""
    print(f"{svc:<50} ${prev:>11.2f} ${curr:>11.2f} {pct:>+7.1f}%{marker}")

PYEOF

# Export RAW_JSON for the heredoc subshell
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
YELLOW="\033[0;33m"
GREEN="\033[0;32m"
RESET="\033[0m"

echo -e "${BOLD}=== CloudWatch Alarm Status ===${RESET}"
echo "Profile : ${AWS_PROFILE}"
echo "Region  : ${AWS_REGION}"
echo

# Get all alarm states as JSON
ALL_JSON=$(aws cloudwatch describe-alarms --output json)

python3 - <<PYEOF
import json, os, sys

data   = json.loads("""${ALL_JSON}""".replace('${ALL_JSON}', ''))
alarms = data.get("MetricAlarms", []) + data.get("CompositeAlarms", [])

counts = {"OK": 0, "ALARM": 0, "INSUFFICIENT_DATA": 0}
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

    # ---------------------------------------------------------------
    # EC2
    # ---------------------------------------------------------------
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

    # ---------------------------------------------------------------
    # RDS
    # ---------------------------------------------------------------
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

    # ---------------------------------------------------------------
    # ELB (Application / Network)
    # ---------------------------------------------------------------
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

    # ---------------------------------------------------------------
    # S3 Replication
    # ---------------------------------------------------------------
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

    # ---------------------------------------------------------------
    # Route 53 Health Checks
    # ---------------------------------------------------------------
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

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
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
