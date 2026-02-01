output "catalog_name" {
  value = databricks_catalog.pr_sandbox.name
}

output "warehouse_id" {
  value = databricks_sql_warehouse.pr_warehouse.id
}

# Output the name of the created catalog for use in other steps/scripts
output "catalog_name" {
  value       = databricks_catalog.pr_sandbox.name
  description = "The name of the ephemeral Unity Catalog created for the PR."
}

# Output the HTTP path for the created SQL warehouse
output "warehouse_http_path" {
  value       = "/sql/1.0/warehouses/${databricks_sql_warehouse.pr_warehouse.id}"
  description = "The HTTP path for the ephemeral SQL Warehouse."
}
