# Aria Operations Standards

Alert naming follows the pattern `ENV-OBJECT_TYPE-CONDITION` (e.g., `PROD-VM-CPU_CONTENTION`) to ensure consistent filtering and routing. Policy hierarchy is structured globally to specifically: a Global Default Policy sets baselines, Environment Policies (prod/non-prod) override thresholds, and Cluster Policies apply workload-specific tuning. Super metric names use the prefix `SM_` followed by a descriptive camel-case name. Custom groups are named by environment and object type, and dashboard names include the team owner prefix (e.g., `INFRA-Capacity-Overview`).

- Alert naming: `ENV-OBJECT_TYPE-CONDITION`
- Policy hierarchy: Global → Environment → Cluster
- Super metric prefix: `SM_`
- Custom group naming: `ENV-ObjectType`
- Dashboard naming: `TEAM-Topic-Scope`
- Report schedules aligned to operational cadence (daily, weekly, monthly)
