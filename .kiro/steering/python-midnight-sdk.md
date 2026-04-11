---
inclusion: auto
description: Python development patterns for the Midnight Python SDK. Covers async patterns, type hints, Pydantic models, error handling, testing with pytest, and SDK architecture patterns.
---

# Python Midnight SDK Development Patterns

## Core Principles

1. **Type Safety**: Use type hints everywhere with Pydantic models
2. **Async First**: Use httpx for async HTTP, support both sync/async APIs
3. **Error Handling**: Custom exceptions with clear error messages
4. **Testing**: pytest with fixtures for Docker services
5. **Documentation**: Docstrings with examples

## SDK Architecture Pattern

```python
# client.py - Main entry point
class MidnightClient:
    def __init__(self, network: str = "preprod"):
        self.wallet = WalletClient(...)
        self.indexer = IndexerClient(...)
        self.prover = ProofClient(...)
        self.contracts = ContractClient(...)
        self.ai = ZKInferenceEngine(self)
```

## Pydantic Models

```python
from pydantic import BaseModel, Field

class Balance(BaseModel):
    dust: int = Field(ge=0, description="DUST balance")
    night: int = Field(ge=0, description="NIGHT balance (shielded)")

class TransactionResult(BaseModel):
    tx_hash: str
    status: str
    explorer_url: str | None = None
```

## Error Handling

```python
# exceptions.py
class MidnightSDKError(Exception):
    """Base exception for all SDK errors"""
    pass

class ProofGenerationError(MidnightSDKError):
    """Raised when ZK proof generation fails"""
    pass

# Usage
try:
    proof = client.prover.generate_proof(...)
except ProofGenerationError as e:
    print(f"Proof failed: {e}")
```

## Async HTTP with httpx

```python
import httpx

class IndexerClient:
    def __init__(self, url: str):
        self._http = httpx.Client(timeout=60.0)
    
    def query(self, gql: str) -> dict:
        response = self._http.post(
            self.url,
            json={"query": gql},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
```

## Testing with pytest

```python
import pytest
from midnight_sdk import MidnightClient

@pytest.fixture
def client():
    return MidnightClient(network="undeployed")

def test_status(client):
    status = client.status()
    assert "node" in status
    assert "indexer" in status
    assert "prover" in status
```

## CLI with Click

```python
import click

@click.group()
def cli():
    """Midnight Python SDK CLI"""
    pass

@cli.command()
def status():
    """Check service status"""
    client = MidnightClient()
    status = client.status()
    for service, alive in status.items():
        click.echo(f"{service}: {'✓' if alive else '✗'}")
```

## Subprocess for Node.js Integration

```python
import subprocess
import json
from pathlib import Path

def get_wallet_address(mnemonic: str) -> str:
    """Call Node.js wallet SDK via subprocess"""
    script = Path("get_wallet_address.mjs")
    result = subprocess.run(
        ["node", str(script)],
        capture_output=True,
        text=True,
        timeout=30,
        env={"MNEMONIC": mnemonic}
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return data["address"]
    raise WalletError(f"Failed: {result.stderr}")
```

## Best Practices

1. **Always use type hints**: `def get_balance(address: str) -> Balance:`
2. **Validate with Pydantic**: Models auto-validate input data
3. **Raise custom exceptions**: Never use generic `Exception`
4. **Add docstrings with examples**: Help users understand usage
5. **Test with Docker**: Use pytest fixtures for service dependencies
6. **Support both networks**: Local (undeployed) and remote (preprod/testnet)
7. **Graceful degradation**: Warn but don't fail if optional services unavailable

## File Organization

```
midnight_sdk/
├── __init__.py          # Public API exports
├── client.py            # Main MidnightClient
├── wallet.py            # WalletClient
├── indexer.py           # IndexerClient
├── proof.py             # ProofClient
├── contract.py          # ContractClient
├── ai.py                # ZKInferenceEngine
├── models.py            # Pydantic models
├── exceptions.py        # Custom exceptions
├── codegen.py           # Auto-codegen from Compact
└── cli.py               # Click CLI
```

## When to Use This Skill

- Writing new SDK modules
- Adding new API methods
- Creating Pydantic models
- Implementing error handling
- Writing tests
- Building CLI commands
- Integrating with Node.js wallet SDK
