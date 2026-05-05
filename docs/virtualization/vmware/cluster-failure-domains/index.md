# Cluster Failure Domains

## What This Means

A failure domain is the boundary where a single failure can impact multiple workloads.

## Typical Failure Domains

Host  
Rack  
Power feed  
Network switch  
Storage controller  
Availability zone

## Why It Matters

Failure domains determine:

- Resiliency
- HA behavior
- Recovery speed
- Maintenance safety

## Operational Checks

- Confirm host distribution across racks
- Confirm power diversity
- Confirm storage path redundancy
- Confirm network uplink diversity
