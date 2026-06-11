# Amazon EVS — Authentication

<div class="kb-summary">
vCenter SSO configuration, Active Directory integration for vSphere and NSX-T, MFA for AWS console access, SSH key rotation for EVS bare-metal hosts, and service account management.
</div>

```text
┌───────────────────────────────────── Amazon EVS — Authentication ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   vCenter SSO: local vsphere.local domain; join AD for centralized authentication             │   │
│   │   NSX-T: local admin account + LDAP integration for group-based access                        │   │
│   │   AWS: MFA enforced for all IAM users; EVS operations require IAM role assumption             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vCenter SSO  = Single Sign-On for all vSphere auth; vsphere.local domain by default                  │
│  AD identity source = Active Directory LDAP connection added to vCenter SSO for user login            │
│  LDAP         = Lightweight Directory Access Protocol; used by vCenter and NSX-T for AD lookup        │
│  NSX-T LDAP   = NSX Manager → System → Users and Roles → LDAP for group-based access                  │
│  MFA          = Multi-Factor Authentication; enforced via IAM policy for console and CLI access       │
│  IAM role assumption = Using sts:AssumeRole to get temporary credentials for EVS API calls            │
│  SSH key      = EC2 key pair for bare-metal host access; rotate regularly; disable after setup        │
│  Service account = Non-human identity for automation; store credentials in Secrets Manager            │
│  Secrets Manager = AWS service for storing and rotating vCenter/SDDC Manager credentials              │
│  AWS SSO      = AWS Identity Center; federates corporate IdP to AWS accounts including EVS            │
│  OIDC         = OpenID Connect; used by AWS SSO for federation with Okta/Entra ID/Google              │
│  Token expiry = IAM temporary credential TTL; default 1 hour for assumed roles; max 12 hours          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## vCenter SSO — Active Directory Integration

```powershell
# Add AD as identity source in vCenter SSO
# vCenter UI → Administration → Single Sign On → Configuration → Identity Sources → Add

# Via API (recommended for automation):
$body = @{
  type = "ActiveDirectory"
  settings = @{
    userBaseDn = "OU=Users,DC=corp,DC=example,DC=com"
    groupBaseDn = "OU=Groups,DC=corp,DC=example,DC=com"
    searchTimeoutSeconds = 300
    serverEndpoints = @(@{ ldapUrl = "ldap://dc01.corp.example.com:389" })
    username = "svc-vsphere@corp.example.com"
    password = $env:AD_SVC_PASSWORD
  }
  domainAlias = "corp"
  name = "corp.example.com"
}
# Submit via vCenter REST API: POST /api/vcenter/identity/providers

# Verify AD groups appear in vCenter
# vCenter → Administration → Single Sign On → Users and Groups → select corp domain
```

## NSX-T LDAP Integration

```bash
# Add LDAP identity source to NSX-T
curl -sk -u "admin:$NSX_PASSWORD" \
  -X POST "$NSX_URL/api/v1/node/aaa/providers/ldap" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "corp-ad",
    "ldap_servers": [{"bind_dn": "CN=svc-nsx,OU=ServiceAccounts,DC=corp,DC=example,DC=com",
                       "bind_password": "PASSWORD",
                       "ldap_url": "ldap://dc01.corp.example.com:389"}],
    "domain_name": "corp.example.com",
    "base_dn": "OU=Users,DC=corp,DC=example,DC=com",
    "type": "ActiveDirectory",
    "enabled": true
  }' | python3 -m json.tool

# Test LDAP connectivity
curl -sk -u "admin:$NSX_PASSWORD" \
  -X POST "$NSX_URL/api/v1/node/aaa/providers/ldap?action=test" | python3 -m json.tool
```

## AWS Console MFA Enforcement

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyAllExceptListedIfNoMFA",
      "Effect": "Deny",
      "NotAction": [
        "iam:CreateVirtualMFADevice",
        "iam:EnableMFADevice",
        "iam:GetUser",
        "iam:ListMFADevices",
        "iam:ListVirtualMFADevices",
        "iam:ResyncMFADevice",
        "sts:GetSessionToken"
      ],
      "Resource": "*",
      "Condition": {
        "BoolIfExists": {
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    }
  ]
}
```

```bash
# Enforce MFA for EVS operations — attach this policy to the EVS operator role/group
aws iam put-user-policy \
  --user-name evs-operator \
  --policy-name RequireMFA \
  --policy-document file://require-mfa.json

# Verify MFA is configured for user
aws iam list-mfa-devices --user-name evs-operator
```

## SSH Key Management (ESXi Hosts)

```bash
# EVS hosts use SSH keys for initial ESXi DCUI access.
# Rotate the key pair periodically:

# 1. Generate new key pair
aws ec2 create-key-pair --key-name evs-cluster-key-new --output text > evs-cluster-key-new.pem
chmod 400 evs-cluster-key-new.pem

# 2. Deploy new public key to each ESXi host
# Note: requires current SSH access or DCUI session
for HOST in $(aws evs list-environment-hosts --environment-id $ENV_ID \
  --query 'hostSummaries[*].hostId' --output text); do
  echo "Updating key on host: $HOST"
  # Add new public key to /etc/ssh/keys-root/authorized_keys via current SSH session
done

# 3. Update EVS host records to reference new key
# (Next host additions will use the new key name)

# 4. Delete old key pair after verification
aws ec2 delete-key-pair --key-name evs-cluster-key
```
