# Key Vault

> Part of the Azure CLI Reference.

```
┌──────────────────────────────────────────────────────────┐
│                   Key Vault CLI Flow                     │
│                                                          │
│  az keyvault create / list / show                        │
│         │                                                │
│         ▼                                                │
│  ┌──────────────────────────────────────────────────┐    │
│  │              Key Vault                           │    │
│  │                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │     │
│  │  │ Secrets  │  │  Keys    │  │ Certificates │   │     │
│  │  │ set/get  │  │ create   │  │ import/show  │   │     │
│  │  │  /delete │  │ /rotate  │  │ /list-vers.  │   │     │
│  │  └────┬─────┘  └────┬─────┘  └──────┬───────┘   │     │
│  └───────┼─────────────┼───────────────┼───────────┘     │
│          │             │               │                 │
│          └─────────────┴───────────────┘                 │
│                        │                                 │
│                        ▼                                 │
│              App retrieves at runtime                    │
│              (SDK / managed identity)                    │
└──────────────────────────────────────────────────────────┘
```

---

```bash
# Vaults
az keyvault list --output table
az keyvault show --name <vault>

# Secrets
az keyvault secret list --vault-name <vault>
az keyvault secret show --vault-name <vault> --name <secret>
az keyvault secret set --vault-name <vault> --name <secret> --value <value>
az keyvault secret delete --vault-name <vault> --name <secret>

# Keys
az keyvault key list --vault-name <vault>
az keyvault key show --vault-name <vault> --name <key>

# Certificates
az keyvault certificate list --vault-name <vault>
az keyvault certificate show --vault-name <vault> --name <cert>
```
