#!/usr/bin/env python3
"""
Development mock servers for Midnight services.
Run this to simulate the Midnight node, indexer, and proof server locally.

Usage:
    python dev_server.py
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any
import hashlib

try:
    from aiohttp import web
    import aiohttp
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    subprocess.check_call(["pip", "install", "aiohttp"])
    from aiohttp import web
    import aiohttp


# In-memory storage
contracts: Dict[str, Dict[str, Any]] = {}
transactions: Dict[str, Dict[str, Any]] = {}
balances: Dict[str, Dict[str, int]] = {}


# ============================================================================
# MIDNIGHT NODE (Port 9944)
# ============================================================================

async def node_health(request):
    """Health check endpoint."""
    return web.json_response({"status": "healthy", "service": "midnight-node"})


async def get_balance(request):
    """Get wallet balance."""
    address = request.match_info['address']
    balance = balances.get(address, {"dust": 1_000_000, "night": 100})
    return web.json_response(balance)


async def sign_transaction(request):
    """Sign a transaction."""
    data = await request.json()
    tx = data.get("transaction", {})
    private_key = data.get("privateKey", "")
    
    # Simulate signing
    signed_tx = {
        **tx,
        "signature": hashlib.sha256(f"{json.dumps(tx)}{private_key}".encode()).hexdigest(),
        "signed": True
    }
    
    return web.json_response({"signedTransaction": signed_tx})


async def submit_transaction(request):
    """Submit a signed transaction."""
    signed_tx = await request.json()
    
    tx_hash = hashlib.sha256(json.dumps(signed_tx).encode()).hexdigest()
    
    transactions[tx_hash] = {
        "tx": signed_tx,
        "status": "confirmed",
        "blockHeight": len(transactions) + 1000,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Update contract state if it's a contract call
    if "contractAddress" in signed_tx:
        addr = signed_tx["contractAddress"]
        if addr in contracts:
            contracts[addr]["state"]["call_count"] = contracts[addr]["state"].get("call_count", 0) + 1
            contracts[addr]["blockHeight"] = len(transactions) + 1000
    
    return web.json_response({
        "txHash": tx_hash,
        "blockHeight": len(transactions) + 1000,
        "status": "confirmed"
    })


async def deploy_contract(request):
    """Deploy a contract."""
    data = await request.json()
    contract_path = data.get("contractPath", "")
    
    # Generate contract address
    contract_address = f"mn_preprod1{hashlib.sha256(contract_path.encode()).hexdigest()[:40]}"
    
    contracts[contract_address] = {
        "address": contract_address,
        "path": contract_path,
        "state": {
            "message_count": 0,
            "latest_message": "",
            "call_count": 0
        },
        "blockHeight": len(transactions) + 1000,
        "deployed_at": datetime.utcnow().isoformat()
    }
    
    return web.json_response({"contractAddress": contract_address})


# ============================================================================
# MIDNIGHT INDEXER (Port 8088)
# ============================================================================

async def indexer_health(request):
    """Health check endpoint."""
    return web.json_response({"status": "healthy", "service": "midnight-indexer"})


async def graphql_query(request):
    """Handle GraphQL queries."""
    data = await request.json()
    query = data.get("query", "")
    variables = data.get("variables", {})
    
    # Parse contract state query
    if "contractState" in query:
        address = variables.get("address", "")
        contract = contracts.get(address, {
            "state": {"error": "Contract not found"},
            "blockHeight": 0
        })
        
        return web.json_response({
            "data": {
                "contractState": {
                    "state": contract.get("state", {}),
                    "blockHeight": contract.get("blockHeight", 0)
                }
            }
        })
    
    return web.json_response({"data": {}})


# ============================================================================
# MIDNIGHT PROOF SERVER (Port 6300)
# ============================================================================

async def proof_health(request):
    """Health check endpoint."""
    return web.json_response({"status": "healthy", "service": "midnight-proof-server"})


async def generate_proof(request):
    """Generate a ZK proof."""
    data = await request.json()
    circuit_id = data.get("circuitId", "")
    private_inputs = data.get("privateInputs", {})
    public_inputs = data.get("publicInputs", {})
    
    # Simulate proof generation (takes a moment)
    await asyncio.sleep(0.5)
    
    # Generate mock proof
    proof_data = f"{circuit_id}{json.dumps(private_inputs)}{json.dumps(public_inputs)}"
    proof = hashlib.sha256(proof_data.encode()).hexdigest()
    
    return web.json_response({
        "proof": f"zk_proof_{proof}",
        "publicOutputs": {
            **public_inputs,
            "verified": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    })


# ============================================================================
# SERVER SETUP
# ============================================================================

async def create_node_app():
    """Create the node server."""
    app = web.Application()
    app.router.add_get('/health', node_health)
    app.router.add_get('/balance/{address}', get_balance)
    app.router.add_post('/wallet/sign', sign_transaction)
    app.router.add_post('/transactions', submit_transaction)
    app.router.add_post('/contracts/deploy', deploy_contract)
    return app


async def create_indexer_app():
    """Create the indexer server."""
    app = web.Application()
    app.router.add_get('/health', indexer_health)
    app.router.add_post('/api/v1/graphql', graphql_query)
    return app


async def create_proof_app():
    """Create the proof server."""
    app = web.Application()
    app.router.add_get('/health', proof_health)
    app.router.add_post('/prove', generate_proof)
    return app


async def start_servers():
    """Start all three servers."""
    # Create apps
    node_app = await create_node_app()
    indexer_app = await create_indexer_app()
    proof_app = await create_proof_app()
    
    # Create runners
    node_runner = web.AppRunner(node_app)
    indexer_runner = web.AppRunner(indexer_app)
    proof_runner = web.AppRunner(proof_app)
    
    await node_runner.setup()
    await indexer_runner.setup()
    await proof_runner.setup()
    
    # Create sites
    node_site = web.TCPSite(node_runner, 'localhost', 9944)
    indexer_site = web.TCPSite(indexer_runner, 'localhost', 8088)
    proof_site = web.TCPSite(proof_runner, 'localhost', 6300)
    
    # Start servers
    await node_site.start()
    await indexer_site.start()
    await proof_site.start()
    
    print("=" * 60)
    print("🌙 Midnight Development Servers Started")
    print("=" * 60)
    print(f"✓ Node:         http://localhost:9944")
    print(f"✓ Indexer:      http://localhost:8088")
    print(f"✓ Proof Server: http://localhost:6300")
    print("=" * 60)
    print("\nServers are running. Press Ctrl+C to stop.")
    print("\nTest with: midnight-py status")
    print("=" * 60)
    
    # Keep running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n\nShutting down servers...")


def main():
    """Main entry point."""
    print("Starting Midnight development servers...")
    try:
        asyncio.run(start_servers())
    except KeyboardInterrupt:
        print("\nServers stopped.")


if __name__ == "__main__":
    main()
