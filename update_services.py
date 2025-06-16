#!/usr/bin/env python3
"""
update_services.py

This script checks for the latest versions of services and optionally updates
the docker-compose.yml file with new versions.
"""

import os
import re
import json
import subprocess
import argparse
import requests
from typing import Dict, Optional, Tuple
from packaging import version

# Service configuration with GitHub repo info
SERVICE_CONFIGS = {
    "open-webui": {
        "github_repo": "open-webui/open-webui",
        "image_name": "ghcr.io/open-webui/open-webui",
        "current_pattern": r"image: ghcr\.io/open-webui/open-webui:([\w\.-]+)",
        "compose_line_pattern": r"(\s+image: ghcr\.io/open-webui/open-webui:)[\w\.-]+"
    },
    "n8n": {
        "github_repo": "n8n-io/n8n", 
        "image_name": "n8nio/n8n",
        "current_pattern": r"image: n8nio/n8n:([\w\.-]+)",
        "compose_line_pattern": r"(\s+image: n8nio/n8n:)[\w\.-]+"
    },
    "flowise": {
        "github_repo": "FlowiseAI/Flowise",
        "image_name": "flowiseai/flowise",
        "current_pattern": r"image: flowiseai/flowise:?([\w\.-]*)",
        "compose_line_pattern": r"(\s+image: flowiseai/flowise):?[\w\.-]*"
    },
    "qdrant": {
        "github_repo": "qdrant/qdrant",
        "image_name": "qdrant/qdrant",
        "current_pattern": r"image: qdrant/qdrant:?([\w\.-]*)", 
        "compose_line_pattern": r"(\s+image: qdrant/qdrant):?[\w\.-]*"
    },
    "neo4j": {
        "github_repo": "neo4j/neo4j",
        "image_name": "neo4j",
        "current_pattern": r"image: neo4j:([\w\.-]+)",
        "compose_line_pattern": r"(\s+image: neo4j:)[\w\.-]+"
    },
    "langfuse": {
        "github_repo": "langfuse/langfuse",
        "image_name": "langfuse/langfuse",
        "current_pattern": r"image: langfuse/langfuse:([\w\.-]+)",
        "compose_line_pattern": r"(\s+image: langfuse/langfuse:)[\w\.-]+"
    },
    "langfuse-worker": {
        "github_repo": "langfuse/langfuse",
        "image_name": "langfuse/langfuse-worker", 
        "current_pattern": r"image: langfuse/langfuse-worker:([\w\.-]+)",
        "compose_line_pattern": r"(\s+image: langfuse/langfuse-worker:)[\w\.-]+"
    }
}

def get_latest_github_release(repo: str) -> Optional[str]:
    """Get the latest release version from GitHub API."""
    try:
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        tag_name = data.get('tag_name', '')
        
        # Remove 'v' prefix if present
        if tag_name.startswith('v'):
            return tag_name[1:]
        return tag_name
        
    except Exception as e:
        print(f"Error fetching latest release for {repo}: {e}")
        return None

def get_current_version_from_compose(service_name: str) -> Optional[str]:
    """Extract current version from docker-compose.yml."""
    compose_file = "docker-compose.yml"
    if not os.path.exists(compose_file):
        print(f"Docker compose file not found: {compose_file}")
        return None
        
    config = SERVICE_CONFIGS.get(service_name)
    if not config:
        print(f"Service {service_name} not configured")
        return None
        
    try:
        with open(compose_file, 'r') as f:
            content = f.read()
            
        pattern = config['current_pattern']
        match = re.search(pattern, content)
        
        if match:
            current_version = match.group(1)
            # Handle case where no version tag is specified (latest)
            if not current_version:
                return "latest"
            return current_version
        else:
            print(f"Could not find current version for {service_name}")
            return None
            
    except Exception as e:
        print(f"Error reading docker-compose.yml: {e}")
        return None

def update_service_version(service_name: str, new_version: str) -> bool:
    """Update service version in docker-compose.yml."""
    compose_file = "docker-compose.yml"
    config = SERVICE_CONFIGS.get(service_name)
    
    if not config:
        print(f"Service {service_name} not configured")
        return False
        
    try:
        with open(compose_file, 'r') as f:
            content = f.read()
            
        # Use the compose line pattern for replacement
        pattern = config['compose_line_pattern']
        
        # Handle special case for services that might not have version tags
        if service_name in ["flowise", "qdrant"] and new_version != "latest":
            replacement = rf"\g<1>:{new_version}"
        else:
            replacement = rf"\g<1>{new_version}"
            
        new_content = re.sub(pattern, replacement, content)
        
        if new_content == content:
            print(f"No changes made for {service_name} (pattern might not match)")
            return False
            
        with open(compose_file, 'w') as f:
            f.write(new_content)
            
        print(f"✅ Updated {service_name} to version {new_version}")
        return True
        
    except Exception as e:
        print(f"Error updating {service_name}: {e}")
        return False

def check_service_updates() -> Dict[str, Dict[str, str]]:
    """Check all services for available updates."""
    results = {}
    
    print("🔍 Checking for service updates...\n")
    
    for service_name, config in SERVICE_CONFIGS.items():
        print(f"Checking {service_name}...")
        
        current_version = get_current_version_from_compose(service_name)
        latest_version = get_latest_github_release(config['github_repo'])
        
        if current_version and latest_version:
            try:
                # Compare versions (handle 'latest' special case)
                if current_version == "latest":
                    update_available = True
                    status = "using 'latest' tag"
                elif current_version == latest_version:
                    update_available = False
                    status = "up to date"
                else:
                    # Use semantic versioning comparison
                    current_v = version.parse(current_version)
                    latest_v = version.parse(latest_version)
                    update_available = latest_v > current_v
                    status = "update available" if update_available else "up to date"
                    
            except Exception:
                # Fallback to string comparison if version parsing fails
                update_available = current_version != latest_version
                status = "version comparison failed"
                
            results[service_name] = {
                "current": current_version,
                "latest": latest_version,
                "update_available": update_available,
                "status": status
            }
            
            status_icon = "🆕" if update_available else "✅"
            print(f"  {status_icon} Current: {current_version}, Latest: {latest_version} ({status})")
        else:
            results[service_name] = {
                "current": current_version,
                "latest": latest_version, 
                "update_available": False,
                "status": "error checking versions"
            }
            print(f"  ❌ Error checking versions")
            
        print()
        
    return results

def update_start_services_script():
    """Modify start_services.py to include update checking."""
    script_path = "start_services.py"
    if not os.path.exists(script_path):
        print(f"start_services.py not found")
        return False
        
    try:
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check if update functionality is already added
        if "check_for_updates" in content:
            print("✅ Update checking already integrated in start_services.py")
            return True
            
        # Add import for update_services
        import_addition = """import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from update_services import check_service_updates
except ImportError:
    check_service_updates = None
"""
        
        # Add the import after existing imports
        import_pattern = r"(import argparse\s*\n)"
        new_content = re.sub(import_pattern, f"\\1{import_addition}\n", content)
        
        # Add update check function
        update_function = '''def check_for_updates():
    """Check for service updates before starting."""
    if check_service_updates:
        print("🔍 Checking for service updates...")
        results = check_service_updates()
        
        updates_available = any(result.get('update_available', False) for result in results.values())
        
        if updates_available:
            print("\\n🆕 Updates available! Run 'python update_services.py --update' to update services.")
            print("Or add --skip-update-check to skip this check.\\n")
        else:
            print("✅ All services are up to date.\\n")
    else:
        print("⚠️ Update checking not available (update_services.py not found)\\n")

'''
        
        # Add the function before main()
        main_pattern = r"(def main\(\):)"
        new_content = re.sub(main_pattern, f"{update_function}\\1", new_content)
        
        # Add update check argument
        arg_pattern = r"(parser\.add_argument\('--environment'[^\)]+\))"
        new_arg = "\n    parser.add_argument('--skip-update-check', action='store_true',\n                      help='Skip checking for service updates')"
        new_content = re.sub(arg_pattern, f"\\1{new_arg}", new_content)
        
        # Add update check call in main
        main_call_pattern = r"(\s+)(clone_supabase_repo\(\))"
        update_call = "\\1if not args.skip_update_check:\\1    check_for_updates()\\1\\1\\2"
        new_content = re.sub(main_call_pattern, update_call, new_content)
        
        with open(script_path, 'w') as f:
            f.write(new_content)
            
        print("✅ Added update checking to start_services.py")
        return True
        
    except Exception as e:
        print(f"Error updating start_services.py: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Check and update service versions')
    parser.add_argument('--check', action='store_true', help='Check for updates without applying them')
    parser.add_argument('--update', action='store_true', help='Update services to latest versions')
    parser.add_argument('--service', help='Update specific service only')
    parser.add_argument('--integrate', action='store_true', help='Integrate update checking into start_services.py')
    
    args = parser.parse_args()
    
    if args.integrate:
        update_start_services_script()
        return
        
    results = check_service_updates()
    
    if args.update:
        print("\n🔄 Updating services...\n")
        
        services_to_update = [args.service] if args.service else results.keys()
        
        updated_services = []
        for service_name in services_to_update:
            if service_name not in results:
                print(f"❌ Unknown service: {service_name}")
                continue
                
            result = results[service_name]
            if result.get('update_available', False) and result.get('latest'):
                if update_service_version(service_name, result['latest']):
                    updated_services.append(service_name)
            else:
                print(f"⏭️ {service_name} is already up to date")
                
        if updated_services:
            print(f"\n✅ Updated services: {', '.join(updated_services)}")
            print("\n🔄 You may want to restart services to use the new versions:")
            print("   python start_services.py --skip-update-check")
        else:
            print("\n✅ No updates applied")
            
    elif not args.check:
        # Default behavior - show summary
        print("\n📊 Update Summary:")
        print("=" * 50)
        
        updates_available = 0
        up_to_date = 0
        errors = 0
        
        for service_name, result in results.items():
            if result.get('update_available', False):
                updates_available += 1
                print(f"🆕 {service_name}: {result.get('current', 'unknown')} → {result.get('latest', 'unknown')}")
            elif result.get('latest'):
                up_to_date += 1
            else:
                errors += 1
                
        print(f"\n📈 Stats: {updates_available} updates available, {up_to_date} up to date, {errors} errors")
        
        if updates_available > 0:
            print(f"\n💡 Run 'python update_services.py --update' to update all services")
            print(f"💡 Run 'python update_services.py --update --service SERVICE_NAME' to update specific service")

if __name__ == "__main__":
    main()

