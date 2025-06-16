# Automated Service Update System

🚀 **Local AI Packaged** now includes an automated update system that keeps your services up-to-date with the latest releases from GitHub.

## 🎯 **What's Updated**

### ✅ **Open WebUI Updated to v0.6.15**
The latest stable release with improved features and bug fixes.

### 🔄 **Automated Update Checking for:**
- **Open WebUI** - GitHub: `open-webui/open-webui`
- **n8n** - GitHub: `n8n-io/n8n`  
- **Flowise** - GitHub: `FlowiseAI/Flowise`
- **Qdrant** - GitHub: `qdrant/qdrant`
- **Neo4j** - GitHub: `neo4j/neo4j`
- **Langfuse** - GitHub: `langfuse/langfuse`
- **Langfuse Worker** - GitHub: `langfuse/langfuse`

## 📋 **How to Use**

### **Option 1: Manual Update Checking**

```bash
# Check for updates without applying them
python update_services.py --check

# Check and show summary (default)
python update_services.py

# Update all services to latest versions
python update_services.py --update

# Update specific service only
python update_services.py --update --service open-webui
```

### **Option 2: Automatic Update Checking on Startup**

```bash
# Start services with automatic update checking
python start_with_updates.py

# Start with specific profile and update checking
python start_with_updates.py --profile gpu-nvidia

# Skip update check
python start_with_updates.py --skip-update-check
```

### **Option 3: Traditional Startup (No Update Checking)**

```bash
# Original method - no update checking
python start_services.py
```

## 🛠️ **Update System Features**

### **🔍 Version Detection**
- Automatically detects current service versions from `docker-compose.yml`
- Fetches latest versions from GitHub releases API
- Uses semantic versioning comparison when possible
- Handles special cases like `:latest` tags

### **📊 Status Reporting**
- ✅ **Up to date** - Service is running latest version
- 🆕 **Update available** - Newer version found on GitHub
- ⚠️ **Using 'latest' tag** - Pinned version recommended
- ❌ **Error** - Unable to check versions

### **🎯 Smart Updates**
- Updates `docker-compose.yml` with new version tags
- Preserves original file formatting
- Validates changes before applying
- Shows clear success/failure messages

## 📋 **Example Output**

```
🔍 Checking for service updates...

Checking open-webui...
  ✅ Current: v0.6.15, Latest: 0.6.15 (up to date)

Checking n8n...
  🆕 Current: latest, Latest: n8n@1.98.1 (using 'latest' tag)

Checking flowise...
  🆕 Current: latest, Latest: flowise@3.0.2 (using 'latest' tag)

Checking langfuse...
  🆕 Current: 3, Latest: 3.71.0 (update available)

📊 Update Summary:
==================================================
🆕 n8n: latest → n8n@1.98.1
🆕 flowise: latest → flowise@3.0.2
🆕 langfuse: 3 → 3.71.0
🆕 langfuse-worker: 3 → 3.71.0

📈 Stats: 4 updates available, 1 up to date, 0 errors

💡 Run 'python update_services.py --update' to update all services
```

## ⚙️ **Configuration**

### **Dependencies**
Install required packages:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install requests packaging
```

### **Service Configuration**
Services are configured in `update_services.py` with:
- GitHub repository paths
- Docker image names  
- Regex patterns for version detection
- Update replacement patterns

## 🔄 **Workflow Integration**

### **Recommended Workflow:**
1. **Check for updates**: `python start_with_updates.py`
2. **Review changes**: The script will show available updates
3. **Choose to update**: Answer 'y' to update before starting
4. **Services restart**: Updated services will use new versions

### **CI/CD Integration:**
```bash
# In your CI/CD pipeline
python update_services.py --update
python start_services.py --skip-update-check
```

## 🛡️ **Safety Features**

### **Non-Destructive**
- Never deletes or overwrites data volumes
- Only updates version tags in `docker-compose.yml`
- Preserves all configuration and environment variables

### **Rollback Support**
- Git track changes to `docker-compose.yml`
- Easy rollback with `git checkout docker-compose.yml`
- Manual version pinning always possible

### **Error Handling**
- Graceful failure if GitHub API is unavailable
- Continues with startup even if update check fails
- Clear error messages for troubleshooting

## 📁 **Files Added**

- 📄 **`update_services.py`** - Main update checking script
- 📄 **`start_with_updates.py`** - Startup wrapper with update checking
- 📄 **`requirements.txt`** - Python dependencies
- 📄 **`UPDATE_SYSTEM.md`** - This documentation

## 🎯 **Benefits**

### **🔒 Security**
- Stay current with security patches
- Automatic notification of available updates
- Latest bug fixes and stability improvements

### **🚀 Performance**
- Access to performance improvements
- New features and capabilities
- Better resource utilization

### **🛠️ Maintenance**
- Automated version tracking
- Consistent update process
- Reduced manual configuration errors

---

## 🆘 **Troubleshooting**

### **Update Check Fails**
```bash
# Skip update checking
python start_services.py

# Or with wrapper
python start_with_updates.py --skip-update-check
```

### **Service Won't Start After Update**
```bash
# Rollback docker-compose.yml
git checkout docker-compose.yml

# Restart with previous versions
python start_services.py
```

### **GitHub API Rate Limits**
- GitHub allows 60 requests/hour for unauthenticated requests
- Rate limits reset every hour
- Consider adding GitHub token for higher limits

---

**🎉 Your Local AI setup now stays automatically updated!**

