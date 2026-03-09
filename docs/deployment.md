# Deployment

This document covers cloud infrastructure setup, deployment, and CI/CD for the HappyRobot Carrier Sales API.

The API is deployed to **Azure Container Apps** using **Terraform** for infrastructure as code and **GitHub Actions** for CI/CD.

## Prerequisites

- [Microsoft Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Terraform CLI](https://developer.hashicorp.com/terraform/install)
- An Azure account with an active subscription
- GitHub repository secrets configured (see [CI/CD](#cicd) section)

## Azure Infrastructure Setup

### 1. Login to Azure

Login to Azure and select the subscription you want to deploy to.

```bash
az login
```

### 2. Register Required Resource Providers (one-time)

This step may not be necessary on enterprise subscriptions but is recommended for new accounts.

```bash
chmod +x scripts/register-providers.sh
./scripts/register-providers.sh
```

### 3. Bootstrap Remote State Storage

Terraform state is stored remotely in Azure Blob Storage. Run the bootstrap script once to create the storage account:

```bash
chmod +x infrastructure/terraform/bootstrap.sh
./infrastructure/terraform/bootstrap.sh
```

### 4. Deploy Infrastructure with Terraform

1. Set your variables including secrets:

   ```bash
   cd infrastructure/terraform/
   cp terraform.tfvars.example terraform.tfvars
   # Fill in your values
   ```

2. Initialize the Terraform provider:

   ```bash
   terraform init
   ```

3. Preview the planned changes:

   ```bash
   terraform plan
   ```

4. Apply the infrastructure:

   ```bash
   terraform apply
   ```

> **Note:** The Container App is initially provisioned with a placeholder image (`mcr.microsoft.com/azuredocs/containerapps-helloworld:latest`) since the ACR is empty at this point. The CD pipeline replaces it with the real image on the first push to `main`. Terraform ignores image changes after the initial apply, so subsequent `terraform apply` runs will not revert the image set by the pipeline.

This provisions the following Azure resources:

- **Azure Container Registry (ACR)** — stores Docker images
- **Azure Key Vault** — stores API keys and secrets
- **Azure Container App Environment** — networking and observability layer
- **Azure Container Apps** — runs the containerized API

## CI/CD

Two GitHub Actions workflows handle quality checks and deployment.

### CI Pipeline (`.github/workflows/ci.yaml`)

Runs on every **pull request to `main`**. Three parallel jobs:

| Job             | Tool              | Check                         |
| --------------- | ----------------- | ----------------------------- |
| Code Formatting | `black` + `isort` | Enforces consistent style     |
| Linting         | `pylint`          | Minimum score of 8.5 required |
| Unit Tests      | `pytest`          | All tests must pass           |

### Deploy Pipeline (`.github/workflows/deploy.yaml`)

Runs on every **push to `main`** (and can be triggered manually via `workflow_dispatch`).

Steps:

1. Authenticate with Azure using `AZURE_CREDENTIALS` secret
2. Log in to Azure Container Registry
3. Build and push Docker image tagged with the commit SHA and `latest`
4. Update the Azure Container App to use the new image
5. Print the live app URL

**Image Tagging Strategy**

Each build produces two tags:

- `:latest` — updated on every deploy, useful for quick reference
- `:<commit-sha>` — immutable tag tied to the exact commit, used for the Container App deployment to ensure reproducibility and enable rollbacks

### Required GitHub Secrets & Variables

Configure these in your repository under **Settings → Secrets and variables → Actions**:

| Name                | Type     | Description                   |
| ------------------- | -------- | ----------------------------- |
| `AZURE_CREDENTIALS` | Secret   | Azure service principal JSON  |
| `ACR_NAME`          | Variable | Azure Container Registry name |

To generate `AZURE_CREDENTIALS`:

```bash
az ad sp create-for-rbac \
  --name "happyrobot-github-actions" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/happyrobot-rg \
  --sdk-auth
```

## Accessing the Deployment

Once deployed, retrieve the live URL:

```bash
az containerapp show \
  --name happyrobot-api \
  --resource-group happyrobot-rg \
  --query properties.configuration.ingress.fqdn \
  --output tsv
```

The API will be available at `https://<fqdn>`. Swagger UI at `https://<fqdn>/docs`.

> **Note:** HTTPS is automatically provided by Azure Container Apps — a managed TLS certificate is provisioned for the `*.azurecontainerapps.io` domain with no additional configuration required.

## Reproducing the Deployment

To fully reproduce the deployment from scratch:

1. Fork/clone the repository
2. Create an Azure subscription
3. Run `scripts/register-providers.sh`
4. Run `terraform/bootstrap.sh`
5. Fill in `terraform.tfvars`
6. Run `terraform apply`
7. Configure GitHub secrets (`AZURE_CREDENTIALS`, `ACR_NAME`)
8. Push to `main` — the deploy pipeline handles the rest
