#!/usr/bin/env python3
"""
Test script for MCP protocol communication with the Calendar MCP Server
"""
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

# Set environment variable
os.environ["CALENDAR_API_BASE_URL"] = "http://127.0.0.1:8000"

async def test_mcp_protocol():
    """Test MCP server via JSON-RPC protocol"""
    print("🔌 Testing MCP JSON-RPC protocol...")
    
    # Start the MCP server process
    server_script = Path(__file__).parent / "server.py"
    process = await asyncio.create_subprocess_exec(
        sys.executable, str(server_script),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        # Test 1: Initialize the server
        print("📝 Sending initialization request...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "experimental": {},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        await send_request(process, init_request)
        response = await receive_response(process)
        print(f"✅ Initialization response: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
        
        # Test 2: List tools
        print("\n🛠️  Requesting tools list...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        await send_request(process, tools_request)
        response = await receive_response(process)
        tools = response.get('result', {}).get('tools', [])
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools[:3]:  # Show first 3 tools
            print(f"  - {tool.get('name')}: {tool.get('description')}")
        
        # Test 3: Call a tool
        print("\n📊 Calling get_calendar_statistics tool...")
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_calendar_statistics",
                "arguments": {"period": "month"}
            }
        }
        
        await send_request(process, call_request)
        response = await receive_response(process)
        content = response.get('result', {}).get('content', [])
        if content:
            stats_text = content[0].get('text', '')
            print(f"✅ Statistics result preview: {stats_text[:200]}...")
        
        print("\n🎉 MCP protocol tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ MCP protocol test failed: {e}")
        return False
    
    finally:
        # Clean up
        try:
            process.terminate()
            await process.wait()
        except:
            pass

async def send_request(process, request):
    """Send a JSON-RPC request to the MCP server"""
    message = json.dumps(request) + "\n"
    process.stdin.write(message.encode())
    await process.stdin.drain()

async def receive_response(process):
    """Receive a JSON-RPC response from the MCP server"""
    line = await process.stdout.readline()
    if not line:
        raise Exception("No response received")
    
    try:
        return json.loads(line.decode().strip())
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON response: {e}")

async def main():
    """Run the MCP protocol test"""
    print("🎓 Redwood Digital University Calendar MCP Protocol Test")
    print("=" * 60)
    
    # First check if the calendar API is running
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/") as response:
                if response.status != 200:
                    print("❌ Calendar API not running on port 8000")
                    return 1
    except:
        print("❌ Calendar API not accessible")
        return 1
    
    # Run the protocol test
    if await test_mcp_protocol():
        print("\n✅ All MCP protocol tests passed!")
        return 0
    else:
        print("\n❌ MCP protocol tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))