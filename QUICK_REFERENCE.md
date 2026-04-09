# Quick Reference Guide

Fast reference for common tasks after directory reorganization.

## Quick Start Commands

### 1. Setup
```bash
# Install dependencies
pip install -e .
npm install

# Start Docker services
docker-compose up -d
```

### 2. Wallet Operations
```bash
# Create new wallet
python scripts/wallet/create_wallet.py

# Get wallet address
node scripts/wallet/get_wallet_address.mjs

# Get private keys
node scripts/wallet/get_private_key.mjs

# Fund wallet (local network)
python scripts/wallet/fund_wallet.py
```

### 3. Contract Deployment
```bash
# Deploy hello world contract
python scripts/deployment/deploy_hello_world.py

# Call contract circuit
python scripts/deployment/call_contract.py

# Deploy to preprod
node scripts/deployment/deploy_real_preprod.mjs
```

### 4. Utilities
```bash
# Check service status
python scripts/utilities/check_services.py

# Check balance
python scripts/utilities/check_real_balance.py

# Manage transactions
python scripts/utilities/manage_transactions.py

# Start services
python scripts/utilities/start_services.py
```

### 5. Testing
```bash
# Run all tests
python scripts/testing/run_all_tests.py

# Run specific test
python scripts/testing/test_complete_workflow.py

# Verify installation
python scripts/testing/verify_all.py
```

## CLI Commands

```bash
# Check service status
midnight-sdk status

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

## File Locations

### Configuration
- Mnemonic: `mnemonic.txt` (root)
- Docker config: `docker-compose.yml` (root)
- Python config: `pyproject.toml` (root)
- Node config: `package.json` (root)

### Contracts
- Source: `contracts/*.compact`
- Compiled: `contracts/managed/*/`

### Documentation
- Main: `README.md`
- Getting Started: `GETTING_STARTED.md`
- Quick Start: `QUICKSTART.md`
- Detailed guides: `docs/`

### Scripts (Organized)
- Wallet: `scripts/wallet/`
- Deployment: `scripts/deployment/`
- Testing: `scripts/testing/`
- Utilities: `scripts/utilities/`

## Common Workflows

### First Time Setup
```bash
# 1. Install
pip install -e .
npm install

# 2. Start services
docker-compose up -d

# 3. Create wallet
python scripts/wallet/create_wallet.py

# 4. Deploy contract
python scripts/deployment/deploy_hello_world.py
```

### Daily Development
```bash
# Start services
docker-compose up -d

# Check status
python scripts/utilities/check_services.py

# Deploy and test
python scripts/deployment/deploy_hello_world.py
python scripts/deployment/call_contract.py
```

### Testing
```bash
# Run all tests
python scripts/testing/run_all_tests.py

# Check specific functionality
python scripts/testing/test_complete_workflow.py
```

### Troubleshooting
```bash
# Check services
docker-compose ps
docker-compose logs

# Restart services
docker-compose restart

# Clean restart
docker-compose down -v
docker-compose up -d

# Verify installation
python scripts/testing/verify_all.py
```

## Service URLs

- **Node**: http://localhost:9944
- **Indexer/Explorer**: http://localhost:8088
- **Proof Server**: http://localhost:6300

## Important Notes

1. **Mnemonic Security**: Never commit `mnemonic.txt` to git
2. **Docker Required**: All services run in Docker
3. **Node.js Required**: Wallet SDK uses Node.js
4. **Local Network**: Auto-funded, perfect for development
5. **Preprod Network**: Requires faucet tokens

## Getting Help

- **Documentation**: See `docs/` directory
- **Examples**: See `examples/` directory
- **Issues**: Check `TROUBLESHOOTING.md`
- **Structure**: See `DIRECTORY_STRUCTURE.md`

## Path Updates

If you have existing scripts that reference old paths:

**Old paths:**
- `create_wallet.py`
- `deploy_hello_world.py`
- `check_services.py`

**New paths:**
- `scripts/wallet/create_wallet.py`
- `scripts/deployment/deploy_hello_world.py`
- `scripts/utilities/check_services.py`

Update your imports and commands accordingly!
