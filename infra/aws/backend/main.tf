terraform {

  required_version = "~> 1.0"

  required_providers {

    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

locals {
  prefix                 = "tf-state"
  prefix_project_account = "${local.prefix}-${var.project_name}-${data.aws_caller_identity.current.account_id}"
}

data "aws_caller_identity" "current" {}

module "backend" {
  source                        = "github.com/dmenezesgabriel/tf-aws-modules//modules/aws/backend"
  region                        = var.region
  bucket_name                   = local.prefix_project_account
  dynamodb_table_name           = local.prefix_project_account
  bucket_server_side_encryption = false
  # kms_alias_name = "alias/${local.prefix_project_account}"
}
