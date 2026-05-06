# Pure1 CLI Reference

Pure1 provides a REST API authenticated via OAuth2 client credentials. The `pure1` CLI (if installed) wraps common API calls for interactive use. All programmatic integrations should use the REST API directly with token-based authentication.

**Pure1 REST API:**

| Endpoint | Purpose |
|---|---|
| `POST /oauth2/1.0/token` | Obtain OAuth2 access token |
| `GET /api/1.latest/arrays` | Fleet health and array inventory |
| `GET /api/1.latest/metrics` | Performance metrics data |
| `GET /api/1.latest/alerts` | Active alerts |
| `GET /api/1.latest/metrics/history` | Historical metric data |

**Pure1 CLI (if installed):**

```
pure1 get arrays          # List all arrays and health status
pure1 get alerts          # List active alerts
pure1 get metrics         # Query performance metrics
```
