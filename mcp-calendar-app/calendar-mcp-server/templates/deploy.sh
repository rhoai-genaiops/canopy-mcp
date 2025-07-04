#!/bin/bash
# Simple deployment script for Calendar MCP Server

set -euo pipefail

NAMESPACE=${NAMESPACE:-"redwood-university"}
IMAGE_TAG=${IMAGE_TAG:-"latest"}

echo "🤖 Deploying Calendar MCP Server to $NAMESPACE"

# Create namespace if it doesn't exist
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Apply templates
echo "📦 Applying ConfigMap..."
kubectl apply -f calendar-mcp-server-configmap.yaml

echo "🚀 Applying Deployment and Service..."
kubectl apply -f calendar-mcp-server-deployment.yaml

# Wait for deployment
echo "⏳ Waiting for deployment..."
kubectl rollout status deployment/calendar-mcp-server -n "$NAMESPACE" --timeout=300s

# Show status
echo "✅ Deployment complete!"
kubectl get pods,svc -n "$NAMESPACE" -l app=calendar-mcp-server

# Show logs from one pod
echo "📋 Recent logs from MCP server:"
POD_NAME=$(kubectl get pods -n "$NAMESPACE" -l app=calendar-mcp-server -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
if [[ -n "$POD_NAME" ]]; then
    kubectl logs -n "$NAMESPACE" "$POD_NAME" --tail=10 || echo "No logs available yet"
fi

echo "🔧 MCP Server deployed successfully!"
echo "   - Service: calendar-mcp-server.${NAMESPACE}.svc.cluster.local:8080"
echo "   - Use this service name to connect from AI agents"