# ONTAP — Authentication

> SSO, LDAP, local accounts, and identity sources for NetApp ONTAP.

## Local Accounts

ONTAP supports local admin accounts at both the cluster level and the SVM level.

```bash
# List all login accounts
security login show

# Create a local account with password authentication
security login create \
    -username <user> \
    -application ssh \
    -authentication-method password \
    -role admin \
    -vserver <cluster-or-svm>

# Create a local account with public key authentication
security login create \
    -username <user> \
    -application ssh \
    -authentication-method publickey \
    -role admin \
    -vserver <cluster-or-svm>
```

## Active Directory / CIFS Authentication

Join an SVM to Active Directory to enable CIFS/SMB access and Kerberos-based NFS authentication:

```bash
# Join an SVM to Active Directory for CIFS/SMB
vserver cifs create -vserver <svm> -cifs-server <netbios-name> -domain <domain.corp> -ou "OU=Servers,DC=domain,DC=corp"

# Verify CIFS domain join and DC connectivity
vserver cifs domain info -vserver <svm>

# Check AD join status
vserver cifs show -vserver <svm> -fields ad-status
```

## LDAP Integration

LDAP is used for user mapping (NFS Kerberos UID/GID resolution) and name services:

```bash
# Configure LDAP for NFS Kerberos and user mapping
vserver services name-service ldap create -vserver <svm> -client-config <ldap-config>

# Show LDAP configuration for an SVM
vserver services name-service ldap show -vserver <svm>

# Show name service switch (lookup order)
vserver services name-service ns-switch show -vserver <svm>
```

## SNMPv3 Authentication

```bash
# Configure SNMPv3 user with authentication and privacy
system snmp user create -username snmpv3user -authmethod md5 -authpassword <auth-pass> -privmethod aes128 -privpassword <priv-pass>

# Add SNMPv3 trap host
system snmp traphost add -ipaddr <monitoring-host> -username snmpv3user
```

Disable SNMPv1/v2c if enabled:
```bash
system snmp community delete -community-name public
system snmp community delete -community-name <any-other-v1v2-community>
```

## SSH Key Authentication

Disable password authentication for the admin account and require SSH public keys:

```bash
# Add a public key for a user
security login publickey create -username admin -index 0 -publickey "ssh-rsa AAAA..."

# Verify public keys configured
security login publickey show

# Disable password authentication (after confirming key works)
security login modify -username admin -application ssh -authentication-method publickey
```
