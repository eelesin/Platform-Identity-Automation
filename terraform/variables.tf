variable "resource_group_name" {
  default = "provision-user-rg"
}

variable "location" {
  default = "westus2"
}

variable "acr_name" {
  default = "provisionuseracr"
}

variable "container_name" {
  default = "provision-user"
}

variable "image_name" {
  description = "Full image name with tag"
}

variable "subscription_id" {
  description = "Azure subscription ID"
}

variable "acr_username" {
  description = "ACR username"
}

variable "acr_password" {
  description = "ACR password"
  sensitive   = true
}

variable "jira_url" {
  description = "Jira base URL"
}

variable "jira_email" {
  description = "Jira email"
}

variable "jira_api_token" {
  description = "Jira API token"
  sensitive   = true
}

variable "graph_tenant_id" {
  description = "Azure AD tenant ID"
}

variable "graph_client_id" {
  description = "Azure AD client ID"
}

variable "graph_client_secret" {
  description = "Azure AD client secret"
  sensitive   = true
}