#!/usr/bin/env python3
"""
Mock Midnight Indexer Server
Provides GraphQL API for querying blockchain state
"""

import asyncio
import json
from datetime import datetime
from aiohttp import web
import hashlib

# In-memory state storage
contracts = {}
transactions = {}


async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "service": "midnight-indexer"
    })


async def graphql_handler(request):
    """Handle GraphQL queries"""
    data = await request.json()
    query = data.get("query", "")
    variables = data.get("variables", {})
    
    # Parse query type
    if "__typename" in query:
        # Schema introspection
        return web.json_response({
            "data": {"__typename": "Query"}
        })
    
    elif "contractState" in query:
        # Contract state query
        address = variables.get("address", "")
        
        if address not in contracts:
            # Create default state
            contracts[address] = {
                "state": {
                    "message_count": 0,
                    "latest_message": "",
                    "call_count": 0
                },
                "blockHeight": 1000
            }
        
        contract = contracts[address]
        return web.json_response({
            "data": {
                "contractState": {
                    "state": contract["state"],
                    "blockHeight": contract["blockHeight"]
                }
            }
        })
    
    elif "transaction" in query:
        # Transaction query
        tx_hash = variables.get("hash", "")
        tx = transactions.get(tx_hash, {
            "hash": tx_hash,
            "blockHeight": 1000,
            "status": "confirmed"
        })
        return web.json_response({
            "data": {"transaction": tx}
        })
    
    elif "contractEvents" in query:
        # Contract events subscription (for WebSocket)
        address = variables.get("address", "")
        return web.json_response({
            "data": {
                "contractEvents": {
                    "eventType": "StateChanged",
                    "data": {},
                    "blockHeight": 1000,
                    "txHash": "0xabc123"
                }
            }
        })
    
    else:
        return web.json_response({
            "errors": [{"message": "Unknown query"}]
        })


async def websocket_handler(request):
    """Handle WebSocket connections for subscriptions"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            data = json.loads(msg.data)
            
            if data.get("type") == "start":
                # Send initial event
                await ws.send_json({
                    "type": "data",
                    "payload": {
                        "data": {
                            "contractEvents": {
                                "eventType": "StateChanged",
                                "data": {},
                                "blockHeight": 1000,
                                "txHash": "0xabc123"
                            }
                        }
                    }
                })
    
    return ws


async def init_app():
    """Initialize the application"""
    app = web.Application()
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_post('/api/v3/graphql', graphql_handler)
    app.router.add_get('/api/v3/graphql/ws', websocket_handler)
    
    return app


def main():
    """Main entry point"""
    print("Starting Midnight Indexer Mock Server on port 8088...")
    app = asyncio.run(init_app())
    web.run_app(app, host='0.0.0.0', port=8088)


if __name__ == "__main__":
    main()
