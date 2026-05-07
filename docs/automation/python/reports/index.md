# Python Reports

## pandas DataFrames

pandas is the standard library for tabular data manipulation in Python.

```bash
pip install pandas openpyxl
```

```python
import pandas as pd

# Create a DataFrame from a list of dicts
data = [
    {'host': 'web01', 'cpu': 45.2, 'memory': 72.1, 'disk': 38.0},
    {'host': 'web02', 'cpu': 12.8, 'memory': 55.3, 'disk': 61.4},
    {'host': 'db01',  'cpu': 88.6, 'memory': 91.0, 'disk': 74.2},
]
df = pd.DataFrame(data)

# Filter rows where CPU > 50%
high_cpu = df[df['cpu'] > 50]

# Add a calculated column
df['status'] = df['cpu'].apply(lambda x: 'critical' if x > 80 else 'ok')

# Summary statistics
print(df.describe())
print(df.groupby('status').size())
```

## CSV and Excel Output

```python
# Export to CSV
df.to_csv('reports/host_metrics.csv', index=False, encoding='utf-8')

# Read back
df = pd.read_csv('reports/host_metrics.csv')

# Export to Excel with multiple sheets
with pd.ExcelWriter('reports/server_report.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='All Hosts', index=False)
    high_cpu.to_excel(writer, sheet_name='High CPU', index=False)

# Read from Excel
df = pd.read_excel('reports/server_report.xlsx', sheet_name='All Hosts')
```

## Jinja2 HTML Reports

Jinja2 templates separate report logic from HTML structure.

```bash
pip install jinja2
```

```python
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime

template_str = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    tr.critical { background-color: #fdd; }
    tr.ok { background-color: #dfd; }
  </style>
</head>
<body>
  <h1>Server Health Report</h1>
  <p>Generated: {{ generated_at }}</p>
  <table>
    <tr><th>Host</th><th>CPU %</th><th>Memory %</th><th>Status</th></tr>
    {% for row in rows %}
    <tr class="{{ row.status }}">
      <td>{{ row.host }}</td>
      <td>{{ row.cpu }}</td>
      <td>{{ row.memory }}</td>
      <td>{{ row.status }}</td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>"""

env = Environment()
template = env.from_string(template_str)
html = template.render(
    generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    rows=data
)
Path('reports/health.html').write_text(html, encoding='utf-8')
```

## Sending Reports by Email

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def send_report(
    smtp_host: str,
    to_addresses: list[str],
    subject: str,
    html_body: str,
    attachments: list[str] = None
) -> None:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'automation@example.com'
    msg['To'] = ', '.join(to_addresses)
    msg.attach(MIMEText(html_body, 'html'))

    for path in (attachments or []):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(Path(path).read_bytes())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{Path(path).name}"')
        msg.attach(part)

    with smtplib.SMTP(smtp_host, 587) as smtp:
        smtp.starttls()
        smtp.sendmail(msg['From'], to_addresses, msg.as_string())
```

## Reporting Format Comparison

| Format | Library | Best for |
|---|---|---|
| CSV | `pandas` / `csv` | Data exchange, Excel import |
| Excel (.xlsx) | `pandas` + `openpyxl` | Rich tables, multi-sheet, formulas |
| HTML | `jinja2` | Emailed reports, browser viewing |
| JSON | `json` / `pandas` | API output, programmatic consumption |
| PDF | `weasyprint` / `reportlab` | Formal printed documents |
| Markdown | plain string | Wiki, GitHub, MkDocs |
