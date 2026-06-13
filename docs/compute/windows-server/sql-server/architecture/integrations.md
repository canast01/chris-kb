---
tags:
  - architecture
  - windows
---
# SQL Server — Integrations

<div class="kb-summary">
SQL Server integration points — application drivers (JDBC, ODBC, ADO.NET, pyodbc), linked servers, SSRS/SSIS/SSAS, monitoring via DMVs and third-party tools.
</div>

```text
┌────────────────────────────────────── SQL Server — Integrations ──────────────────────────────────────┐
│                                                                                                       │
│   SQL Server connects to applications via ODBC, JDBC, ADO.NET, pyodbc, and native drivers             │
│   Linked servers enable T-SQL queries across SQL Server instances and heterogeneous sources           │
│   Monitoring uses DMVs natively; third-party tools scrape DMV metrics via sql_exporter                │
│                                                                                                       │
│   Application drivers                                                                                 │
│   .NET: Microsoft.Data.SqlClient; Server=host;Database=db;User Id=u;Password=p;                       │
│   Java: mssql-jdbc; jdbc:sqlserver://host:1433;databaseName=db                                        │
│   Python: pyodbc + ODBC Driver 18; mssql+pyodbc://user:pass@host/db?driver=...                        │
│   Node.js: mssql / tedious npm package; connection pool recommended                                   │
│                                                                                                       │
│   Linked servers                                                                                      │
│   sp_addlinkedserver: registers remote SQL Server or heterogeneous OLE DB source                      │
│   sp_addlinkedsrvlogin: maps local login to remote login credentials                                  │
│   Query: SELECT * FROM [REMOTE_SERVER].[database].[schema].[table]                                    │
│                                                                                                       │
│   Analytics components (SSIS / SSRS / SSAS)                                                           │
│   SSIS: ETL and data integration; packages deployed to SSISDB; scheduled via SQL Agent                │
│   SSRS: reporting server; connects to SQL data sources; REST API for embedding                        │
│   SSAS: analytical / OLAP; tabular or multidimensional model; Power BI compatible                     │
│                                                                                                       │
│   Key terms:                                                                                          │
│   ODBC         = Open Database Connectivity; standard API for relational database access              │
│   DMV          = Dynamic Management View; sys.dm_* views exposing SQL Server runtime state            │
│   SSISDB       = SQL Server Integration Services catalog database; package deployment target          │
│   sql_exporter = Prometheus exporter for SQL Server; collects DMV metrics for Grafana                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Application Drivers

| Language | Driver | Connection string |
|---|---|---|
| .NET | `Microsoft.Data.SqlClient` | `Server=host;Database=db;User Id=u;Password=p;` |
| Java | `mssql-jdbc` | `jdbc:sqlserver://host:1433;databaseName=db` |
| Python | `pyodbc` + ODBC Driver 18 | `mssql+pyodbc://user:pass@host/db?driver=ODBC+Driver+18+for+SQL+Server` |
| Node.js | `mssql` / `tedious` | Use `mssql` npm package with pool configuration |
| Go | `go-mssqldb` | `sqlserver://user:pass@host?database=db` |

## Linked Servers

Linked servers allow T-SQL queries across instances:

```sql
-- Create a linked server
EXEC sp_addlinkedserver @server = 'REMOTE_SERVER', @srvproduct = 'SQL Server';
EXEC sp_addlinkedsrvlogin @rmtsrvname = 'REMOTE_SERVER', @useself = 'false',
     @rmtuser = 'remote_user', @rmtpassword = 'pass';

-- Query via linked server
SELECT * FROM [REMOTE_SERVER].[database].[schema].[table];
```

## SSIS / SSRS / SSAS

| Component | Role | Integration |
|---|---|---|
| SSIS | ETL / data integration | Packages deployed to SSISDB; scheduled via SQL Agent |
| SSRS | Reporting server | Connects to SQL Server data sources; REST API for embedding |
| SSAS | Analytical / OLAP | Tabular or multidimensional model; Power BI can connect directly |

## Monitoring Integration

| Tool | Method |
|---|---|
| SQL Server Management Studio | DMV queries; Activity Monitor; Query Store |
| Prometheus | `sql_exporter` or `mssql_exporter` — exposes DMV metrics |
| Datadog | SQL Server integration; collects DMV and WMI metrics |
| SolarWinds DPA | Deep query analysis; execution plan history |
| Redgate SQL Monitor | Instance/AG health; performance baselines |

Key DMVs for monitoring: `sys.dm_os_wait_stats`, `sys.dm_exec_query_stats`, `sys.dm_os_performance_counters`
