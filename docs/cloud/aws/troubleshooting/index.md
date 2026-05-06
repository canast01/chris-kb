# AWS Troubleshooting

EC2 connectivity failures are diagnosed by checking security group inbound rules, route table entries, and NACL allow/deny order before escalating to instance-level checks such as OS firewall and the SSM agent status. S3 access-denied errors require checking the bucket policy, the caller's IAM policy, and whether S3 Block Public Access is overriding a permissive bucket ACL. RDS connection-refused errors are most commonly caused by a missing security group rule from the client CIDR, an incorrect parameter group setting (e.g., `rds.force_ssl`), or the database not yet accepting connections after a failover.

| Issue | First checks | Commands |
|---|---|---|
| EC2 no connectivity | Security group, route table, NACL, source/dest check | `aws ec2 describe-security-groups`, `aws ec2 describe-route-tables` |
| S3 Access Denied | Bucket policy, IAM policy, Block Public Access, ACL | `aws s3api get-bucket-policy`, `aws s3api get-public-access-block` |
| RDS Connection refused | SG inbound rule, parameter group, subnet group | `aws rds describe-db-instances`, check VPC SG on port 5432/3306 |
| Lambda timeout | Function timeout setting, downstream latency, VPC config | CloudWatch Logs, X-Ray trace, `aws lambda get-function-configuration` |
| IAM Access Denied | Policy simulator, SCP blocks, permission boundary | `aws iam simulate-principal-policy` |
