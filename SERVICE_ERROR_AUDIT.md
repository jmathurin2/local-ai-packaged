# Service Error Audit Report

**Generated**: 2025-06-14T02:34:09Z  
**Project**: localai  
**Total Services Checked**: 17

## Summary

| Service | Status | Errors Found | Priority |
|---------|--------|--------------|----------|
| n8n | ✅ Running | ✅ None | - |
| flowise | ✅ Running | ✅ None | - |
| open-webui | ⚠️ Issues | ❌ 404 JS/CSS Errors | **Medium** |
| qdrant | ✅ Running | ✅ None | - |
| neo4j | ✅ Running | ✅ None | - |
| langfuse-web | ⚠️ Warnings | ⚠️ Redis Auth Warnings | Low |
| langfuse-worker | ⚠️ Warnings | ⚠️ Redis Auth Warnings | Low |
| postgres | ⚠️ Minor | ⚠️ Connection Resets | Low |
| clickhouse | ✅ Running | ✅ None | - |
| minio | ✅ Running | ✅ None | - |
| redis | ✅ Running | ✅ None | - |
| searxng | ⚠️ Warnings | ⚠️ Missing limiter.toml | Low |
| caddy | ⚠️ Warnings | ⚠️ Format/TLS Warnings | Low |
| supabase-analytics | ✅ Running | ✅ None | - |
| supabase-db | ✅ Running | ✅ None | - |
| supabase-imgproxy | ✅ Running | ✅ None | - |
| supabase-vector | ✅ Running | ✅ None | - |

---

## Detailed Error Analysis

### 1. n8n Service
**Container**: `n8n`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- User settings loaded successfully
- Task Broker ready on port 5679
- JS Task Runner registered successfully
- Editor accessible at http://localhost:5678
```

### 2. Flowise Service
**Container**: `flowise`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- All initialization steps completed successfully
- Server listening on :3001
- All components initialized properly
```

### 3. Open WebUI Service
**Container**: `open-webui`  
**Status**: ⚠️ Running with Issues  
**Logs Analysis**: 
```
❌ ERRORS FOUND:
- Multiple 404 errors for missing JS/CSS files:
  - GET /_app/immutable/chunks/Dhpi6yf_.js HTTP/1.1" 404
  - GET /_app/immutable/entry/app.JP-QuiSN.js HTTP/1.1" 404  
  - GET /_app/immutable/entry/start.BUf7yNPq.js HTTP/1.1" 404

🔍 ANALYSIS: Frontend assets missing, likely version mismatch
📊 IMPACT: UI may be broken or have missing functionality
```

### 4. Qdrant Service
**Container**: `qdrant`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- Qdrant HTTP listening on 6333
- Qdrant gRPC listening on 6334
- Distributed mode disabled (expected for single instance)
- Telemetry enabled
```

### 5. Neo4j Service
**Container**: `localai-neo4j-1`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- Neo4j 2025.05.0 started successfully
- Bolt enabled on 0.0.0.0:7687
- HTTP enabled on 0.0.0.0:7474
- Remote interface available at http://localhost:7474/
```

### 6. Langfuse Web Service
**Container**: `localai-langfuse-web-1`  
**Status**: ⚠️ Running with Warnings  
**Logs Analysis**: 
```
⚠️ WARNINGS FOUND:
- [WARN] Redis server's 'default' user does not require password, but password supplied

✅ Otherwise healthy:
- Next.js server ready
- Database migrations completed
- Ready in 6.3s
```

### 7. Langfuse Worker Service
**Container**: `localai-langfuse-worker-1`  
**Status**: ⚠️ Running with Warnings  
**Logs Analysis**: 
```
⚠️ WARNINGS FOUND:
- Redis connection error: AUTH <password> called without password configured
- [WARN] Redis server's 'default' user does not require password, but password supplied

✅ Otherwise healthy:
- Background migrations completed
- Default model prices upserted
- PostHog and Blob Storage jobs running
```

### 8. PostgreSQL Service
**Container**: `localai-postgres-1`  
**Status**: ⚠️ Running with Minor Issues  
**Logs Analysis**: 
```
⚠️ MINOR ISSUES:
- "could not receive data from client: Connection reset by peer"

✅ Otherwise healthy:
- PostgreSQL 17.5 started successfully
- Database system ready to accept connections
- Checkpoints completing successfully
```

### 9. ClickHouse Service
**Container**: `localai-clickhouse-1`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- Configuration processed successfully
- Database initialization skipped (existing data)
- User 'clickhouse' created
- Logging to /var/log/clickhouse-server/
```

### 10. MinIO Service
**Container**: `localai-minio-1`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- MinIO Object Storage Server running
- API available at http://172.18.0.2:9000
- WebUI available at http://172.18.0.2:9001
- Version: RELEASE.2025-05-24T17-08-30Z
```

### 11. Redis Service
**Container**: `redis`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- Valkey server (Redis-compatible) running
- Graceful shutdown handling works
- No connection issues reported
```

### 12. SearXNG Service
**Container**: `searxng`  
**Status**: ⚠️ Running with Warnings  
**Logs Analysis**: 
```
⚠️ WARNINGS FOUND:
- WARNING: missing config file: /etc/searxng/limiter.toml (repeated 4 times)

✅ Otherwise healthy:
- uWSGI master process spawned
- 4 workers with 4 cores each spawned
- WSGI app ready in 4 seconds
```

### 13. Caddy Service
**Container**: `caddy`  
**Status**: ⚠️ Running with Warnings  
**Logs Analysis**: 
```
⚠️ WARNINGS FOUND:
- Caddyfile input is not formatted; run 'caddy fmt --overwrite'
- Multiple "HTTP/2 skipped because it requires TLS" warnings
- Multiple "HTTP/3 skipped because it requires TLS" warnings

✅ Otherwise healthy:
- 6 servers running on ports 8001, 8002, 8003, 8005, 8007, 8008
- Admin endpoint started on localhost:2019
- TLS cache maintenance started
```

### 14. Supabase Analytics Service
**Container**: `supabase-analytics`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- Regular log processing messages
- "All logs logged!" and "Logs last second!" repeating normally
- Healthy operation
```

### 15. Supabase Database Service
**Container**: `supabase-db`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- Supabase PostgreSQL variant running healthy
- Part of Supabase stack
```

### 16. Supabase Imgproxy Service
**Container**: `supabase-imgproxy`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- Imgproxy service healthy
- No errors in recent logs
```

### 17. Supabase Vector Service
**Container**: `supabase-vector`  
**Status**: ✅ Running  
**Logs Analysis**: 
```
✅ NO ERRORS FOUND
- Vector/Timber.io service healthy
- Log processing pipeline running
```

---

## Missing Services

**Ollama Services**: Not currently running  
- `ollama-cpu` / `ollama-gpu` / `ollama-gpu-amd`
- `ollama-pull-llama-cpu` / `ollama-pull-llama-gpu` / `ollama-pull-llama-gpu-amd`

---

## Action Items

### Medium Priority (Functional Issues)
- [ ] **Fix Open WebUI Frontend Assets (404 Errors)**
  - Issue: Multiple JS/CSS files returning 404 errors
  - Impact: UI may be broken or have missing functionality
  - Files affected: `Dhpi6yf_.js`, `app.JP-QuiSN.js`, `start.BUf7yNPq.js`
  - Suggested fix: Update Open WebUI image or rebuild frontend assets

### Low Priority (Configuration Warnings)
- [ ] **Fix Redis Authentication Configuration**
  - Issue: Langfuse services warning about Redis password when none required
  - Services affected: `langfuse-web`, `langfuse-worker`
  - Suggested fix: Update Redis configuration or remove password from Langfuse config

- [ ] **Add SearXNG Limiter Configuration**
  - Issue: Missing `/etc/searxng/limiter.toml` config file
  - Service affected: `searxng`
  - Suggested fix: Create limiter.toml configuration file or disable limiter warnings

- [ ] **Format Caddyfile and Configure TLS**
  - Issue: Caddyfile formatting warnings and TLS warnings
  - Service affected: `caddy`
  - Suggested fix: Run `caddy fmt --overwrite` and consider TLS configuration

- [ ] **Investigate PostgreSQL Connection Resets**
  - Issue: Occasional "Connection reset by peer" messages
  - Service affected: `postgres`
  - Suggested fix: Monitor for patterns, may be normal client disconnections

### Future Considerations
- [ ] **Start Ollama Services (if needed)**
  - Missing: All Ollama-related services
  - Decision needed: Whether local LLM serving is required

---

## Overall Health Status

**🎯 Summary**: 
- **17 services analyzed**
- **11 services running perfectly** (65%)
- **6 services with minor warnings** (35%)
- **1 service with functional issues** (6%)
- **0 services completely broken**

**✅ Core functionality intact**: All critical services (databases, APIs, web interfaces) are operational.

**🔧 Maintenance needed**: Mostly cosmetic/configuration issues that don't affect core functionality.

---

**Last Updated**: 2025-06-14T02:36:00Z  
**Audit Completed**: ✅ Yes  
**Next Review**: Recommend after fixing Medium priority issues

