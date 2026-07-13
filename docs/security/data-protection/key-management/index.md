---
tags:
  - security
---
# Data Protection — Key Management

```bash
# Create a key
aws kms create-key --description "prod-data-key" --key-usage ENCRYPT_DECRYPT

# Enable automatic rotation (annual, symmetric only)
aws kms enable-key-rotation --key-id <key-id>

# Check rotation status
aws kms get-key-rotation-status --key-id <key-id>

# Schedule deletion (7–30 day waiting period)
aws kms schedule-key-deletion --key-id <key-id> --pending-window-in-days 30

# Cancel deletion
aws kms cancel-key-deletion --key-id <key-id>
```


```text title="Expected output"
{
    "KeyMetadata": {
        "AWSAccountId": "123456789012",
        "KeyId": "arn:aws:kms:us-east-1:123456789012:key/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "Arn": "arn:aws:kms:us-east-1:123456789012:key/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "CreationDate": "2024-01-15T10:32:44.123000+00:00",
        "Enabled": true,
        "Description": "prod-data-key",
        "KeyUsage": "ENCRYPT_DECRYPT",
        "KeyState": "Enabled",
        "Origin": "AWS_KMS",
        "MultiRegion": false
    }
}
(no output — command completes silently)
{
    "KeyRotationEnabled": true
}
{
    "KeyId": "arn:aws:kms:us-east-1:123456789012:key/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "DeletionDate": "2024-02-14T10:35:22.456000+00:00"
}
{
    "KeyId": "arn:aws:kms:us-east-1:123456789012:key/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidKeyId.Malformed) when calling the EnableKeyRotation operation: 1 validation error detected: Value at 'keyId' failed to satisfy constraint: Member must satisfy regular expression pattern: [\w-]{1,2048}` | Replace `<key-id>` placeholder with the actual key ID or ARN from the create-key output. |
    | `An error occurred (UnsupportedOperationException) when calling the EnableKeyRotation operation: The request is not valid for key spec ENCRYPT_SIGN.` | Key rotation is only supported for symmetric keys; asymmetric or signing keys cannot have automatic rotation enabled. |
    | `An error occurred (InvalidStateException) when calling the CancelKeyDeletion operation: arn:aws:kms:us-east-1:123456789012:key/a1b2c3d4-e5f6-7890-abcd-ef1234567890 is not scheduled for deletion.` | Verify the key is actually in PendingDeletion state before attempting cancellation. |
```bash
# Check key manager status
security key-manager show

# Query encryption keys
security key-manager key query

# Check volume encryption state
volume show -fields encryption-state
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

