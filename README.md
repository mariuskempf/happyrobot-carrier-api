# HappyRobot - Inbound Carrier Sales API Server

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

# FCSMA API

- [FCSMA - Federal Motor Carrier Safety Administration](https://mobile.fmcsa.dot.gov/QCDevsite/)
- [FCSMA - API Documentation](https://mobile.fmcsa.dot.gov/QCDevsite/docs/getStarted)

API elements considered relevant regarding eligibility of a carrier:

| Field            | Description                                                         | Type       |
| ---------------- | ------------------------------------------------------------------- | ---------- |
| allowToOperate   | Indicates if a carrier is allowed to operate by law                 | Y or N     |
| outOfService     | Carrier received out of service order and is not allowed to operate | Y or N     |
| outOfServiceDate | The date the carrier received out of service order                  | MM/DD/YYYY |
| complaintCount   | Number of customer complaints about the carrier received by FMCSA   | Number     |
| dotNumber        | U.S. DOT registered number for the carrier                          | Number     |
| mcNumber         | U.S. DOT registered motor carrier number for the carrier            | Number     |
| legalName        | Legal registered name of the carrier                                | String     |
| dbaName          | Alternative operating name of the carrier                           | String     |

## Local Development

...
