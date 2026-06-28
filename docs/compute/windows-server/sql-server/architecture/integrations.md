---
tags:
  - architecture
  - windows
---
# SQL Server — Integrations

<div class="kb-summary">
SQL Server integration points — application drivers (JDBC, ODBC, ADO.NET, pyodbc), linked servers, SSRS/SSIS/SSAS, monitoring via DMVs and third-party tools.

*Applies to: SQL Server 2019 / 2022*
</div>
![SQL Server — Integrations](../../../../assets/compute-windows-server-sql-server-architecture-integrations.svg)




```d2
direction: right

center: "SQL Server" {shape: hexagon}
application_drivers: "Application Drivers" {shape: rectangle}
linked_servers: "Linked Servers" {shape: rectangle}
ssis_ssrs_ssas: "SSIS / SSRS / SSAS" {shape: rectangle}
monitoring_integration: "Monitoring Integration" {shape: rectangle}

center -> application_drivers
center -> linked_servers
center -> ssis_ssrs_ssas
center -> monitoring_integration
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

---

## See also

- [Sql Server — How It Works](how-it-works/)
- [Sql Server — Design Standards](design-standards/)
