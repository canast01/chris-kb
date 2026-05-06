# Dell AIOps Architecture

Dell AIOps (formerly APEX AIOps) is Dell's AI-driven IT operations platform integrated with CloudIQ and the Apex Console, providing anomaly detection, root cause analysis, and predictive recommendations across the Dell storage estate. Telemetry is collected from on-premises Dell storage arrays via the Secure Connect Gateway (SCG), which forwards data to Dell's cloud AI pipeline for processing. The AI models analyse telemetry streams to surface anomalies and generate prioritised recommendations without requiring on-premises AI infrastructure. The platform is fully SaaS-delivered, with no customer-managed compute components beyond the SCG.

| Component | Role |
|---|---|
| CloudIQ / Apex Console | SaaS portal — recommendations, anomaly dashboard, health scores |
| Secure Connect Gateway (SCG) | On-premises telemetry collection and secure forwarding agent |
| Dell AI Pipeline (cloud) | Anomaly detection and root cause analysis (Dell-managed) |
| Storage Arrays | Data sources: PowerStore, PowerMax, PowerScale, Unity XT, etc. |
