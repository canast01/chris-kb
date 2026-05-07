# SVMs (Storage Virtual Machines)

> Part of the [NetApp ONTAP CLI Reference](../).

SVMs (also called Vservers) are the data access layer in ONTAP. Each SVM has its own namespace, protocols, network interfaces, and security configuration.
## List and View SVMs

```bash
# All SVMs
vserver show

# SVM with protocol and state info
vserver show -fields vserver, type, state, allowed-protocols

# Specific SVM detail
vserver show -vserver <svm>
```

## Create an SVM

```bash
# Create with NFS and CIFS protocols
vserver create \
    -vserver <svm_name> \
    -rootvolume <vol_name> \
    -aggregate <aggr_name> \
    -rootvolume-security-style unix \
    -language C.UTF-8

# Set allowed protocols
vserver modify -vserver <svm_name> -allowed-protocols nfs, cifs
```

## Delete an SVM

```bash
# Stop the SVM first
vserver stop -vserver <svm_name>

# Delete (removes all volumes and configuration)
vserver delete -vserver <svm_name>
```

## Protocol Management

```bash
# View protocols enabled on an SVM
vserver show-protocols -vserver <svm_name>

# Modify allowed protocols
vserver modify -vserver <svm_name> -allowed-protocols nfs, cifs, iscsi
```

## Network Interfaces (LIFs)

```bash
# List LIFs for an SVM
network interface show -vserver <svm_name>

# Create a data LIF
network interface create \
    -vserver <svm_name> \
    -lif <lif_name> \
    -role data \
    -data-protocol nfs \
    -home-node <node_name> \
    -home-port <port> \
    -address <ip> \
    -netmask <mask>

# Migrate a LIF to another port
network interface migrate \
    -vserver <svm_name> \
    -lif <lif_name> \
    -dest-node <node_name> \
    -dest-port <port>
```

## CIFS / Active Directory Join

```bash
# Join SVM to Active Directory
vserver cifs create \
    -vserver <svm_name> \
    -cifs-server <netbios_name> \
    -domain corp.local \
    -ou "OU=StorageServers,DC=corp,DC=local"

# Check AD join status
vserver cifs show -vserver <svm_name>
```

## NFS Service

```bash
# Enable NFS on an SVM
vserver nfs create -vserver <svm_name> -access true -v3 enabled -v4.1 enabled

# NFS status
vserver nfs show -vserver <svm_name>
```

## SVM State Management

```bash
# Stop an SVM (client access suspended)
vserver stop -vserver <svm_name>

# Start an SVM
vserver start -vserver <svm_name>
```

## SVM DR (Disaster Recovery)

```bash
# SnapMirror relationships on an SVM
snapmirror show -destination-vserver <svm_name>
```
