# Directory Structure

Clean and organized directory layout for the Midnight Python SDK.

## Root Structure

```
midnight_python_sdk/
├── .git/                      # Git repository
├── .github/                   # GitHub workflows and configs
├── .kiro/                     # Kiro AI assistant configs
│   └── steering/              # AI development guidelines
├── config/                    # Configuration files
│   ├── mnemonic.txt.example   # Example mnemonic file
│   └── prepod.mnemonic.txt    # Preprod network mnemonic
├── contracts/                 # Smart contracts
│   ├── *.compact              # Contract source files
│   └── managed/               # Compiled contracts
├── data/                      # Local blockchain data
├── docker/                    # Docker service definitions
│   ├── indexer/               # GraphQL indexer + explorer
│   ├── node/                  # Midnight node
│   └── proof/                 # Proof server
├── docs/                      # Documentation
│   ├── CONTRACT_TESTING_GUIDE.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── DOCKER_SETUP.md
│   ├── GETTING_STARTED.md
│   ├── PRODUCTION_SETUP.md
│   ├── PROJECT_STRUCTURE.md
│   ├── QUICK_SIGNING_GUIDE.md
│   └── QUICK_START.md
├── examples/                  # Example scripts
│   ├── ai_inference*.py
│   ├── bulletin_board*.py
│   ├── complete_*.py
│   ├── private_*.py
│   └── real_*.py
├── midnight_sdk/              # Core SDK package
│   ├── __init__.py
│   ├── ai.py                  # AI inference
│   ├── cli.py                 # CLI commands
│   ├── client.py              # Main client
│   ├── codegen.py             # Contract codegen
│   ├── contract.py            # Contract operations
│   ├── exceptions.py          # Custom exceptions
│   ├── indexer.py             # Indexer client
│   ├── lace_connector.py      # Lace wallet connector
│   ├── models.py              # Data models
│   ├── network_detector.py    # Network detection
│   ├── proof.py               # Proof generation
│   ├── pytest_plugin.py       # Pytest plugin
│   └── wallet.py              # Wallet operations
├── node_modules/              # Node.js dependencies
├── scripts/                   # Organized scripts
│   ├── deployment/            # Deployment scripts
│   │   ├── call_contract.py
│   │   ├── deploy_contract_real.mjs
│   │   ├── deploy_hello_world.py
│   │   └── deploy_real_preprod.mjs
│   ├── testing/               # Testing scripts
│   │   ├── run_all_tests.py
│   │   ├── test_*.py
│   │   └── verify_*.py
│   ├── utilities/             # Utility scripts
│   │   ├── check_*.py
│   │   ├── check_*.mjs
│   │   ├── debug_check.py
│   │   ├── get_real_balance.mjs
│   │   ├── manage_transactions.py
│   │   ├── read_balance.mjs
│   │   └── start_*.py
│   └── wallet/                # Wallet scripts
│       ├── create_wallet.py
│       ├── fund_wallet.py
│       ├── get_addresses_all_networks.mjs
│       ├── get_private_key.mjs
│       ├── get_real_wallet.mjs
│       ├── get_wallet_address.mjs
│       └── lace_bridge.mjs
├── tests/                     # Test suite
│   ├── conftest.py
│   └── test_*.py
├── .gitignore                 # Git ignore rules
├── CLEANUP_SUMMARY.md         # Cleanup documentation
├── CONTRIBUTING.md            # Contribution guidelines
├── deployed_contract.txt      # Last deployed contract
├── DIRECTORY_STRUCTURE.md     # This file
├── docker-compose.yml         # Docker services config
├── GETTING_STARTED.md         # Getting started guide
├── LICENSE                    # MIT License
├── Makefile                   # Build commands
├── mnemonic.txt               # Your wallet mnemonic (KEEP SECRET!)
├── package.json               # Node.js dependencies
├── package-lock.json          # Node.js lock file
├── package_wallet.json        # Wallet SDK dependencies
├── pyproject.toml             # Python project config
├── QUICKSTART.md              # Quick start guide
├── README.md                  # Main documentation
├── RENAME_SUMMARY.md          # Rename documentation
└── setup.sh                   # Setup script
```

## Key Directories

### `/scripts` - Organized Scripts

All helper scripts are now organized by purpose:

- **`deployment/`** - Contract deployment and interaction
  - `deploy_hello_world.py` - Deploy hello world contract
  - `call_contract.py` - Call contract circuits
  - `deploy_contract_real.mjs` - Real network deployment
  - `deploy_real_preprod.mjs` - Preprod deployment

- **`wallet/`** - Wallet management
  - `create_wallet.py` - Generate new wallet
  - `get_wallet_address.mjs` - Get wallet address
  - `get_private_key.mjs` - Derive private keys
  - `fund_wallet.py` - Fund wallet on local network

- **`testing/`** - Test scripts
  - `run_all_tests.py` - Run all tests
  - `test_*.py` - Individual test files
  - `verify_*.py` - Verification scripts

- **`utilities/`** - Utility scripts
  - `check_services.py` - Check service status
  - `check_*_balance.*` - Balance checking
  - `manage_transactions.py` - Transaction management
  - `start_*.py` - Service startup scripts

### `/midnight_sdk` - Core SDK

The main Python package with all SDK functionality.

### `/contracts` - Smart Contracts

- Source `.compact` files
- Compiled contracts in `managed/`

### `/docker` - Docker Services

- Node, Indexer, and Proof Server definitions
- Each service has its own Dockerfile

### `/docs` - Documentation

Comprehensive guides for all aspects of the SDK.

### `/examples` - Example Code

Working examples demonstrating SDK features.

### `/tests` - Test Suite

Pytest-based test suite for the SDK.

### `/config` - Configuration

Configuration files and examples (mnemonics, etc.)

## Usage After Reorganization

### Quick Start

```bash
# 1. Create wallet
python scripts/wallet/create_wallet.py

# 2. Deploy contract
python scripts/deployment/deploy_hello_world.py

# 3. Call contract
python scripts/deployment/call_contract.py

# 4. Check services
python scripts/utilities/check_services.py
```

### Testing

```bash
# Run all tests
python scripts/testing/run_all_tests.py

# Run specific test
python scripts/testing/test_complete_workflow.py
```

### Utilities

```bash
# Check service status
python scripts/utilities/check_services.py

# Check balance
python scripts/utilities/check_real_balance.py

# Manage transactions
python scripts/utilities/manage_transactions.py
```

## Important Files

### Keep Secret
- `mnemonic.txt` - Your wallet seed phrase (NEVER commit!)
- `deployed_contract.txt` - Last deployed contract address

### Configuration
- `docker-compose.yml` - Docker services
- `pyproject.toml` - Python package config
- `package.json` - Node.js dependencies

### Documentation
- `README.md` - Main documentation
- `GETTING_STARTED.md` - Detailed getting started
- `QUICKSTART.md` - Quick 5-minute start
- `docs/` - Comprehensive guides

## Benefits of This Structure

1. **Clear Organization** - Scripts grouped by purpose
2. **Easy Navigation** - Find what you need quickly
3. **Clean Root** - Less clutter in root directory
4. **Logical Grouping** - Related files together
5. **Scalable** - Easy to add new scripts

## Migration Notes

All scripts have been moved but not deleted. If you have scripts that reference old paths, update them:

**Old:**
```python
from create_wallet import create_wallet
```

**New:**
```python
from scripts.wallet.create_wallet import create_wallet
```

Or run from the new location:
```bash
python scripts/wallet/create_wallet.py
```
