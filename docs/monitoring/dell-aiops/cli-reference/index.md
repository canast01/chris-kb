# Dell AIOps CLI Reference

Dell AIOps does not have a dedicated CLI — all interaction is via the CloudIQ web portal or REST API. The CloudIQ REST API uses OAuth2 client credentials authentication and provides programmatic access to recommendations, anomalies, and system health data.

**Authentication**

```bash
# Obtain OAuth2 access token (client credentials flow)
POST https://api.cloudiq.dell.com/auth/oauth/v2/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=<CLIENT_ID>&client_secret=<CLIENT_SECRET>
```

**Key REST API Endpoints**

| Endpoint | Method | Purpose |
|---|---|---|
| `/cloudiq/rest/v1/recommendations` | GET | List all AI-generated recommendations |
| `/cloudiq/rest/v1/anomalies` | GET | List detected anomalies |
| `/cloudiq/rest/v1/systems` | GET | List all monitored storage systems |
| `/cloudiq/rest/v1/systems/{id}/health` | GET | Health score for a specific system |
| `/cloudiq/rest/v1/alerts` | GET | List active alerts |

All API requests include `Authorization: Bearer <token>` and `Content-Type: application/json` headers. The CloudIQ API base URL is `https://api.cloudiq.dell.com`.
