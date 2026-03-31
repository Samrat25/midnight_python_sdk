#!/usr/bin/env python3
"""
Mock Midnight Proof Server
Simulates ZK proof generation
"""

import asyncio
import json
import hashlib
from datetime import datetime
from aiohttp import web


async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "service": "midnight-proof-server"
    })


async def generate_proof(request):
    """Generate a ZK proof"""
    data = await request.json()
    circuit_id = data.get("circuitId", "")
    private_inputs = data.get("privateInputs", {})
    public_inputs = data.get("publicInputs", {})
    
    # Simulate proof generation delay (real proofs take 10-30 seconds)
    # For demo purposes, we'll make it faster
    await asyncio.sleep(2)
    
    # Generate mock proof
    proof_data = f"{circuit_id}{json.dumps(private_inputs)}{json.dumps(public_inputs)}"
    proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()
    
    # Create a realistic-looking ZK proof
    proof = f"zk_snark_proof_{proof_hash}"
    
    return web.json_response({
        "proof": proof,
        "publicOutputs": {
            **public_inputs,
            "verified": True,
            "timestamp": datetime.utcnow().isoformat(),
            "circuitId": circuit_id
        }
    })


async def verify_proof(request):
    """Verify a ZK proof"""
    data = await request.json()
    proof = data.get("proof", "")
    
    # Simulate verification
    await asyncio.sleep(0.5)
    
    return web.json_response({
        "valid": True,
        "verified_at": datetime.utcnow().isoformat()
    })


async def init_app():
    """Initialize the application"""
    app = web.Application()
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_post('/prove', generate_proof)
    app.router.add_post('/verify', verify_proof)
    
    return app


def main():
    """Main entry point"""
    print("Starting Midnight Proof Server Mock on port 6300...")
    app = asyncio.run(init_app())
    web.run_app(app, host='0.0.0.0', port=6300)


if __name__ == "__main__":
    main()
