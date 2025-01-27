# Terraform Infrastructure Configuration

This directory contains Terraform configurations to manage the infrastructure for the fullstack developer capstone project. It handles the deployment of:

- AWS Amplify for the React frontend
- MongoDB Atlas for the database
- Associated AWS services and configurations

## Prerequisites

1. [Terraform](https://www.terraform.io/downloads.html) installed (v1.0.0+)
2. AWS Account and credentials
3. MongoDB Atlas account and API keys
4. GitHub personal access token

## Getting Started

1. **Configure Credentials**:
   - Copy `terraform.tfvars.example` to `terraform.tfvars`
   - Fill in your credentials and configuration values in `terraform.tfvars`

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```

3. **Review the Plan**:
   ```bash
   terraform plan
   ```

4. **Apply Configuration**:
   ```bash
   terraform apply
   ```

## Important Notes

- Keep your `terraform.tfvars` file secure and never commit it to version control
- The MongoDB Atlas M0 cluster is free tier but has limitations
- AWS Amplify will automatically build and deploy your frontend when you push to the configured branch

## Infrastructure Components

- **AWS Amplify**: Hosts and deploys the React frontend
- **MongoDB Atlas**: Manages the MongoDB database
- **AWS Region**: Default is us-east-1, can be changed in variables
- **Environment Variables**: Configured for both development and production

## Destroying Infrastructure

To tear down the infrastructure:
```bash
terraform destroy
```

**Warning**: This will destroy all resources managed by Terraform. Make sure to backup any important data before running this command.

## Variables Reference

| Variable | Description |
|----------|-------------|
| aws_access_key | AWS Access Key |
| aws_secret_key | AWS Secret Key |
| mongodb_atlas_public_key | MongoDB Atlas Public Key |
| mongodb_atlas_private_key | MongoDB Atlas Private Key |
| mongodb_atlas_project_id | MongoDB Atlas Project ID |
| github_token | GitHub Personal Access Token |
| environment | Environment (dev/prod) |

## Outputs

- `amplify_app_id`: ID of the created Amplify app
- `amplify_default_domain`: Default domain for the Amplify app
- `mongodb_connection_string`: MongoDB connection string (sensitive)
- `mongodb_cluster_name`: Name of the MongoDB cluster
- `environment`: Current environment
- `aws_region`: AWS region being used
