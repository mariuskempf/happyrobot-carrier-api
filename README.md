# happyrobot-carrier-api

...

## Set Up Cloud Infrastructure

You must have a Microsoft Azure cloud account available with an active subscription.

- [Microsoft Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Terraform CLI](https://developer.hashicorp.com/terraform/install)

### Create Azure Blob Storage for Remote State Management

1.  Login to Azure & choose subscription to be used

    ```bash
    az login
    ```

2.  Register required resource providers (optional)

    ```bash
    chmod +x scripts/register-providers.sh
    ./scripts/register-providers.sh
    ```

3.  Bootstrap storage account for terraform state management

    ```bash
    chmod +x terraform/bootstrap.sh
    ./terraform/bootstrap.sh
    ```

Note: Before running `bootstrap.sh`, ensure all required Azure resource providers are registered on your subscription by running `scripts/register-providers.sh` — this is a one-time step that may not be necessary on enterprise subscriptions.

### Deploy infrastructure using Terraform

1. Set variables for infrastructure deployment, including secrets

   ```bash
   cd infrastructure/terraform/
   cp terraform.tfvars.example terraform.tfvars  # fill in your secrets
   ```

2. Initialize terraform provider and run planning

   ```bash
   terraform init
   terraform plan
   ```

3. Apply infrastructure configuration

   ```bash
   terraform apply
   ```

## Local Development

...
