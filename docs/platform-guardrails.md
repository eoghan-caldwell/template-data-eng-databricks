# Platform Guardrails

This document defines mandatory guardrails and governance controls applied to the Databricks platform. All workspaces, pipelines, users, and jobs must comply with these constraints.

---

## 1. Identity & Access Guardrails

- All identities originate from Entra ID (Azure AD).
- SCIM-based provisioning manages user/group lifecycle.
- No local Databricks users except service-managed identities.
- Permissions are assigned to **groups** only.
- Unity Catalog grantees must always be groups.

---

## 2. Compute Guardrails

### 2.1 Cluster Policies
Cluster policies are mandatory for all compute resources and enforce:

- Allowed node types  
- Max workers  
- Browser‑based termination (timeout settings)  
- Restrictions on secret usage  
- UC‑only access mode  
- Blocking of DBFS data access  
- Mandatory tagging

### 2.2 Cluster Types
Two cluster types are allowed:

- **All‑purpose clusters** for development  
- **Job clusters** for scheduled workloads  

### 2.3 Instance Pools
All compute must use designated instance pools unless explicitly exempted.

---

## 3. Storage Guardrails

- All data must be stored in Unity Catalog-managed or UC‑approved external locations.
- Direct access to ADLS paths via spark configs is not allowed.
- No use of DBFS for persistent storage.
- Data must follow the medallion architecture:
  - `raw` → `bronze` → `silver` → `gold`

---

## 4. Networking Guardrails

- Workspaces must follow network standards defined in the landing zone.
- Egress is restricted unless approved.
- When Private Link is enabled:
  - Public workspace URLs disabled
  - Private DNS rules must be applied
- Storage accounts must block public access.

---

## 5. Development Guardrails

- All production code must be committed to Git.
- Workspace notebooks are allowed only for development, not deployment.
- CI/CD pipelines must deploy:
  - Jobs
  - Pipelines
  - Terraform changes
  - Configuration updates
- Direct table modifications in gold layer are prohibited.

---

## 6. Deployment Guardrails

- **Terraform is the source of truth** for infrastructure.
- **Bootstrap scripts** configure the workspace and UC.
- Any manual change to workspace settings must be automated in Terraform or bootstrap.
- Jobs must use Job Clusters unless justified.
- No unmanaged external tables.

---

## 7. Security Guardrails

- Secrets must be stored in Azure Key Vault or Databricks Secrets.
- Personal Access Tokens (PATs) must follow rotation policies.
- Production workspaces must have:
  - MFA enforced via Entra
  - Token usage auditing
  - Audit logs exported
- UC permissions must follow least privilege.

---

## 8. Monitoring & Logging Guardrails

- Workspace audit logs must be sent to Log Analytics.
- Cluster logs must be stored in a secure location.
- Job failures must generate:
  - Alerts
  - Tickets (if integrated)
- Monitoring dashboards must exist for:
  - Job throughput
  - Cluster utilization
  - Cost visibility

---

## 9. Data Quality & Lineage Guardrails

- All ingestion must use Auto Loader or a structured ingestion pattern.
- Data quality checks must be documented and applied.
- DLT (Delta Live Tables) is recommended for new projects.
- Lineage must be preserved via UC and DAG relationships.

---

These guardrails ensure that the platform remains secure, maintainable, cost‑effective, and compliant with modern data governance standards.