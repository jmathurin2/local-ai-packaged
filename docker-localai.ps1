#!/usr/bin/env pwsh
# Local AI Docker Management Script
# Usage: .\docker-localai.ps1 [command] [service]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "restart", "logs", "status", "ps", "down", "up", "help")]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [string]$Service = ""
)

$PROJECT_NAME = "localai"
$PROJECT_DIR = "C:\Users\hatia\OneDrive\Documents\GitHub\local-ai-packaged"
$COMPOSE_FILES = @("-f", "docker-compose.yml", "-f", "docker-compose.override.private.yml")

function Show-Help {
    Write-Host "Local AI Docker Management Script" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\docker-localai.ps1 [command] [service]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Cyan
    Write-Host "  start [service]   - Start all services or specific service"
    Write-Host "  stop [service]    - Stop all services or specific service"
    Write-Host "  restart [service] - Restart all services or specific service"
    Write-Host "  logs [service]    - Show logs for all services or specific service"
    Write-Host "  status            - Show status of all services"
    Write-Host "  ps                - Show running containers"
    Write-Host "  up                - Start all services (alias for start)"
    Write-Host "  down              - Stop and remove all containers"
    Write-Host "  help              - Show this help"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\docker-localai.ps1 start          # Start all services"
    Write-Host "  .\docker-localai.ps1 start n8n      # Start only n8n"
    Write-Host "  .\docker-localai.ps1 logs n8n       # Show n8n logs"
    Write-Host "  .\docker-localai.ps1 restart n8n    # Restart n8n"
    Write-Host "  .\docker-localai.ps1 status         # Show all service status"
    Write-Host ""
    Write-Host "Project Info:" -ForegroundColor Magenta
    Write-Host "  Project Name: $PROJECT_NAME"
    Write-Host "  Project Dir:  $PROJECT_DIR"
    Write-Host "  Network:      ${PROJECT_NAME}_default"
    Write-Host ""
    Write-Host "Services:" -ForegroundColor Magenta
    Write-Host "  n8n, flowise, open-webui, qdrant, neo4j,"
    Write-Host "  langfuse-web, langfuse-worker, postgres,"
    Write-Host "  clickhouse, minio, redis, searxng, caddy"
}

function Invoke-DockerCompose {
    param([string[]]$Arguments)
    
    Push-Location $PROJECT_DIR
    try {
        $fullArgs = @("docker-compose", "-p", $PROJECT_NAME) + $COMPOSE_FILES + $Arguments
        Write-Host "Executing: $($fullArgs -join ' ')" -ForegroundColor Gray
        & $fullArgs[0] $fullArgs[1..($fullArgs.Length-1)]
    }
    finally {
        Pop-Location
    }
}

function Show-ProjectInfo {
    Write-Host "Local AI Project Status" -ForegroundColor Green
    Write-Host "======================" -ForegroundColor Green
    Write-Host "Project Name: $PROJECT_NAME" -ForegroundColor Cyan
    Write-Host "Network: ${PROJECT_NAME}_default" -ForegroundColor Cyan
    Write-Host "Directory: $PROJECT_DIR" -ForegroundColor Cyan
    Write-Host ""
}

# Change to project directory
if (-not (Test-Path $PROJECT_DIR)) {
    Write-Error "Project directory not found: $PROJECT_DIR"
    exit 1
}

switch ($Command) {
    "help" {
        Show-Help
    }
    { $_ -in @("start", "up") } {
        Show-ProjectInfo
        if ($Service) {
            Write-Host "Starting service: $Service" -ForegroundColor Yellow
            Invoke-DockerCompose @("up", "-d", $Service)
        } else {
            Write-Host "Starting all services..." -ForegroundColor Yellow
            Invoke-DockerCompose @("up", "-d")
        }
    }
    "stop" {
        Show-ProjectInfo
        if ($Service) {
            Write-Host "Stopping service: $Service" -ForegroundColor Yellow
            Invoke-DockerCompose @("stop", $Service)
        } else {
            Write-Host "Stopping all services..." -ForegroundColor Yellow
            Invoke-DockerCompose @("stop")
        }
    }
    "restart" {
        Show-ProjectInfo
        if ($Service) {
            Write-Host "Restarting service: $Service" -ForegroundColor Yellow
            Invoke-DockerCompose @("restart", $Service)
        } else {
            Write-Host "Restarting all services..." -ForegroundColor Yellow
            Invoke-DockerCompose @("restart")
        }
    }
    "down" {
        Show-ProjectInfo
        Write-Host "Stopping and removing all containers..." -ForegroundColor Red
        Invoke-DockerCompose @("down")
    }
    "logs" {
        if ($Service) {
            Write-Host "Showing logs for: $Service" -ForegroundColor Yellow
            Invoke-DockerCompose @("logs", "-f", $Service)
        } else {
            Write-Host "Showing logs for all services..." -ForegroundColor Yellow
            Invoke-DockerCompose @("logs", "-f")
        }
    }
    "status" {
        Show-ProjectInfo
        Write-Host "Service Status:" -ForegroundColor Yellow
        Invoke-DockerCompose @("ps")
        Write-Host ""
        Write-Host "Network Status:" -ForegroundColor Yellow
        docker network ls | Where-Object { $_ -match $PROJECT_NAME }
    }
    "ps" {
        Write-Host "Running Containers:" -ForegroundColor Yellow
        docker ps --filter "network=${PROJECT_NAME}_default" --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
    }
    default {
        Write-Error "Unknown command: $Command"
        Show-Help
        exit 1
    }
}

Write-Host ""
Write-Host "Command completed." -ForegroundColor Green

