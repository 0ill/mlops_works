# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
  client_id       = var.azure_client_id
  client_secret   = var.azure_client_secret
  tenant_id       = var.azure_tenant_id
}

# Define variables for GitHub secrets
variable "azure_subscription_id" {}
variable "azure_client_id" {}
variable "azure_client_secret" {}
variable "azure_tenant_id" {}
variable "dockerhub_username" {}
variable "dockerhub_token" {}

# Create a resource group
resource "azurerm_resource_group" "test-apps-dev" {
  name     = "test-apps-dev"
  location = "australiaeast"
}

# Important Note: 
# If the resource group "test-apps-dev" already exists in Azure and is not managed by Terraform, 
# you need to import it into the Terraform state before applying the configuration.
#
# To import the existing resource group, run:
# terraform import azurerm_resource_group.test-apps-dev /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/test-apps-dev
#
# Replace YOUR_SUBSCRIPTION_ID with your actual Azure subscription ID.

# Create a Container Apps Environment
resource "azurerm_container_app_environment" "test-apps-dev" {
  name                = "test-apps-dev"
  location            = azurerm_resource_group.test-apps-dev.location
  resource_group_name = azurerm_resource_group.test-apps-dev.name
}

# Create a Container Registry
resource "azurerm_container_registry" "test-apps-dev" {
  name                = "testdevappsacr"
  resource_group_name = azurerm_resource_group.test-apps-dev.name
  location            = azurerm_resource_group.test-apps-dev.location
  sku                 = "Basic"
  admin_enabled       = true
}

# Create a Container App
resource "azurerm_container_app" "test-apps-dev" {
  name                         = "test-apps-dev"
  container_app_environment_id = azurerm_container_app_environment.test-apps-dev.id
  resource_group_name          = azurerm_resource_group.test-apps-dev.name
  revision_mode                = "Single"

  template {
    container {
      name   = "test-apps-dev"
      image  = "${azurerm_container_registry.test-apps-dev.login_server}/test-apps:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }

  ingress {
    external_enabled = true
    target_port      = 80
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  registry {
    server               = azurerm_container_registry.test-apps-dev.login_server
    username             = azurerm_container_registry.test-apps-dev.admin_username
    password_secret_name = "registry-password"
  }

  secret {
    name  = "registry-password"
    value = azurerm_container_registry.test-apps-dev.admin_password
  }
}

# Output the FQDN of the Container App
output "app_fqdn" {
  value = azurerm_container_app.test-apps-dev.latest_revision_fqdn
}

# Output the ACR login server
output "acr_login_server" {
  value = azurerm_container_registry.test-apps-dev.login_server
}
