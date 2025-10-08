#!/usr/bin/env python3
"""
RTX 5090 Optimized Startup Script for Local AI Package

This script starts the local AI package with RTX 5090 optimized settings.
It automatically uses the gpu-nvidia profile and sets appropriate environment variables.
"""

import subprocess
import sys
import os

def main():
    """Start services optimized for RTX 5090"""
    
    print("🚀 Starting Local AI Package with RTX 5090 optimizations...")
    print("📊 Profile: gpu-nvidia")
    print("🎯 Models: qwen2.5:32b, qwen2.5:7b, llama3.2:70b")
    print("💾 VRAM: Configured for 32GB RTX 5090")
    print()
    
    # Set RTX 5090 optimized environment variables
    env = os.environ.copy()
    env.update({
        'CUDA_VISIBLE_DEVICES': '0',
        'NVIDIA_VISIBLE_DEVICES': '0',
    })
    
    # Determine environment argument (default to private for development)
    environment = "private"
    if "--public" in sys.argv:
        environment = "public"
        print("🔒 Environment: public (production mode)")
    else:
        print("🔓 Environment: private (development mode)")
    
    print()
    print("Starting services...")
    
    try:
        # Run the main startup script with gpu-nvidia profile
        cmd = [sys.executable, "start_services.py", "--profile", "gpu-nvidia", "--environment", environment]
        result = subprocess.run(cmd, env=env, check=True)
        
        print()
        print("✅ Local AI Package started successfully!")
        print()
        print("🌐 Access your services:")
        print("   • n8n Workflows: http://localhost:5678")
        print("   • Open WebUI Chat: http://localhost:8080") 
        print("   • Flowise: http://localhost:3001")
        print("   • Langfuse: http://localhost:3000")
        print("   • Neo4j Browser: http://localhost:7474")
        print()
        print("🤖 RTX 5090 optimized models will be downloaded automatically")
        print("   This may take some time on first run...")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting services: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Startup interrupted by user")
        sys.exit(1)

if __name__ == "__main__":
    main()