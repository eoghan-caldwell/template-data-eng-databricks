"""
Bootstrap Script: Users & Groups Setup
Purpose: Create baseline groups, add users, and assign permissions.
"""

import yaml
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import AlreadyExists
import logging

# -------------------------------------------------
# Setup Logging
# -------------------------------------------------
# Configure logging so each step prints helpful status messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap-users-groups")

# -------------------------------------------------
# Load Config
# -------------------------------------------------
# Path to the YAML file containing groups and user definitions
CONFIG_PATH = "config/users_and_groups.yml"

# Load YAML configuration (groups + users)
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

groups = config.get("groups", [])  # List of groups to create
users = config.get("users", [])    # List of users with group memberships

# Databricks Workspace Client (auth handled externally)
w = WorkspaceClient()

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------
def safe_create_group(name: str):
    """
    Create a group if it does not already exist.
    Groups are used to manage permissions centrally.
    """
    try:
        logger.info(f"Ensuring group exists: {name}")
        w.groups.create(name=name)
    except AlreadyExists:
        logger.info(f"Group already exists: {name}")

def safe_add_user(email: str):
    """
    Create a user account if it does not already exist.
    Email address becomes the Databricks username.
    """
    try:
        logger.info(f"Ensuring user exists: {email}")
        w.users.create(user_name=email)
    except AlreadyExists:
        logger.info(f"User already exists: {email}")

def safe_add_user_to_group(user, group):
    """
    Adds a user to a group.
    Looks up IDs for both the user and group before linking.
    """
    logger.info(f"Adding user {user} to group {group}")

    # Find group ID by display name
    gid = w.groups.list(filter=f"displayName eq '{group}'")[0].id
    # Find user ID by username (email)
    uid = w.users.list(filter=f"userName eq '{user}'")[0].id

    # Add the user to the specified group
    w.groups.add_member(gid, uid)

# -------------------------------------------------
# Main Logic
# -------------------------------------------------
def bootstrap_users_and_groups():
    """
    Main bootstrap sequence for Users & Groups.
    - Creates groups
    - Creates users
    - Assigns each user to their configured groups
    """
    logger.info("Starting Users & Groups Bootstrap")

    # 1. Create all groups defined in the config
    for group in groups:
        safe_create_group(group)

    # 2. Create users and link them to groups
    for user in users:
        email = user["email"]
        safe_add_user(email)

        # Add user to all their groups
        for g in user.get("groups", []):
            safe_add_user_to_group(email, g)

    logger.info("Users & Groups bootstrap complete!")

# Run script when executed directly
if __name__ == "__main__":
    bootstrap_users_and_groups()