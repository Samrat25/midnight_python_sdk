# Midnight Python SDK - Deployment Guide

Complete guide for deploying and using the Midnight Python SDK with transaction signing.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Starting Services](#starting-services)
5. [CLI Commands](#cli-commands)
6. [Transaction Management](#transaction-management)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 22+** - [Download](https://nodejs.org/) (for wallet SDK)
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
- **WSL/Ubuntu** (Windows only) - For contract compilation

### Required Files

- `mnemonic.txt` - Your 24-word mnemonic phrase (DO NOT commit to git!)
- `.gitignore` - Must include `mnemonic.txt`

## Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd midnightsdk
```

### 2. Install Python Dependencies

```bash
pip install -e .
```

This installs:
- `midnight-sdk` package
- `midnight-sdk` CLI command
- All dependencies (httpx, typer, rich, sklearn, etc.)

### 3. Install Node.js Dependencies

```bash
npm install
```

This installs the Midnight wallet SDK for address derivation and key management.

### 4. Verify Installation

```bash
# Check CLI is installed
midnight-sdk --help

# Check Python package
python -c "from midnight_sdk import MidnightClient; print('OK')"
```

## Configuration

### 1. Create Mnemonic File

Create `mnemonic.txt` in the project root:

```
your twenty four word mnemonic phrase goes here in this file
```

**IMPORTANT**: Add to `.gitignore`:

```
mnemonic.txt
*.txt
.wallet_*.json
```

### 2. Fund Your Wallet

Get your wallet address:

```bash
node get_wallet_address.mjs
```

Fund it using the [Midnight Faucet](https://faucet.midnight.network/).

### 3. Configure Docker Services

The `docker-compose.yml` is pre-configured with:
- Proof Server (port 6300)
- Node Server (port 9944)
- Indexer/Explorer (port 8088)

Data persists in `./data/node/` directory.

## Starting Services

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Check status
docker ps

# View logs
docker logs midnightsdk-midnight-node-1
docker logs midnightsdk-midnight-indexer-1
docker logs midnightsdk-proof-server-1

# Stop services
docker-compose down
```

### Option 2: Python Scripts (Development)

```bash
# Start services without Docker
python start_services.py

# Stop with Ctrl+C
```

### Verify Services

```bash
# Check all services
midnight-sdk status

# Or manually
curl http://localhost:6300/health  # Proof server
curl http://localhost:9944/health  # Node
curl http://localhost:8088/health  # Indexer
```

## CLI Commands

### Service Status

```bash
midnight-sdk status
```

Shows status of all Midnight services (node, indexer, prover).

### AI Inference

#### Train Model

```bash
midnight-sdk ai train
```

Trains the iris classification model.

#### Run Inference (No Transaction)

```bash
midnight-sdk ai infer --features "5.1,3.5,1.4,0.2"
```

Runs ZK inference without submitting a transaction.

#### Run Inference with Transaction Signing

```bash
midnight-sdk ai infer --features "5.1,3.5,1.4,0.2" --sign
```

Runs ZK inference and submits a signed transaction to the blockchain.

**Output:**
- Prediction and confidence
- ZK proof hash
- Transaction hash
- Explorer URL

### Transaction Management

#### List All Transactions

```bash
midnight-sdk tx list
```

Shows all transactions grouped by status (pending, confirmed, rejected).

#### Check Transaction Status

```bash
midnight-sdk tx status <tx_hash>
```

Shows detailed information about a specific transaction.

#### Approve Pending Transaction

```bash
midnight-sdk tx approve <tx_hash>
```

Manually confirms a pending transaction.

#### Reject Pending Transaction

```bash
midnight-sdk tx reject <tx_hash> "Reason for rejection"
```

Manually rejects a pending transaction with a reason.

### Contract Operations

#### Deploy Contract

```bash
midnight-sdk deploy contracts/hello_world.compact --wallet <address> --sign
```

Deploys a compiled contract with transaction signing.

#### Call Contract Function

```bash
midnight-sdk call <contract_address> <circuit_name> \
  --wallet <address> \
  --args '{"key": "value"}' \
  --sign
```

Calls a circuit function on a deployed contract.

### Wallet Operations

#### Check Balance

```bash
midnight-sdk balance <wallet_address>
```

Shows DUST and NIGHT token balances.

#### Get Wallet Address

```bash
node get_wallet_address.mjs
```

Derives wallet address from mnemonic.

#### Get Private Keys

```bash
node get_private_key.mjs
```

Derives private keys from mnemonic (use with caution!).

## Transaction Management

### Transaction Lifecycle

```
Submit → Pending (3 sec) → Confirmed
                        ↘ Rejected (manual)
```

### Auto-Confirmation

By default, transactions are automatically confirmed after 3 seconds. This simulates:
- Block production time
- Contract execution
- Proof verification

### Manual Approval Workflow

1. **Submit transaction**
   ```bash
   midnight-sdk ai infer --features "5.1,3.5,1.4,0.2" --sign
   ```

2. **List pending transactions**
   ```bash
   midnight-sdk tx list
   ```

3. **Review transaction**
   ```bash
   midnight-sdk tx status <tx_hash>
   ```

4. **Approve or reject**
   ```bash
   # Approve
   midnight-sdk tx approve <tx_hash>
   
   # Or reject
   midnight-sdk tx reject <tx_hash> "Invalid proof"
   ```

5. **View in explorer**
   ```
   http://localhost:8088/tx/<tx_hash>
   ```

### Transaction Status Colors

In the explorer UI:
- 🟠 **Orange** = Pending
- 🟢 **Green** = Confirmed
- 🔴 **Red** = Rejected

## Examples

### Example 1: Simple AI Inference

```bash
# Train model
midnight-sdk ai train

# Run inference
midnight-sdk ai infer --features "5.1,3.5,1.4,0.2"
```

### Example 2: AI Inference with Transaction

```bash
# Run inference and submit transaction
midnight-sdk ai infer --features "5.1,3.5,1.4,0.2" --sign

# Wait 4 seconds for auto-confirmation

# Check status
midnight-sdk tx list
```

### Example 3: Complete Workflow

```bash
# Run the complete workflow demo
python examples/complete_transaction_workflow.py
```

This demonstrates:
1. Client initialization
2. Model training
3. Private key derivation
4. ZK inference
5. Transaction submission
6. Status checking
7. Auto-confirmation
8. Explorer integration

### Example 4: Manual Transaction Approval

```bash
# Submit transaction
midnight-sdk ai infer --features "5.1,3.5,1.4,0.2" --sign

# Get transaction hash from output
TX_HASH="<transaction_hash>"

# Check status (should be pending)
midnight-sdk tx status $TX_HASH

# Manually approve
midnight-sdk tx approve $TX_HASH

# Verify confirmed
midnight-sdk tx status $TX_HASH
```

### Example 5: Using Python API

```python
from midnight_sdk import MidnightClient
from pathlib import Path

# Initialize client
client = MidnightClient(
    network="undeployed",
    wallet_address="mn_addr_...",
    proof_server_url="http://localhost:6300"
)

# Get private key
mnemonic = Path("mnemonic.txt").read_text().strip()
keys = client.wallet.get_private_keys(mnemonic)
private_key = keys['nightExternal']

# Run inference with signing
result = client.ai.predict_private(
    features=[5.1, 3.5, 1.4, 0.2],
    sign_transaction=True,
    private_key=private_key
)

print(f"Prediction: {result.prediction}")
print(f"Transaction: {result.transaction_hash}")
```

## Troubleshooting

### Services Not Starting

**Problem**: Docker containers show as "unhealthy"

**Solution**:
```bash
# Check logs
docker logs midnightsdk-midnight-node-1

# Restart services
docker-compose restart

# Rebuild if needed
docker-compose up -d --build
```

### Port Conflicts

**Problem**: Port 9944 or 8088 already in use

**Solution**:
```bash
# Windows
netstat -ano | Select-String ":9944"
Stop-Process -Id <PID> -Force

# Linux/Mac
lsof -i :9944
kill -9 <PID>
```

### Transaction Stuck in Pending

**Problem**: Transaction not auto-confirming

**Solution**:
```bash
# Manually approve
midnight-sdk tx approve <tx_hash>

# Or check node logs
docker logs midnightsdk-midnight-node-1
```

### Mnemonic Not Found

**Problem**: `ERROR: mnemonic.txt not found`

**Solution**:
```bash
# Create mnemonic.txt in project root
echo "your twenty four word mnemonic here" > mnemonic.txt

# Verify
cat mnemonic.txt
```

### Wallet Not Funded

**Problem**: Insufficient balance for transactions

**Solution**:
1. Get wallet address: `node get_wallet_address.mjs`
2. Fund at: https://faucet.midnight.network/
3. Verify: `midnight-sdk balance <address>`

### Contract Compilation Errors

**Problem**: `compactc` not found or compilation fails

**Solution**:
```bash
# Windows: Install WSL/Ubuntu
wsl --install

# Install compactc in WSL
# Follow Midnight documentation

# Verify
wsl compactc --version
```

### Explorer Not Showing Transaction

**Problem**: Transaction not visible in explorer

**Solution**:
```bash
# Check if transaction exists in node
curl http://localhost:9944/tx/<tx_hash>

# Restart indexer
docker-compose restart midnight-indexer

# Check indexer logs
docker logs midnightsdk-midnight-indexer-1
```

## Production Deployment

For production use:

1. **Disable auto-confirmation** - Require manual approval
2. **Add authentication** - Protect approval endpoints
3. **Use real Midnight testnet** - Connect to testnet-02
4. **Implement proper key management** - Use hardware wallets/HSMs
5. **Add monitoring** - Track transaction success rates
6. **Enable HTTPS** - Secure all endpoints
7. **Add rate limiting** - Prevent spam transactions
8. **Implement backup** - Regular database backups

## Next Steps

- Deploy contracts to Midnight testnet
- Integrate with real Midnight explorer
- Add multi-signature approval workflow
- Implement transaction batching
- Add gas fee estimation
- Create production monitoring dashboard

## Support

- Documentation: `README.md`, `TRANSACTION_MANAGEMENT.md`
- Examples: `examples/` directory
- Issues: GitHub Issues
- Community: Midnight Discord

## License

See `LICENSE` file for details.
