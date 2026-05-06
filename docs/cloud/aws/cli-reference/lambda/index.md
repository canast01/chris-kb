# Lambda

> Part of the AWS CLI Reference.

---

```bash
# Functions
aws lambda list-functions
aws lambda get-function --function-name <name>
aws lambda invoke --function-name <name> --payload '{}' response.json

# Deploy
aws lambda update-function-code --function-name <name> --zip-file fileb://function.zip

# Logs
aws logs tail /aws/lambda/<function_name> --follow
```
