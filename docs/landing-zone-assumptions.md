# Databricks Landing Zone – Assumptions

This document outlines all assumptions that must hold true before deploying the Databricks landing zone using Terraform and bootstrap automation. These assumptions ensure consistency, governance, and a smooth deployment lifecycle across environments.

---

## 1. Cloud & Subscription Prerequisites

- An Azure subscription is available for provisioning Databricks and associated resources.
- Resource group strategy is defined (platform RG, data RGs, networking RG, etc.).
- Subscription governance (management groups, policies, budgets) is already in place.
- Region selection is approved and meets data residency requirements.

---

## 2. Identity & Access Requirements

- Entra ID (Azure Active Directory) is the identity provider for Databricks.
- SCIM provisioning model is defined (AAD → Databricks groups).
- A Managed Identity for Databricks is already created and assigned appropriate permissions.
- Terraform service principal(s) have:
  - Contributor on required resource groups
  - User Access Administrator (for role assignments)
  - Ability to create Key Vault secrets if needed

---

## 3. Networking Requirements

- Virtual network and subnets are either pre‑created or deployable by Terraform.
- IP address ranges and subnet sizing are approved by network architecture.
- Networking decisions have been finalized:
  - Standard vs Private Link workspace deployment
  - Egress restrictions
  - Firewall and NSG rules
  - Connectivity to storage accounts
- DNS integration patterns are established if using Private Link.

---

## 4. Storage Assumptions

- Storage account(s) for the data lake already exist or will be created through Terraform.
- Container structure is agreed:
  - `raw`, `bronze`, `silver`, `gold`, `sandbox`, `audit`
- Access model for the storage account is defined:
  - Managed Identity permissions
  - Private Endpoints (if used)
  - Network access controls

---

## 5. Governance & Security Assumptions

- Unity Catalog will be the primary governance model — **hive_metastore is deprecated** for new development.
- Data classiﬁcation and retention policies are documented.
- Lineage requirements are understood and accepted.
- Permissions will be assigned through groups, not ad‑hoc user grants.
- Key Vault (or Databricks Secrets) is the approved secret management strategy.
- Encryption requirements (default vs customer‑managed key) are agreed.

---

## 6. Operational Assumptions

- Monitoring requirements are agreed (Azure Monitor, Log Analytics, Databricks system tables).
- Alerting strategy is defined for compute, jobs, pipeline failures, storage, and networking.
- Logging requirements (audit logs, cluster logs, job logs) are known.
- Backup & DR expectations are defined at the storage layer.
- RACI for platform support teams is documented.

---

## 7. Development & CI/CD Assumptions

- Git integration strategy is confirmed (Repos, GitHub, Azure DevOps).
- Branching model is defined (trunk-based, GitFlow, etc.).
- CI/CD tooling is agreed for running Terraform and deploying jobs/pipelines.
- Standard environments exist (dev → test → prod) with clear promotion paths.

---

## 8. Platform Capability Assumptions

- All workloads will follow the Medallion Architecture (raw → bronze → silver → gold).
- Ingestion pipelines will use:
  - Auto Loader
  - Delta Live Tables or Jobs workflows
- Clusters will be governed using cluster policies.
- UC permissions will be enforced centrally and not overridden manually.

---

If any assumption in this document is not true, the platform deployment may fail or result in an unsupported configuration. Please validate all assumptions before initiating Terraform or bootstrap workflows.
``