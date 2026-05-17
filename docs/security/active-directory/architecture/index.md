# Active Directory — Architecture

<div class="kb-summary">
Windows Server Active Directory forest with multi-site domain controllers, Kerberos authentication, LDAP directory services, and FSMO role delegation across primary and replica DCs.
</div>

![Active Directory Architecture](../../../assets/active-directory-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Forest hierarchy, FSMO roles, Kerberos auth, replication topology, and LDAP flows.</span>
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

## FSMO Roles

| FSMO Role | Scope | Recommended DC |
|---|---|---|
| Schema Master | Forest-wide | Forest root DC 1 |
| Domain Naming Master | Forest-wide | Forest root DC 1 |
| PDC Emulator | Per domain | Most capable DC; close to users (time source) |
| RID Master | Per domain | Same site as PDC Emulator preferred |
| Infrastructure Master | Per domain | Not a GC DC (if single-domain, can be GC) |

## Forest and Domain Hierarchy

```mermaid
graph TB
  FOREST["AD Forest\n(security boundary)"] --> ROOT["Forest Root Domain\ncorp.example.com"]
  ROOT --> DC1["DC-01 Site A\nPDC · RID · Infra Master"]
  ROOT --> DC2["DC-02 Site A\nGlobal Catalog"]
  ROOT -->|"AD replication"| DC3["DC-03 · DC-04\nSite B — replica DCs"]
  ROOT --> CHILD["Child Domain\ndivision.corp.example.com"]
  CHILD --> CDC["Child DC"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class DC1,DC2,DC3,CDC ctrl
  class FOREST,ROOT,CHILD mgmt
```
