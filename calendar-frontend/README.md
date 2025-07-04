# Redwood Digital University Calendar Frontend

Enterprise-ready React frontend for the university calendar system, designed for containerized deployment in Kubernetes and OpenShift environments.

## 🏗️ Architecture

```
calendar-frontend/
├── src/                      # Application source code
│   ├── components/          # React components
│   ├── public/             # Static assets  
│   ├── config.js           # Environment configuration
│   ├── Containerfile       # Container build specification
│   └── nginx.conf          # Production web server config
├── templates/              # Simple deployment templates
│   ├── calendar-frontend-deployment.yaml
│   ├── calendar-frontend-configmap.yaml
│   ├── calendar-frontend-route.yaml
│   └── deploy.sh           # Simple deployment script
└── README.md              # This file
```

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
npm install

# Set environment variables
export REACT_APP_CALENDAR_API_URL="http://127.0.0.1:8000"

# Start development server
npm start
```

### Container Build
```bash
# Build production container
podman build -t calendar-frontend:latest src/

# Run container locally
podman run -p 8080:8080 \
  -e REACT_APP_CALENDAR_API_URL="http://calendar-api:8000" \
  calendar-frontend:latest
```

### OpenShift Deployment
```bash
# Deploy to OpenShift
cd templates/
./deploy.sh

# Check status
kubectl get pods,svc,route -n redwood-university -l app=calendar-frontend
```

## ⚙️ Configuration

The application supports environment-based configuration through ConfigMaps:

| Variable | Description | Default |
|----------|-------------|---------|
| `REACT_APP_CALENDAR_API_URL` | Backend API URL | `http://calendar-api:8000` |
| `REACT_APP_UNIVERSITY_NAME` | University name | `Redwood Digital University` |
| `REACT_APP_SYSTEM_BRANDING` | System branding | `Powered by CanopyAI` |

## 🎯 Features

### Frontend Capabilities
- **📅 Calendar Views** - Monthly calendar with event display
- **➕ Event Management** - Create, edit, delete events
- **🔍 Event Details** - Click events to view full information
- **📱 Responsive Design** - Works on desktop, tablet, mobile
- **🎨 University Branding** - Redwood Digital University theme
- **🗑️ Delete Functionality** - Remove events with confirmation

### Container Features
- **🔒 Security** - Non-root user, minimal nginx image
- **⚡ Performance** - Nginx static file serving
- **🏥 Health Checks** - Simple HTTP health probes
- **📦 Simple Build** - Multi-stage Docker build

### OpenShift Integration
- **📦 ConfigMaps** - Environment-based configuration
- **🚪 Routes** - External access with TLS termination
- **📈 Scaling** - Multiple replicas for availability

## 🐳 Production Deployment

### Container Registry
```bash
# Tag for registry
podman tag calendar-frontend:latest quay.io/redwood-university/calendar-frontend:v1.0.0

# Push to registry
podman push quay.io/redwood-university/calendar-frontend:v1.0.0
```

### Environment-Specific Deployments
```bash
# Development
NAMESPACE=redwood-dev ./deploy.sh

# Production
NAMESPACE=redwood-prod ./deploy.sh
```

## 🔧 Available Scripts

### Development
- `npm start` - Start development server (port 3000)
- `npm test` - Run test suite
- `npm run build` - Build production bundle
- `npm run eject` - Eject from Create React App

### Container Operations
- `podman build -t calendar-frontend src/` - Build container
- `podman run -p 8080:8080 calendar-frontend` - Run container

### Deployment
- `./templates/deploy.sh` - Deploy to OpenShift cluster

## 🛡️ Security

### Container Security
- Non-root user (UID/GID 1001)
- Minimal base image (nginx:alpine)
- Simple nginx configuration

### Network Security
- TLS termination at OpenShift route
- CORS configuration for API access

## 📝 Access URLs

After deployment, the frontend will be accessible at:

**OpenShift Route:** `https://calendar.redwood-university.apps.cluster.local`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally and in containers
5. Submit a pull request

## 📄 License

This project is part of the Redwood Digital University calendar system and follows the same licensing terms.