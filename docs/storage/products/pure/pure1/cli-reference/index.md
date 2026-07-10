---
tags:
  - pure
---
# Pure1 — CLI and API Reference

```bash
# Generate RSA key pair for Pure1 API auth
openssl genrsa -out pure1-private.pem 2048
openssl rsa -in pure1-private.pem -pubout -out pure1-public.pem

# Create a JWT assertion (Python example)
python3 -c "
import jwt, time
payload = {'iss': '<application_id>', 'iat': int(time.time()), 'exp': int(time.time()) + 86400}
token = jwt.encode(payload, open('pure1-private.pem').read(), algorithm='RS256')
print(token)
"

# Exchange JWT for access token
curl -X POST https://api.pure1.purestorage.com/oauth2/1.0/token   -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange&subject_token=<jwt>&subject_token_type=urn:ietf:params:oauth:token-type:jwt"
```


```text title="Expected output"
Generating RSA private key, 2048 bit long modulus (2 primes)
.......................................................................+++
...................+++
e is 65537 (0x010001)
writing RSA key
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcHBfMTIzNDU2Nzg5MCIsImlhdCI6MTcwMjQwMTIzNCwiZXhwIjoxNzAyNDg3NjM0fQ.KxL9vF2mN8pQrStUwXyZ1aB3cD4eF5gH6iJ7kL0mN1oPqRsT2uV3wX4yZ5aB6cD7eF8gH9iJ0kL1mN2oPqRsT3uV4wX5yZ6aB7cD8eF9gH0iJ1kL2mN3oPqRsT4uV5wX6yZ7aB8cD9eF0gH1iJ2kL3mN4oPqRsT5uV6wX7yZ8aB9cD0eF1gH2iJ3kL4mN5oPqRsT6uV7wX8yZ9aB0cD1eF2gH3iJ4kL5mN6oPqRsT7uV8wX9yZ0aB1cD2eF3gH4iJ5kL6mN7oPqRsT8uV9wX0yZ1aB2cD3eF4gH5iJ6kL7mN8oPqRsT9uV0wX1yZ2aB3cD4eF5gH6iJ7kL8mN9oPqRsT0uV1wX2yZ3aB4cD5eF6gH7iJ8kL9mN0oPqRsT1uV2wX3yZ4aB5cD6eF7gH8iJ9kL0mN1oPqRsT2uV3wX4yZ5aB6cD7eF8gH9iJ0kL1mN2oPqRsT3uV4wX5yZ6aB7cD8eF9gH0iJ1kL2mN3oPqRsT4uV5wX6yZ7aB8cD9eF0gH1iJ2kL3mN4oPqRsT5uV6wX7yZ8aB9cD0eF1gH2iJ3kL4mN5oPqRsT6uV7wX8yZ9aB0cD1eF2gH3iJ4kL5mN6oPqRsT7uV8wX9yZ0aB1cD2eF3gH4iJ5kL6mN7oPqRsT8uV9wX0
```
```bash
# Get capacity metrics for all arrays
curl -X GET "https://api.pure1.purestorage.com/api/1.latest/arrays?fields=name,capacity,space"   -H "Authorization: Bearer <token>"

# Get capacity for a specific array
curl -X GET "https://api.pure1.purestorage.com/api/1.latest/arrays?filter=name%3D%27<array_name>%27&fields=name,capacity,space"   -H "Authorization: Bearer <token>"
```
```python
from py_pure_client import PureOneClient

client = PureOneClient(private_key_file="pure1-private.pem",
                       private_key_password=None,
                       app_id="<application_id>")

# List all arrays
arrays = client.get_arrays()
for a in arrays.items:
    print(a.name, a.model)

# Get active alerts
alerts = client.get_alerts(filter="state='open'")
for alert in alerts.items:
    print(alert.summary, alert.severity)
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## See also

- [Pure1 — Overview](../../)
