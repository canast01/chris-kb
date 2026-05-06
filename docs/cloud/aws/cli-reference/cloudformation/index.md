# CloudFormation

> Part of the AWS CLI Reference.

---

```bash
# Stacks
aws cloudformation list-stacks
aws cloudformation describe-stacks --stack-name <name>
aws cloudformation create-stack --stack-name <name> --template-body file://template.yaml --parameters ParameterKey=Env,ParameterValue=prod
aws cloudformation update-stack --stack-name <name> --template-body file://template.yaml
aws cloudformation delete-stack --stack-name <name>

# Stack status
aws cloudformation describe-stack-events --stack-name <name>
aws cloudformation wait stack-create-complete --stack-name <name>

# Validate
aws cloudformation validate-template --template-body file://template.yaml
```
