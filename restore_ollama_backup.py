#!/usr/bin/env python3
"""
Ollama Backup Restoration Script

This script helps restore Ollama models from a backup directory.
Designed for use with RTX 5090 optimized Local AI Package.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def main():
    """Restore Ollama models from backup"""
    
    print("🔄 Ollama Backup Restoration Tool")
    print("=" * 50)
    
    # Default backup path from user's context
    default_backup_path = "E:\\docker-backups\\backup_20250930_101628"
    
    print(f"📂 Default backup location: {default_backup_path}")
    print()
    
    # Ask user for backup path
    backup_path = input(f"Enter backup path (or press Enter for default): ").strip()
    if not backup_path:
        backup_path = default_backup_path
    
    # Validate backup path exists
    if not os.path.exists(backup_path):
        print(f"❌ Error: Backup path does not exist: {backup_path}")
        sys.exit(1)
    
    print(f"✅ Using backup path: {backup_path}")
    print()
    
    # Check if Docker is running
    print("🔍 Checking Docker status...")
    try:
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True, check=True)
        print("✅ Docker is running")
    except subprocess.CalledProcessError:
        print("❌ Docker is not running. Please start Docker first.")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Docker command not found. Please install Docker.")
        sys.exit(1)
    
    print()
    
    # Check if localai containers are running
    print("🔍 Checking Local AI containers...")
    try:
        result = subprocess.run(["docker", "ps", "--filter", "name=ollama", "--format", "{{.Names}}"], 
                              capture_output=True, text=True, check=True)
        if "ollama" in result.stdout:
            print("🛑 Ollama container is running. Please stop Local AI services first.")
            print("   Run: docker-compose -p localai down")
            response = input("Stop containers now? (y/n): ").strip().lower()
            if response == 'y':
                print("🛑 Stopping containers...")
                subprocess.run(["docker-compose", "-p", "localai", "down"], check=True)
                print("✅ Containers stopped")
            else:
                print("❌ Cannot restore while containers are running.")
                sys.exit(1)
        else:
            print("✅ Ollama container is not running")
    except subprocess.CalledProcessError:
        print("⚠️  Could not check container status")
    
    print()
    
    # Method selection
    print("🔧 Restoration Methods:")
    print("1. Volume restore (recommended for complete backup)")
    print("2. Directory copy (if backup contains .ollama directory)")
    print("3. Model import (if backup contains individual model files)")
    print()
    
    method = input("Select method (1-3): ").strip()
    
    if method == "1":
        restore_volume(backup_path)
    elif method == "2":
        restore_directory(backup_path)
    elif method == "3":
        restore_models(backup_path)
    else:
        print("❌ Invalid selection")
        sys.exit(1)

def restore_volume(backup_path):
    """Restore from volume backup"""
    print("📦 Volume Restore Method")
    print("-" * 30)
    
    # Look for volume backup files
    backup_files = list(Path(backup_path).glob("*ollama*.tar.gz"))
    backup_files.extend(list(Path(backup_path).glob("*ollama*.tar")))
    
    if not backup_files:
        print("❌ No Ollama volume backup files found")
        print("   Looking for files like: *ollama*.tar.gz or *ollama*.tar")
        return
    
    print(f"📁 Found backup files:")
    for i, file in enumerate(backup_files, 1):
        print(f"   {i}. {file.name}")
    
    if len(backup_files) == 1:
        selected_file = backup_files[0]
    else:
        selection = input("Select backup file number: ").strip()
        try:
            selected_file = backup_files[int(selection) - 1]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
    
    print(f"🔄 Restoring from: {selected_file}")
    
    try:
        # Create volume if it doesn't exist and restore
        cmd = [
            "docker", "run", "--rm",
            "-v", "localai_ollama_storage:/data",
            "-v", f"{selected_file.parent}:/backup",
            "alpine",
            "tar", "xzf", f"/backup/{selected_file.name}", "-C", "/data"
        ]
        
        subprocess.run(cmd, check=True)
        print("✅ Volume restore completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Volume restore failed: {e}")

def restore_directory(backup_path):
    """Restore from .ollama directory backup"""
    print("📁 Directory Restore Method")
    print("-" * 30)
    
    ollama_dirs = list(Path(backup_path).glob("**/.ollama"))
    ollama_dirs.extend(list(Path(backup_path).glob("**/ollama")))
    
    if not ollama_dirs:
        print("❌ No .ollama directories found in backup")
        return
    
    print(f"📁 Found Ollama directories:")
    for i, dir_path in enumerate(ollama_dirs, 1):
        print(f"   {i}. {dir_path}")
    
    if len(ollama_dirs) == 1:
        selected_dir = ollama_dirs[0]
    else:
        selection = input("Select directory number: ").strip()
        try:
            selected_dir = ollama_dirs[int(selection) - 1]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
    
    print(f"🔄 Copying from: {selected_dir}")
    
    try:
        # Copy directory contents to volume
        cmd = [
            "docker", "run", "--rm",
            "-v", "localai_ollama_storage:/data",
            "-v", f"{selected_dir}:/backup:ro",
            "alpine",
            "cp", "-r", "/backup/.", "/data/"
        ]
        
        subprocess.run(cmd, check=True)
        print("✅ Directory restore completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Directory restore failed: {e}")

def restore_models(backup_path):
    """Restore individual model files"""
    print("🤖 Model Import Method")
    print("-" * 30)
    print("⚠️  This method requires manual Ollama commands")
    print("    Start Local AI services first, then use:")
    print(f"    ollama create <model-name> -f {backup_path}/<modelfile>")
    print()
    print("📋 Available for RTX 5090:")
    print("   • qwen2.5:32b-instruct-q4_K_M (recommended)")
    print("   • qwen2.5:7b-instruct-q4_K_M (fast)")
    print("   • Any other models in your backup")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Restoration cancelled by user")
        sys.exit(1)