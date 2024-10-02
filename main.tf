terraform {
  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 4.0"
    }
  }
}

provider "heroku" {
  email   = var.heroku_email
  api_key = var.heroku_api_key
}

resource "heroku_app" "mlops_app" {
  name   = "mlops"
  region = "us"

  config_vars = {
    PYTHON_VERSION = "3.8.12"
  }

  buildpacks = [
    "heroku/python"
  ]
}

resource "heroku_build" "mlops_build" {
  app = heroku_app.mlops_app.id

  source {
    url = var.github_repo_url
  }
}