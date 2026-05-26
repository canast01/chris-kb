# AWS — Operations

┌─────────────────────────────────────── AWS Operations Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              AWS Operations — Health Checks, Procedures, Patching, and Automation             │   │
│   │   Health Checks: EC2 status checks · RDS availability · CloudWatch alarm state · AWS Health   │   │
│   │    Procedures: instance lifecycle, AMI management, EBS expansion, ASG scaling, RDS failover   │   │
│   │  Patching: Systems Manager Patch Manager applies OS patches on schedule; compliance reporting │   │
│   │      Backup/Restore: AWS Backup jobs · EBS snapshot restore · RDS point-in-time recovery      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Health checks prevent failures · Procedures execute changes safely                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Health Checks        │  │          Procedures         │  │          Automation         │   │
│   │    EC2 status: 2/2 checks   │  │    Start/stop/reboot EC2    │  │    SSM Run Command: fleet   │   │
│   │    RDS: available + IOPS    │  │    Resize: instance type    │  │  EventBridge: auto-trigger  │   │
│   │    CW Alarms: OK vs ALARM   │  │   EBS: extend + resize fs   │  │    Lambda: remediation fn   │   │
│   │    AWS Health: svc events   │  │    ASG: refresh instances   │  │  CloudFormation: IaC drift  │   │
│   │   TGW + VPN: BGP sessions   │  │    RDS failover: promote    │  │   Step Functions: workflow  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Health checks detect issues · Procedures resolve them                                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Health Checks   │    Procedures    │      Patching     │  Backup/Restore  │     Scripts      │   │
│   │   EC2 2/2 OK?    │   AMI: create    │   Patch baseline  │ Backup job: run  │  CLI: describe   │   │
│   │  CW alarms: OK   │   EBS: extend    │    Patch window   │ EBS snap restore │   Boto3: boto3   │   │
│   │  RDS: available  │   ASG: refresh   │  Compliance: view │     RDS PITR     │   SSM scripts    │   │
│   │ AWS Health: evts │   RDS failover   │  Reboot if needed │ Cross-region: cp │     CDK / TF     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  EC2 hosts on Nitro · EBS storage fabric · RDS managed infrastructure · AZs for HA · VPC networking   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  EC2 status checks = System check (AWS infra) + instance check (OS/app); both must pass (2/2)         │
│  AWS Health        = Personalised service health and maintenance events for your account and resources│
│  Patch Manager     = SSM feature; applies OS patches per baseline; records compliance per instance    │
│  Patch baseline    = Defines which patches to install; AWS-managed or custom per OS and severity      │
│  AMI               = Amazon Machine Image; golden image snapshot; used for ASG instance refresh       │
│  ASG instance refresh= Rolling replacement of instances in an ASG with a new launch template version  │
│  EBS expansion     = Increase volume size; then extend filesystem (growpart + resize2fs or diskpart)  │
│  RDS PITR          = Point-in-time recovery; restore RDS to any second within the retention window    │
│  CloudFormation drift= Detects manual changes to stack resources not captured in the template         │
│  Step Functions    = AWS serverless workflow orchestrator; chains Lambda, SSM, ECS tasks with retries │
│  Run Command       = SSM feature executing commands/scripts on EC2 fleet; no SSH or VPN needed        │
│  EventBridge rule  = Triggers Lambda/SSM/SQS on schedule or event pattern; enables auto-remediation   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Change Readiness

- [ ] AMI snapshot or RDS snapshot taken and verified before change
- [ ] IAM permission changes reviewed and least-privilege confirmed
- [ ] VPC and security group changes peer-reviewed
- [ ] CloudTrail is enabled in all relevant regions
- [ ] Rollback plan documented and tested
- [ ] Change window communicated to stakeholders
- [ ] Target instances/services identified and `--limit` or ARN scope set

| Item | Status | Notes |
|---|---|---|
| Pre-change snapshot | | AMI ID or RDS snapshot ID |
| IAM review | | Reviewer name |
| VPC/SG peer review | | PR or ticket reference |
| Rollback plan | | Link to runbook |
| Stakeholder notification | | Date/time sent |

## Incident Triage

- [ ] Check AWS Health Dashboard for active events affecting the region or service
- [ ] Review CloudWatch alarms to identify the affected resource
- [ ] Check service-specific logs (EC2 system log, RDS error log, ALB access log)
- [ ] Review CloudTrail for recent changes in the 2 hours before the incident
- [ ] Confirm VPC routing and security group rules have not changed unexpectedly
- [ ] Check ELB target health and deregister unhealthy targets if needed
- [ ] Engage AWS Support if the event is service-side

| Question | Answer |
|---|---|
| Is this an AWS service outage? | Check health.aws.amazon.com |
| Which resource is affected? | EC2 / RDS / ELB / S3 / Other |
| When did the issue start? | CloudTrail timestamp |
| What changed recently? | CloudTrail last 2 hours |
| Is a rollback possible? | Yes / No — snapshot available? |

## Maintenance Window

1. Notify stakeholders of the planned maintenance window start time.
2. Verify pre-change snapshot (AMI or RDS snapshot) exists and is complete.
3. For EC2: stop the instance, perform maintenance, start and confirm instance status OK.
4. For RDS: schedule the maintenance window in the RDS console or via CLI; monitor the event log.
5. For ELB: enable connection draining before removing targets; wait for active connections to drain.
6. Test Route 53 health check failover if DNS-based failover is configured.
7. Confirm all CloudWatch alarms return to OK state after the change.
8. Close the maintenance window and notify stakeholders.

## Post-Change Validation

- [ ] All CloudWatch alarms are in OK state
- [ ] EC2 instances report healthy instance and system status
- [ ] RDS instances are in `available` state
- [ ] ELB target groups show all targets as healthy
- [ ] Application-level smoke test passes (login, key transaction, API call)
- [ ] CloudTrail shows only expected operations from the maintenance window
- [ ] No new AWS Health events opened for affected services
- [ ] Cost Explorer shows no unexpected resource charge spikes from the change
