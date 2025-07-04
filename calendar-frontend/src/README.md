# Redwood Digital University Calendar Frontend

React-based frontend application for the university calendar system, designed for containerized deployment in Kubernetes/OpenShift environments.

## 📁 Structure

```
src/
├── components/           # React components
│   ├── Calendar.js      # Main calendar component
│   ├── Calendar.css     # Calendar styles
│   ├── Day.js           # Day component
│   ├── Day.css          # Day styles
│   ├── EventModal.js    # Event details modal
│   └── EventModal.css   # Modal styles
├── public/              # Static assets
│   ├── index.html       # HTML template
│   ├── canopyai-logo.png # University logo
│   └── favicon.ico      # Site favicon
├── config.js            # Environment configuration
├── Containerfile        # Container build file
├── nginx.conf           # Nginx configuration
└── README.md           # This file
```

## 🔧 Configuration

The application uses `config.js` for environment-based configuration:

```javascript
// Environment variables supported:
REACT_APP_CALENDAR_API_URL    # Backend API URL
REACT_APP_UNIVERSITY_NAME     # University name
REACT_APP_SYSTEM_BRANDING     # System branding text
REACT_APP_ENABLE_DELETE       # Enable delete functionality
REACT_APP_ENABLE_EDIT         # Enable edit functionality  
REACT_APP_ENABLE_CREATE       # Enable create functionality
REACT_APP_DEBUG               # Debug mode
```

## 🐳 Container Build

```bash
# Build container image
podman build -t calendar-frontend:latest .

# Run locally
podman run -p 8080:8080 \
  -e REACT_APP_CALENDAR_API_URL="http://calendar-api:8000" \
  calendar-frontend:latest
```

## 🚀 Local Development

```bash
# Install dependencies
npm install

# Set environment variables
export REACT_APP_CALENDAR_API_URL="http://127.0.0.1:8000"

# Start development server
npm start
```

## 📦 Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Event Management** - Create, view, edit, and delete events
- **Modern UI** - Clean, professional university branding
- **Configurable** - Environment-based configuration
- **Secure** - Non-root container, security headers
- **High Availability** - Multiple replicas, health checks