#!/usr/bin/env python3
"""
Test script for the Calendar MCP Server
"""
import asyncio
import json
import os
import sys
from server import make_calendar_api_request, handle_list_tools, handle_call_tool

# Set environment variable
os.environ["CALENDAR_API_BASE_URL"] = "http://127.0.0.1:8000"

async def test_api_connection():
    """Test basic API connectivity"""
    print("🔗 Testing Calendar API connection...")
    try:
        result = await make_calendar_api_request("GET", "/")
        print(f"✅ API Status: {result}")
        
        events = await make_calendar_api_request("GET", "/schedules")
        print(f"✅ Found {len(events)} events in calendar")
        return True
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

async def test_list_tools():
    """Test MCP tool listing"""
    print("\n🛠️  Testing MCP tool listing...")
    try:
        tools = await handle_list_tools()
        print(f"✅ Found {len(tools)} MCP tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        return True
    except Exception as e:
        print(f"❌ Tool listing failed: {e}")
        return False

async def test_get_all_events():
    """Test get_all_events tool"""
    print("\n📅 Testing get_all_events tool...")
    try:
        result = await handle_call_tool("get_all_events", {})
        print(f"✅ get_all_events result:")
        print(result[0].text[:300] + "..." if len(result[0].text) > 300 else result[0].text)
        return True
    except Exception as e:
        print(f"❌ get_all_events failed: {e}")
        return False

async def test_get_event():
    """Test get_event tool"""
    print("\n📋 Testing get_event tool...")
    try:
        result = await handle_call_tool("get_event", {"event_id": "class-cs301"})
        print(f"✅ get_event result:")
        print(result[0].text[:300] + "..." if len(result[0].text) > 300 else result[0].text)
        return True
    except Exception as e:
        print(f"❌ get_event failed: {e}")
        return False

async def test_create_event():
    """Test create_event tool"""
    print("\n➕ Testing create_event tool...")
    try:
        event_data = {
            "name": "MCP Test Event",
            "content": "Test event created by MCP server",
            "category": "Meeting",
            "level": 1,
            "start_time": "2025-07-10 14:00:00",
            "end_time": "2025-07-10 15:00:00"
        }
        result = await handle_call_tool("create_event", event_data)
        print(f"✅ create_event result:")
        print(result[0].text)
        return True
    except Exception as e:
        print(f"❌ create_event failed: {e}")
        return False

async def test_search_events():
    """Test search_events tool"""
    print("\n🔍 Testing search_events tool...")
    try:
        result = await handle_call_tool("search_events", {"query": "Machine Learning"})
        print(f"✅ search_events result:")
        print(result[0].text[:300] + "..." if len(result[0].text) > 300 else result[0].text)
        return True
    except Exception as e:
        print(f"❌ search_events failed: {e}")
        return False

async def test_get_upcoming_events():
    """Test get_upcoming_events tool"""
    print("\n⏰ Testing get_upcoming_events tool...")
    try:
        result = await handle_call_tool("get_upcoming_events", {"days": 7})
        print(f"✅ get_upcoming_events result:")
        print(result[0].text[:300] + "..." if len(result[0].text) > 300 else result[0].text)
        return True
    except Exception as e:
        print(f"❌ get_upcoming_events failed: {e}")
        return False

async def test_get_calendar_statistics():
    """Test get_calendar_statistics tool"""
    print("\n📊 Testing get_calendar_statistics tool...")
    try:
        result = await handle_call_tool("get_calendar_statistics", {"period": "month"})
        print(f"✅ get_calendar_statistics result:")
        print(result[0].text[:400] + "..." if len(result[0].text) > 400 else result[0].text)
        return True
    except Exception as e:
        print(f"❌ get_calendar_statistics failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🎓 Redwood Digital University Calendar MCP Server Test Suite")
    print("=" * 60)
    
    tests = [
        test_api_connection,
        test_list_tools,
        test_get_all_events,
        test_get_event,
        test_create_event,
        test_search_events,
        test_get_upcoming_events,
        test_get_calendar_statistics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if await test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MCP server is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))