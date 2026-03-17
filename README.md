# Terraform-Project
This project demonstrates infrastructure-as-code practices using Terraform to automate the deployment and configuration of virtual machines and containerized services.

## Project Overview

It provides a robust framework for building and managing test environments using Terraform. The project leverages the Proxmox virtualization platform to provision QEMU virtual machines and LXC containers in an automated, reproducible manner.

### Purpose

This project serves as a complete infrastructure-as-code solution for:
- Automating VM and container provisioning on Proxmox
- Managing network configurations and resource allocation
- Testing and validating infrastructure deployments in a controlled environment
- Demonstrating Infrastructure-as-Code best practices for lab environments

## Project Structure

```
Terraform-Project/
├── L2-test-env/
│   ├── Provisioner/
│        └── terraform/
│         └── baseline/
│             ├── main.tf              # Primary Terraform configuration
│             ├── variables.tf         # Input variables definition
│             ├── outputs.tf           # Output values definition
│             ├── terraform.tfvars     # Variable values
│             ├── terraform.tfstate    # State file
│             └── .terraform/          # Terraform provider dependencies
└── README.md                          # This file
```

### Key Components

**Terraform Infrastructure (L2-test-env/Provisioner/terraform/baseline):**
- **main.tf** - Core infrastructure configuration using the Telmate Proxmox Terraform provider
- **variables.tf** - Declarative input variables for customizable deployments
- **outputs.tf** - Output values for reference and integration
- **terraform.tfvars** - Variable assignments for the deployment configuration
- **State Files** - Terraform state tracking for infrastructure management

## Getting Started

### Prerequisites
- Terraform >= 1.0
- Proxmox VE installation with API access

### Terraform Infrastructure Setup

1. Clone the repository:
```bash
git clone https://github.com/silvio2804/Terraform-Project.git
cd Terraform-Project/L2-test-env/Provisioner/terraform/baseline
```

2. Initialize Terraform:
```bash
terraform init
```

3. Configure variables in `terraform.tfvars`:
```hcl
# Example configuration
proxmox_url = "https://your-proxmox-server:8006/api2/json"
proxmox_user = "root@pam"
proxmox_password = "your-password"
```

4. Plan the deployment:
```bash
terraform plan
```

5. Apply the configuration:
```bash
terraform apply
```



### Terraform Configuration

#### terraform.tfvars
Contains environment-specific variables such as:
- Proxmox API credentials and endpoints
- VM specifications (CPU, memory, disk)
- Network configurations
- SSH keys for remote access

#### variables.tf
Defines all input variables with:
- Variable names and types
- Default values
- Descriptions and constraints

#### outputs.tf
Exposes computed values for:
- VM IP addresses
- Resource IDs
- Connection information


### Monitor Infrastructure
```bash
# Terraform state
terraform state show
```

### Destroy Infrastructure
Clean up all provisioned resources:
```bash
terraform destroy
```


## Additional Resources

- [Terraform Documentation](https://www.terraform.io/docs/)
- [Proxmox Official Documentation](https://pve.proxmox.com/pve-docs/)
- [Telmate Proxmox Provider Documentation](https://github.com/Telmate/terraform-provider-proxmox)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/overview.html)