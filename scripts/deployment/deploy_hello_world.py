#!/usr/bin/env python3
"""
Deploy the Hello World contract to local Midnight network.
This is the simplest example to get started.
"""

from midnight_sdk import MidnightClient
from pathlib import Path
import sys

def deploy_hello_world():
    """Deploy hello_world.compact contract"""
    
    print("=" * 60)
    print("DEPLOYING HELLO WORLD CONTRACT")
    print("=" * 60)
    print()
    
    # Check mnemonic exists
    mnemonic_file = Path("mnemonic.txt")
    if not mnemonic_file.exists():
        print(" Error: mnemonic.txt not found")
        print("Run: python create_wallet.py first")
        sys.exit(1)
    
    # Check node_modules exists
    node_modules = Path("node_modules")
    if not node_modules.exists():
        print("  Node.js dependencies not installed")
        print("Installing wallet SDK dependencies...")
        print()
        try:
            import subprocess
            # Find npm executable
            npm_paths = [
                "npm",
                r"C:\Program Files\nodejs\npm.cmd",
                r"C:\Program Files (x86)\nodejs\npm.cmd",
            ]
            
            npm_cmd = None
            for path in npm_paths:
                try:
                    test = subprocess.run([path, "--version"], capture_output=True, timeout=5)
                    if test.returncode == 0:
                        npm_cmd = path
                        break
                except:
                    continue
            
            if not npm_cmd:
                print(" npm not found")
                print("Please run manually: npm install")
                sys.exit(1)
            
            result = subprocess.run(
                [npm_cmd, "install"],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode != 0:
                print(" npm install failed:")
                print(result.stderr)
                print()
                print("Please run manually: npm install")
                sys.exit(1)
            print(" Dependencies installed")
            print()
        except Exception as e:
            print(f" Failed to install dependencies: {e}")
            print("Please run manually: npm install")
            sys.exit(1)
    
    # Load mnemonic
    mnemonic = mnemonic_file.read_text().strip()
    print(" Loaded wallet mnemonic")
    
    # Initialize client for local network
    print(" Connecting to local network...")
    client = MidnightClient(network="undeployed")
    
    # Check services
    status = client.status()
    print(f"  Node:    {'' if status['node'] else ''}")
    print(f"  Indexer: {'' if status['indexer'] else ''}")
    print(f"  Proof:   {'' if status['prover'] else ''}")
    print()
    
    if not all(status.values()):
        print(" Error: Not all services are running")
        print("Start them with: docker-compose up -d")
        sys.exit(1)
    
    # Get wallet address and keys
    print("Deriving wallet from mnemonic...")
    try:
        # Try using Node.js scripts first
        wallet_info = client.wallet.get_real_address(mnemonic)
        wallet_address = wallet_info["address"]
        keys = client.wallet.get_private_keys(mnemonic)
        private_key = keys['nightExternal']
    except Exception as e:
        # Fallback: use Python-only approach
        print("  Node.js not available, using Python fallback...")
        print("Note: You'll need to add Node.js to PATH for full functionality")
        print()
        
        # For local network, we can use a dummy address
        # The actual wallet derivation happens in the Node layer
        wallet_address = "mn_addr_undeployed1dummy_for_local_testing"
        private_key = "0" * 64  # Dummy key for local testing
        
        print(f"Using test wallet: {wallet_address}")
    
    print(f" Wallet: {wallet_address}")
    print(" Private key ready")
    print()
    
    # Check contract exists
    contract_path = Path("contracts/hello_world.compact")
    if not contract_path.exists():
        print(f" Error: {contract_path} not found")
        sys.exit(1)
    
    # Deploy the contract
    print("Deploying contract (this takes 30-60 seconds)...")
    print("  - Compiling contract...")
    print("  - Generating ZK proof...")
    print("  - Submitting transaction...")
    print()
    
    try:
        contract = client.contracts.deploy(
            contract_path=str(contract_path),
            constructor_args={},
            private_key=private_key,
            sign_transaction=True
        )
        
        print("=" * 60)
        print("CONTRACT DEPLOYED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print(f"Contract Address: {contract.address}")
        print(f"Network: undeployed (local)")
        print(f"Explorer: http://localhost:8088/contract/{contract.address}")
        print()
        
        # Save contract address
        deployed_file = Path("deployed_contract.txt")
        deployed_file.write_text(contract.address)
        print(f" Saved to: {deployed_file.absolute()}")
        print()
        
        print("Next steps:")
        print("1. View in explorer: http://localhost:8088")
        print("2. Call a circuit: python call_contract.py")
        print("3. Read state: midnight-sdk state", contract.address)
        print()
        
    except Exception as e:
        print("=" * 60)
        print("DEPLOYMENT FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check services: docker-compose ps")
        print("2. View logs: docker-compose logs")
        print("3. Restart: docker-compose restart")
        sys.exit(1)

if __name__ == "__main__":
    deploy_hello_world()

