---
tags:
  - aria-operations
  - aria-logs
  - aria-automation
  - aria-networks
  - aria-suite-lifecycle
  - operations
description: "Choose the right Aria product for your need: performance monitoring, log management, infrastructure automation, network visibility, or lifecycle..."
---
# Aria Product Selection Decision Tree

*Applies to: All products*

<div class="kb-summary">
Choose the right Aria product for your need: performance monitoring, log management, infrastructure automation, network visibility, or lifecycle management of the Aria Suite itself.
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "Aria Operations\nformerly vROps\nAdapters: vCenter · NSX · storage" {shape: rectangle}
D: "Aria Logs\nformerly Log Insight\nliagent or syslog UDP/514" {shape: rectangle}
E: "Aria Automation\nformerly vRA\nCloud accounts: vCenter · AWS · Azure" {shape: rectangle}
F: "Aria Networks\nformerly vRNI\nData sources: NSX · vCenter · switches" {shape: rectangle}
G: "Aria Suite Lifecycle\nformerly LCM\nDeploys all Aria Suite products" {shape: rectangle}
H: "H" {shape: rectangle}
I: "Use Aria Suite Lifecycle\nto deploy and manage all products\nSingle pane for certs and upgrades" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Deploy Workspace ONE Access\nformerly VMware Identity Manager\nSAML IdP for all Aria products" {shape: rectangle}
L: "Deploy product directly\nLocal admin auth\nOVA or LCM-managed" {shape: rectangle}
M: "Full Aria Suite stack\nLCM + Workspace ONE Access\n+ chosen Aria products" {shape: rectangle}
A: "Start: Which Aria product do I need?" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
D -> H
E -> H
F -> H
H -> I
G -> J
I -> J
J -> K
J -> L
K -> M
```

## Product summary

| Product | Purpose | Key API | Replaces |
|---|---|---|---|
| Aria Operations | Performance monitoring, alerting, capacity | `suite-api/api` | vRealize Operations (vROps) |
| Aria Logs | Log aggregation and search | REST `/api/v1` + liagent | vRealize Log Insight |
| Aria Automation | Self-service IaaS catalog | `/deployment/api` | vRealize Automation (vRA) |
| Aria Networks | Network visibility and path analysis | `/api/ni` | vRealize Network Insight (vRNI) |
| Aria Suite Lifecycle | Deploy and upgrade Aria Suite | `lcm/api/v2` | vRealize Suite Lifecycle Manager (LCM) |
| Workspace ONE Access | SSO and identity for Aria | SAML / LDAP | VMware Identity Manager (vIDM) |

## Deployment order when installing the full suite

1. **Workspace ONE Access** — must be first; all other products register with it for SSO
2. **Aria Operations** — connect vCenter and NSX adapters immediately after deploy
3. **Aria Logs** — configure liagent on VMs and forward vCenter/NSX syslog
4. **Aria Automation** — add vCenter and NSX cloud accounts after deploy
5. **Aria Networks** — add NSX and vCenter as data sources after deploy

All steps are orchestrated by **Aria Suite Lifecycle** when deploying via LCM.

## See also

- [Aria Operations Cheat Sheet](../../cheat-sheets/aria-operations/)
- [Aria Logs Cheat Sheet](../../cheat-sheets/aria-logs/)
- [Aria Automation Cheat Sheet](../../cheat-sheets/aria-automation/)
- [Aria Networks Cheat Sheet](../../cheat-sheets/aria-networks/)
- [Aria Suite Lifecycle Cheat Sheet](../../cheat-sheets/aria-suite-lifecycle/)
- [Automation Interaction Map](../../interaction-map/automation/)
- [Back to Decision Trees](index.md)
