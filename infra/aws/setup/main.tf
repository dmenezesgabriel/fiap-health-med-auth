terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws",
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = var.aws_region_name
  profile    = var.aws_profile
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key

  s3_use_path_style           = var.s3_use_path_style
  skip_credentials_validation = var.skip_credentials_validation
  skip_metadata_api_check     = var.skip_metadata_api_check
  skip_requesting_account_id  = var.skip_requesting_account_id


  endpoints {
    apigateway     = var.aws_service_endpoints["apigateway"]
    apigatewayv2   = var.aws_service_endpoints["apigatewayv2"]
    cloudformation = var.aws_service_endpoints["cloudformation"]
    cloudwatch     = var.aws_service_endpoints["cloudwatch"]
    cognitoidp     = var.aws_service_endpoints["cognitoidp"]
    dynamodb       = var.aws_service_endpoints["dynamodb"]
    ec2            = var.aws_service_endpoints["ec2"]
    es             = var.aws_service_endpoints["es"]
    elasticache    = var.aws_service_endpoints["elasticache"]
    firehose       = var.aws_service_endpoints["firehose"]
    iam            = var.aws_service_endpoints["iam"]
    kinesis        = var.aws_service_endpoints["kinesis"]
    lambda         = var.aws_service_endpoints["lambda"]
    rds            = var.aws_service_endpoints["rds"]
    redshift       = var.aws_service_endpoints["redshift"]
    route53        = var.aws_service_endpoints["route53"]
    s3             = var.aws_service_endpoints["s3"]
    secretsmanager = var.aws_service_endpoints["secretsmanager"]
    ses            = var.aws_service_endpoints["ses"]
    sns            = var.aws_service_endpoints["sns"]
    sqs            = var.aws_service_endpoints["sqs"]
    ssm            = var.aws_service_endpoints["ssm"]
    stepfunctions  = var.aws_service_endpoints["stepfunctions"]
    sts            = var.aws_service_endpoints["sts"]
  }
}

module "cognito" {
  source = "github.com/dmenezesgabriel/tf-aws-modules//modules/aws/cognito"

  name            = "main"
  aws_region_name = var.aws_region_name
  project_name    = var.project_name
  cognito_user_pool_password_policy = {
    minimum_length    = 6
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }
  cognito_user_pool_verified_attributes          = ["email"]
  cognito_user_pool_email_verification_subject   = "Your verification code"
  cognito_user_pool_email_verification_message   = "Your verification code is {####}"
  cognito_user_pool_default_email_option         = "CONFIRM_WITH_CODE"
  cognito_user_pool_mfa_configuration            = "OFF"
  cognito_user_pool_allow_admin_create_user_only = false
  cognito_user_pool_account_recovery = {
    name     = "verified_email"
    priority = 1
  }
  cognito_user_pool_schemas = [{
    name                = "email"
    attribute_data_type = "String"
    mutable             = false
    required            = true
    },
    {
      name                = "name"
      attribute_data_type = "String"
      mutable             = true
      required            = true
    },
    {
      name                = "role"
      attribute_data_type = "String"
      mutable             = true
      required            = false
    },
    {
      name                = "cpf"
      attribute_data_type = "String"
      mutable             = true
      required            = false
    },
    {
      name                = "crm"
      attribute_data_type = "String"
      mutable             = true
      required            = false
    }
  ]
  cognito_user_pool_client_generate_secret = false
  cognito_user_pool_client_explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]
  cognito_user_pool_client_refresh_token_validity        = 30
  cognito_user_pool_client_access_token_validity         = 24
  cognito_user_pool_client_id_token_validity             = 24
  cognito_user_pool_client_prevent_user_existence_errors = "ENABLED"
  cognito_user_pool_client_enable_token_revocation       = true
  cognito_user_pool_client_write_attributes              = null
  cognito_user_pool_client_read_attributes               = null
  save_to_ssm                                            = true
}
