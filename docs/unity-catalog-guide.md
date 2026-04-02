# Unity Catalog Guide

Unity Catalog (UC) is the central governance framework for data, AI assets, permissions, and lineage within the Databricks platform. This document explains how UC is structured, how data teams should use it, and how governance is applied across environments.

---

## 1. What Is Unity Catalog?

Unity Catalog provides:

- Centralized governance across all workspaces
- Fine‑grained permissions (catalog → schema → table → column)
- Consistent access patterns for data, models, functions, and ML assets
- Built‑in lineage for tables and jobs
- Secure access to ADLS using managed identities

This landing zone uses UC exclusively for all datasets. Use of the legacy `hive_metastore` is prohibited.

---

## 2. Unity Catalog Hierarchy

UC defines a three‑level namespace:
<catalog>.<schema>.</schema></catalog>

### 2.1 Metastore
Top‑level container holding all catalogs.  
One metastore is deployed per environment.

### 2.2 Catalogs
Catalogs logically group data domains or quality layers.  
This platform uses:

- `raw`
- `bronze`
- `silver`
- `gold`
- `sandbox`

### 2.3 Schemas
Schemas exist inside catalogs and represent domains or workload areas.

Example:
raw.landing
bronze.events
silver.curated
gold.bi

### 2.4 Tables & Views
Assets stored as Delta Tables with optional views for consumption layers.

---

## 3. Naming Conventions

### Catalog Names
Use lowercase, functional names:
raw, bronze, silver, gold, sandbox

### Schema Names
Schemas typically follow domain or logical function naming:
events, operational, curated, audit

### Table Names
Tables must use `snake_case`.

Examples:
- `sales_orders`
- `customer_events`
- `product_catalog`

---

## 4. Storage Model

Unity Catalog relies on:

- **Storage Credentials** (managed identity)
- **External Locations** (paths in ADLS)

Example structure:
abfss://raw@datalake.dfs.core.windows.net/
abfss://bronze@datalake.dfs.core.windows.net/

All storage access is mediated through UC — **no direct access from clusters**.

---

## 5. Permissions & Governance

UC enforces least‑privilege access via groups:

| Group             | Raw | Bronze | Silver | Gold | Sandbox |
|------------------|------|--------|--------|-------|----------|
| admins           | ALL | ALL | ALL | ALL | ALL |
| data-engineers   | RW  | RW | RW | R | RW |
| analysts         | R   | R  | R  | R | - |

Key rules:

- Permissions must be granted to groups only.
- No user‑level grants.
- No third‑party storage access via SAS keys.

---

## 6. Lineage

Unity Catalog automatically tracks:

- Table lineage  
- Job dependencies  
- Notebook lineage  
- Column-level lineage

This informs downstream impact analysis and data governance.

---

## 7. Catalog & Schema Creation Process

Non‑platform teams must request new catalogs or schemas.  
The platform team will:

1. Update UC config
2. Approve external locations if needed
3. Apply appropriate privileges

Unauthorized catalog creation is blocked.

---

## 8. Bootstrap Automation

The `unity-catalog-setup.py` script:

- Creates the metastore (if not existing)
- Assigns workspace to the metastore
- Creates storage credentials
- Creates external locations
- Creates catalogs & schemas
- Applies base permissions
- Ensures idempotency across runs

---

## 9. Expectations for Data Teams

- Always write data into the UC namespace (not DBFS).
- Use catalog‑qualified table names.
- Follow the medallion architecture.
- Request permissions via group membership.
- Document lineage through workflows.

---

Unity Catalog is the foundation of this platform’s governance model. All data work must follow the patterns described in this document.