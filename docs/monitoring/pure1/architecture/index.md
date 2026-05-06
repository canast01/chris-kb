# Pure1 Architecture

Pure1 is Pure Storage's cloud-based management and analytics platform. It collects telemetry from all Pure FlashArray and FlashBlade systems via outbound HTTPS from each array. No on-premises management infrastructure is required. Pure1 Meta provides AI-driven workload analytics and capacity forecasting.

| Component | Role |
|---|---|
| Pure1 Cloud | SaaS platform hosted by Pure Storage |
| Array telemetry | Outbound HTTPS from each FlashArray/FlashBlade to pure1.purestorage.com |
| Pure1 Meta | AI/ML engine for workload analytics and capacity forecasting |
| Pure1 REST API | Programmatic access to fleet health, metrics, and alerts |
