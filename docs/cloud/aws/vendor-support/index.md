# AWS Vendor Support

AWS Support plans range from Developer (business-hours email, general guidance) through Business (24/7 phone/chat, <1 hr critical response, Trusted Advisor full checks) to Enterprise (TAM, <15 min critical response, concierge support). Support cases are opened via the AWS Console under Support Center or programmatically via the AWS Support API (`aws support create-case`). Before opening a case, collect the affected resource ARNs, account ID, region, approximate start time of the issue, and relevant CloudWatch logs or VPC Flow Logs.

| Plan | Best for | Critical response SLA |
|---|---|---|
| Developer | Dev/test, individual | < 12 hours (business hours) |
| Business | Production workloads | < 1 hour |
| Enterprise On-Ramp | Growing production | < 30 minutes |
| Enterprise | Mission-critical / large scale | < 15 minutes + TAM |

**Key resources:**

- AWS Support Center: `console.aws.amazon.com/support`
- AWS Health Dashboard: `health.aws.amazon.com` — service event and account-specific health notifications
- Trusted Advisor: automated checks for cost, security, fault tolerance, performance, and service limits
- Support API: `aws support describe-cases`, `aws support create-case` (requires Business or Enterprise plan)
