# Calendar MCP Server - Kubernetes/OpenShift Deployment

Enterprise-ready deployment templates for the Redwood Digital University Calendar MCP Server.

## 🏗️ Architecture

The MCP Server provides AI agents with access to the calendar system through 9 specialized tools:

- **get_all_events** - Retrieve all calendar events
- **get_events_by_date** - Find events for specific dates
- **get_events_by_category** - Filter events by category
- **create_event** - Create new calendar entries
- **update_event** - Modify existing events
- **delete_event** - Remove events
- **get_academic_calendar** - Get semester/term information
- **search_events** - Search events by keywords
- **get_event_statistics** - Analytics and reporting

## 🚀 Quick Deployment

### Build Container
```bash
cd calendar-mcp-server/
podman build -t calendar-mcp-server:latest .
```

### Deploy to OpenShift
```bash
cd templates/
./deploy.sh
```

### Check Status
```bash
kubectl get pods,svc -n redwood-university -l app=calendar-mcp-server
```

## ⚙️ Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `CALENDAR_API_BASE_URL` | Backend API URL | `http://calendar-api:8000` |
| `UNIVERSITY_NAME` | University name | `Redwood Digital University` |
| `SYSTEM_BRANDING` | System branding | `Powered by CanopyAI` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🔧 Usage

### AI Agent Integration

The MCP server runs as a cluster service and can be accessed by AI agents:

```bash
# Service endpoint
calendar-mcp-server.redwood-university.svc.cluster.local:8080
```

### Local Testing
```bash
# Run with local backend
podman run -p 8080:8080 \
  -e CALENDAR_API_BASE_URL="http://127.0.0.1:8000" \
  calendar-mcp-server:latest
```

## 📦 Deployment Components

- **ConfigMap**: Environment configuration
- **Deployment**: 2 replicas with resource limits
- **Service**: Internal cluster access
- **Security**: Non-root user, read-only filesystem

## 🛡️ Security Features

- Non-root container user (UID 1000)
- Read-only root filesystem
- Dropped capabilities
- Resource limits enforced
- Health check probes

## 📊 Monitoring

The MCP server logs all tool operations and API calls:

```bash
# View logs
kubectl logs -l app=calendar-mcp-server -n redwood-university -f
```

## 🤝 Dependencies

- **calendar-api**: Backend API service
- **calendar-frontend**: Web interface (optional)

Deploy in this order:
1. calendar-api
2. calendar-mcp-server
3. calendar-frontend

## 🔄 Scaling

The MCP server supports horizontal scaling:

```bash
kubectl scale deployment calendar-mcp-server --replicas=3 -n redwood-university
```

## 📝 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure calendar-api is running
   - Check CALENDAR_API_BASE_URL configuration

2. **MCP Tools Not Working**
   - Verify JSON-RPC communication
   - Check AI agent MCP client configuration

3. **Container Won't Start**
   - Check resource limits
   - Verify image availability

### Debug Commands

```bash
# Check pod status
kubectl describe pod -l app=calendar-mcp-server -n redwood-university

# Test API connectivity
kubectl exec -it deployment/calendar-mcp-server -n redwood-university -- \
  curl -f http://calendar-api:8000/health
```