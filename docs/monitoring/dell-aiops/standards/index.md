# Dell AIOps Standards

CloudIQ tagging should be aligned with organisational standards: every storage system must be tagged with `site`, `environment` (prod/non-prod), and `tier` (tier1/tier2/tier3) for effective recommendation filtering and reporting. Alert routing rules are configured per recommendation severity: Critical and High recommendations trigger immediate notifications; Medium and Low are reviewed in the weekly operational queue. AI-generated recommendations that require infrastructure changes must follow the standard change management approval workflow before action is taken. Integration with the ITSM system ensures all actioned recommendations are tracked as change records.

- Required tags: `site`, `environment`, `tier`
- Alert routing: Critical/High → immediate notification; Medium/Low → weekly review queue
- Recommendation action: requires change management approval for infrastructure changes
- ITSM tracking: all actioned recommendations logged as change records
