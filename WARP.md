# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**local-ai-packaged** is a self-hosted AI platform that orchestrates multiple AI services via Docker Compose. It combines n8n workflow automation, Open WebUI for chat interfaces, Ollama for local LLMs, Supabase for database/auth, and additional services like Flowise, Neo4j, Langfuse, and SearXNG into a unified local AI development environment.

## Core Architecture

### Multi-Service Docker Stack
- **Project Name**: `localai` (used in all docker-compose commands)
- **Network**: `localai_default` - all services communicate within this network
- **Compose Strategy**: Main `docker-compose.yml` + environment-specific overrides
- **Volume Management**: Persistent storage for n8n workflows, Ollama models, databases

### Service Dependencies & Communication
```
n8n ── depends on ──→ postgres (localai-postgres-1)
langfuse ── depends on ──→ postgres + clickhouse + minio + redis
ollama ← connects to ← n8n (via internal hostname 'ollama:11434')
open-webui ← integrates ← n8n (via webhook + n8n_pipe.py function)
```

### GPU Profile Architecture
The system supports different hardware configurations via Docker Compose profiles:
- `cpu`: Software-only inference
- `gpu-nvidia`: NVIDIA GPU acceleration
- `gpu-amd`: AMD GPU with ROCm support  
- `none`: External Ollama (e.g., Mac M1 running Ollama locally)

## Essential Development Commands

### Service Management
```bash
# RTX 5090 optimized startup (recommended for RTX 5090 users)
python start_rtx5090.py

# Standard profiles (replace gpu-amd with your profile)
python start_services.py --profile gpu-nvidia  # RTX 5090/other NVIDIA GPUs
python start_services.py --profile gpu-amd     # AMD GPUs
python start_services.py --profile cpu         # CPU only

# Environment options
python start_services.py --profile gpu-nvidia --environment private  # Development
python start_services.py --profile gpu-nvidia --environment public   # Production
```

### Direct Docker Compose Operations
```bash
# Always use project name 'localai' and include override files
cd /path/to/local-ai-packaged

# Start all services
docker-compose -p localai -f docker-compose.yml -f docker-compose.override.private.yml --profile gpu-amd up -d

# Restart specific service
docker-compose -p localai restart n8n

# View service logs
docker-compose -p localai logs -f n8n

# Stop all services
docker-compose -p localai down

# Force recreate service
docker-compose -p localai up -d --force-recreate n8n
```

### Service Status & Debugging
```bash
# Check running containers
docker ps

# Check service health
docker-compose -p localai ps

# Check network connectivity
docker network inspect localai_default

# Database connection test
docker exec -it localai-postgres-1 pg_isready -U postgres
```

## Environment Setup

### Critical Environment Variables (.env file)
```bash
# N8N (required)
N8N_ENCRYPTION_KEY=<generate with `openssl rand -hex 32`>
N8N_USER_MANAGEMENT_JWT_SECRET=<generate with `openssl rand -hex 32`>

# Supabase/Database (required)  
POSTGRES_PASSWORD=<secure password - avoid @ symbol>
JWT_SECRET=<32+ character string>
ANON_KEY=<from Supabase generation>
SERVICE_ROLE_KEY=<from Supabase generation>

# Neo4j (required)
NEO4J_AUTH=neo4j/your_password

# Langfuse (required)
CLICKHOUSE_PASSWORD=<secure password>
MINIO_ROOT_PASSWORD=<secure password>
LANGFUSE_SALT=<secure password>
NEXTAUTH_SECRET=<secure password>
ENCRYPTION_KEY=<generate with `openssl rand -hex 32`>

# Production hostnames (optional - for public deployment)
N8N_HOSTNAME=n8n.yourdomain.com
WEBUI_HOSTNAME=openwebui.yourdomain.com
# ... other service hostnames
```

## Service Integration Patterns

### N8N ↔ Open WebUI Integration
1. **n8n_pipe.py**: Python function that bridges Open WebUI to n8n webhooks
2. **Workflow Setup**: Import included n8n workflows, create webhook URLs  
3. **Open WebUI Function**: Install n8n_pipe.py as custom function, configure webhook URL
4. **Credential Management**: Configure n8n with Ollama (`ollama:11434`), Qdrant (`qdrant:6333`), Postgres (`db:5432`)

### File System Integration
- **Shared Directory**: `./shared` → `/data/shared` (inside n8n container)
- **N8N Backups**: `./n8n/backup/` contains workflows and credentials
- **Persistent Volumes**: `n8n_storage`, `ollama_storage`, `qdrant_storage` for data retention

## Container & Network References

### Key Service URLs (Private Mode)
- n8n: http://localhost:5678
- Open WebUI: http://localhost:8080  
- Flowise: http://localhost:3001
- Langfuse: http://localhost:3000
- Neo4j Browser: http://localhost:7474
- Supabase Studio: http://localhost:4000

### Container Naming Pattern
- Simple services: `{service-name}` (e.g., `n8n`, `ollama`)
- Complex services: `localai-{service-name}-1` (e.g., `localai-postgres-1`)

## Upgrade & Maintenance

### Container Updates
```bash
# Stop services
docker-compose -p localai down

# Pull latest images
docker-compose -p localai pull

# Restart with updates
python start_services.py --profile <your-profile>
```

### Data Backup
```bash
# Backup n8n data
docker run --rm -v localai_n8n_storage:/data -v $(pwd)/backups:/backup alpine tar czf /backup/n8n_backup_$(date +%Y%m%d).tar.gz -C /data .
```

## Common Issues & Solutions

### Database Connection Errors
- Verify `localai-postgres-1` container is running and healthy
- Check password doesn't contain '@' symbol (complicates connection strings)
- Ensure n8n credentials use `db` as hostname (not `localhost`)

### Port Conflicts
- Check existing services: `docker ps`
- Private mode exposes many ports; public mode only exposes 80/443

### GPU Support Issues
- NVIDIA: Ensure Docker has GPU support enabled
- AMD: Verify `/dev/kfd` and `/dev/dri` device access
- Windows: Enable WSL2 backend in Docker Desktop

### File Permission Errors
- Already resolved via `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`
- For manual fixes: `sudo chown -R 1000:1000 ./shared`

## References

Reference the `DOCKER_PROJECT_REFERENCE.md` file for detailed container management and troubleshooting when starting, stopping, or restarting local-ai-packaged containers.