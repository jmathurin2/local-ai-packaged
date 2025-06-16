#!/usr/bin/env pwsh
# Simple alias for docker-localai.ps1
# Usage: .\localai.ps1 [command] [service]

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$Command = "help",
    
    [Parameter(Mandatory=$false, Position=1)]
    [string]$Service = ""
)

$scriptPath = Join-Path $PSScriptRoot "docker-localai.ps1"

if (Test-Path $scriptPath) {
    if ($Service) {
        & $scriptPath $Command $Service
    } else {
        & $scriptPath $Command
    }
} else {
    Write-Error "docker-localai.ps1 not found in $PSScriptRoot"
}

