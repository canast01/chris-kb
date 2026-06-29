---
title: AWS — Certifications
tags:
  - aws
  - certifications
---

# AWS — Certifications

<div class="kb-summary">
Certifications reference covering Overview, Core Certification Paths, Daily Study Focus, Useful Commands, Renewal Notes.
</div>

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="cloud-practitioner/">
  <strong>Cloud Practitioner CLF-C02</strong>
  <span>14-day study plan — 3 hrs/day, 50 Q&A per day. Covers all 4 domains.</span>
</a>

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
<a class="kb-card" href="services/"><strong>Services</strong><span>Per-service study notes — IAM, EC2, VPC, S3, RDS, Lambda, and more.</span></a>

</div>

## Overview

AWS certifications validate skills in designing, deploying, operating, and securing workloads in Amazon Web Services environments.

## Core Certification Paths

- Cloud Practitioner
- Solutions Architect Associate
- Solutions Architect Professional
- SysOps Administrator
- DevOps Engineer
- Security Specialty

## Daily Study Focus

- Review core AWS services
- Practice architecture design scenarios
- Study cost and security best practices
- Use hands-on labs

## Useful Commands

```bash
aws configure
aws ec2 describe-instances
aws s3 ls
aws iam list-users
```


```text title="Expected output"
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: json

RESERVATION-ID	OWNER-ID	GROUP-NAME
r-0a1b2c3d4e5f6g7h8	123456789012	default

BUCKET	CREATION-DATE
my-app-bucket	2023-11-15T09:42:31.000Z
logs-archive-prod	2023-10-22T14:18:22.000Z
backup-2024	2024-01-08T16:55:47.000Z

USER	ARN	CREATE-DATE
admin-user	arn:aws:iam::123456789012:user/admin-user	2023-06-10T12:34:56+00:00
dev-team-lead	arn:aws:iam::123456789012:user/dev-team-lead	2023-09-21T08:19:22+00:00
ci-pipeline	arn:aws:iam::123456789012:user/ci-pipeline	2024-01-03T11:47:09+00:00
```

!!! warning "Common errors"
    **`Unable to locate credentials`** — Run `aws configure` with valid AWS Access Key ID and Secret Access Key, or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
    **`An error occurred (UnauthorizedOperation) when calling the DescribeInstances operation: You are not authorized to perform: ec2:DescribeInstances`** — Ensure the IAM user or role has the `ec2:DescribeInstances` permission attached in the IAM policy.
    **`An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied`** — Verify the IAM user has `s3:ListAllMyBuckets` and `s3:GetBucketLocation` permissions in their policy.
## Renewal Notes

AWS certifications typically require renewal every 3 years.
