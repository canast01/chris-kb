# Aria Operations CLI Reference

Aria Operations is primarily managed via its REST API and web UI. The REST API base path is `/suite-api/api/` and requires a session token obtained by POSTing credentials to `/suite-api/api/auth/token/acquire`. SSH access to nodes is available for platform diagnostics using the `admin` or `root` accounts.

**REST API — Key Endpoints**

| Endpoint | Method | Purpose |
|---|---|---|
| `/suite-api/api/auth/token/acquire` | POST | Obtain authentication token |
| `/suite-api/api/resources` | GET | List all monitored objects |
| `/suite-api/api/alertdefinitions` | GET | List all alert definitions |
| `/suite-api/api/alerts` | GET | List active and historical alerts |
| `/suite-api/api/adapterkinds` | GET | List registered adapter kinds |

**SSH Node Commands**

```bash
# Check watchdog service status
watchdog status

# Check database controller status
db-controller status

# List all configured adapters
vcops-admin list

# Check cluster node status
vcops-admin cluster status
```
