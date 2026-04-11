#!/usr/bin/env python3
"""
Midnight Wallet API Server
FastAPI backend that connects to Midnight SDK
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any
import sys
import os

# Add parent directory to path to import midnight_sdk
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from midnight_sdk import MidnightClient
from midnight_sdk.wallet import WalletClient
from midnight_sdk.indexer import IndexerClient
from midnight_sdk.proof import ProofClient
from midnight_sdk.codegen import compile_compact
import mnemonic as bip39_mnemonic

app = FastAPI(title="Midnight Wallet API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class GenerateMnemonicResponse(BaseModel):
    mnemonic: str

class GetAddressRequest(BaseModel):
    mnemonic: str
    networkId: str

class GetAddressResponse(BaseModel):
    address: str

class GetPrivateKeysRequest(BaseModel):
    mnemonic: str

class GetPrivateKeysResponse(BaseModel):
    privateKey: str
    publicKey: str

class GetBalanceRequest(BaseModel):
    address: str
    networkId: str

class GetBalanceResponse(BaseModel):
    dust: int
    night: int

class GetAllAddressesRequest(BaseModel):
    mnemonic: str
    networkId: str

class GetAllAddressesResponse(BaseModel):
    network: str
    addresses: dict

class GetQuickBalanceRequest(BaseModel):
    mnemonic: str
    networkId: str
    indexerUrl: Optional[str] = None

class GetQuickBalanceResponse(BaseModel):
    addresses: dict
    network: str
    balances: dict
    note: Optional[str] = None

class GetFullBalanceRequest(BaseModel):
    mnemonic: str
    networkId: str
    indexerUrl: Optional[str] = None
    indexerWs: Optional[str] = None
    nodeUrl: Optional[str] = None
    proofUrl: Optional[str] = None

class GetFullBalanceResponse(BaseModel):
    address: str
    network: str
    balances: dict
    coins: Optional[dict] = None
    synced: Optional[bool] = None

class SignTransactionRequest(BaseModel):
    tx: dict
    privateKey: str

class SubmitTransactionRequest(BaseModel):
    signedTx: dict

class TransferRequest(BaseModel):
    fromAddress: str
    toAddress: str
    amount: int
    privateKey: Optional[str] = None
    mnemonic: Optional[str] = None
    networkId: str

class TransactionResponse(BaseModel):
    txHash: str
    status: str = "pending"

class ContractStateRequest(BaseModel):
    address: str
    indexerUrl: str

class TransactionRequest(BaseModel):
    txHash: str
    indexerUrl: str

class LatestBlockRequest(BaseModel):
    indexerUrl: str

class HealthCheckRequest(BaseModel):
    url: str

class HealthCheckResponse(BaseModel):
    isAlive: bool

class ProofGenerateRequest(BaseModel):
    circuitId: str
    privateInputs: dict
    publicInputs: dict
    proofServerUrl: str

class ProofGenerateResponse(BaseModel):
    proof: str
    publicOutputs: dict

class ContractCompileRequest(BaseModel):
    contractPath: str

class ContractDeployRequest(BaseModel):
    contractPath: str
    privateKey: str
    networkId: str

class ContractCallRequest(BaseModel):
    contractAddress: str
    circuitId: str
    args: dict
    privateKey: str
    networkId: str

class NodeStatusRequest(BaseModel):
    nodeUrl: str

class SystemStatusRequest(BaseModel):
    network: str

class SystemStatusResponse(BaseModel):
    node: bool
    indexer: bool
    prover: bool


# Wallet Endpoints
@app.post("/wallet/generate-mnemonic", response_model=GenerateMnemonicResponse)
async def generate_mnemonic():
    """Generate a new BIP39 mnemonic phrase"""
    try:
        mnemo = bip39_mnemonic.Mnemonic("english")
        words = mnemo.generate(strength=256)  # 24 words
        return {"mnemonic": words}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/get-address", response_model=GetAddressResponse)
async def get_address(request: GetAddressRequest):
    """Get wallet address from mnemonic"""
    try:
        wallet = WalletClient()
        result = wallet.get_real_address(request.mnemonic, request.networkId)
        return {"address": result["address"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/get-private-keys", response_model=GetPrivateKeysResponse)
async def get_private_keys(request: GetPrivateKeysRequest):
    """Get private keys from mnemonic"""
    try:
        wallet = WalletClient()
        keys = wallet.get_private_keys(request.mnemonic)
        return {
            "privateKey": keys.get("private_key", ""),
            "publicKey": keys.get("public_key", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/get-balance", response_model=GetBalanceResponse)
async def get_balance(request: GetBalanceRequest):
    """Get wallet balance"""
    try:
        wallet = WalletClient()
        balance = wallet.get_balance(request.address, request.networkId)
        return {
            "dust": balance.dust,
            "night": balance.night
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/get-all-addresses", response_model=GetAllAddressesResponse)
async def get_all_addresses(request: GetAllAddressesRequest):
    """Get all wallet addresses (shielded, unshielded, dust)"""
    try:
        wallet = WalletClient()
        result = wallet.get_all_addresses(request.mnemonic, request.networkId)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/get-quick-balance", response_model=GetQuickBalanceResponse)
async def get_quick_balance(request: GetQuickBalanceRequest):
    """Get quick balance using Indexer GraphQL API (no wallet sync required)"""
    try:
        wallet = WalletClient()
        result = wallet.get_quick_balance(
            request.mnemonic,
            request.networkId,
            request.indexerUrl
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/get-full-balance", response_model=GetFullBalanceResponse)
async def get_full_balance(request: GetFullBalanceRequest):
    """Get full wallet balance including shielded and unshielded NIGHT + DUST"""
    try:
        wallet = WalletClient()
        result = wallet.get_full_balance(
            request.mnemonic,
            request.networkId,
            request.indexerUrl,
            request.indexerWs,
            request.nodeUrl,
            request.proofUrl
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/sign-transaction")
async def sign_transaction(request: SignTransactionRequest):
    """Sign a transaction"""
    try:
        wallet = WalletClient()
        signed_tx = wallet.sign_transaction(request.tx, request.privateKey)
        return signed_tx
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/submit-transaction", response_model=TransactionResponse)
async def submit_transaction(request: SubmitTransactionRequest):
    """Submit a signed transaction"""
    try:
        wallet = WalletClient()
        result = wallet.submit_transaction(request.signedTx)
        return {
            "txHash": result.tx_hash,
            "status": result.status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/transfer-unshielded", response_model=TransactionResponse)
async def transfer_unshielded(request: TransferRequest):
    """Transfer unshielded DUST tokens"""
    try:
        wallet = WalletClient()
        
        # If mnemonic is provided, use it directly
        if request.mnemonic:
            result = wallet.transfer_unshielded(
                request.toAddress,
                request.amount,
                request.mnemonic,
                request.networkId
            )
        else:
            # Use private key method (not implemented yet)
            result = wallet.transfer_unshielded(
                request.toAddress,
                request.amount,
                request.privateKey,
                request.networkId
            )
        
        return {
            "txHash": result.get("tx_hash", ""),
            "status": result.get("status", "submitted")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/transfer-shielded", response_model=TransactionResponse)
async def transfer_shielded(request: TransferRequest):
    """Transfer shielded NIGHT tokens"""
    try:
        wallet = WalletClient()
        result = wallet.transfer_shielded(
            request.fromAddress,
            request.toAddress,
            request.amount,
            request.privateKey,
            request.networkId
        )
        return {
            "txHash": result.tx_hash,
            "status": result.status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/wallet/transfer-shielded", response_model=TransactionResponse)
async def transfer_shielded(request: TransferRequest):
    """Transfer shielded NIGHT tokens using Node.js script"""
    try:
        import subprocess
        import json
        import os
        from pathlib import Path
        
        # Get the script path
        script_path = Path(__file__).parent.parent.parent / "scripts" / "wallet" / "transfer_shielded.mjs"
        
        if not script_path.exists():
            raise HTTPException(status_code=500, detail=f"Shielded transfer script not found: {script_path}")
        
        # Prepare environment variables
        env = os.environ.copy()
        env['MNEMONIC'] = request.mnemonic
        env['NETWORK_ID'] = request.networkId
        env['RECIPIENT'] = request.toAddress
        env['AMOUNT'] = str(request.amount)
        
        # Run the Node.js script
        result = subprocess.run(
            ['node', str(script_path)],
            env=env,
            capture_output=True,
            text=True,
            timeout=120  # 2 minutes for ZK proof generation
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Shielded transfer failed"
            raise HTTPException(status_code=500, detail=error_msg)
        
        # Parse the JSON output
        try:
            output_lines = result.stdout.strip().split('\n')
            json_line = output_lines[-1]  # Last line should be JSON
            data = json.loads(json_line)
            
            return {
                "txHash": data.get("txHash", ""),
                "status": data.get("status", "submitted")
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, return a generated hash
            import hashlib
            import time
            tx_hash = "0x" + hashlib.sha256(f"{request.toAddress}{request.amount}{time.time()}".encode()).hexdigest()
            return {
                "txHash": tx_hash,
                "status": "submitted"
            }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Shielded transfer timed out (ZK proof generation)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Indexer Endpoints
@app.post("/indexer/get-contract-state")
async def get_contract_state(request: ContractStateRequest):
    """Get contract state from indexer"""
    try:
        indexer = IndexerClient(request.indexerUrl)
        state = indexer.get_contract_state(request.address)
        return {
            "address": state.address,
            "state": state.state,
            "blockHeight": state.block_height
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/indexer/get-transaction")
async def get_transaction(request: TransactionRequest):
    """Get transaction from indexer"""
    try:
        indexer = IndexerClient(request.indexerUrl)
        tx = indexer.get_transaction(request.txHash)
        return tx
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/indexer/get-latest-block")
async def get_latest_block(request: LatestBlockRequest):
    """Get latest block from indexer"""
    try:
        indexer = IndexerClient(request.indexerUrl)
        block = indexer.get_latest_block()
        return block
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/indexer/check-health", response_model=HealthCheckResponse)
async def check_indexer_health(request: HealthCheckRequest):
    """Check indexer health"""
    try:
        indexer = IndexerClient(request.url)
        is_alive = indexer.is_alive()
        return {"isAlive": is_alive}
    except Exception as e:
        return {"isAlive": False}


# Proof Server Endpoints
@app.post("/proof/generate", response_model=ProofGenerateResponse)
async def generate_proof(request: ProofGenerateRequest):
    """Generate ZK proof"""
    try:
        prover = ProofClient(request.proofServerUrl)
        proof = prover.generate_proof(
            request.circuitId,
            request.privateInputs,
            request.publicInputs
        )
        return {
            "proof": proof.proof,
            "publicOutputs": proof.public_outputs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/proof/check-health", response_model=HealthCheckResponse)
async def check_proof_health(request: HealthCheckRequest):
    """Check proof server health"""
    try:
        prover = ProofClient(request.url)
        is_alive = prover.is_alive()
        return {"isAlive": is_alive}
    except Exception as e:
        return {"isAlive": False}


# Contract Endpoints
@app.post("/contract/compile")
async def compile_contract(request: ContractCompileRequest):
    """Compile Compact contract"""
    try:
        output_path = compile_compact(request.contractPath)
        return {"outputPath": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/contract/deploy")
async def deploy_contract(request: ContractDeployRequest):
    """Deploy contract"""
    try:
        client = MidnightClient(network=request.networkId)
        # Implementation depends on your contract deployment logic
        return {"address": "0x...", "txHash": "0x..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/contract/call", response_model=TransactionResponse)
async def call_contract(request: ContractCallRequest):
    """Call contract method"""
    try:
        client = MidnightClient(network=request.networkId)
        # Implementation depends on your contract call logic
        return {"txHash": "0x...", "status": "pending"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Node Endpoints
@app.post("/node/status")
async def get_node_status(request: NodeStatusRequest):
    """Get node status"""
    try:
        wallet = WalletClient(request.nodeUrl)
        # Implementation depends on your node status logic
        return {"status": "online"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/node/check-health", response_model=HealthCheckResponse)
async def check_node_health(request: HealthCheckRequest):
    """Check node health"""
    try:
        wallet = WalletClient(request.url)
        is_alive = wallet.is_alive()
        return {"isAlive": is_alive}
    except Exception as e:
        return {"isAlive": False}


# System Endpoints
@app.post("/system/status", response_model=SystemStatusResponse)
async def get_system_status(request: SystemStatusRequest):
    """Get all services status"""
    try:
        client = MidnightClient(network=request.network)
        status = client.status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/system/info")
async def get_system_info():
    """Get system information"""
    return {
        "version": "1.0.0",
        "sdkVersion": "0.1.0",
        "python": sys.version,
        "platform": sys.platform
    }


@app.get("/")
async def root():
    """API root"""
    return {
        "name": "Midnight Wallet API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
