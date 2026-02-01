terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "1.4.0"
    }
  }
}

provider "databricks" {
  # Configure authentication using environment variables
  # DATABRICKS_HOST and DATABRICKS_TOKEN
}
