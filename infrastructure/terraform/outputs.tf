output "app_url" {
  description = "Public HTTPS URL of the deployed Container App"
  value       = "https://${azurerm_container_app.main.ingress[0].fqdn}"
}

output "acr_login_server" {
  description = "ACR login server (used in GitHub Actions)"
  value       = azurerm_container_registry.acr.login_server
}

output "acr_name" {
  description = "ACR name (used in GitHub Actions secret ACR_NAME)"
  value       = azurerm_container_registry.acr.name
}

output "app_identity_client_id" {
  description = "Client ID of the user-assigned managed identity"
  value       = azurerm_user_assigned_identity.app_identity.client_id
}
