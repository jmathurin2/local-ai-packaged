# Local AI Packaged - Git Workflow Helper
# Usage: .\git-workflow.ps1 [sync-upstream|new-feature|update-supabase]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("sync-upstream", "new-feature", "update-supabase", "help")]
    [string]$Action,
    [string]$FeatureName = ""
)

function Show-Help {
    Write-Host "Local AI Packaged Git Workflow Helper" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  sync-upstream     - Get latest changes from upstream without affecting your work"
    Write-Host "  new-feature       - Create a new feature branch (requires -FeatureName)"
    Write-Host "  update-supabase   - Update Supabase submodule to latest version"
    Write-Host "  help              - Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\git-workflow.ps1 sync-upstream"
    Write-Host "  .\git-workflow.ps1 new-feature -FeatureName 'my-awesome-feature'"
    Write-Host "  .\git-workflow.ps1 update-supabase"
}

function Sync-Upstream {
    Write-Host "Syncing with upstream..." -ForegroundColor Yellow
    
    # Fetch latest from upstream
    git fetch upstream
    
    # Switch to stable and update it
    git checkout stable
    git merge upstream/stable
    git push origin stable
    
    # Go back to develop and merge stable changes
    git checkout develop
    git merge stable
    
    Write-Host "Upstream sync complete!" -ForegroundColor Green
    Write-Host "Your develop branch now has the latest upstream changes." -ForegroundColor Cyan
}

function New-Feature {
    if ([string]::IsNullOrEmpty($FeatureName)) {
        Write-Host "Feature name is required for new-feature command" -ForegroundColor Red
        Write-Host "Usage: .\git-workflow.ps1 new-feature -FeatureName 'your-feature-name'" -ForegroundColor Yellow
        return
    }
    
    Write-Host "Creating new feature branch: $FeatureName" -ForegroundColor Yellow
    
    # Make sure we're on develop
    git checkout develop
    git pull origin develop
    
    # Create and switch to new feature branch
    $branchName = "feature/$FeatureName"
    git checkout -b $branchName
    
    Write-Host "Feature branch '$branchName' created!" -ForegroundColor Green
    Write-Host "You can now make your changes and commit them." -ForegroundColor Cyan
    Write-Host "When done, run: git push origin $branchName" -ForegroundColor Cyan
}

function Update-Supabase {
    Write-Host "Updating Supabase submodule..." -ForegroundColor Yellow
    
    # Update submodule to latest
    git submodule update --remote supabase
    
    # Stage the submodule update
    git add supabase
    
    Write-Host "Supabase submodule updated!" -ForegroundColor Green
    Write-Host "Do not forget to commit this change: git commit -m 'chore: update Supabase submodule'" -ForegroundColor Cyan
}

switch ($Action) {
    "sync-upstream" { Sync-Upstream }
    "new-feature" { New-Feature }
    "update-supabase" { Update-Supabase }
    "help" { Show-Help }
}

