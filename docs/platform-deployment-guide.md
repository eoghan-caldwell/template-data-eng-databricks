# Databricks Landing Zone – Full Deployment & Operations Guide

## 1. Introduction
This Landing Zone is deployed using:
- **Terraform** — infrastructure provisioning  
- **Bootstrap Scripts** — workspace initialization  
- **Unity Catalog** — platform-wide governance  
- **Cluster Policies** — secure compute governance  
- **Configuration Files** — declarative platform setup  
- **Ingestion Pipelines** — reference medallion patterns

This guide walks through every phase required to deploy and operate the platform.

## 2. Prerequisites
Before starting:
### Required Access
- Contributor access to required Azure Resource Groups
- Ability to create service principals
- Access to Data Lake Storage Accounts
- Access to Databricks Workspace URL (once provisioned)
- Permission to run Terraform pipelines

### Required Tools
- Terraform CLI
- Python 3.9+
- `databricks-sdk` Python package
- Git CLI
- Access to your GitHub or Azure DevOps repo

### Required Knowledge
- Terraform basics
- Databricks compute concepts
- Unity Catalog hierarchy
- YAML + Python familiarity

## 3. Environment Setup
Set required environment variables:
```sh
export ARM_CLIENT_ID="<terraform-spn>"
export ARM_CLIENT_SECRET="<spn-secret>"
export ARM_TENANT_ID="<tenant-id>"
export ARM_SUBSCRIPTION_ID="<subscription-id>"
```

## 4. Terraform Deployment (Infrastructure Layer)
```sh
terraform init
terraform validate
terraform plan -out=tfplan
terraform apply "tfplan"
```
Terraform will create the workspace, networking, storage, identities, RBAC and secrets.

## 5. Bootstrap Scripts (Workspace Initialization)
Install dependencies:
```sh
pip install databricks-sdk pyyaml
```
Authenticate:
```sh
databricks configure --token
```

## 6. Bootstrap Step 1 — Users and Groups
```sh
python users_and_groups.py
```
Creates platform groups, users, and workspace permissions.

## 7. Bootstrap Step 2 — Unity Catalog Setup
```sh
python unity-catalog-setup.py
```
Creates metastore, schemas, catalogs, external locations, and permissions.

## 8. Bootstrap Step 3 — Clusters, Pools & Policies
```sh
python create-clusters.py
```
Creates instance pools, cluster policies, and baseline clusters.

## 9. Ingestion & Medallion Pipeline Execution
Use notebooks in `examples/ingestion-pipeline/` to run Bronze then Silver processing.

## 10. CI/CD + Operational Best Practices
Includes repo structure, Git workflow, monitoring, cost controls, security operations.

## 11. Validation Checklist
Validate workspace, metastore, UC catalogs, clusters, ingestion flow.

## 12. Summary
You now have a full Databricks Landing Zone deployed and operational.
