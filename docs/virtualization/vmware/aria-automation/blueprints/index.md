# Aria Automation — Blueprints

## Overview

Blueprints (Cloud Templates) define infrastructure-as-code for Aria Automation deployments. They are written in YAML and describe resources, their properties, and relationships. Blueprints are versioned and can be published to the Service Catalog.

## Blueprint Structure

A Cloud Template YAML has three top-level sections:

```yaml
formatVersion: 1
inputs:
  vmName:
    type: string
    title: VM Name
    default: my-vm
  cpuCount:
    type: integer
    title: CPU Count
    default: 2
    enum: [2, 4, 8]

resources:
  Cloud_vSphere_Machine_1:
    type: Cloud.vSphere.Machine
    properties:
      name: ${input.vmName}
      image: ubuntu-22-04
      flavor: medium
      cpuCount: ${input.cpuCount}
      memoryInMB: 4096
      networks:
        - network: ${resource.Cloud_vSphere_Network_1.id}
          assignment: static
      tags:
        - key: owner
          value: ${env.requestedBy}

  Cloud_vSphere_Network_1:
    type: Cloud.vSphere.Network
    properties:
      networkType: existing
      name: VLAN-100-Servers
```

## Inputs

Inputs allow users to parameterise deployments at request time:

| Input Type | Example Use | Constraints Available |
|---|---|---|
| `string` | VM name, hostname | `minLength`, `maxLength`, `pattern` |
| `integer` | CPU count, disk size | `minimum`, `maximum`, `enum` |
| `number` | Memory GB | `minimum`, `maximum` |
| `boolean` | Enable monitoring | — |
| `object` | Custom tags map | — |
| `array` | List of IP addresses | `items`, `minItems` |

```yaml
inputs:
  environment:
    type: string
    title: Target Environment
    enum:
      - dev
      - staging
      - prod
    default: dev
  diskSizeGB:
    type: integer
    title: Additional Disk Size (GB)
    minimum: 50
    maximum: 2048
    default: 100
```

## Resource Types

Common resource types used in blueprints:

| Resource Type | Description |
|---|---|
| `Cloud.vSphere.Machine` | Virtual machine on vSphere |
| `Cloud.vSphere.Network` | vSphere port group or NSX segment |
| `Cloud.vSphere.Disk` | Additional managed disk |
| `Cloud.NSX.Network` | NSX-T overlay segment |
| `Cloud.NSX.LoadBalancer` | NSX load balancer |
| `Cloud.AWS.EC2.Instance` | AWS EC2 instance |
| `Cloud.Azure.Machine` | Azure virtual machine |

## Blueprint Versioning and Publishing

```bash
# List blueprints via vRA API
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints \
  | python3 -m json.tool

# Get a specific blueprint
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints/<blueprint-id> \
  | python3 -m json.tool

# Create a new blueprint version
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints/<blueprint-id>/versions \
  -H "Content-Type: application/json" \
  -d '{"version": "1.2", "description": "Added NSX segment"}'

# Publish a version to Service Catalog
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints/<blueprint-id>/versions/<version>/actions/publish
```

## Constraints and Placement Policies

Use constraints to control where resources are placed:

```yaml
resources:
  Cloud_vSphere_Machine_1:
    type: Cloud.vSphere.Machine
    properties:
      name: ${input.vmName}
      image: ubuntu-22-04
      flavor: medium
      constraints:
        - tag: env:prod
        - tag: "datacenter:dc01"
      networks:
        - network: ${resource.Cloud_vSphere_Network_1.id}
```

## Blueprint Validation

```bash
# Validate blueprint YAML locally (requires vRA CLI)
vra-cli blueprint validate --file ./blueprint.yaml

# Validate via API
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints/validate \
  -H "Content-Type: application/json" \
  -d @blueprint.json

# Get API token for automation
curl -sk -X POST https://<vra-fqdn>/csp/gateway/am/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' \
  | python3 -m json.tool | grep "access_token"
```
