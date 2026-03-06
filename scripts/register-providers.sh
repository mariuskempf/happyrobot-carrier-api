#!/bin/bash

# register-providers.sh
#
# Run this ONCE before bootstrap.sh to register all required Azure resource
# providers on your subscription. This is a one-time step per subscription
# and may not be necessary on enterprise subscriptions.
#
# Prerequisites: az login must already be done before running this script.

set -e

PROVIDERS=(
  "Microsoft.Storage"
  "Microsoft.App"
  "Microsoft.ContainerRegistry"
  "Microsoft.KeyVault"
  "Microsoft.OperationalInsights"
  "Microsoft.ManagedIdentity"
)

echo "▶ Registering Azure resource providers..."
for PROVIDER in "${PROVIDERS[@]}"; do
  echo "   Registering $PROVIDER..."
  az provider register --namespace "$PROVIDER"
done

echo ""
echo "▶ Waiting for all providers to finish registering..."
for PROVIDER in "${PROVIDERS[@]}"; do
  echo -n "   $PROVIDER: "
  while true; do
    STATE=$(az provider show --namespace "$PROVIDER" --query registrationState --output tsv | tr -d '[:space:]')
    echo -n "$STATE "
    if [ "$STATE" == "Registered" ]; then
      echo "✔"
      break
    fi
    sleep 5
  done
done

echo ""
echo "✅ All providers registered. You can now run bootstrap.sh."