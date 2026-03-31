#!/usr/bin/env python3
"""
Mock Midnight Node Server
Simulates a real Midnight blockchain node with JSON-RPC interface
"""

import asyncio
import json
import hashlib
from datetime import datetime
from aiohttp import web

# In-memory blockchain state
blockchain = {
    "blocks": [],
    "transactions": {},
    "contracts": {},
    "balances": {},
    "current_height": 0,
}


async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "service": "midnight-node",
        "network": "undeployed",
        "block_height": blockchain["current_height"]
    })


async def json_rpc(request):
    """JSON-RPC 2.0 endpoint"""
    data = await request.json()
    method = data.get("method")
    params = data.get("params", [])
    request_id = data.get("id", 1)
    
    # Handle different RPC methods
    if method == "system_health":
        result = {
            "peers": 3,
            "isSyncing": False,
            "shouldHavePeers": True
        }
    elif method == "chain_getBlockHash":
        height = params[0] if params else blockchain["current_height"]
        result = f"0x{hashlib.sha256(str(height).encode()).hexdigest()}"
    elif method == "chain_getBlock":
        result = {
            "block": {
                "header": {
                    "number": blockchain["current_height"],
                    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
                },
                "extrinsics": []
            }
        }
    elif method == "state_getStorage":
        # Return balance or contract state
        key = params[0] if params else ""
        result = "0x" + "00" * 32  # Empty storage
    else:
        result = {"error": f"Unknown method: {method}"}
    
    return web.json_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    })


async def get_balance(request):
    """Get wallet balance"""
    address = request.match_info.get('address', '')
    balance = blockchain["balances"].get(address, {
        "dust": 1_000_000,
        "night": 100
    })
    return web.json_response(balance)


async def sign_transaction(request):
    """Sign a transaction"""
    data = await request.json()
    tx = data.get("transaction", {})
    private_key = data.get("privateKey", "")
    
    # Simulate signing
    tx_hash = hashlib.sha256(json.dumps(tx).encode()).hexdigest()
    signed_tx = {
        **tx,
        "signature": hashlib.sha256(f"{tx_hash}{private_key}".encode()).hexdigest(),
        "signed": True,
        "hash": tx_hash
    }
    
    return web.json_response({"signedTransaction": signed_tx})


async def submit_transaction(request):
    """Submit a signed transaction"""
    signed_tx = await request.json()
    
    tx_hash = signed_tx.get("hash") or hashlib.sha256(
        json.dumps(signed_tx).encode()
    ).hexdigest()
    
    # Store transaction
    blockchain["transactions"][tx_hash] = {
        "tx": signed_tx,
        "status": "confirmed",
        "blockHeight": blockchain["current_height"] + 1,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Update contract state if applicable
    if "contractAddress" in signed_tx:
        addr = signed_tx["contractAddress"]
        if addr not in blockchain["contracts"]:
            blockchain["contracts"][addr] = {
                "state": {},
                "blockHeight": blockchain["current_height"] + 1
            }
        blockchain["contracts"][addr]["state"]["call_count"] = \
            blockchain["contracts"][addr]["state"].get("call_count", 0) + 1
    
    # Increment block height
    blockchain["current_height"] += 1
    
    return web.json_response({
        "txHash": tx_hash,
        "blockHeight": blockchain["current_height"],
        "status": "confirmed"
    })


async def deploy_contract(request):
    """Deploy a contract"""
    data = await request.json()
    contract_path = data.get("contractPath", "")
    
    # Generate contract address
    contract_address = f"mn1{hashlib.sha256(contract_path.encode()).hexdigest()[:40]}"
    
    blockchain["contracts"][contract_address] = {
        "address": contract_address,
        "path": contract_path,
        "state": {
            "message_count": 0,
            "latest_message": "",
            "call_count": 0
        },
        "blockHeight": blockchain["current_height"] + 1,
        "deployed_at": datetime.utcnow().isoformat()
    }
    
    blockchain["current_height"] += 1
    
    return web.json_response({"contractAddress": contract_address})


async def init_app():
    """Initialize the application"""
    app = web.Application()
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_post('/', json_rpc)
    app.router.add_get('/balance/{address}', get_balance)
    app.router.add_post('/wallet/sign', sign_transaction)
    app.router.add_post('/transactions', submit_transaction)
    app.router.add_post('/contracts/deploy', deploy_contract)
    
    return app


def main():
    """Main entry point"""
    print("Starting Midnight Node Mock Server on port 9944...")
    app = asyncio.run(init_app())
    web.run_app(app, host='0.0.0.0', port=9944)


if __name__ == "__main__":
    main()
