# Local AI Packaged - Quick Start

🚀 **Project Name**: `localai`  
📁 **Directory**: `C:\Users\hatia\OneDrive\Documents\GitHub\local-ai-packaged`  
🌐 **Network**: `localai_default`

## Quick Start

### Using the Management Script (Recommended)
```powershell
# Simple alias (shorter)
.\localai.ps1 start        # Start all services
.\localai.ps1 start n8n    # Start specific service
.\localai.ps1 status       # Check status
.\localai.ps1 ps           # Show running containers
.\localai.ps1 logs n8n     # View logs

# Full script (same functionality)
.\docker-localai.ps1 start
.\docker-localai.ps1 help
```

### Manual Commands
```bash
# Always use project name 'localai'
cd "C:\Users\hatia\OneDrive\Documents\GitHub\local-ai-packaged"
docker-compose -p localai -f docker-compose.yml -f docker-compose.override.private.yml up -d
```

## Service URLs
- **n8n**: http://localhost:5678
- **Open WebUI**: http://localhost:8080
- **Flowise**: http://localhost:3001
- **Langfuse**: http://localhost:3000
- **Neo4j**: http://localhost:7474

## Important Files
- 📖 **[DOCKER_PROJECT_REFERENCE.md](DOCKER_PROJECT_REFERENCE.md)** - Complete documentation
- 🔧 **[docker-localai.ps1](docker-localai.ps1)** - Management script
- ⚙️ **docker-compose.yml** - Main configuration
- 🔒 **docker-compose.override.private.yml** - Port mappings

## ⚠️ Critical Rules
1. **Always use project name `localai`** (not `local-ai-packaged`)
2. **Include both compose files** when running manual commands
3. **Check existing containers** before starting new ones

---
*For detailed documentation, see [DOCKER_PROJECT_REFERENCE.md](DOCKER_PROJECT_REFERENCE.md)*

