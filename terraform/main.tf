# Create a unique catalog for the PR
resource "databricks_catalog" "pr_sandbox" {
  name  = "sandbox_pr_${var.pr_number}"
  comment = "Sandbox catalog for PR #${var.pr_number}"
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
  catalog = databricks_catalog.pr_sandbox.name
  grant {
    principal  = var.pr_author
    privileges = ["USE_CATALOG", "USE_SCHEMA", "CREATE_SCHEMA"]
  }
}

# Grant usage on the catalog to the service principal
resource "databricks_grants" "sp_usage" {
  catalog = databricks_catalog.pr_sandbox.name
  grant {
    principal  = var.service_principal_id
    privileges = ["ALL_PRIVILEGES"]
  }
}
