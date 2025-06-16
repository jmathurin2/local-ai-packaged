#!/usr/bin/env python3
"""
start_with_updates.py

Wrapper script that checks for updates before starting services.
"""

import sys
import os
import subprocess
from pathlib import Path

def check_and_update_services():
    """Check for service updates and optionally apply them."""
    try:
        from update_services import check_service_updates
        
        print("Checking for service updates...")
        results = check_service_updates()
        
        updates_available = any(result.get('update_available', False) for result in results.values())
        
        if updates_available:
            print("\nUpdates available! Would you like to update services before starting? (y/n)")
            choice = input().strip().lower()
            
            if choice in ['y', 'yes']:
                print("\nUpdating services...")
                subprocess.run([sys.executable, "update_services.py", "--update"])
                print("\nServices updated! Continuing with startup...\n")
            else:
                print("\nSkipping updates. You can update later with: python update_services.py --update\n")
        else:
            print("All services are up to date.\n")
            
    except ImportError:
        print("Update checking not available. Continuing with startup...\n")
    except Exception as e:
        print(f"Error checking for updates: {e}. Continuing with startup...\n")

def main():
    # Check for updates first
    if "--skip-update-check" not in sys.argv:
        check_and_update_services()
    
    # Remove our custom argument before passing to start_services.py
    args = [arg for arg in sys.argv[1:] if arg != "--skip-update-check"]
    
    # Run the original start_services.py with remaining arguments
    cmd = [sys.executable, "start_services.py"] + args
    print(f"Starting services with: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting services: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

