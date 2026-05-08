# Python Automation — Components

Key libraries, packages, virtual environments, and parsing tools used in the Python automation environment.

## Parsing

### JSON and YAML Parsing

Standard library `json` handles JSON; `PyYAML` or `ruamel.yaml` handles YAML.

```bash
pip install pyyaml
```

```python
import json
import yaml
from pathlib import Path

# Parse JSON from a file
data = json.loads(Path('config.json').read_text())

# Parse JSON from an API response
import requests
resp = requests.get('https://api.example.com/v1/data')
data = resp.json()

# Write JSON (pretty-printed)
Path('output.json').write_text(json.dumps(data, indent=2, default=str))

# Parse YAML
config = yaml.safe_load(Path('config.yml').read_text())

# Parse multi-document YAML
docs = list(yaml.safe_load_all(Path('manifests.yml').read_text()))

# Write YAML
Path('output.yml').write_text(yaml.dump(config, default_flow_style=False))
```

### XML Parsing

Use `xml.etree.ElementTree` from the standard library for simple XML, or `lxml` for XPath.

```python
import xml.etree.ElementTree as ET

tree = ET.parse('report.xml')
root = tree.getroot()

# Iterate over child elements
for server in root.findall('./servers/server'):
    name = server.find('name').text
    status = server.get('status')
    print(f"{name}: {status}")

# Namespace-aware parsing
NS = {'v': 'http://example.com/schema'}
for item in root.findall('v:item', NS):
    print(item.text)
```

### argparse for CLI Scripts

```python
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Process inventory and generate report'
    )
    parser.add_argument('input', help='Path to input file')
    parser.add_argument('-o', '--output', default='report.csv',
                        help='Output file path (default: report.csv)')
    parser.add_argument('-e', '--env',
                        choices=['dev', 'staging', 'prod'],
                        default='dev', help='Target environment')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without making changes')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print(f"Input: {args.input}, Env: {args.env}, Dry run: {args.dry_run}")
```

### Regex Parsing

```python
import re

log_line = '2026-05-07 14:32:01 ERROR [web01] Connection refused: 192.168.1.50:5432'

# Named groups for readable extraction
pattern = re.compile(
    r'(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) '
    r'(?P<level>\w+) \[(?P<host>\w+)\] (?P<message>.+)'
)
match = pattern.match(log_line)
if match:
    print(match.groupdict())

# Find all IP addresses in text
ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', log_line)

# Extract version numbers
versions = re.findall(r'\d+\.\d+\.\d+', 'nginx/1.24.0 openssl/3.0.2')
```

### Jinja2 Templates

```bash
pip install jinja2
```

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('config.conf.j2')

rendered = template.render(
    hostname='web01',
    ip_address='10.0.1.10',
    ports=[80, 443],
    ssl_enabled=True
)
print(rendered)
```

### Parsing Format Reference

| Format | Library | Load function | Dump function |
|---|---|---|---|
| JSON | `json` (stdlib) | `json.loads()` | `json.dumps()` |
| YAML | `pyyaml` | `yaml.safe_load()` | `yaml.dump()` |
| XML | `xml.etree.ElementTree` (stdlib) | `ET.parse()` | `tree.write()` |
| INI/TOML | `configparser` / `tomllib` (stdlib 3.11+) | `config.read()` | `config.write()` |
| CSV | `csv` (stdlib) | `csv.DictReader()` | `csv.DictWriter()` |
| Regex | `re` (stdlib) | `re.findall()`, `re.match()` | N/A |
