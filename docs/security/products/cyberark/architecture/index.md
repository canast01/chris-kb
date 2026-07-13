---
tags:
  - architecture
  - security
description: "PAM platform with Digital Vault as the encrypted credential store, CPM for automated rotation, PSM for session proxying and recording, and PVWA as the web..."
---
# CyberArk — Architecture

<div class="kb-summary">
PAM platform with Digital Vault as the encrypted credential store, CPM for automated rotation, PSM for session proxying and recording, and PVWA as the web interface; primary and DR Vault pair with asynchronous replication.

*Applies to: CyberArk PAM*
</div>

![CyberArk — Architecture — Diagram](../../../../assets/security-cyberark-architecture-diagram.svg)

![CyberArk Architecture](../../../../assets/cyberark-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Component roles, network topology, credential checkout, HA, and DR activation.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## Component Overview

| Component | Role | Typical Count |
|---|---|---|
| Digital Vault | Encrypted credential store, core engine | 2 (primary + DR) |
| CPM (Central Policy Manager) | Automated password rotation | 1–2 per site |
| PSM (Privileged Session Manager) | Session proxy, recording, isolation | 2+ (load-balanced) |
| PVWA (Password Vault Web Access) | Web UI and REST API | 2+ (load-balanced) |
| PSMP | SSH proxy for Linux privileged access | 1–2 per site |
| DR Vault | Asynchronous replication replica of Vault | 1 per DR site |

## PAM Component Topology

```d2
direction: right

PVWA: "PVWA\n(web interface" {shape: rectangle}
PSM: "PSM\n(session proxy" {shape: rectangle}
CPM: "CPM\n(rotation engine" {shape: rectangle}
VAULT: "CyberArk Vault\n(encrypted credential store" {shape: rectangle}
USER: "Privileged User" {shape: rectangle}
TARGET: "Target Servers" {shape: rectangle}

PVWA -> PSM
PSM -> CPM
CPM -> VAULT
USER -> PVWA
PSM -> TARGET
CPM -> TARGET
```
