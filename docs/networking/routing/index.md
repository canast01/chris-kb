# Routing

## Overview

Routing determines how traffic moves between networks. It is required for server access, storage replication, cloud connectivity, backup traffic, and application communication.

## Daily Checks

- Confirm default gateway reachability
- Review route tables
- Check dynamic routing neighbor state
- Validate critical path connectivity

## Health Commands

```bash
ip route
route print
show ip route
show ip ospf neighbor
show bgp summary
```

## Troubleshooting Workflow

1. Confirm source subnet
2. Confirm destination subnet
3. Check local route table
4. Trace path
5. Review firewall and ACL rules
