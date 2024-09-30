variable "aws_region_name" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type = string
}

variable "aws_profile" {
  description = "Aws profile"
  type        = string
  default     = null
}

variable "aws_access_key" {
  description = "The AWS access key."
  type        = string
  default     = null
}

variable "aws_secret_key" {
  description = "The AWS secret key."
  type        = string
  default     = null
}

variable "s3_use_path_style" {
  description = "Use path-style access for S3."
  type        = bool
  default     = false
}

variable "skip_credentials_validation" {
  description = "Skip credentials validation."
  type        = bool
  default     = false
}

variable "skip_metadata_api_check" {
  description = "Skip metadata API check."
  type        = bool
  default     = false
}

variable "skip_requesting_account_id" {
  description = "Skip requesting account ID."
  type        = bool
  default     = false
}

variable "aws_service_endpoints" {
  description = "Custom endpoints for AWS services."
  type        = map(string)
  default = {
    apigateway     = null
    apigatewayv2   = null
    cloudformation = null
    cloudwatch     = null
    cognitoidp     = null
    dynamodb       = null
    ec2            = null
    es             = null
    elasticache    = null
    firehose       = null
    iam            = null
    kinesis        = null
    lambda         = null
    rds            = null
    redshift       = null
    route53        = null
    s3             = null
    secretsmanager = null
    ses            = null
    sns            = null
    sqs            = null
    ssm            = null
    stepfunctions  = null
    sts            = null
  }
}
