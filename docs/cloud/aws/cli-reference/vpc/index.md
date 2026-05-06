# VPC & Networking

> Part of the AWS CLI Reference.

---

```bash
# VPCs
aws ec2 describe-vpcs
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 delete-vpc --vpc-id <id>

# Subnets
aws ec2 describe-subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc_id>"
aws ec2 create-subnet --vpc-id <id> --cidr-block 10.0.1.0/24 --availability-zone us-east-1a

# Route tables
aws ec2 describe-route-tables
aws ec2 create-route --route-table-id <rt_id> --destination-cidr-block 0.0.0.0/0 --gateway-id <igw_id>

# Internet gateways
aws ec2 describe-internet-gateways
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --internet-gateway-id <igw_id> --vpc-id <vpc_id>

# Elastic IPs
aws ec2 describe-addresses
aws ec2 allocate-address --domain vpc
aws ec2 associate-address --instance-id <id> --allocation-id <eip_id>
aws ec2 release-address --allocation-id <eip_id>
```
