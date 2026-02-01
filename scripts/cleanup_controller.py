import os
import json
import requests
import argparse # New import

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

# Protect shared catalogs that should never be deleted by automation
PROTECTED_CATALOGS = {"trial_dbt"}

def cleanup_databricks_resources(catalog_name, warehouse_id):
    """
    Uses the Databricks API to delete the ephemeral resources.
    """
    if not catalog_name:
        print("No catalog name provided for cleanup.")
        return

    print(f"Starting cleanup for catalog: {catalog_name}")

    if catalog_name in PROTECTED_CATALOGS:
        print(f"Catalog '{catalog_name}' is protected and will not be deleted.")
    else:
        headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}

        # 1. Delete the Catalog (requires all objects within to be deleted first)
        # This is a recursive delete, which is a powerful and dangerous operation.
        # The Databricks API for Unity Catalog requires care.
        catalog_url = f"https://{DATABRICKS_HOST}/api/2.1/unity-catalog/catalogs/{catalog_name}?force=true"
        response = requests.delete(catalog_url, headers=headers)
        if response.status_code == 200:
            print(f"Successfully deleted catalog: {catalog_name}")
        else:
            print(f"Error deleting catalog: {response.status_code} - {response.text}")

    headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}

    # 2. Delete the SQL Warehouse
    if warehouse_id:
        warehouse_url = f"https://{DATABRICKS_HOST}/api/2.0/sql/warehouses/{warehouse_id}"
        response = requests.delete(warehouse_url, headers=headers)
        if response.status_code == 200:
            print(f"Successfully deleted SQL warehouse: {warehouse_id}")
        else:
            print(f"Error deleting SQL warehouse: {response.status_code} - {response.text}")


def handle_pr_closed_event(pr_number, catalog_name=None, warehouse_id=None):
    """
    Main handler for a 'PR Closed' event.
    """
    print(f"Received 'PR Closed' event for PR #{pr_number}")
    
    # In a real scenario, you would first run `terraform destroy` for the specific PR workspace.
    # By passing catalog_name and warehouse_id directly, we are moving closer to that robust approach.

    if catalog_name:
        cleanup_databricks_resources(catalog_name, warehouse_id)
    else:
        print(f"No catalog name provided for PR #{pr_number}. Skipping cleanup.")


if __name__ == "__main__":
    # This is a simulation of the controller being triggered.
    # In a real application, this would be triggered by a webhook from GitHub.
    # For example, an AWS Lambda function or a service running in a container.

    parser = argparse.ArgumentParser(description="Cleanup controller for ephemeral Databricks resources.")
    parser.add_argument("--pr-number", type=int, required=True, help="The pull request number.")
    parser.add_argument("--catalog-name", type=str, help="The name of the Unity Catalog to clean up.")
    parser.add_argument("--warehouse-id", type=str, help="The ID of the SQL Warehouse to clean up.")

    args = parser.parse_args()
    
    print("--- State-Aware Cleanup Controller ---")
    print("This script is a conceptual model.")
    print("It outlines the logic for cleaning up ephemeral resources after a PR is closed.")
    print("In a real implementation, this would be part of a robust CI/CD webhook system.\n")
    handle_pr_closed_event(args.pr_number, args.catalog_name, args.warehouse_id)

    print("\nCleanup controller simulation finished.")
