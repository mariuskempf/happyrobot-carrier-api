variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "westus"
}

variable "resource_group_name" {
  description = "Name of the main resource group"
  type        = string
  default     = "happyrobot-rg"
}

variable "acr_name" {
  description = "Azure Container Registry name"
  type        = string
  default     = "happyrobotacr"
}

variable "key_vault_name" {
  description = "Azure Key Vault name (globally unique)"
  type        = string
  default     = "happyrobot-kv"
}

variable "app_name" {
  description = "Container App name"
  type        = string
  default     = "happyrobot-api"
}

variable "fmcsa__api_key" {
  description = "FMCSA API key"
  type        = string
  sensitive   = true
}

variable "api_key" {
  description = "API key for securing your FastAPI endpoints"
  type        = string
  sensitive   = true
}
