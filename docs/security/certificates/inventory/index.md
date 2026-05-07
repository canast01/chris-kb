# Certificate Inventory

Maintaining an accurate certificate inventory prevents surprise expirations. Inventory should cover all certificates: public-facing TLS, internal services, code signing, client authentication.

## Discovery Methods

| Method | Coverage | Effort |
|---|---|---|
| Port scanning with nmap | External/internal TLS endpoints | Low — automated |
| openssl per host | Targeted host checks | Low — scriptable |
| Venafi / DigiCert One | Managed certificates | Low (integrated) |
| AD Certificate Services | Internally issued certs | Low (ADCS reports) |
| Manual tracking spreadsheet | Small environments | Medium — human |
| Shodan / Censys | External internet-facing | Low (API) |

## Port Scanning for Certificates

```bash
# Scan a subnet for TLS on common ports
nmap -p 443,8443,636,993,995 --script ssl-cert 192.168.1.0/24 \
    -oX ssl-scan.xml

# Extract CN and expiry from nmap XML output
grep -A5 "ssl-cert" ssl-scan.xml | grep -E "commonName|notAfter"

# Quick single-host TLS cert dump
nmap -p 443 --script ssl-cert example.com \
    | grep -E "Subject:|Not valid after"
```

## openssl-Based Discovery

```bash
# Grab cert details from a live endpoint
echo | openssl s_client -connect example.com:443 2>/dev/null \
    | openssl x509 -noout -subject -issuer -dates -fingerprint

# Check SAN entries (Subject Alternative Names)
echo | openssl s_client -connect example.com:443 2>/dev/null \
    | openssl x509 -noout -text | grep -A2 "Subject Alternative Name"

# Extract cert to file for further analysis
echo | openssl s_client -connect example.com:443 2>/dev/null \
    | openssl x509 > example-com.pem
```

## Windows Certificate Store Inventory

```powershell
# List all certs in the local machine Personal store
Get-ChildItem Cert:\LocalMachine\My |
    Select-Object Subject, Issuer, Thumbprint, NotBefore, NotAfter |
    Export-Csv C:\CertInventory.csv -NoTypeInformation

# List certs across all stores
foreach ($store in @("My","CA","Root","TrustedPeople")) {
    Get-ChildItem "Cert:\LocalMachine\$store" |
        Select-Object @{N="Store";E={$store}}, Subject, NotAfter, Thumbprint
}

# Find certs issued by a specific CA
Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.Issuer -like "*Internal CA*"} |
    Select-Object Subject, NotAfter, Thumbprint
```

## Tracking Spreadsheet Columns

Minimum fields for a useful inventory:

| Field | Notes |
|---|---|
| FQDN / Subject CN | Primary identifier |
| SANs | All covered hostnames |
| Issuer / CA | Root or intermediate that issued it |
| Expiry Date | ISO 8601 format |
| Owner / Team | Who is responsible for renewal |
| Renewal Method | Manual / Venafi / ACME / ADCS |
| Last Renewed | Track renewal history |
| Notes | Any special install steps |

## Venafi Inventory Queries (REST API)

```bash
# Authenticate and get API token
curl -s -X POST https://tpp.corp.example.com/vedauth/authorize \
    -H "Content-Type: application/json" \
    -d '{"Username":"svc-venafi","Password":"P@ssw0rd!"}' \
    | jq '.APIKey'

# List certificates expiring in 90 days
curl -s https://tpp.corp.example.com/vedsdk/certificates \
    -H "X-Venafi-API-Key: $TOKEN" \
    -G --data-urlencode "ValidToLess=2026-08-01" \
    | jq '.Certificates[] | {CN: .Name, Expiry: .ValidTo}'
```
