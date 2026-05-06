# Masking Views

A Masking View on PowerMax connects three components — a Storage Group (volumes), a Port Group (FA ports), and an Initiator Group (host HBAs) — to grant a host access to storage. All three must exist before the Masking View can be created.

## List and Inspect

```bash
# List all masking views
symaccess list -sid <sid> view

# Show a specific masking view
symaccess show view <view_name> -sid <sid>

# Show which masking views a host's initiators are in
symaccess show -inits <wwn> -sid <sid>

# Show all masking views for a storage group
symaccess list -sid <sid> view -sg <sg_name>
```

## Initiator Groups

```bash
# List all initiator groups
symaccess list -sid <sid> -type initiator

# Show initiators in a group
symaccess show <ig_name> -sid <sid> -type initiator

# Create an initiator group
symaccess create -sid <sid> -name <ig_name> -type initiator

# Add host HBA WWN to initiator group
symaccess -sid <sid> -name <ig_name> -type initiator add -wwn <wwn>

# Remove initiator
symaccess -sid <sid> -name <ig_name> -type initiator remove -wwn <wwn>

# Create a cascaded (parent) initiator group
symaccess create -sid <sid> -name <parent_ig> -type initiator
symaccess -sid <sid> -name <parent_ig> -type initiator add -ig <child_ig>
```

## Port Groups

```bash
# List all port groups
symaccess list -sid <sid> -type port

# Show ports in a group
symaccess show <pg_name> -sid <sid> -type port

# Create a port group
symaccess create -sid <sid> -name <pg_name> -type port

# Add FA port to port group
symaccess -sid <sid> -name <pg_name> -type port add -dirport <dir_id>:<port_id>

# Remove port
symaccess -sid <sid> -name <pg_name> -type port remove -dirport <dir_id>:<port_id>
```

## Creating a Masking View

```bash
# Prerequisites: SG, IG, and PG must all exist
# Create the masking view linking all three
symaccess create view -sid <sid> -name <view_name> \
    -sg <sg_name> \
    -ig <ig_name> \
    -pg <pg_name>
```

## Deleting a Masking View

```bash
# Delete masking view (does not delete SG/IG/PG)
symaccess delete view <view_name> -sid <sid>

# Delete an initiator group (must not be in any masking view)
symaccess delete -sid <sid> -name <ig_name> -type initiator

# Delete a port group
symaccess delete -sid <sid> -name <pg_name> -type port
```

## Troubleshooting Host Access

```bash
# Verify host WWN is registered with the array
symcfg -sid <sid> list -dir all | grep <wwn>

# Check which LUNs a host can see
symaccess show view <view_name> -sid <sid> | grep -A 20 "Storage Group"

# Verify host-to-LUN assignment is correct
symdev show <devname> -sid <sid> | grep -A 5 "Host"
```
