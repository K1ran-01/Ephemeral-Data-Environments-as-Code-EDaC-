terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = ">=1.72"
    }
  }

  backend "azurerm" {
    subscription_id      = "105849c7-0a47-45d0-a4db-8ece4fd39ade"
    resource_group_name  = "EnterpriseData-NonProd-RG"
    storage_account_name = "enterprisedatafcstonedev"
    container_name       = "np-tfstates"
    key                  = "test-EDAC.tfstate"
  }
}

provider "databricks" {
  host  = var.databricks_host
  token = var.databricks_token
}
