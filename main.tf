provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "logicapp-rg"
  location = "Central India"
}

# Logic App (Consumption Plan - easier)
resource "azurerm_logic_app_workflow" "logicapp" {
  name                = "mail-forward-logicapp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  definition = <<JSON
{
  "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2019-05-01/workflowdefinition.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "$connections": {
      "type": "Object"
    }
  },
  "triggers": {
    "When_a_new_email_arrives": {
      "type": "ApiConnection",
      "inputs": {
        "host": {
          "connection": {
            "name": "@parameters('$connections')['office365']['connectionId']"
          }
        },
        "method": "get",
        "path": "/v3/Mail/OnNewEmail"
      }
    }
  },
  "actions": {
    "Forward_email": {
      "type": "ApiConnection",
      "inputs": {
        "host": {
          "connection": {
            "name": "@parameters('$connections')['office365']['connectionId']"
          }
        },
        "method": "post",
        "path": "/v2/Mail/Send",
        "body": {
          "To": "canvasdentalcare@gmail.com",
          "Subject": "Forwarded: @{triggerBody()?['Subject']}",
          "Body": "@{triggerBody()?['Body']}"
        }
      }
    }
  }
}
JSON

  parameters = {
    "$connections" = jsonencode({
      office365 = {
        connectionId   = "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RG>/providers/Microsoft.Web/connections/office365"
        connectionName = "office365"
        id             = "/subscriptions/<SUBSCRIPTION_ID>/providers/Microsoft.Web/locations/centralindia/managedApis/office365"
      }
    })
  }
}
