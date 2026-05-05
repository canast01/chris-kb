# HA Admission Control

## Purpose

Ensures enough resources exist to restart VMs after a host failure.

## Common Policies

Host failures cluster tolerates

Percentage of cluster resources reserved

Dedicated failover hosts

## Operational Check

Cluster → Configure → vSphere HA

Verify:

Admission control enabled  
Failover capacity available  
No warnings

## Risk Indicator

Insufficient failover capacity warning
