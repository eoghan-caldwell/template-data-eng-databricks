"""
Bootstrap Script: Unity Catalog Setup
Purpose: Build metastore, catalogs, schemas, permissions, and external locations.
"""

import yaml
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import AlreadyExists
import logging

# Set up logging for visibility into each setup step
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap-uc")

# Path to YAML configuration that defines all UC objects
CONFIG_PATH = "config/unity_catalog.yml"

# Load Unity Catalog configuration file
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Databricks API client (auth handled externally)
w = WorkspaceClient()

# -------------------------------------------------
# Metastore Setup
# -------------------------------------------------
def ensure_metastore(ms_config):
    """
    Ensures that the Unity Catalog metastore exists.
    If it already exists, returns the existing one.
    """
    try:
        logger.info("Creating metastore...")
        return w.metastores.create(
            name=ms_config["name"],
            storage_root=ms_config["storage_root"]
        )
    except AlreadyExists:
        logger.info("Metastore already exists.")
        # Get the first (and typically only) existing metastore
        return w.metastores.list()[0]

def assign_workspace_to_metastore(metastore):
    """
    Assigns the current Databricks workspace to the metastore.
    Sets the assignment as the default for Unity Catalog usage.
    """
    wid = w.current_workspace.get().workspace_id
    logger.info("Assigning workspace to metastore...")
    w.metastores.assign(metastore.id, workspace_id=wid, default=True)

# -------------------------------------------------
# Storage Credentials
# -------------------------------------------------
def ensure_storage_credential(sc):
    """
    Creates a Storage Credential (e.g., Azure Managed Identity).
    Used to authenticate external data access.
    """
    try:
        logger.info(f"Creating Storage Credential: {sc['name']}")
        w.storage_credentials.create(
            name=sc["name"],
            azure_managed_identity=sc["managed_identity"]
        )
    except AlreadyExists:
        logger.info(f"Storage credential already exists: {sc['name']}")

# -------------------------------------------------
# External Locations
# -------------------------------------------------
def ensure_external_location(loc):
    """
    Registers an external location (e.g., ADLS container or folder)
    that can be referenced by Unity Catalog-managed tables.
    """
    try:
        logger.info(f"Creating External Location: {loc['name']}")
        w.external_locations.create(
            name=loc["name"],
            url=loc["url"],
            credential_name=loc["credential"],
            read_only=False
        )
    except AlreadyExists:
        logger.info(f"Location already exists: {loc['name']}")

# -------------------------------------------------
# Catalog + Schema Creation
# -------------------------------------------------
def ensure_catalog(catalog):
    """
    Ensures a catalog exists. Catalogs are the top layer in UC.
    """
    try:
        logger.info(f"Creating catalog: {catalog}")
        w.catalogs.create(name=catalog)
    except AlreadyExists:
        logger.info(f"Catalog already exists: {catalog}")

def ensure_schema(catalog, schema):
    """
    Ensures a schema exists inside a catalog.
    Equivalent to databases in pre-UC Databricks.
    """
    try:
        logger.info(f"Creating schema: {catalog}.{schema}")
        w.schemas.create(name=schema, catalog_name=catalog)
    except AlreadyExists:
        logger.info(f"Schema already exists: {catalog}.{schema}")

# -------------------------------------------------
# Permissions
# -------------------------------------------------
def apply_permissions(perm):
    """
    Applies catalog-level permissions (privileges)
    to Databricks groups or service principals.
    """
    logger.info(f"Granting permissions on {perm['catalog']} to {perm['group']}")
    w.grants.update(
        securable_type="catalog",
        securable_name=perm["catalog"],
        grants=[{
            "principal": perm["group"],
            "privileges": perm["privileges"]
        }]
    )

# -------------------------------------------------
# MAIN WORKFLOW
# -------------------------------------------------
def bootstrap_uc():
    """
    Main bootstrap sequence for Unity Catalog.
    Creates:
        - Metastore
        - Storage Credentials
        - External Locations
        - Catalogs + Schemas
        - Permissions
    All based on definitions in unity_catalog.yml.
    """
    logger.info("Starting Unity Catalog bootstrap")

    # Setup metastore and bind workspace to it
    ms = ensure_metastore(config["metastore"])
    assign_workspace_to_metastore(ms)

    # Storage credentials (e.g. managed identities)
    for cred in config["storage_credentials"]:
        ensure_storage_credential(cred)

    # External locations pointing to cloud storage paths
    for loc in config["external_locations"]:
        ensure_external_location(loc)

    # Create catalogs and schemas
    for catalog in config["catalogs"]:
        ensure_catalog(catalog["name"])

        for schema in catalog["schemas"]:
            ensure_schema(catalog["name"], schema)

    # Apply catalog-level permissions
    for perm in config["permissions"]:
        apply_permissions(perm)

    logger.info("Unity Catalog bootstrap completed!")

# Script entry point
if __name__ == "__main__":
    bootstrap_uc()