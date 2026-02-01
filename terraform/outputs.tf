output "catalog_name" {
  value = databricks_catalog.pr_sandbox.name
}

output "warehouse_id" {
  value = databricks_sql_warehouse.pr_warehouse.id
}
