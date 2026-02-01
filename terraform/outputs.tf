output "catalog_name" {
  value = databricks_catalog.pr_sandbox.name
}

output "warehouse_id" {
  value = databricks_sql_endpoint.pr_warehouse.id
}
# Output the HTTP path for the created SQL warehouse
output "warehouse_http_path" {
  value       = "/sql/1.0/warehouses/${databricks_sql_endpoint.pr_warehouse.id}"
  description = "The HTTP path for the ephemeral SQL Warehouse."
}
