#!/usr/bin/env python3
"""
Call the storeMessage circuit on the deployed Hello World contract.
"""

from midnight_sdk import MidnightClient
from pathlib import Path
import sys

def call_contract():
    """Call storeMessage circuit"""
    
    print("=" * 60)
    print(" CALLING CONTRACT")
    print("=" * 60)
    print()
    
    # Check files exist
    mnemonic_file = Path("mnemonic.txt")
    contract_file = Path("deployed_contract.txt")
    
    if not mnemonic_file.exists():
        print(" Error: mnemonic.txt not found")
        sys.exit(1)
    
    if not contract_file.exists():
        print(" Error: deployed_contract.txt not found")
        print("Deploy a contract first: python deploy_hello_world.py")
        sys.exit(1)
    
    # Load data
    mnemonic = mnemonic_file.read_text().strip()
    contract_address = contract_file.read_text().strip()
    
    print(f"Contract: {contract_address}")
    print()
    
    # Initialize client
    client = MidnightClient(network="undeployed")
    
    # Get private key
    keys = client.wallet.get_private_keys(mnemonic)
    private_key = keys['nightExternal']
    
    # Load the contract
    print("Loading contract...")
    contract = client.get_contract(
        address=contract_address,
        circuit_ids=["storeMessage"]
    )
    print(" Contract loaded")
    print()
    
    # Get message from user
    message = input("Enter message (max 11 chars): ").strip()
    if len(message) > 11:
        message = message[:11]
        print(f"Truncated to: {message}")
    
    # Pad to 11 bytes
    message_bytes = message.encode('utf-8').ljust(11, b'\x00')
    
    print()
    print("Calling storeMessage circuit...")
    print("  - Generating ZK proof...")
    print("  - Signing transaction...")
    print("  - Submitting...")
    print()
    
    try:
        result = contract.call(
            circuit="storeMessage",
            args={"newMessage": message_bytes},
            private_key=private_key
        )
        
        print("=" * 60)
        print(" TRANSACTION SUCCESSFUL!")
        print("=" * 60)
        print()
        print(f"TX Hash: {result.tx_hash}")
        print(f"Explorer: http://localhost:8088/tx/{result.tx_hash}")
        print()
        
        # Read the new state
        print("Reading contract state...")
        state = contract.get_state()
        stored_message = state.get('message', b'').decode('utf-8').rstrip('\x00')
        print(f"Current message: '{stored_message}'")
        print()
        
    except Exception as e:
        print("=" * 60)
        print(" CALL FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    call_contract()

