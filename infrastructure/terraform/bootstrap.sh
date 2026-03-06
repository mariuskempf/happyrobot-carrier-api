#!/bin/bash

# bootstrap.sh
#
# Run this ONCE before `terraform init` to create the remote state storage.
# After this runs, all other infrastructure is managed by Terraform itself.
# Prerequisites: az login must already be done before running this script.

set -e

LOCATION="westus"
TF_STATE_RG="happyrobot-tfstate-rg"
TF_STATE_SA="fdehappyrobotmarius"   # note: this must be globally unique, lowercase, no hyphens
TF_STATE_CONTAINER="tfstate"


### Confirm Active Subscription Subscription ###

echo "▶ Checking active Azure subscription..."
SUBSCRIPTION_ID=$(az account show --query id --output tsv | tr -d '[:space:]')
SUBSCRIPTION_NAME=$(az account show --query name --output tsv | tr -d '[:space:]')

echo "   Subscription : $SUBSCRIPTION_NAME"
echo "   ID           : $SUBSCRIPTION_ID"
echo ""
read -r -p "Press Enter to continue with this subscription, or Ctrl+C to abort..."

az account set --subscription "$SUBSCRIPTION_ID"


### Create Resources ###

echo "▶ Creating resource group for Terraform state..."
az group create \
  --name $TF_STATE_RG \
  --location $LOCATION \
  --subscription "$SUBSCRIPTION_ID"

echo "▶ Creating storage account for Terraform state..."
az storage account create \
  --name $TF_STATE_SA \
  --resource-group $TF_STATE_RG \
  --location $LOCATION \
  --sku Standard_LRS \
  --encryption-services blob \
  --min-tls-version TLS1_2 \
  --subscription "$SUBSCRIPTION_ID"

echo "▶ Creating blob container for Terraform state..."
az storage container create \
  --name $TF_STATE_CONTAINER \
  --account-name $TF_STATE_SA \
  --subscription "$SUBSCRIPTION_ID" \
  --auth-mode login


### Print Summary ###

PORTAL_URL="https://portal.azure.com/#resource/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${TF_STATE_RG}/providers/Microsoft.Storage/storageAccounts/${TF_STATE_SA}/blobServices/default/containers/${TF_STATE_CONTAINER}"

echo ""
echo "✅ Remote state storage ready."
echo ""
echo "🔗 View in Azure Portal:"
echo "   $PORTAL_URL"
echo ""
