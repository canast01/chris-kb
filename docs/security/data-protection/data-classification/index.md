---
tags:
  - security
---
# Data Protection — Data Classification
![Data Protection — Data Classification](../../../assets/security-data-protection-data-classification-index.svg)


```powershell
Install-Module ExchangeOnlineManagement
Connect-IPPSSession

# List sensitivity labels
Get-Label | Select-Object DisplayName, Priority, IsDefault, Guid

# Check label policy assignments
Get-LabelPolicy | Select-Object Name, Labels, Users, Workloads
```


```d2
direction: right

center: "Data Classification" {shape: hexagon}
component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

center -> component_a
center -> component_b
center -> component_c
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

