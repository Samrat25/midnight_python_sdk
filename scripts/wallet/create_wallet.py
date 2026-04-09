#!/usr/bin/env python3
"""
Create a new Midnight wallet with a fresh mnemonic.
This generates a 24-word mnemonic phrase and saves it securely.
"""

from mnemonic import Mnemonic
from pathlib import Path

def create_wallet():
    """Generate a new 24-word mnemonic and save it"""
    
    # Generate 24-word mnemonic (256 bits of entropy)
    mnemo = Mnemonic("english")
    mnemonic_phrase = mnemo.generate(strength=256)
    
    print("=" * 60)
    print(" NEW MIDNIGHT WALLET CREATED")
    print("=" * 60)
    print()
    print("Your 24-word mnemonic phrase:")
    print()
    print(mnemonic_phrase)
    print()
    print("=" * 60)
    print("  IMPORTANT SECURITY NOTES:")
    print("=" * 60)
    print("1. Write this phrase down on paper")
    print("2. Store it in a secure location")
    print("3. Never share it with anyone")
    print("4. This phrase controls your funds")
    print("5. If lost, your funds are GONE FOREVER")
    print()
    
    # Save to file
    mnemonic_file = Path("mnemonic.txt")
    mnemonic_file.write_text(mnemonic_phrase)
    print(f" Saved to: {mnemonic_file.absolute()}")
    print()
    print("Next steps:")
    print("1. Start Docker services: docker-compose up -d")
    print("2. Get wallet address: node get_wallet_address.mjs")
    print("3. Deploy a contract: python deploy_hello_world.py")
    print()

if __name__ == "__main__":
    create_wallet()

