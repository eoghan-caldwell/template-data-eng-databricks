"""
Bootstrap Script: Cluster + Policy Setup
Purpose: Create cluster policies, instance pools, and baseline clusters.
"""

import yaml
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import AlreadyExists
import logging

# Configure logging so we can see informative messages during execution
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap-clusters")

# Path to YAML configuration file containing pools, policies, clusters, etc.
CONFIG_PATH = "config/clusters.yml"

# Load the config file into a Python dictionary
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Initialise Databricks workspace client (auth handled by environment config)
w = WorkspaceClient()

# -------------------------------------------------
# Instance Pools
# -------------------------------------------------
def ensure_instance_pool(pool):
    """
    Ensure an instance pool exists.
    Creates the pool if missing; ignores if it already exists.
    """
    try:
        logger.info(f"Creating instance pool: {pool['name']}")
        w.instance_pools.create(
            instance_pool_name=pool["name"],
            node_type_id=pool["node_type"],
            min_idle_instances=pool["min_idle"],
            max_capacity=pool["max_capacity"]
        )
    except AlreadyExists:
        # Databricks returns AlreadyExists when the pool name is in use
        logger.info(f"Pool exists: {pool['name']}")

# -------------------------------------------------
# Cluster Policies
# -------------------------------------------------
def ensure_policy(policy):
    """
    Ensure a cluster policy exists.
    Cluster policies enforce required settings on clusters.
    """
    try:
        logger.info(f"Creating cluster policy: {policy['name']}")
        w.cluster_policies.create(
            name=policy["name"],
            definition=policy["definition"]
        )
    except AlreadyExists:
        logger.info(f"Policy already exists: {policy['name']}")

# -------------------------------------------------
# Clusters
# -------------------------------------------------
def ensure_cluster(cluster):
    """
    Ensure a baseline cluster exists.
    Creates a cluster if missing; otherwise logs that it’s already present.
    """
    try:
        logger.info(f"Creating cluster: {cluster['name']}")
        w.clusters.create(
            cluster_name=cluster["name"],
            spark_version=cluster["spark_version"],
            node_type_id=cluster["node_type"],
            autoscale=cluster["autoscale"],
            policy_id=cluster["policy_id"]
        )
    except AlreadyExists:
        logger.info(f"Cluster exists: {cluster['name']}")

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def bootstrap_clusters():
    """
    Main entry point.
    Processes instance pools, cluster policies, and clusters
    in that order to ensure the workspace is correctly bootstrapped.
    """
    logger.info("Starting Cluster bootstrap")

    # Create instance pools first (clusters may depend on them)
    for pool in config["instance_pools"]:
        ensure_instance_pool(pool)

    # Set cluster policies that enforce rules for cluster creation
    for policy in config["cluster_policies"]:
        ensure_policy(policy)

    # Create the baseline clusters with the correct policies applied
    for cluster in config["clusters"]:
        ensure_cluster(cluster)

    logger.info("Cluster bootstrap completed!")

# Run script if executed directly
if __name__ == "__main__":
    bootstrap_clusters()