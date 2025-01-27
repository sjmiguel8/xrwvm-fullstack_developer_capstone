# AWS Provider configuration
provider "aws" {
  region = "us-east-1"  # Change this to your preferred region
}

# Amplify App
resource "aws_amplify_app" "frontend" {
  name                     = "fullstack-capstone"
  repository              = "https://github.com/YOUR_USERNAME/xrwvm-fullstack_developer_capstone"  
  enable_branch_auto_build = true

  # Build settings
  build_spec = <<-EOT
    version: 1
    frontend:
      phases:
        preBuild:
          commands:
            - cd server/frontend
            - npm install
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: server/frontend/build
        files:
          - '**/*'
      cache:
        paths:
          - node_modules/**/*
  EOT

  # Environment variables
  environment_variables = {
    ENV = "prod"
  }
}

# MongoDB Atlas Provider (requires setup)
provider "mongodbatlas" {
  public_key  = var.mongodb_atlas_public_key
  private_key = var.mongodb_atlas_private_key
}

# MongoDB Atlas Cluster
resource "mongodbatlas_cluster" "cluster" {
  project_id = var.mongodb_atlas_project_id
  name       = "capstone-cluster"

  provider_name               = "AWS"
  provider_region_name       = "US_EAST_1"
  provider_instance_size_name = "M0"  # Free tier
  
  mongo_db_major_version     = "5.0"
  auto_scaling_disk_gb_enabled = false
}
