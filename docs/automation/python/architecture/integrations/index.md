---
tags:
  - architecture
  - python
description: "Python automation integrations: REST API call patterns, retry-with-backoff wrappers, requests session management, Ansible Python API, and Terraform..."
---
# Python Automation — Integrations

<div class="kb-summary">
Python automation integrations: REST API call patterns, retry-with-backoff wrappers, `requests` session management, Ansible Python API, and Terraform subprocess automation.

*Applies to: Python 3.x*
</div>

## API Call and Retry Flow

```d2
direction: right

buildReq: "Build Request\n(URL + headers + body" {shape: rectangle}
sendReq: "Send HTTP Request\n(requests.get/post" {shape: rectangle}
checkStatus: "Check Response\nStatus Code" {shape: rectangle}
parseBody: "Parse JSON\nBody" {shape: rectangle}
returnData: "Return Data\nto Caller" {shape: rectangle}
checkRetry: "Retry attempt\n< max_retries?" {shape: rectangle}
backoff: "Exponential Backoff\n(backoff_factor" {shape: rectangle}
raiseAlert: "Raise Exception\n/ Alert" {shape: rectangle}

buildReq -> sendReq
sendReq -> checkStatus
checkStatus -> parseBody
parseBody -> returnData
checkStatus -> checkRetry
checkRetry -> backoff
backoff -> sendReq
checkRetry -> raiseAlert
```

### Pagination

Most APIs paginate large result sets. Handle both cursor-based and offset-based pagination.

```python
def get_all_pages(url: str, headers: dict) -> list:
    """Collect all items from a paginated API using cursor-based pagination."""
    items = []
    params = {'limit': 100}

    while url:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        items.extend(data.get('items', []))
        # Follow next_cursor or next_url — adapt to the API's convention
        next_url = data.get('pagination', {}).get('next_url')
        url = next_url
        params = {}   # params already embedded in next_url

    return items

# Offset/limit pagination
def get_all_offset(base_url: str, headers: dict) -> list:
    items, offset, limit = [], 0, 100
    while True:
        resp = requests.get(base_url, headers=headers,
                            params={'limit': limit, 'offset': offset})
        resp.raise_for_status()
        page = resp.json()['items']
        items.extend(page)
        if len(page) < limit:
            break
        offset += limit
    return items
```

### Error Handling and Retry

```python
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def build_session(retries: int = 3, backoff: float = 1.0) -> requests.Session:
    """Session with automatic retry on transient errors."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=['GET', 'POST', 'PUT', 'DELETE'],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session

# Handle specific HTTP errors
try:
    resp = session.get('https://api.example.com/v1/servers', timeout=30)
    resp.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Resource not found")
    elif e.response.status_code == 429:
        retry_after = int(e.response.headers.get('Retry-After', 60))
        time.sleep(retry_after)
    else:
        raise
except requests.exceptions.ConnectionError:
    print("Connection failed — check network and API endpoint")
except requests.exceptions.Timeout:
    print("Request timed out")
```

### API Client Patterns

| Pattern | Use case | Implementation |
|---|---|---|
| Bearer token | REST APIs with OAuth / JWT | `Authorization: Bearer <token>` header |
| API key header | Simple API authentication | Custom header (e.g. `X-API-Key`) |
| Basic auth | Legacy or internal APIs | `requests.auth.HTTPBasicAuth` |
| Session object | Multiple requests to same host | `requests.Session()` |
| Retry adapter | Resilience against transient failures | `HTTPAdapter(max_retries=Retry(...))` |
| Timeout | Avoid hanging scripts | `timeout=(connect_timeout, read_timeout)` |

---

## See also

- [Python — Design Standards](../design-standards/)
