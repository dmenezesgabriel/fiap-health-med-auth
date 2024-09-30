output "tf_state_bucket_name" {
  value = module.backend.backend_state_bucket_name
}

output "tf_state_lock_dynamo_db_table_name" {
  value = module.backend.backend_state_dynamo_lock_table_name
}

output "tf_state_bucket_encryption_kms_alias_name" {
  value = module.backend.backend_state_kms_key_alias_name
}
