# Redwood Digital University Calendar MCP Server

This directory contains a custom Model Context Protocol (MCP) server that integrates with the Redwood Digital University academic calendar system, providing AI agents with comprehensive access to university scheduling, events, and academic activities.

## Overview

The Calendar MCP server (`server.py`) provides comprehensive academic calendar functionality including:
- **Event Management**: Create, read, update, and delete academic events
- **Schedule Queries**: Search and filter events by various criteria
- **Academic Planning**: View upcoming events and calendar statistics
- **University Integration**: Seamless integration with Redwood Digital University systems

## Key Features

- Integrates with the Calendar API via REST calls
- Supports all major calendar operations through 9 specialized tools
- Handles academic event categories (Lectures, Labs, Assignments, etc.)
- Provides detailed error handling and logging
- Optimized for university academic workflows

## Prerequisites

Before using the Calendar MCP server, make sure you have deployed the Calendar API:

```bash
# Start the Calendar API backend
cd calendar-api/src
uv run uvicorn server:app --reload --host 127.0.0.1 --port 8000

# Or using traditional pip
pip install -r requirements.txt
python build.py  # Initialize database
uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

## Local Development

### Setup with pipx (Recommended for macOS)

**pipx** is the recommended way to install MCP tools globally on macOS for VS Code integration:

```bash
# Install pipx if you don't have it
brew install pipx
pipx ensurepath

# Install MCP CLI tools globally
pipx install mcp
pipx install fastmcp

# Install MCP Inspector for debugging and method discovery
pipx install mcp-inspector

# Verify installation
mcp --version
fastmcp --version
mcp-inspector --version
```

### VS Code Integration & Method Discovery

After installing with pipx, you can use VS Code with MCP support:

```bash
# Install VS Code MCP extension (if available)
code --install-extension anthropic.mcp

# Use MCP Inspector to explore available tools
mcp-inspector calendar-mcp-server

# Or inspect the server directly
cd /path/to/calendar-mcp-server
mcp-inspector server.py
```

### Alternative: Setup Python environment (Local Development)

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### Test locally

```bash
# Make the server executable
chmod +x server.py

# Set environment variables for local Calendar API
export CALENDAR_API_BASE_URL="http://127.0.0.1:8000"

# Make sure Calendar API is running first
cd ../calendar-api/src
uv run uvicorn server:app --reload --host 127.0.0.1 --port 8000 &
cd ../../calendar-mcp-server

# Run the MCP server directly (it will wait for JSON-RPC input)
python server.py
```

## Available Tools

The Calendar MCP server provides the following tools for AI agents:

### Core Calendar Operations
1. **get_all_events** - Get all events with optional filtering by category or status
2. **get_event** - Get detailed information about a specific event by ID
3. **create_event** - Create a new academic event in the calendar
4. **update_event** - Update an existing event (including status changes)
5. **delete_event** - Remove an event from the calendar

### Advanced Queries
6. **get_upcoming_events** - Get upcoming events within specified days
7. **get_events_by_date** - Get all events for a specific date
8. **search_events** - Search events by name or content
9. **get_calendar_statistics** - Get calendar overview and statistics

### Academic Event Categories
- **Lecture** - Class lectures and presentations
- **Lab** - Laboratory sessions and practical work
- **Meeting** - Faculty meetings and administrative sessions
- **Office Hours** - Student consultation times
- **Assignment** - Due dates and deadlines
- **Defense** - Thesis and project defenses
- **Workshop** - Academic workshops and training
- **Study Group** - Student study sessions
- **Seminar** - Research seminars and talks
- **Grading** - Assessment and grading periods
- **Advising** - Academic advising sessions

## Testing with AI Agents

Once deployed, you can test the Calendar MCP server with various queries:

### Sample Queries
- "Show me all upcoming lectures this week"
- "Create a new lab session for CS 301 on Friday at 2 PM"
- "What events are scheduled for tomorrow?"
- "Search for all machine learning related events"
- "Update the status of assignment due-001 to completed"
- "Show me calendar statistics for this month"
- "What are the office hours for Dr. Chen?"
- "Delete the canceled workshop event"

### Example API Calls
```bash
# Get all events
curl -X GET "http://127.0.0.1:8000/schedules"

# Get specific event
curl -X GET "http://127.0.0.1:8000/schedules/event-123"

# Create new event
curl -X POST "http://127.0.0.1:8000/schedules" \\
  -H "Content-Type: application/json" \\
  -d '{
    "sid": "new-event-123",
    "name": "CS 401: Advanced AI",
    "content": "Deep learning applications",
    "category": "Lecture",
    "level": 3,
    "status": 0.0,
    "creation_time": "2025-07-03 12:00:00",
    "start_time": "2025-07-04 10:00:00",
    "end_time": "2025-07-04 11:30:00"
  }'
```

## Configuration

The Calendar MCP server uses the following environment variables:

- `CALENDAR_API_BASE_URL` - Base URL for the Calendar API (default: "http://127.0.0.1:8000")

### Docker/Container Configuration
```bash
# Run with custom API URL
docker run -e CALENDAR_API_BASE_URL="http://calendar-api:8000" calendar-mcp-server:latest
```