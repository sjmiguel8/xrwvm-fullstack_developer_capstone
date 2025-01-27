output "amplify_app_id" {
  value = aws_amplify_app.frontend.id
}

output "amplify_default_domain" {
  value = aws_amplify_app.frontend.default_domain
}

output "mongodb_connection_string" {
  value     = mongodbatlas_cluster.cluster.connection_strings[0].standard
  sensitive = true
}

output "mongodb_cluster_name" {
  value = mongodbatlas_cluster.cluster.name
}

output "environment" {
  value = var.environment
}

output "aws_region" {
  value = data.aws_region.current.name
}
