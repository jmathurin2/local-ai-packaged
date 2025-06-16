# Local AI Packaged - Docker Project Reference

## Project Overview

**Project Name**: `localai`  
**Repository**: `C:\Users\hatia\OneDrive\Documents\GitHub\local-ai-packaged`  
**Docker Compose Project Name**: `localai` (not `local-ai-packaged`)  

⚠️ **IMPORTANT**: Always use the project name `localai` when running docker-compose commands!

## Docker Compose Configuration

### Main Files
- **Primary**: `docker-compose.yml` - Main service definitions
- **Override**: `docker-compose.override.private.yml` - Port mappings and private overrides
- **Network**: `localai_default` - All services run in this network

### Correct Docker Compose Commands

```bash
# Navigate to project directory first
cd "C:\Users\hatia\OneDrive\Documents\GitHub\local-ai-packaged"

# Start all services
docker-compose -p localai -f docker-compose.yml -f docker-compose.override.private.yml up -d

# Start specific service (e.g., n8n)
docker-compose -p localai -f docker-compose.yml -f docker-compose.override.private.yml up -d n8n

# Restart service
docker-compose -p localai -f docker-compose.yml -f docker-compose.override.private.yml restart n8n

# View logs
docker-compose -p localai logs n8n

# Stop all services
docker-compose -p localai down

# Stop specific service
docker-compose -p localai stop n8n
```

## Service Container Names

All containers follow the naming pattern: `{service-name}` or `localai-{service-name}-1`

| Service | Container Name | Ports |
|---------|----------------|---------|
| n8n | `n8n` | 127.0.0.1:5678:5678 |
| n8n-import | `n8n-import` | (helper container) |
| flowise | `flowise` | 127.0.0.1:3001:3001 |
| open-webui | `open-webui` | 127.0.0.1:8080:8080 |
| qdrant | `qdrant` | 127.0.0.1:6333:6333, 127.0.0.1:6334:6334 |
| neo4j | `localai-neo4j-1` | 127.0.0.1:7473:7473, 127.0.0.1:7474:7474, 127.0.0.1:7687:7687 |
| langfuse-web | `localai-langfuse-web-1` | 127.0.0.1:3000:3000 |
| langfuse-worker | `localai-langfuse-worker-1` | 127.0.0.1:3030:3030 |
| postgres | `localai-postgres-1` | 127.0.0.1:5433:5432 |
| clickhouse | `localai-clickhouse-1` | 127.0.0.1:8123:8123, 127.0.0.1:9000:9000, 127.0.0.1:9009:9009 |
| minio | `localai-minio-1` | 127.0.0.1:9010:9000, 127.0.0.1:9011:9001 |
| redis | `redis` | 127.0.0.1:6379:6379 |
| searxng | `searxng` | 127.0.0.1:8081:8080 |
| caddy | `caddy` | 0.0.0.0:80:80, 0.0.0.0:443:443 |
| supabase-analytics | `supabase-analytics` | 0.0.0.0:4000:4000 |
| supabase-db | `supabase-db` | (internal) |
| supabase-imgproxy | `supabase-imgproxy` | (internal) |
| supabase-vector | `supabase-vector` | (internal) |

## Service Access URLs

- **n8n Workflow Automation**: http://localhost:5678
- **Flowise AI Flows**: http://localhost:3001
- **Open WebUI (ChatGPT-like)**: http://localhost:8080
- **Langfuse (LLM Observability)**: http://localhost:3000
- **Neo4j Browser**: http://localhost:7474
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **SearXNG Search**: http://localhost:8081
- **MinIO Console**: http://localhost:9011
- **Supabase Studio**: http://localhost:4000

## Network Information

**Network Name**: `localai_default`  
**Network Type**: bridge  
**Network ID**: Use `docker network ls` to get current ID

## Important Notes

### n8n Configuration
- **Environment Variables Added for Issue Resolution**:
  - `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true` - Automatically fixes file permissions
  - `N8N_RUNNERS_ENABLED=true` - Enables task runners (removes deprecation warning)

### Database Dependencies
- **n8n** depends on **postgres** (`localai-postgres-1`)
- **langfuse** depends on **postgres**, **clickhouse**, **minio**, **redis**
- Always ensure database services are running before dependent services

### Volume Mounts
- `n8n_storage:/home/node/.n8n` - n8n data persistence
- `./n8n/backup:/backup` - n8n backup directory
- `./shared:/data/shared` - Shared data between services

## Troubleshooting Commands

```bash
# Check all running containers
docker ps

# Check all containers (including stopped)
docker ps -a

# Check specific service logs
docker logs n8n
docker logs localai-postgres-1

# Check service health
docker-compose -p localai ps

# Check network connectivity
docker network ls
docker network inspect localai_default

# Restart problematic service
docker-compose -p localai restart n8n

# Force recreate service
docker-compose -p localai up -d --force-recreate n8n
```

## Common Issues and Solutions

### Issue: Container name conflicts
**Solution**: Always use project name `localai` with docker-compose commands

### Issue: Services can't connect to database
**Solution**: Ensure postgres container `localai-postgres-1` is running and healthy

### Issue: Port already in use
**Solution**: Check if services are already running with `docker ps`

### Issue: n8n file permissions warning
**Solution**: Already resolved with `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`

### Issue: Task runners deprecation warning
**Solution**: Already resolved with `N8N_RUNNERS_ENABLED=true`

## Environment Files

Ensure these environment variables are set in your `.env` file:
- `POSTGRES_PASSWORD`
- `N8N_ENCRYPTION_KEY`
- `N8N_USER_MANAGEMENT_JWT_SECRET`
- `FLOWISE_USERNAME` (optional)
- `FLOWISE_PASSWORD` (optional)

## Backup and Recovery

### n8n Backups
- Backup location: `./n8n/backup/`
- Credentials: `./n8n/backup/credentials/`
- Workflows: `./n8n/backup/workflows/`

### Volume Backups
```bash
# Backup n8n data
docker run --rm -v localai_n8n_storage:/data -v $(pwd)/backups:/backup alpine tar czf /backup/n8n_backup_$(date +%Y%m%d).tar.gz -C /data .
```

---

**Last Updated**: $(date)
**Version**: 1.0
**Maintained by**: Local AI Project Team

