# Superna Eyeglass — Initial Deployment

## Prerequisites

PowerScale (Isilon) clusters at both sites (production and DR), vSphere for Eyeglass virtual appliance, network access between Eyeglass and both clusters (HTTPS 8080/443), Eyeglass licence, DNS entries for both cluster SmartConnect zones.

## Deploy the Eyeglass Appliance

Download OVA from Superna portal, deploy to vSphere, assign IP/DNS/gateway, power on, complete first-boot wizard.

## Connect to Source Cluster

Eyeglass Configuration → Add Cluster → enter source PowerScale management IP/FQDN → credentials (admin or service account with appropriate role) → test connectivity → save.

## Connect to DR Cluster

Add second cluster (DR PowerScale) → credentials → test → save.

## Configure Replication Jobs

Eyeglass → Configuration Replication → New Job → select source cluster → select shares/exports/quotas to replicate → select DR cluster as target → set schedule → save.

## Configure User and Group Sync

Eyeglass → User and Group Replication → enable → select source and target clusters → test sync.

## Run First Sync

Trigger manual sync for all replication jobs → verify shares/exports/quotas appear on DR cluster → verify ACLs are preserved.

## Validate the Deployment

Eyeglass → DR Testing → Runbook → generate DR readiness report → verify all jobs show Ready → document last sync timestamp → schedule first DR test.
