terraform {
  backend "s3" {
    bucket         = "salma-terraform-backend"
    key            = "env/dev/terraform.tfstate"
    region         = "us-east-1"
    use_lockfile   = true
  }
}