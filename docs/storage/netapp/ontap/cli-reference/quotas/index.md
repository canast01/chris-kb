# Quotas

> Part of the [NetApp ONTAP CLI Reference](../).

ONTAP quotas limit disk space and file counts on volumes, trees (qtrees), or users.
## View Quota Status

```bash
# Quota status on all volumes
volume quota show

# Quota report for a specific volume (current usage vs limits)
volume quota report -vserver <svm> -volume <vol>

# Quota rules for an SVM
volume quota policy rule show -vserver <svm>
```

## Enable and Disable Quotas

```bash
# Enable quotas on a volume
volume quota on -vserver <svm> -volume <vol>

# Disable quotas
volume quota off -vserver <svm> -volume <vol>

# Resize without disabling (picks up new rules)
volume quota resize -vserver <svm> -volume <vol>
```

## Quota Rule Types

| Type | Scope |
|---|---|
| `tree` | Applies to a qtree |
| `user` | Applies to a specific user |
| `group` | Applies to a group |

## Create Quota Rules

```bash
# Tree quota — limit a qtree to 500 GB
volume quota policy rule create \
    -vserver <svm> \
    -policy-name default \
    -volume <vol> \
    -type tree \
    -target /qtree_name \
    -disk-limit 500g \
    -soft-disk-limit 400g

# User quota — default user limit (empty target = all users)
volume quota policy rule create \
    -vserver <svm> \
    -policy-name default \
    -volume <vol> \
    -type user \
    -target "" \
    -disk-limit 100g

# Specific user quota
volume quota policy rule create \
    -vserver <svm> \
    -policy-name default \
    -volume <vol> \
    -type user \
    -target "DOMAIN\username" \
    -disk-limit 200g
```

## Modify a Quota Rule

```bash
volume quota policy rule modify \
    -vserver <svm> \
    -policy-name default \
    -volume <vol> \
    -type tree \
    -target /qtree_name \
    -disk-limit 1t
```

## Delete a Quota Rule

```bash
volume quota policy rule delete \
    -vserver <svm> \
    -policy-name default \
    -volume <vol> \
    -type tree \
    -target /qtree_name
```

## Quota Report Interpretation

```bash
# Full report output
volume quota report -vserver <svm> -volume <vol>
```

| Field | Meaning |
|---|---|
| Disk Used | Current space consumed |
| Disk Limit | Hard limit |
| Soft Disk Limit | Soft limit — warning threshold |
| Files Used | Current file count |
| File Limit | Maximum file count |

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Quota not enforced | Quotas enabled on volume? | `volume quota show` → state |
| Rule not applied | Did you resize? | `volume quota resize -vserver <svm> -volume <vol>` |
| User over limit | Soft or hard limit exceeded? | `volume quota report` → usage vs limits |
