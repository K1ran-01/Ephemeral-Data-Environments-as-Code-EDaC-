
# Reference the existing Unity Catalog using the correct data source

# Use the correct data source and attribute for Databricks Unity Catalog
data "databricks_catalogs" "all" {}

locals {
  existing_catalog = contains(data.databricks_catalogs.all.ids, "trial_dbt") ? "trial_dbt" : null
}

# Create a schema inside the existing catalog for this PR
resource "databricks_schema" "pr_schema" {
  name         = "pr_schema_${var.pr_number}"
  catalog_name = local.existing_catalog
  comment      = "Ephemeral schema for PR #${var.pr_number}"
  properties = {
    "managed-by" = "eda-controller"
  }
}

# Create a serverless SQL endpoint for the PR
resource "databricks_sql_endpoint" "pr_warehouse" {
  name                         = "pr_warehouse_${var.pr_number}"
  cluster_size                 = "2X-Small"
  enable_serverless_compute    = true
  auto_stop_mins               = 10
  tags {
    custom_tags {
      key   = "managed-by"
      value = "eda-controller"
    }
  }
}

# Grant usage on the catalog to the PR author
resource "databricks_grants" "author_usage" {
  catalog = local.existing_catalog
  grant {
    principal  = var.pr_author
    privileges = ["USE_CATALOG", "USE_SCHEMA", "CREATE_SCHEMA"]
  }
}

# Grant schema-level privileges to the PR author
resource "databricks_grants" "author_schema" {
  schema = databricks_schema.pr_schema.id
  grant {
    principal  = var.pr_author
    privileges = ["ALL_PRIVILEGES"]
  }
}

# Grant usage on the catalog to the service principal
resource "databricks_grants" "sp_usage" {
  catalog = local.existing_catalog
  grant {
    principal  = var.service_principal_id
    privileges = ["ALL_PRIVILEGES"]
  }
}

# Grant schema-level privileges to the service principal
resource "databricks_grants" "sp_schema" {
  schema = databricks_schema.pr_schema.id
  grant {
    principal  = var.service_principal_id
    privileges = ["ALL_PRIVILEGES"]
  }
}
