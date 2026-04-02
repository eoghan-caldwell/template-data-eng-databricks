# Databricks Data Engineering Template

A practical, production‑minded template for building Databricks‑native data platforms. It includes ready‑made patterns for **Unity Catalog governance**, **secure ADLS ingestion**, **Auto Loader pipelines**, **cluster policy enforcement**, and **medallion‑layer ETL**.

Use this as a **GitHub Template Repository** to provide a fast, consistent starting point for Databricks projects or full landing‑zone deployments.

---

# What’s included

### ✅ End‑to‑end flow  
Extract → Auto Loader → Raw → Bronze → Silver → Gold  
Featuring:
- Auto Loader streaming/batch ingestion  
- Unity Catalog governance  
- Delta Lake medallion architecture  
- Structured ETL patterns with notebooks and Python  
- Workspace bootstrap automation  

### ✅ Databricks platform modules
- Unity Catalog metastore creation  
- Storage credentials & external locations  
- Catalogs, schemas, and permission assignment  
- Cluster policies & instance pools  
- Secure all‑purpose + job clusters  

### ✅ Extras
- Example medallion ingestion pipeline  
- Workspace bootstrap scripts (config‑driven)  
- Environment‑specific YAML configuration  
- Documentation (guardrails, assumptions, quickstart, full deployment guide)

### ✅ Dev experience
- Config files  
- Python requirements  
- Optional GitHub Actions for CI  
- Makefile templates (optional)  
- Clear project structure for Terraform + Bootstrap + ETL  

---

# Reference Architecture

```
┌───────────────────────────────────────────┐
│              Source Systems               │
│      Files / APIs / Events / Databases    │
└───────────────────────────────────────────┘
                    │
                    ▼
      ┌──────────────────────────────────┐
      │     Auto Loader Ingestion        │
      │   (Schema inference + streaming) │
      └──────────────────────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │        RAW (ADLS)          │
        │ External location via UC    │
        └────────────────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │      BRONZE Tables         │
        │ Ingested data + metadata   │
        └────────────────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │       SILVER Tables        │
        │ Cleaned & conformed data   │
        └────────────────────────────┘
                    │
                    ▼
        ┌────────────────────────────┐
        │        GOLD Tables         │
        │ BI models / aggregates     │
        └────────────────────────────┘
                    │
                    ▼
      ┌──────────────────────────────────┐
      │      Dashboards / ML / BI        │
      │ PowerBI, Databricks SQL, MLflow  │
      └──────────────────────────────────┘
```

---

# Project Layout (key folders)

```
terraform/                     # Infrastructure IaC
    workspace/
    clusters/
    unity-catalog/
    secrets/
    jobs/
    networking/
    observability/

bootstrap/                     # Workspace bootstrap automation
    users_and_groups.py
    unity-catalog-setup.py
    create-clusters.py

config/                        # Environment configuration
    users_and_groups.yml
    unity_catalog.yml
    clusters.yml

examples/                      # Example ETL pipelines
    ingestion-pipeline/
        01-ingest.ipynb
        02-transform.ipynb

docs/                          # Documentation
    landing-zone-assumptions.md
    unity-catalog-guide.md
    platform-guardrails.md
    quickstart-guide.md
    platform-deployment-guide.md

.github/workflows/             # Optional CI/CD pipeline templates
    ci.yml                     # Linting, terraform validate, tests

Makefile                       # Optional developer shortcuts
requirements.txt               # Python dependencies
env.example                    # Example environment variables
README.md                      # This file
```

---

# Quick Start

### 1. Clone the template repo  
```sh
git clone <repo-url>
cd databricks-template
```

### 2. Deploy infrastructure (Terraform)
```sh
cd terraform/
terraform init
terraform apply
```

### 3. Bootstrap the workspace  
Install dependencies:
```sh
pip install -r requirements.txt
```

Authenticate:
```sh
export DATABRICKS_HOST="https://<workspace>"
export DATABRICKS_TOKEN="<token>"
```

Run bootstrap:
```sh
python bootstrap/users_and_groups.py
python bootstrap/unity-catalog-setup.py
python bootstrap/create-clusters.py
```

### 4. Run example ingestion pipelines  
In Databricks workspace UI:
- Open `01-ingest.ipynb` → run Bronze ingestion  
- Open `02-transform.ipynb` → run Silver transformations  

---

# IAM, Security & Governance

- Identity managed through Entra ID + SCIM  
- Permissions are **group‑based only**  
- All data governed via **Unity Catalog**  
- External locations use **managed identity authentication**  
- Cluster policies enforce:  
  - Node type restrictions  
  - UC-only access  
  - Auto-termination  
  - No DBFS data access  

---

# Best Practices

✅ Use Unity Catalog for all data (no DBFS tables)  
✅ Use cluster policies — do not allow freestyle clusters  
✅ Store secrets in Key Vault / Databricks Secrets  
✅ Use Auto Loader for ingestion  
✅ Maintain medallion architecture consistency  
✅ Deploy via CI/CD (Terraform + Jobs)  
✅ Use YAML config files for bootstrap  
✅ Keep notebooks versioned in Git  

---

# Ready to Extend

This template can be extended to include:
- Delta Live Tables pipelines  
- MLflow model training & registry patterns  
- Multi-workspace deployments  
- Streaming ingestion (Kafka/Event Hub → Auto Loader)  
- CI/CD workflows for Databricks Jobs & Repos  
- Enterprise guardrails (SOC2, logging, monitoring)  

PRs and enhancements welcome.
