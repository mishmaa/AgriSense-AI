Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path ".env.production")) {
  throw "Create .env.production from .env.production.example before production deployment."
}

docker compose -f docker-compose.prod.yml up --build -d
