variable "region" {
  type = string
}

variable "project_name" {
  type = string
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Valid values for var: environment are dev, staging, prod."
  }
}
