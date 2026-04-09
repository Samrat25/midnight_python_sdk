---
inclusion: auto
description: Docker Compose setup and testing patterns for Midnight local development. Covers service orchestration, health checks, pytest fixtures, and integration testing with containerized services.
---

# Docker & Testing for Midnight Development

## Docker Compose Architecture

### Service Stack

```yaml
services:
  midnight-node:
    build: ./docker/node
    ports: ["9944:9944"]
    environment:
      - NETWORK_ID=undeployed
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9944"]
      interval: 10s
      timeout: 5s
      retries: 5

  midnight-indexer:
    build: ./docker/indexer
    ports: ["8088:8088"]
    depends_on:
      - midnight-node
    environment:
      - NODE_URL=http://midnight-node:9944

  midnight-proof:
    build: ./docker/proof
    ports: ["6300:6300"]
    environment:
      - NETWORK_ID=undeployed
```

## Service Health Checks

```python
import httpx
import time

def wait_for_services(timeout: int = 60):
    """Wait for all services to be ready"""
    services = {
        "node": "http://localhost:9944",
        "indexer": "http://localhost:8088/api/v4/graphql",
        "proof": "http://localhost:6300"
    }
    
    start = time.time()
    while time.time() - start < timeout:
        all_ready = True
        for name, url in services.items():
            try:
                response = httpx.get(url, timeout=5.0)
                if response.status_code not in [200, 404]:
                    all_ready = False
            except:
                all_ready = False
        
        if all_ready:
            return True
        time.sleep(2)
    
    raise TimeoutError("Services did not start in time")
```

## pytest Fixtures

```python
import pytest
from midnight_sdk import MidnightClient

@pytest.fixture(scope="session")
def docker_services():
    """Start Docker services once per test session"""
    import subprocess
    subprocess.run(["docker-compose", "up", "-d"], check=True)
    wait_for_services()
    yield
    subprocess.run(["docker-compose", "down"], check=True)

@pytest.fixture
def client(docker_services):
    """Provide MidnightClient with services running"""
    return MidnightClient(network="undeployed")

@pytest.fixture
def wallet_with_funds(client):
    """Provide funded wallet for testing"""
    mnemonic = "test test test test test test test test test test test junk"
    address = client.wallet.get_real_address(mnemonic)
    # Fund wallet in local network
    return {"address": address, "mnemonic": mnemonic}
```

## Integration Testing

```python
def test_full_workflow(client, wallet_with_funds):
    """Test complete contract deployment and interaction"""
    # 1. Deploy contract
    contract = client.contracts.deploy(
        "contracts/hello_world.compact",
        wallet=wallet_with_funds["address"]
    )
    assert contract.address
    
    # 2. Call circuit
    result = contract.call(
        "storeMessage",
        args={"message": "Hello Test"},
        private_key=wallet_with_funds["private_key"]
    )
    assert result.tx_hash
    
    # 3. Read state
    state = contract.get_state()
    assert state["message"] == "Hello Test"
```

## Mock Services for Unit Tests

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_proof_server():
    """Mock proof server for unit tests"""
    with patch('midnight_sdk.proof.ProofClient') as mock:
        mock.return_value.generate_proof.return_value = {
            "proof": "0x1234...",
            "proof_hash": "0xabcd..."
        }
        yield mock

def test_ai_inference_without_docker(mock_proof_server):
    """Test AI inference logic without real proof server"""
    from midnight_sdk.ai import ZKInferenceEngine
    engine = ZKInferenceEngine(client)
    result = engine.predict_private([5.1, 3.5, 1.4, 0.2])
    assert result.prediction in ["setosa", "versicolor", "virginica"]
```

## Docker Build Patterns

```dockerfile
# docker/node/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY server.py blockchain.py ./
RUN pip install aiohttp

EXPOSE 9944
CMD ["python", "server.py"]
```

## Service Startup Script

```python
#!/usr/bin/env python3
"""Start all Midnight services"""

import subprocess
import sys
import time

def start_services():
    print("Starting Midnight services...")
    subprocess.run(["docker-compose", "up", "-d"], check=True)
    
    print("Waiting for services to be ready...")
    wait_for_services(timeout=60)
    
    print("✓ All services ready")
    print("  Node:    http://localhost:9944")
    print("  Indexer: http://localhost:8088")
    print("  Proof:   http://localhost:6300")

if __name__ == "__main__":
    try:
        start_services()
    except Exception as e:
        print(f"✗ Failed to start services: {e}")
        sys.exit(1)
```

## Testing Best Practices

1. **Use session-scoped fixtures** for Docker services
2. **Mock external services** for unit tests
3. **Test with real services** for integration tests
4. **Clean up after tests** with teardown fixtures
5. **Use health checks** to ensure services are ready
6. **Parallel test execution** with pytest-xdist
7. **Test both success and failure paths**

## Common Issues

### Services Not Starting

```bash
# Check logs
docker-compose logs midnight-node

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Port Conflicts

```bash
# Check what's using ports
lsof -i :9944
lsof -i :8088
lsof -i :6300

# Kill processes
kill -9 <PID>
```

### Slow Tests

```python
# Use pytest-xdist for parallel execution
pytest -n auto tests/

# Skip slow tests in development
@pytest.mark.slow
def test_full_deployment():
    pass

# Run only fast tests
pytest -m "not slow"
```

## When to Use This Skill

- Setting up Docker Compose for local development
- Writing integration tests with Docker services
- Creating pytest fixtures for services
- Debugging service connectivity issues
- Optimizing test execution speed
- Mocking services for unit tests
