variable "resource_group_name" {
  default = "provision-user-rg"
}

variable "location" {
  default = "westus2"
}

variable "acr_name" {
  default = "provisionuseracr"
}

variable "image_name" {
  description = "Full image name with tag"
}

variable "image_name" {
  default = "provisionuseracr.azurecr.io/provision-user:1.0"
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