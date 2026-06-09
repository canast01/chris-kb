# CloudFormation


<div class="kb-summary">
AWS CloudFormation CLI reference — stack lifecycle, change set preview, drift detection, and StackSet operations.
</div>

```text
┌────────────────────────────────────── AWS CLI — CloudFormation ───────────────────────────────────────┐
│                                                                                                       │
│  Key CloudFormation CLI commands for stack management, drift detection, and StackSets.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Stack Operations               │  │               Stack Inspection              │   │
│   │        create-stack: deploy template         │  │           describe-stacks: status           │   │
│   │         update-stack: apply changes          │  │           list-stacks: all stacks           │   │
│   │            delete-stack: teardown            │  │          describe-stack-events: log         │   │
│   │          create-change-set: preview          │  │           describe-stack-resources          │   │
│   │          execute-change-set: apply           │  │           get-template: fetch yaml          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Always preview via change-set before executing; describe-stack-events for failures                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Drift and Validation             │  │                  StackSets                  │   │
│   │          detect-stack-drift: check           │  │           create-stack-set: define          │   │
│   │         describe-stack-drift-result          │  │        create-stack-instances: deploy       │   │
│   │           validate-template: lint            │  │            update-stack-instances           │   │
│   │          cfn-lint: local pre-check           │  │             list-stack-instances            │   │
│   │         package: upload S3 artifacts         │  │            delete-stack-instances           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS CloudFormation service · S3 (template storage) · IAM · target AWS resources                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Stack           = CloudFormation deployment unit; collection of AWS resources                        │
│  Change set      = Preview of changes before applying; shows add/modify/remove                        │
│  Stack drift     = Resource has been modified outside of CloudFormation                               │
│  StackSet        = Multi-account/region CloudFormation deployment                                     │
│  Stack instance  = Single stack deployment within a StackSet target                                   │
│  validate-template= Checks CloudFormation YAML/JSON syntax before deployment                          │
│  cfn-lint        = Open-source linter; checks CloudFormation best practices                           │
│  package         = Uploads local artifacts to S3 and rewrites template references                     │
│  describe-stack-events= Chronological log of resource operations during deploy                        │
│  get-template    = Retrieves the template used to create or update the stack                          │
│  DELETE_FAILED   = Stack deletion failed; manual resource cleanup then retry                          │
│  ROLLBACK        = Failed update reverts to last known good configuration                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
