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