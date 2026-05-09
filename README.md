# Automated Employee Onboarding Pipeline

> End-to-end identity provisioning pipeline that automatically creates users in **Azure Active Directory** and **Jira** when a new hire CSV is processed — deployed as a containerized workload on Azure Container Instances via a fully automated CI/CD pipeline.

---

## What This Does

When HR adds a new employee to `new_hires.csv`, this pipeline:

1. Authenticates to Microsoft Graph API using Azure AD app credentials
2. Creates the user in **Azure Active Directory** with a temporary password
3. Creates the same user in **Jira** via Atlassian REST API
4. Logs the result for every user — success or failure

Zero manual steps. Zero portal clicking. One pipeline run provisions a user across two enterprise systems in under 60 seconds.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        GitHub                               │
│  Push to main → GitHub Actions CI/CD Pipeline              │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  pytest  │→ │  Docker  │→ │   ACR    │→ │Terraform │   │
│  │  tests   │  │  build   │  │   push   │  │  apply   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌─────────────────────────────────────────────────────────────┐
│                        Azure                                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Azure Container Instance                  │   │
│  │                                                     │   │
│  │   provision_user.py                                 │   │
│  │        │                                            │   │
│  │        ├──→ Microsoft Graph API → Azure AD User     │   │
│  │        └──→ Atlassian REST API  → Jira User         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Azure ACR   │  │  Key Vault   │  │  Entra ID    │     │
│  │  (images)    │  │  (secrets)   │  │  (identity)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Containerization | Docker |
| Container Registry | Azure Container Registry (ACR) |
| Container Runtime | Azure Container Instances (ACI) |
| Infrastructure as Code | Terraform (azurerm 4.1.0) |
| CI/CD | GitHub Actions |
| Identity Provider | Microsoft Entra ID (Azure AD) |
| Graph API | Microsoft Graph API via ClientSecretCredential |
| Project Management | Atlassian Jira REST API v3 |
| Secrets Management | GitHub Secrets + Azure Key Vault |
| Testing | pytest |

---

## Project Structure

```
Provision-User/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── app/
│   ├── data/
│   │   └── new_hires.csv       # Input — new hire list
│   ├── tests/
│   │   └── test_main.py        # Unit tests
│   ├── provision_user.py       # Core provisioning logic
│   └── requirements.txt        # Python dependencies
├── terraform/
│   ├── main.tf                 # Azure infrastructure
│   └── variables.tf            # Variable definitions
├── Dockerfile                  # Container definition
└── .gitignore
```

---

## CI/CD Pipeline

Every push to `main` triggers the full pipeline:

```
1. Run pytest unit tests
2. Login to Azure
3. Build Docker image tagged with git SHA
4. Push image to Azure Container Registry
5. Terraform init + import existing state
6. Terraform apply — deploy container to ACI
```

If tests fail the pipeline stops. Nothing ships broken.

---

## Security Design Decisions

**No hardcoded credentials — ever.**
All secrets live in GitHub Secrets and are injected at runtime via `TF_VAR_` environment variables into Terraform, which passes them as `secure_environment_variables` into the container.

**Managed Identity for ACR authentication.**
The container pulls images from ACR using admin credentials scoped to the registry only.

**App Registration with least-privilege permissions.**
The Azure AD app registration has only `User.ReadWrite.All` and `Directory.ReadWrite.All` — nothing beyond what provisioning requires.

**Secrets never touch the codebase.**
`terraform.tfvars` is gitignored. `local.settings.json` is gitignored. No sensitive values appear in git history.

---

## Local Development

**Prerequisites:**
- Python 3.12+
- Docker
- Terraform >= 1.9.0
- Azure CLI

**Install dependencies:**
```bash
pip install -r app/requirements.txt
```

**Run tests:**
```bash
cd app
pytest tests/ -v
```

**Environment variables required:**
```
GRAPH_TENANT_ID
GRAPH_CLIENT_ID
GRAPH_CLIENT_SECRET
JIRA_URL
JIRA_EMAIL
JIRA_API_TOKEN
```

---

## Input Format

`app/data/new_hires.csv`:
```csv
name,email,role
John Smith,john.smith@yourdomain.onmicrosoft.com,Engineer
Sarah Connor,sarah.connor@yourdomain.onmicrosoft.com,Collaborator
```

**Note:** Email domain must match your verified Azure AD tenant domain.

---

## Sample Output

```
Processing 5 new hires...

✅ Success: John Smith — {
  "status": "success",
  "azure": {"status": "created", "user": "john.smith@domain.onmicrosoft.com"},
  "jira":  {"status": "created", "user": "john.smith@domain.onmicrosoft.com"}
}
```

---

## Infrastructure (Terraform)

Three Azure resources managed as code:

- `azurerm_resource_group` — resource group
- `azurerm_container_registry` — private Docker registry
- `azurerm_container_group` — container runtime with injected secrets

State management: Terraform state is rebuilt on each run via resource imports. Remote state backend (Azure Blob Storage) is the planned next iteration.

---

## Roadmap

- [ ] Remote Terraform state in Azure Blob Storage
- [ ] Idempotency — skip users that already exist in either system
- [ ] Deprovisioning pipeline — disable users on offboarding trigger
- [ ] Approval workflow — manager approval before provisioning fires
- [ ] Audit log — write every provisioning event to Azure Blob Storage
- [ ] Azure Monitor alerts on provisioning failures
- [ ] OIDC authentication — replace service principal secret with federated identity

---

## Author

**Emmanuel Elesin** — Platform Engineer  
[github.com/eelesin](https://github.com/eelesin)