variable "mongodb_atlas_public_key" {
  description = "MongoDB Atlas public key"
  type        = string
}

variable "mongodb_atlas_private_key" {
  description = "MongoDB Atlas private key"
  type        = string
}

variable "mongodb_atlas_project_id" {
  description = "MongoDB Atlas project ID"
  type        = string
}

variable "aws_access_key" {
  description = "AWS access key"
  type        = string
}

variable "aws_secret_key" {
  description = "AWS secret key"
  type        = string
}

variable "github_token" {
  description = "GitHub personal access token"
  type        = string
  sensitive   = true
}

variable "environment" {
  description = "Environment (dev/prod)"
  type        = string
  default     = "dev"
}
