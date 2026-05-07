# AD Groups

AD groups control access to resources and distribution of email. Choosing the correct type and scope prevents replication overhead and simplifies permission management.

## Group Types and Scopes

| Scope | Can Contain | Used For | Replicates To |
|---|---|---|---|
| Domain Local | Users, Global, Universal from any domain | Assigning permissions to local resources | Domain only |
| Global | Users and Global from same domain | Grouping users by role | Entire forest |
| Universal | Users, Global, Universal from any domain | Cross-domain role assignments | Global Catalog |
| Distribution | Any | Email only (not security) | Domain only |

Best practice: follow AGDLP — Accounts in Global groups, Global in Domain Local groups, Domain Local assigned Permissions.

## Creating Groups

```powershell
# Create a security group (Global scope)
New-ADGroup -Name "SG-ServerAdmins" `
    -GroupScope Global `
    -GroupCategory Security `
    -Path "OU=Groups,DC=corp,DC=example,DC=com" `
    -Description "Server administrators"

# Create a distribution group
New-ADGroup -Name "DG-ITTeam" `
    -GroupScope Universal `
    -GroupCategory Distribution `
    -Path "OU=Groups,DC=corp,DC=example,DC=com"

# Create a Domain Local group for resource access
New-ADGroup -Name "DL-FileShare-Finance-RW" `
    -GroupScope DomainLocal `
    -GroupCategory Security `
    -Path "OU=Groups,DC=corp,DC=example,DC=com"
```

## Managing Group Membership

```powershell
# Add a single member
Add-ADGroupMember -Identity "SG-ServerAdmins" -Members "jsmith"

# Add multiple members
Add-ADGroupMember -Identity "SG-ServerAdmins" -Members "jsmith","bwilson","DC01$"

# Remove a member
Remove-ADGroupMember -Identity "SG-ServerAdmins" -Members "jsmith" -Confirm:$false

# List all members recursively
Get-ADGroupMember -Identity "SG-ServerAdmins" -Recursive

# List all groups a user belongs to
Get-ADPrincipalGroupMembership -Identity "jsmith" | Select-Object Name, GroupScope, GroupCategory
```

## Group Nesting

```powershell
# Add a Global group into a Domain Local group (AGDLP)
Add-ADGroupMember -Identity "DL-FileShare-Finance-RW" -Members "SG-FinanceUsers"

# Find nested groups inside a group
Get-ADGroupMember -Identity "DL-FileShare-Finance-RW" -Recursive |
    Where-Object {$_.objectClass -eq "group"}

# Show full group chain for a user
Get-ADPrincipalGroupMembership -Identity "jsmith" -Recursive |
    Select-Object Name, GroupScope | Sort-Object Name
```

## Auditing and Reporting

```powershell
# Find empty groups
Get-ADGroup -Filter * -Properties Members |
    Where-Object {$_.Members.Count -eq 0} | Select-Object Name

# Find groups with no members and not nested anywhere
Get-ADGroup -Filter * -Properties Members, MemberOf |
    Where-Object {$_.Members.Count -eq 0 -and $_.MemberOf.Count -eq 0} |
    Select-Object Name, DistinguishedName

# Export group membership to CSV
Get-ADGroupMember "SG-ServerAdmins" |
    Select-Object Name, SamAccountName, objectClass |
    Export-Csv C:\Reports\SG-ServerAdmins.csv -NoTypeInformation

# Find all groups a computer account is in
Get-ADPrincipalGroupMembership -Identity "DC01$" | Select-Object Name
```
