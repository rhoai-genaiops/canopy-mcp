#!/usr/bin/env python3
"""
Redwood Digital University Calendar MCP Server - Provides access to academic calendar through MCP tools.
"""

import asyncio
import json
import logging
import os
from typing import Any, Sequence
import aiohttp
from datetime import datetime, timedelta

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("calendar-mcp-server")

# Create the server instance
server = Server("calendar-mcp-server")

# Calendar API configuration
CALENDAR_API_BASE_URL = os.getenv("CALENDAR_API_BASE_URL", "http://127.0.0.1:8000")

async def make_calendar_api_request(method: str, endpoint: str, data: dict = None) -> dict:
    """Make a request to the Calendar API."""
    url = f"{CALENDAR_API_BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            if method.upper() == "GET":
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise ValueError(f"API request failed with status {response.status}")
            elif method.upper() == "POST":
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise ValueError(f"API request failed with status {response.status}")
            elif method.upper() == "PUT":
                async with session.put(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise ValueError(f"API request failed with status {response.status}")
            elif method.upper() == "DELETE":
                async with session.delete(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise ValueError(f"API request failed with status {response.status}")
    except Exception as e:
        logger.error(f"Calendar API request failed: {e}")
        raise ValueError(f"Calendar API request failed: {str(e)}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available calendar tools."""
    return [
        types.Tool(
            name="get_all_events",
            description="Get all events/schedules from the Redwood Digital University calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["Lecture", "Lab", "Meeting", "Office Hours", "Assignment", "Defense", "Workshop", "Study Group", "Seminar", "Grading", "Advising"],
                        "description": "Filter by event category (optional)"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["not_started", "in_progress", "completed"],
                        "description": "Filter by completion status (optional)"
                    }
                }
            }
        ),
        types.Tool(
            name="get_event",
            description="Get detailed information about a specific event by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "Event ID to retrieve"
                    }
                },
                "required": ["event_id"]
            }
        ),
        types.Tool(
            name="create_event",
            description="Create a new academic event in the calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Event name/title"
                    },
                    "content": {
                        "type": "string",
                        "description": "Event description/details"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["Lecture", "Lab", "Meeting", "Office Hours", "Assignment", "Defense", "Workshop", "Study Group", "Seminar", "Grading", "Advising"],
                        "description": "Event category"
                    },
                    "level": {
                        "type": "integer",
                        "enum": [1, 2, 3],
                        "description": "Priority level (1=Low, 2=Medium, 3=High)"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time in YYYY-MM-DD HH:MM:SS format"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in YYYY-MM-DD HH:MM:SS format"
                    }
                },
                "required": ["name", "category", "level", "start_time", "end_time"]
            }
        ),
        types.Tool(
            name="update_event",
            description="Update an existing event in the calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "Event ID to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "Event name/title"
                    },
                    "content": {
                        "type": "string",
                        "description": "Event description/details"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["Lecture", "Lab", "Meeting", "Office Hours", "Assignment", "Defense", "Workshop", "Study Group", "Seminar", "Grading", "Advising"],
                        "description": "Event category"
                    },
                    "level": {
                        "type": "integer",
                        "enum": [1, 2, 3],
                        "description": "Priority level (1=Low, 2=Medium, 3=High)"
                    },
                    "status": {
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "description": "Completion status (0.0=Not Started, 0.5=In Progress, 1.0=Completed)"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time in YYYY-MM-DD HH:MM:SS format"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in YYYY-MM-DD HH:MM:SS format"
                    }
                },
                "required": ["event_id"]
            }
        ),
        types.Tool(
            name="delete_event",
            description="Delete an event from the calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "Event ID to delete"
                    }
                },
                "required": ["event_id"]
            }
        ),
        types.Tool(
            name="get_upcoming_events",
            description="Get upcoming events within a specified number of days",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 30,
                        "description": "Number of days to look ahead (default: 7)"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["Lecture", "Lab", "Meeting", "Office Hours", "Assignment", "Defense", "Workshop", "Study Group", "Seminar", "Grading", "Advising"],
                        "description": "Filter by event category (optional)"
                    }
                }
            }
        ),
        types.Tool(
            name="get_events_by_date",
            description="Get all events for a specific date",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format"
                    }
                },
                "required": ["date"]
            }
        ),
        types.Tool(
            name="search_events",
            description="Search events by name or content",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to match against event names and descriptions"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_calendar_statistics",
            description="Get calendar statistics and overview",
            inputSchema={
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "enum": ["week", "month", "semester"],
                        "description": "Time period for statistics (default: month)"
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle calendar tool calls."""
    
    try:
        if name == "get_all_events":
            result = await make_calendar_api_request("GET", "/schedules")
            
            events = result if isinstance(result, list) else []
            
            # Apply filters if provided
            if arguments:
                if "category" in arguments:
                    events = [e for e in events if e.get("category") == arguments["category"]]
                if "status" in arguments:
                    status_map = {"not_started": 0.0, "in_progress": 0.5, "completed": 1.0}
                    target_status = status_map.get(arguments["status"])
                    if target_status is not None:
                        if target_status == 0.0:
                            events = [e for e in events if e.get("status", 0) == 0.0]
                        elif target_status == 0.5:
                            events = [e for e in events if 0.0 < e.get("status", 0) < 1.0]
                        else:  # completed
                            events = [e for e in events if e.get("status", 0) == 1.0]
            
            summary = f"Found {len(events)} events in Redwood Digital University calendar"
            
            event_list = "\\n".join([
                f"• {event['name']} ({event['category']})\\n"
                f"  📅 {event['start_time']} - {event['end_time']}\\n"
                f"  📋 {event.get('content', 'No description')}\\n"
                f"  🎯 Priority: {['', 'Low', 'Medium', 'High'][event.get('level', 1)]}\\n"
                f"  ✅ Status: {int(event.get('status', 0) * 100)}% complete\\n"
                for event in events[:10]  # Limit to first 10 for readability
            ])
            
            if len(events) > 10:
                event_list += f"\\n... and {len(events) - 10} more events"
            
            return [
                types.TextContent(
                    type="text",
                    text=f"{summary}\\n\\n{event_list}"
                )
            ]
        
        elif name == "get_event":
            if not arguments or "event_id" not in arguments:
                raise ValueError("Event ID is required")
            
            event_id = arguments["event_id"]
            result = await make_calendar_api_request("GET", f"/schedules/{event_id}")
            
            # If result is a list (as the backend currently returns), take the first item
            event = result[0] if isinstance(result, list) and result else result
            
            details = f"""📚 Redwood Digital University Event Details:

🎓 **{event['name']}**
📋 **Category:** {event['category']}
📝 **Description:** {event.get('content', 'No description provided')}

📅 **Schedule:**
• Start: {event['start_time']}
• End: {event['end_time']}

🎯 **Priority:** {['', 'Low', 'Medium', 'High'][event.get('level', 1)]}
✅ **Status:** {int(event.get('status', 0) * 100)}% complete
🆔 **Event ID:** {event['sid']}
🕐 **Created:** {event.get('creation_time', 'Unknown')}"""
            
            return [
                types.TextContent(
                    type="text",
                    text=details
                )
            ]
        
        elif name == "create_event":
            if not arguments:
                raise ValueError("Event details are required")
            
            required_fields = ["name", "category", "level", "start_time", "end_time"]
            for field in required_fields:
                if field not in arguments:
                    raise ValueError(f"{field} is required")
            
            # Generate unique SID
            timestamp = int(datetime.now().timestamp() * 1000)
            sid = f"mcp-event-{timestamp}"
            
            # Prepare event data
            event_data = {
                "sid": sid,
                "name": arguments["name"],
                "content": arguments.get("content", ""),
                "category": arguments["category"],
                "level": arguments["level"],
                "status": 0.0,  # New events start as not started
                "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "start_time": arguments["start_time"],
                "end_time": arguments["end_time"]
            }
            
            result = await make_calendar_api_request("POST", "/schedules", event_data)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"✅ Event created successfully!\\n\\n🎓 **{result['name']}**\\n📋 Category: {result['category']}\\n📅 Time: {result['start_time']} - {result['end_time']}\\n🆔 Event ID: {result['sid']}"
                )
            ]
        
        elif name == "update_event":
            if not arguments or "event_id" not in arguments:
                raise ValueError("Event ID is required")
            
            event_id = arguments["event_id"]
            
            # Get current event data first
            current_event = await make_calendar_api_request("GET", f"/schedules/{event_id}")
            if isinstance(current_event, list) and current_event:
                current_event = current_event[0]
            
            # Prepare update data (merge with current data)
            update_data = {
                "sid": event_id,
                "name": arguments.get("name", current_event["name"]),
                "content": arguments.get("content", current_event.get("content", "")),
                "category": arguments.get("category", current_event["category"]),
                "level": arguments.get("level", current_event["level"]),
                "status": arguments.get("status", current_event.get("status", 0.0)),
                "creation_time": current_event.get("creation_time"),
                "start_time": arguments.get("start_time", current_event["start_time"]),
                "end_time": arguments.get("end_time", current_event["end_time"])
            }
            
            result = await make_calendar_api_request("PUT", f"/schedules/{event_id}", update_data)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"✅ Event updated successfully!\\n\\n🎓 **{result['name']}**\\n📋 Category: {result['category']}\\n✅ Status: {int(result.get('status', 0) * 100)}% complete"
                )
            ]
        
        elif name == "delete_event":
            if not arguments or "event_id" not in arguments:
                raise ValueError("Event ID is required")
            
            event_id = arguments["event_id"]
            result = await make_calendar_api_request("DELETE", f"/schedules/{event_id}")
            
            return [
                types.TextContent(
                    type="text",
                    text=f"🗑️ Event deleted successfully: {event_id}"
                )
            ]
        
        elif name == "get_upcoming_events":
            days = arguments.get("days", 7) if arguments else 7
            category_filter = arguments.get("category") if arguments else None
            
            # Get all events and filter for upcoming ones
            all_events = await make_calendar_api_request("GET", "/schedules")
            
            now = datetime.now()
            future_date = now + timedelta(days=days)
            
            upcoming_events = []
            for event in all_events:
                try:
                    event_start = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M:%S")
                    if now <= event_start <= future_date:
                        if not category_filter or event.get("category") == category_filter:
                            upcoming_events.append(event)
                except:
                    continue  # Skip events with invalid dates
            
            # Sort by start time
            upcoming_events.sort(key=lambda x: x["start_time"])
            
            summary = f"📅 Upcoming events in next {days} day{'s' if days != 1 else ''}"
            if category_filter:
                summary += f" (filtered by {category_filter})"
            summary += f": {len(upcoming_events)} found"
            
            event_list = "\\n".join([
                f"• {event['name']} ({event['category']})\\n  📅 {event['start_time']}"
                for event in upcoming_events[:10]
            ])
            
            return [
                types.TextContent(
                    type="text",
                    text=f"{summary}\\n\\n{event_list}"
                )
            ]
        
        elif name == "get_events_by_date":
            if not arguments or "date" not in arguments:
                raise ValueError("Date is required (YYYY-MM-DD format)")
            
            target_date = arguments["date"]
            all_events = await make_calendar_api_request("GET", "/schedules")
            
            date_events = []
            for event in all_events:
                try:
                    event_date = event["start_time"].split()[0]  # Extract date part
                    if event_date == target_date:
                        date_events.append(event)
                except:
                    continue
            
            summary = f"📅 Events on {target_date}: {len(date_events)} found"
            
            event_list = "\\n".join([
                f"• {event['name']} ({event['category']})\\n  🕐 {event['start_time'].split()[1]} - {event['end_time'].split()[1]}"
                for event in date_events
            ])
            
            return [
                types.TextContent(
                    type="text",
                    text=f"{summary}\\n\\n{event_list if event_list else 'No events scheduled for this date.'}"
                )
            ]
        
        elif name == "search_events":
            if not arguments or "query" not in arguments:
                raise ValueError("Search query is required")
            
            query = arguments["query"].lower()
            all_events = await make_calendar_api_request("GET", "/schedules")
            
            matching_events = []
            for event in all_events:
                if (query in event["name"].lower() or 
                    query in event.get("content", "").lower()):
                    matching_events.append(event)
            
            summary = f"🔍 Search results for '{arguments['query']}': {len(matching_events)} events found"
            
            event_list = "\\n".join([
                f"• {event['name']} ({event['category']})\\n  📅 {event['start_time']}"
                for event in matching_events[:10]
            ])
            
            return [
                types.TextContent(
                    type="text",
                    text=f"{summary}\\n\\n{event_list if event_list else 'No events match your search query.'}"
                )
            ]
        
        elif name == "get_calendar_statistics":
            period = arguments.get("period", "month") if arguments else "month"
            all_events = await make_calendar_api_request("GET", "/schedules")
            
            # Calculate statistics
            total_events = len(all_events)
            completed_events = len([e for e in all_events if e.get("status", 0) == 1.0])
            in_progress_events = len([e for e in all_events if 0 < e.get("status", 0) < 1.0])
            pending_events = len([e for e in all_events if e.get("status", 0) == 0.0])
            
            # Category breakdown
            categories = {}
            for event in all_events:
                cat = event.get("category", "Unknown")
                categories[cat] = categories.get(cat, 0) + 1
            
            category_breakdown = "\\n".join([
                f"• {cat}: {count} events" 
                for cat, count in sorted(categories.items())
            ])
            
            completion_rate = (completed_events / total_events * 100) if total_events > 0 else 0
            
            stats = f"""📊 Redwood Digital University Calendar Statistics ({period})

📈 **Overview:**
• Total Events: {total_events}
• Completed: {completed_events} ({completion_rate:.1f}%)
• In Progress: {in_progress_events}
• Pending: {pending_events}

📋 **By Category:**
{category_breakdown}

🎯 **Academic Activity Level:** {'High' if total_events > 50 else 'Medium' if total_events > 20 else 'Low'}"""
            
            return [
                types.TextContent(
                    type="text",
                    text=stats
                )
            ]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"❌ Error: {str(e)}"
            )
        ]

async def main():
    # Run the server using stdio
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="calendar-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())