---
tags:
  - aws
description: "RDS reference covering Snapshots, Parameter Groups, Subnet Groups, Events and Event Subscriptions, Read Replicas and 2 more sections."
---
# RDS

<div class="kb-summary">
RDS reference covering Snapshots, Parameter Groups, Subnet Groups, Events and Event Subscriptions, Read Replicas and 2 more sections.

*Applies to: AWS*
</div>

```d2
direction: down

parameter_groups: "Parameter Groups" {shape: rectangle}
subnet_groups: "Subnet Groups" {shape: rectangle}
events_and_event_subscriptions: "Events and Event Subscriptions" {shape: rectangle}
read_replicas: "Read Replicas" {shape: rectangle}
aurora_clusters: "Aurora Clusters" {shape: rectangle}
log_export_and_monitoring: "Log Export and Monitoring" {shape: rectangle}

parameter_groups -> subnet_groups: uses
subnet_groups -> events_and_event_subscriptions: uses
events_and_event_subscriptions -> read_replicas: uses
read_replicas -> aurora_clusters: uses
aurora_clusters -> log_export_and_monitoring: uses
```

## Parameter Groups

```bash
# List all DB parameter groups
aws rds describe-db-parameter-groups

# Describe parameters inside a group
aws rds describe-db-parameters --db-parameter-group-name <group_name>

# Create a custom parameter group (e.g. for MySQL 8.0)
aws rds create-db-parameter-group \
  --db-parameter-group-name my-mysql80-params \
  --db-parameter-group-family mysql8.0 \
  --description "Custom MySQL 8.0 parameters"

# Modify a parameter inside a group
aws rds modify-db-parameter-group \
  --db-parameter-group-name my-mysql80-params \
  --parameters "ParameterName=max_connections,ParameterValue=500,ApplyMethod=immediate"

# Apply a parameter group to an instance (takes effect at next maintenance window)
aws rds modify-db-instance \
  --db-instance-identifier <id> \
  --db-parameter-group-name my-mysql80-params \
  --apply-immediately
```


```text title="Expected output"
{
    "DBParameterGroups": [
        {
            "DBParameterGroupName": "default.mysql8.0",
            "DBParameterGroupArn": "arn:aws:rds:us-east-1:123456789012:pg:default.mysql8.0",
            "DBParameterGroupFamily": "mysql8.0",
            "Description": "Default parameter group for mysql8.0",
            "DBParameterGroupStatus": "in-sync"
        },
        {
            "DBParameterGroupName": "my-mysql80-params",
            "DBParameterGroupArn": "arn:aws:rds:us-east-1:123456789012:pg:my-mysql80-params",
            "DBParameterGroupFamily": "mysql8.0",
            "Description": "Custom MySQL 8.0 parameters",
            "DBParameterGroupStatus": "in-sync"
        }
    ]
}
{
    "Parameters": [
        {
            "ParameterName": "max_connections",
            "ParameterValue": "500",
            "Description": "The maximum permitted number of simultaneous client connections",
            "Source": "user",
            "IsModifiable": true,
            "DataType": "integer",
            "AllowedValues": "1-100000",
            "ApplyMethod": "immediate"
        },
        {
            "ParameterName": "slow_query_log",
            "ParameterValue": "1",
            "Description": "Enable the slow query log",
            "Source": "user",
            "IsModifiable": true,
            "DataType": "integer"
        }
    ]
}
{
    "DBParameterGroup": {
        "DBParameterGroupName": "my-mysql80-params",
        "DBParameterGroupArn": "arn:aws:rds:us-east-1:123456789012:pg:my-mysql80-params",
        "DBParameterGroupFamily": "mysql8.0",
        "Description": "Custom MySQL 8.0 parameters",
        "DBParameterGroupStatus": "in-sync"
    }
}
{
    "DBParameterGroupName": "my-mysql80-params"
}
{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-mysql-db-01",
        "DBInstanceStatus": "modifying",
        "DBParameterGroups": [
            {
                "DBParameterGroupName": "my-mysql80-params",
                "ParameterApplyStatus": "pending-reboot"
            }
        ],
        "PendingModifiedValues": {
            "DBParameterGroupName": "my-mysql80-params"
        }
    }
}
```

!!! warning "Common errors"
    **`An error occurred (DBParameterGroupNotFound) when calling the DescribeDBParameterGroups operation: DB parameter group not found`** — Verify the parameter group name exists with `aws rds describe-db-parameter-groups` and check for typos.
    **`An error occurred (InvalidParameterValue) when calling the ModifyDBParameterGroup operation: The parameter max_connections cannot be modified because it is not modifiable`** — Check if the parameter is modifiable by reviewing its properties in `describe-db-parameters` output;
## Subnet Groups

```bash
# List all DB subnet groups
aws rds describe-db-subnet-groups

# Describe a specific subnet group
aws rds describe-db-subnet-groups --db-subnet-group-name <group_name>

# Create a subnet group spanning two AZs
aws rds create-db-subnet-group \
  --db-subnet-group-name my-subnet-group \
  --db-subnet-group-description "Multi-AZ subnet group" \
  --subnet-ids subnet-aaa111 subnet-bbb222
```


```text title="Expected output"
{
    "DBSubnetGroups": [
        {
            "DBSubnetGroupName": "default",
            "DBSubnetGroupDescription": "default",
            "VpcId": "vpc-12345678",
            "SubnetGroupStatus": "Complete",
            "Subnets": [
                {
                    "SubnetIdentifier": "subnet-aaa111",
                    "SubnetAvailabilityZone": {
                        "Name": "us-east-1a"
                    },
                    "SubnetStatus": "Active"
                },
                {
                    "SubnetIdentifier": "subnet-bbb222",
                    "SubnetAvailabilityZone": {
                        "Name": "us-east-1b"
                    },
                    "SubnetStatus": "Active"
                }
            ]
        },
        {
            "DBSubnetGroupName": "my-subnet-group",
            "DBSubnetGroupDescription": "Multi-AZ subnet group",
            "VpcId": "vpc-87654321",
            "SubnetGroupStatus": "Complete",
            "Subnets": [
                {
                    "SubnetIdentifier": "subnet-aaa111",
                    "SubnetAvailabilityZone": {
                        "Name": "us-east-1a"
                    },
                    "SubnetStatus": "Active"
                },
                {
                    "SubnetIdentifier": "subnet-bbb222",
                    "SubnetAvailabilityZone": {
                        "Name": "us-east-1b"
                    },
                    "SubnetStatus": "Active"
                }
            ]
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (DBSubnetGroupNotFoundFault) when calling the DescribeDBSubnetGroups operation: DB subnet group not found`** — Verify the subnet group name exists with `aws rds describe-db-subnet-groups` and use the correct name.
    **`An error occurred (InvalidParameterValue) when calling the CreateDBSubnetGroup operation: DB subnet group already exists`** — Choose a unique subnet group name or delete the existing group before recreating it.
## Events and Event Subscriptions

```bash
# List recent RDS events (last 60 minutes)
aws rds describe-events \
  --duration 60

# Filter events for a specific instance
aws rds describe-events \
  --source-identifier <id> \
  --source-type db-instance \
  --duration 1440

# List existing event subscriptions
aws rds describe-event-subscriptions

# Create an SNS event subscription for instance failures
aws rds create-event-subscription \
  --subscription-name prod-failure-alerts \
  --sns-topic-arn arn:aws:sns:<region>:<account_id>:<topic-name> \
  --source-type db-instance \
  --event-categories failure \
  --enabled
```


```text title="Expected output"
{
    "Events": [
        {
            "SourceIdentifier": "prod-mysql-01",
            "SourceType": "db-instance",
            "Message": "DB instance created",
            "EventCategories": [
                "creation"
            ],
            "Date": "2024-01-15T14:32:18.123000+00:00"
        },
        {
            "SourceIdentifier": "prod-mysql-01",
            "SourceType": "db-instance",
            "Message": "DB instance started",
            "EventCategories": [
                "availability"
            ],
            "Date": "2024-01-15T14:35:42.456000+00:00"
        },
        {
            "SourceIdentifier": "staging-postgres-02",
            "SourceType": "db-instance",
            "Message": "Automated backup completed",
            "EventCategories": [
                "backup"
            ],
            "Date": "2024-01-15T14:28:11.789000+00:00"
        }
    ]
}

{
    "Events": [
        {
            "SourceIdentifier": "prod-mysql-01",
            "SourceType": "db-instance",
            "Message": "DB instance restarted",
            "EventCategories": [
                "availability"
            ],
            "Date": "2024-01-14T09:15:33.210000+00:00"
        }
    ]
}

{
    "EventSubscriptionsList": [
        {
            "CustomerAwsId": "123456789012",
            "CustSubscriptionId": "prod-failure-alerts",
            "SnsTopicArn": "arn:aws:sns:us-east-1:123456789012:rds-alerts",
            "Status": "active",
            "SubscriptionCreationTime": "2024-01-10T11:22:33.000000+00:00",
            "SourceType": "db-instance",
            "SourceIdsList": [],
            "EventCategoriesList": [
                "failure"
            ],
            "Enabled": true
        }
    ]
}

{
    "EventSubscription": {
        "CustomerAwsId": "123456789012",
        "CustSubscriptionId": "prod-failure-alerts",
        "SnsTopicArn": "arn:aws:sns:us-east-1:123456789012:rds-alerts",
        "Status": "creating",
        "SubscriptionCreationTime": "2024-01-15T14:45:22.000000+00:00",
        "SourceType": "db-instance",
        "SourceIdsList": [],
        "EventCategoriesList": [
            "failure"
        ],
        "Enabled": true
    }
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValue) when calling the DescribeEvents operation: Invalid duration value`** — Ensure duration is specified in minutes (1–1440) and is a valid integer.
    **`An error occurred (InvalidParameterCombination) when calling the CreateEventSubscription operation: SNS topic does not exist or you do not have permission to access it`** —
## Read Replicas

```bash
# Create a read replica in the same region
aws rds create-db-instance-read-replica \
  --db-instance-identifier <replica_id> \
  --source-db-instance-identifier <source_id>

# Create a cross-region read replica
aws rds create-db-instance-read-replica \
  --db-instance-identifier <replica_id> \
  --source-db-instance-identifier arn:aws:rds:<source_region>:<account_id>:db:<source_id> \
  --region <target_region>

# Promote a read replica to a standalone instance
aws rds promote-read-replica \
  --db-instance-identifier <replica_id>
```


```text title="Expected output"
{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-db-replica-1",
        "DBInstanceClass": "db.t3.large",
        "Engine": "mysql",
        "DBInstanceStatus": "creating",
        "MasterUsername": "admin",
        "AllocatedStorage": 100,
        "EngineVersion": "8.0.35",
        "DBInstanceArn": "arn:aws:rds:us-east-1:123456789012:db:prod-db-replica-1",
        "ReadReplicaSourceDBInstanceIdentifier": "prod-db-primary"
    }
}
{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-db-replica-eu",
        "DBInstanceClass": "db.t3.large",
        "Engine": "mysql",
        "DBInstanceStatus": "creating",
        "AvailabilityZone": "eu-west-1a",
        "DBInstanceArn": "arn:aws:rds:eu-west-1:123456789012:db:prod-db-replica-eu",
        "ReadReplicaSourceDBInstanceIdentifier": "arn:aws:rds:us-east-1:123456789012:db:prod-db-primary"
    }
}
{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-db-replica-1",
        "DBInstanceStatus": "available",
        "ReadReplicaSourceDBInstanceIdentifier": null,
        "DBInstanceArn": "arn:aws:rds:us-east-1:123456789012:db:prod-db-replica-1"
    }
}
```

!!! warning "Common errors"
    **`An error occurred (DBInstanceNotFound) when calling the CreateDBInstanceReadReplica operation: DBInstance not found`** — Verify the source database identifier exists and is in the correct region using `aws rds describe-db-instances --db-instance-identifier <source_id>`.
    **`An error occurred (InvalidDBInstanceState) when calling the CreateDBInstanceReadReplica operation: Source database instance is not in available state`** — Wait for the source database to reach "available" status before creating a replica; check with `aws rds describe-db-instances --db-instance-identifier <source_id>`.
    **`An error occurred (DBInstanceAlreadyExists) when calling the PromoteReadReplica operation: DB instance already exists`** — Choose a unique replica identifier that doesn't already exist in your account.
## Aurora Clusters

```bash
# List Aurora DB clusters
aws rds describe-db-clusters

# Describe a specific cluster
aws rds describe-db-clusters --db-cluster-identifier <cluster_id>

# Failover to a specific reader instance (promotes it to writer)
aws rds failover-db-cluster \
  --db-cluster-identifier <cluster_id> \
  --target-db-instance-identifier <reader_instance_id>

# Failover without specifying a target (Aurora picks automatically)
aws rds failover-db-cluster --db-cluster-identifier <cluster_id>

# Create a cluster snapshot
aws rds create-db-cluster-snapshot \
  --db-cluster-identifier <cluster_id> \
  --db-cluster-snapshot-identifier <snap_name>
```


```text title="Expected output"
{
    "DBClusters": [
        {
            "DBClusterIdentifier": "prod-aurora-cluster-01",
            "Engine": "aurora-mysql",
            "EngineVersion": "8.0.mysql_aurora.3.02.0",
            "Status": "available",
            "MasterUsername": "admin",
            "DBClusterMembers": [
                {
                    "DBInstanceIdentifier": "prod-aurora-cluster-01-instance-1",
                    "IsClusterWriter": true,
                    "DBInstanceStatus": "available"
                },
                {
                    "DBInstanceIdentifier": "prod-aurora-cluster-01-instance-2",
                    "IsClusterWriter": false,
                    "DBInstanceStatus": "available"
                }
            ],
            "Endpoint": "prod-aurora-cluster-01.cluster-c9akciq32.us-east-1.rds.amazonaws.com",
            "ReaderEndpoint": "prod-aurora-cluster-01.cluster-ro-c9akciq32.us-east-1.rds.amazonaws.com"
        }
    ]
}

{
    "DBClusterIdentifier": "prod-aurora-cluster-01",
    "Status": "failing-over",
    "DBClusterMembers": [
        {
            "DBInstanceIdentifier": "prod-aurora-cluster-01-instance-2",
            "IsClusterWriter": true,
            "DBInstanceStatus": "available"
        },
        {
            "DBInstanceIdentifier": "prod-aurora-cluster-01-instance-1",
            "IsClusterWriter": false,
            "DBInstanceStatus": "rebooting"
        }
    ]
}

{
    "DBClusterSnapshot": {
        "DBClusterSnapshotIdentifier": "prod-snapshot-20240115",
        "DBClusterIdentifier": "prod-aurora-cluster-01",
        "SnapshotCreateTime": "2024-01-15T14:32:45.123000+00:00",
        "Engine": "aurora-mysql",
        "Status": "creating",
        "Port": 3306,
        "MasterUsername": "admin",
        "SnapshotType": "manual",
        "PercentProgress": 15,
        "StorageEncrypted": true
    }
}
```

!!! warning "Common errors"
    **`An error occurred (DBClusterNotFoundFault) when calling the DescribeDBClusters operation: DBCluster not found: <cluster_id>`** — Verify the cluster identifier is correct and exists in the current AWS region using `aws rds describe-db-clusters`.
    **`An error occurred (InvalidDBInstanceState) when calling the FailoverDBCluster operation: Failover cannot be performed on <cluster_id> because it is not in available state`** — Wait for the cluster to reach "available" status before attempting failover; check status with `aws rds describe-db-clusters --db-cluster-identifier <cluster_id>`.
    **`An error occurred (DBClusterSnapshotAlreadyExistsFault) when calling the CreateDBClusterSnapshot operation: <snap_name> already exists`** — Use a unique snapshot identifier or delete the existing snapshot with `aws rds delete-db-cluster-snapshot --db-
## Log Export and Monitoring

```bash
# List available log files for an instance
aws rds describe-db-log-files --db-instance-identifier <id>

# Download the last 1 MB of the error log
aws rds download-db-log-file-portion \
  --db-instance-identifier <id> \
  --log-file-name error/mysql-error.log \
  --output text

# Stream log file pages (paginate with --marker)
aws rds download-db-log-file-portion \
  --db-instance-identifier <id> \
  --log-file-name error/mysql-error.log \
  --number-of-lines 200

# Enable enhanced monitoring (60-second granularity)
aws rds modify-db-instance \
  --db-instance-identifier <id> \
  --monitoring-interval 60 \
  --monitoring-role-arn arn:aws:iam::<account_id>:role/rds-monitoring-role \
  --apply-immediately
```


```text title="Expected output"
{
    "DBLogFiles": [
        {
            "LogFileName": "error/mysql-error.log",
            "LastWritten": 1704067200000,
            "Size": 1048576
        },
        {
            "LogFileName": "slowquery/mysql-slowquery.log",
            "LastWritten": 1704053800000,
            "Size": 524288
        },
        {
            "LogFileName": "audit/mysql-audit.log",
            "LastWritten": 1704010200000,
            "Size": 2097152
        }
    ]
}
2024-01-01T12:00:00Z [Note] InnoDB: Buffer pool(s) load completed at 240101 12:00:00
2024-01-01T12:00:15Z [Warning] [MY-013360] [Server] Plugin mysql_native_password reported: ''mysql_native_password' is deprecated and will be removed in a future MySQL version.'
2024-01-01T12:00:45Z [ERROR] [MY-010584] [InnoDB] Tablespace ID mismatch in datafile './mysql.ibd'
2024-01-01T12:01:22Z [Note] [MY-010733] [Server] Binlog file mysql-bin.000042 is being used for recovery.
2024-01-01T12:02:10Z [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-mysql-01",
        "MonitoringInterval": 60,
        "MonitoringRoleArn": "arn:aws:iam::123456789012:role/rds-monitoring-role",
        "PendingModifiedValues": {
            "MonitoringInterval": 60
        },
        "DBInstanceStatus": "modifying"
    }
}
```

!!! warning "Common errors"
    **`InvalidDBInstanceIdentifier: DBInstance not found`** — Verify the instance identifier matches exactly using `aws rds describe-db-instances --query 'DBInstances[].DBInstanceIdentifier'`.
    **`AccessDenied: User is not authorized to perform: rds:DownloadDBLogFilePortion`** — Add the `rds:DownloadDBLogFilePortion` permission to your IAM user or role policy.
    **`InvalidParameterValue: The IAM role arn:aws:iam::123456789012:role/rds-monitoring-role is not valid`** — Ensure the monitoring role exists and has the `AmazonRDSEnhancedMonitoringRole` trust relationship configured for RDS.
## See also

- [AWS CLI Reference](../index.md)
- [AWS Storage](../../storage/index.md)
- [AWS Operations](../../operations/index.md)
