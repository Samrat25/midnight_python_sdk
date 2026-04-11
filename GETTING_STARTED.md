# 🚀 Getting Started: Wallet Creation & Contract Deployment

Complete guide to creating a wallet and deploying your first contract on Midnight.

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.11+
- Docker & Docker Compose
- Node.js 22+
- Git

## Step 1: Install the SDK

```bash
# Clone the repository
git clone https://github.com/yourusername/midnight-python-sdk.git
cd midnight-python-sdk

# Install Python package
pip install -e .

# Install Node.js dependencies (for wallet SDK)
npm install

# Verify installation
midnight-sdk --help
```

## Step 2: Start Local Services

For local development, start the Docker services:

```bash
# Start all services (node, indexer, proof server)
docker-compose up -d

# Wait a few seconds for services to start
sleep 10

# Check service status
midnight-sdk status
```

You should see:
```
✓ Node:    http://localhost:9944
✓ Indexer: http://localhost:8088
✓ Proof:   http://localhost:6300
```

## Step 3: Create a Wallet

### Option A: Generate New Mnemonic (Recommended for Testing)

```bash
# Generate a new 24-word mnemonic
python -c "from mnemonic import Mnemonic; print(Mnemonic('english').generate(strength=256))"
```

This outputs something like:
```
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art
```

### Option B: Use Existing Mnemonic

If you already have a mnemonic from another wallet, you can use it.

### Save Your Mnemonic

```bash
# Create mnemonic.txt file
echo "your twenty four word mnemonic phrase goes here" > mnemonic.txt

# IMPORTANT: Keep this file secure and never commit it to git
```

## Step 4: Get Your Wallet Address

### For Local Network (undeployed)

```bash
# Derive your wallet address
node get_wallet_address.mjs
```

This will output:
```json
{
  "address": "mn_addr_undeployed1zaa268rc7sjz0cts...",
  "dust": "0",
  "night": "0"
}
```

### For Preprod Network

```bash
# Set network environment variable
export NETWORK_ID=preprod

# Get preprod address
node get_wallet_address.mjs
```

**Save your address** - you'll need it for the next steps!

## Step 5: Fund Your Wallet

### For Local Network (undeployed)

Local network wallets are automatically funded when you interact with them. No manual funding needed!

### For Preprod Network

1. Visit the faucet: https://faucet.preprod.midnight.network/
2. Paste your wallet address
3. Request tNIGHT tokens
4. Wait 2-3 minutes for funding

### Verify Balance

```bash
# Check your balance
midnight-sdk balance mn_addr_undeployed1your_address_here

# Or use auto-detection
midnight-sdk explore mn_addr_undeployed1your_address_here
```

## Step 6: Choose a Contract to Deploy

The SDK includes 5 sample contracts:

### 1. Hello World (Simplest)
```bash
contracts/hello_world.compact
```
- Stores a message on-chain
- Circuit: `storeMessage(newMessage)`
- Perfect for first deployment

### 2. Counter
```bash
contracts/counter.compact
```
- Increments a counter
- Circuit: `increment()`
- Demonstrates state management

### 3. Bulletin Board
```bash
contracts/bulletin_board.compact
```
- Anonymous message posting
- Circuit: `post(message)`
- Privacy-preserving

### 4. AI Inference
```bash
contracts/ai_inference.compact
```
- ZK-ML inference
- Circuit: `submit_inference_result()`
- Advanced privacy features

### 5. Private Vote
```bash
contracts/private_vote.compact
```
- Anonymous voting
- Circuits: `voteYes()`, `voteNo()`
- Demonstrates commitments

## Step 7: Deploy Your First Contract

### Method 1: Using Python SDK (Recommended)

Create a deployment script `deploy_hello_world.py`:

```python
from midnight_sdk import MidnightClient
from pathlib import Path

# Initialize client
client = MidnightClient(network="undeployed")

# Get your mnemonic
mnemonic = Path("mnemonic.txt").read_text().strip()

# Get wallet address
wallet_info = client.wallet.get_real_address(mnemonic)
wallet_address = wallet_info["address"]

print(f"Deploying from wallet: {wallet_address}")

# Get private key for signing
keys = client.wallet.get_private_keys(mnemonic)
private_key = keys['nightExternal']

# Deploy the contract
print("Deploying hello_world contract...")
contract = client.contracts.deploy(
    contract_path="contracts/hello_world.compact",
    wallet_address=wallet_address,
    private_key=private_key
)

print(f"✓ Contract deployed!")
print(f"  Address: {contract.address}")
print(f"  Explorer: http://localhost:8088/contract/{contract.address}")

# Save contract address for later use
Path("deployed_contract.txt").write_text(contract.address)
```

Run it:
```bash
python deploy_hello_world.py
```

### Method 2: Using CLI

```bash
# Get your private key
export MIDNIGHT_KEY=$(node get_private_key.mjs | jq -r '.nightExternal')

# Get your wallet address
export WALLET_ADDR=$(node get_wallet_address.mjs | jq -r '.address')

# Deploy contract
midnight-sdk deploy contracts/hello_world.compact \
  --wallet $WALLET_ADDR \
  --key $MIDNIGHT_KEY
```

### Method 3: Using TypeScript (Production)

For production deployments, use the official TypeScript SDK. See `docs/DEPLOYMENT_GUIDE.md` for details.

## Step 8: Interact with Your Contract

### Call a Circuit

```python
from midnight_sdk import MidnightClient
from pathlib import Path

client = MidnightClient(network="undeployed")

# Load contract address
contract_address = Path("deployed_contract.txt").read_text().strip()

# Get private key
mnemonic = Path("mnemonic.txt").read_text().strip()
keys = client.wallet.get_private_keys(mnemonic)
private_key = keys['nightExternal']

# Load the contract
contract = client.get_contract(
    address=contract_address,
    circuit_ids=["storeMessage"]
)

# Call the storeMessage circuit
result = contract.call(
    circuit="storeMessage",
    args={"newMessage": "Hello Midnight!"},
    private_key=private_key
)

print(f"✓ Transaction submitted!")
print(f"  TX Hash: {result.tx_hash}")
print(f"  Explorer: http://localhost:8088/tx/{result.tx_hash}")
```

Or using CLI:
```bash
# Call circuit
midnight-sdk call <contract_address> storeMessage \
  --args '{"newMessage": "Hello Midnight!"}'
```

### Read Contract State

```python
# Read the current state
state = contract.get_state()
print(f"Current message: {state['message']}")
```

Or using CLI:
```bash
midnight-sdk state <contract_address>
```

## Step 9: View in Explorer

Open your browser to:
```
http://localhost:8088
```

You'll see:
- All transactions
- Contract deployments
- Transaction details
- Real-time updates

## 🎯 Quick Reference

### Essential Commands

```bash
# Check services
midnight-sdk status

# Get wallet address
node get_wallet_address.mjs

# Check balance
midnight-sdk balance <address>

# Deploy contract
midnight-sdk deploy contracts/hello_world.compact

# Call circuit
midnight-sdk call <contract_addr> <circuit_name> --args '{...}'

# Read state
midnight-sdk state <contract_addr>

# View transaction
midnight-sdk tx get <tx_hash>
```

### File Structure After Setup

```
midnight-python-sdk/
├── mnemonic.txt              # Your 24-word mnemonic (KEEP SECRET!)
├── deployed_contract.txt     # Contract address
├── contracts/
│   ├── hello_world.compact   # Your contract source
│   └── managed/              # Compiled contracts
└── data/                     # Blockchain data (local only)
```

## 🔐 Security Best Practices

1. **Never commit mnemonic.txt** - It's in .gitignore by default
2. **Use different mnemonics** for testnet and mainnet
3. **Keep private keys secure** - Never share them
4. **Test on local/preprod first** before mainnet
5. **Backup your mnemonic** - Write it down physically

## 🐛 Troubleshooting

### Services Not Starting

```bash
# Check Docker logs
docker-compose logs

# Restart services
docker-compose restart

# Clean restart
docker-compose down -v
docker-compose up -d
```

### "Proof server not running"

```bash
# Check proof server status
curl http://localhost:6300/health

# Restart proof server
docker-compose restart proof-server
```

### "Insufficient DUST balance"

For local network, DUST is auto-generated. For preprod:
1. Ensure you have tNIGHT tokens
2. Wait 2-5 minutes after funding
3. DUST accumulates from registered UTXOs

### "Contract compilation failed"

```bash
# Install Compact compiler
npm install -g @midnight-ntwrk/compact-compiler

# Verify installation
compact --version
```

## 📚 Next Steps

1. **Try other contracts** - Deploy counter, bulletin_board, etc.
2. **Run examples** - Check `examples/` directory
3. **Read documentation** - See `docs/` for detailed guides
4. **Test on preprod** - Deploy to real testnet
5. **Build your own contract** - Write custom `.compact` contracts

## 🎓 Learning Resources

- **Quick Start**: `docs/QUICK_START.md`
- **Contract Testing**: `docs/CONTRACT_TESTING_GUIDE.md`
- **Transaction Signing**: `docs/QUICK_SIGNING_GUIDE.md`
- **Production Setup**: `docs/PRODUCTION_SETUP.md`
- **Examples**: `examples/` directory

## 💬 Need Help?

- Check `docs/` for detailed guides
- Run `midnight-sdk --help` for CLI help
- See `examples/` for working code
- Review `TROUBLESHOOTING.md` for common issues

---

**Congratulations!** 🎉 You've created a wallet and deployed your first Midnight contract!
