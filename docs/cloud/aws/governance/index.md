# AWS Governance

<div class="kb-summary">
AWS governance is structured around AWS Organizations with a management account, Security/Log Archive accounts, and workload accounts per environment. SCPs enforce preventive guardrails at the OU level; AWS Config with conformance packs handles detective compliance. Tagging standards and naming conventions underpin cost allocation and resource ownership.
</div>

![AWS Governance Architecture](../../../assets/aws-governance-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="aws-config/">
  <strong>AWS Config</strong>
  <span>Resource inventory, compliance rules, and drift review.</span>
</a>

<a class="kb-card" href="aws-organizations/">
  <strong>AWS Organizations</strong>
  <span>Accounts, OUs, policies, and governance boundaries.</span>
</a>

<a class="kb-card" href="service-control-policies/">
  <strong>Service Control Policies</strong>
  <span>SCP design, guardrails, testing, and exceptions.</span>
</a>

<a class="kb-card" href="account-structure/">
  <strong>Account Structure</strong>
  <span>Account layout, ownership, environment separation, and standards.</span>
</a>

<a class="kb-card" href="tagging-standards/">
  <strong>Tagging Standards</strong>
  <span>Required tags, cost tags, ownership, and compliance.</span>
</a>

<a class="kb-card" href="compliance-review/">
  <strong>Compliance Review</strong>
  <span>Control review, evidence, drift, and remediation tracking.</span>
</a>

</div>
