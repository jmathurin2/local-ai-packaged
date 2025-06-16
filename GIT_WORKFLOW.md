# Git Workflow Guide for Local AI Packaged

This guide explains how to properly manage your fork of the local-ai-packaged repository while keeping it synchronized with upstream updates.

## Repository Structure

- **Upstream**: `https://github.com/coleam00/local-ai-packaged` (original repository)
- **Origin**: `https://github.com/jmathurin2/local-ai-packaged` (your fork)
- **Local**: Your local development environment

## Branch Strategy

- **`stable`**: Clean branch that tracks upstream/stable for getting updates
- **`develop`**: Your main development branch where you do your work
- **`feature/*`**: Feature branches for specific new features or changes

## Quick Commands

Use the included PowerShell script for common operations:

```powershell
# Get latest upstream changes
.\git-workflow.ps1 sync-upstream

# Create a new feature branch
.\git-workflow.ps1 new-feature -FeatureName "my-awesome-feature"

# Update Supabase submodule
.\git-workflow.ps1 update-supabase

# Show help
.\git-workflow.ps1 help
```

## Manual Workflow

### 1. Daily Development

```bash
# Work on your develop branch
git checkout develop

# Create a feature branch for new work
git checkout -b feature/my-new-feature

# Make your changes and commit
git add .
git commit -m "feat: add awesome new feature"

# Push to your fork
git push origin feature/my-new-feature

# When ready, merge back to develop
git checkout develop
git merge feature/my-new-feature
git push origin develop
```

### 2. Getting Upstream Updates

```bash
# Fetch latest from upstream
git fetch upstream

# Update your stable branch
git checkout stable
git merge upstream/stable
git push origin stable

# Merge upstream changes into your develop branch
git checkout develop
git merge stable
```

### 3. Handling Conflicts

If upstream changes conflict with your changes:

1. The merge will stop and show conflicts
2. Edit the conflicted files to resolve issues
3. Stage the resolved files: `git add <file>`
4. Complete the merge: `git commit`

### 4. Submodule Management

The Supabase directory is managed as a Git submodule:

```bash
# Update Supabase to latest version
git submodule update --remote supabase
git add supabase
git commit -m "chore: update Supabase submodule"

# When cloning this repo elsewhere, initialize submodules
git clone --recursive https://github.com/jmathurin2/local-ai-packaged.git
# OR after cloning:
git submodule init
git submodule update
```

## Commit Message Standards

Use conventional commit format:

- `feat: add new feature`
- `fix: resolve bug in component`
- `docs: update README`
- `style: format code`
- `refactor: reorganize functions`
- `test: add unit tests`
- `chore: update dependencies`

## Best Practices

1. **Never work directly on `stable`** - This branch should only track upstream
2. **Always create feature branches** - Don't commit directly to `develop` for significant changes
3. **Sync regularly** - Run sync-upstream weekly or before starting new features
4. **Test before merging** - Ensure your local AI setup still works after changes
5. **Keep commits focused** - One logical change per commit
6. **Write good commit messages** - Future you will thank present you

## Troubleshooting

### Merge Conflicts
If you get merge conflicts during upstream sync:
1. Don't panic! This is normal
2. Open the conflicted files in your editor
3. Look for `<<<<<<<`, `=======`, and `>>>>>>>` markers
4. Keep the changes you want, remove the conflict markers
5. Test that everything still works
6. Commit the resolved conflicts

### Submodule Issues
If Supabase submodule has issues:
```bash
# Reset submodule to tracked version
git submodule deinit supabase
git submodule init
git submodule update
```

### Lost Changes
If you accidentally lose work:
```bash
# Check reflog for recent commits
git reflog

# Recover a lost commit
git checkout <commit-hash>
git cherry-pick <commit-hash>
```

## Getting Help

If you run into issues:
1. Check this guide
2. Use `git status` to see current state
3. Use `git log --oneline -10` to see recent commits
4. Use the helper script: `.\git-workflow.ps1 help`

