#!/usr/bin/env python3
"""
Test Wallet Integration
Tests all new wallet endpoints added from contributor updates
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from midnight_sdk.wallet import WalletClient

def print_section(title: str):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_get_all_addresses():
    """Test get_all_addresses method"""
    print_section("Test: Get All Addresses")
    
    try:
        wallet = WalletClient()
        
        # Read mnemonic
        mnemonic_file = Path("mnemonic.txt")
        if not mnemonic_file.exists():
            print("❌ mnemonic.txt not found")
            return False
        
        mnemonic = mnemonic_file.read_text().strip()
        
        # Test for local network
        print("Testing for local network (undeployed)...")
        result = wallet.get_all_addresses(mnemonic, "undeployed")
        
        print(f"✅ Network: {result.get('network')}")
        print(f"✅ Addresses:")
        addresses = result.get('addresses', {})
        print(f"   - Unshielded: {addresses.get('unshielded', 'N/A')}")
        print(f"   - Shielded: {addresses.get('shielded', 'N/A')}")
        print(f"   - DUST: {addresses.get('dust', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_quick_balance():
    """Test get_quick_balance method"""
    print_section("Test: Get Quick Balance")
    
    try:
        wallet = WalletClient()
        
        # Read mnemonic
        mnemonic_file = Path("mnemonic.txt")
        if not mnemonic_file.exists():
            print("❌ mnemonic.txt not found")
            return False
        
        mnemonic = mnemonic_file.read_text().strip()
        
        # Test for local network
        print("Testing for local network (undeployed)...")
        result = wallet.get_quick_balance(
            mnemonic,
            "undeployed",
            "http://127.0.0.1:8088/api/v4/graphql"
        )
        
        print(f"✅ Network: {result.get('network')}")
        print(f"✅ Addresses:")
        addresses = result.get('addresses', {})
        print(f"   - Unshielded: {addresses.get('unshielded', 'N/A')}")
        print(f"   - DUST: {addresses.get('dust', 'N/A')}")
        
        print(f"✅ Balances:")
        balances = result.get('balances', {})
        print(f"   - DUST: {balances.get('dust', '0')}")
        print(f"   - NIGHT (unshielded): {balances.get('night_unshielded', '0')}")
        print(f"   - NIGHT (shielded): {balances.get('night_shielded', 'unknown')}")
        
        if 'note' in result:
            print(f"ℹ️  Note: {result['note']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_get_full_balance():
    """Test get_full_balance method"""
    print_section("Test: Get Full Balance")
    
    try:
        wallet = WalletClient()
        
        # Read mnemonic
        mnemonic_file = Path("mnemonic.txt")
        if not mnemonic_file.exists():
            print("❌ mnemonic.txt not found")
            return False
        
        mnemonic = mnemonic_file.read_text().strip()
        
        # Test for local network
        print("Testing for local network (undeployed)...")
        print("⏳ This may take 60-90 seconds for wallet sync...")
        
        result = wallet.get_full_balance(
            mnemonic,
            "undeployed",
            "http://127.0.0.1:8088/api/v4/graphql",
            "ws://127.0.0.1:8088/api/v4/graphql/ws",
            "ws://127.0.0.1:9944",
            "http://127.0.0.1:6300"
        )
        
        print(f"✅ Address: {result.get('address')}")
        print(f"✅ Network: {result.get('network')}")
        print(f"✅ Synced: {result.get('synced', 'unknown')}")
        
        print(f"✅ Balances:")
        balances = result.get('balances', {})
        print(f"   - DUST: {balances.get('dust', '0')}")
        print(f"   - NIGHT (unshielded): {balances.get('night_unshielded', '0')}")
        print(f"   - NIGHT (shielded): {balances.get('night_shielded', '0')}")
        
        if 'coins' in result:
            coins = result['coins']
            print(f"✅ Coin Counts:")
            print(f"   - Shielded: {coins.get('shielded', 0)}")
            print(f"   - Unshielded: {coins.get('unshielded', 0)}")
            print(f"   - DUST: {coins.get('dust', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_wallet_methods():
    """Test existing wallet methods"""
    print_section("Test: Existing Wallet Methods")
    
    try:
        wallet = WalletClient()
        
        # Read mnemonic
        mnemonic_file = Path("mnemonic.txt")
        if not mnemonic_file.exists():
            print("❌ mnemonic.txt not found")
            return False
        
        mnemonic = mnemonic_file.read_text().strip()
        
        # Test get_real_address
        print("Testing get_real_address...")
        addr_result = wallet.get_real_address(mnemonic, "undeployed")
        print(f"✅ Address: {addr_result.get('address')}")
        print(f"✅ Network: {addr_result.get('network')}")
        
        # Test get_private_keys
        print("\nTesting get_private_keys...")
        keys = wallet.get_private_keys(mnemonic)
        print(f"✅ Keys retrieved:")
        print(f"   - zswap: {keys.get('zswap', 'N/A')[:20]}...")
        print(f"   - nightExternal: {keys.get('nightExternal', 'N/A')[:20]}...")
        print(f"   - dust: {keys.get('dust', 'N/A')[:20]}...")
        
        # Test get_balance
        print("\nTesting get_balance...")
        address = addr_result.get('address')
        balance = wallet.get_balance(address, "undeployed")
        print(f"✅ Balance:")
        print(f"   - DUST: {balance.dust}")
        print(f"   - NIGHT: {balance.night}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  WALLET INTEGRATION TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test existing methods
    results.append(("Existing Wallet Methods", test_wallet_methods()))
    
    # Test new methods
    results.append(("Get All Addresses", test_get_all_addresses()))
    results.append(("Get Quick Balance", test_get_quick_balance()))
    
    # Note: Full balance test is commented out by default as it takes 60-90 seconds
    # Uncomment to test:
    # results.append(("Get Full Balance", test_get_full_balance()))
    
    # Print summary
    print_section("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
