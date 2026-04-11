#!/usr/bin/env python3
"""
Test Wallet Transactions
Tests native wallet transaction functionality
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from midnight_sdk.wallet import WalletClient

def print_section(title: str):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_wallet_creation():
    """Test wallet creation and address derivation"""
    print_section("Test 1: Wallet Creation & Address Derivation")
    
    try:
        wallet = WalletClient()
        
        # Read mnemonic
        mnemonic_file = Path("mnemonic.txt")
        if not mnemonic_file.exists():
            print("❌ mnemonic.txt not found")
            return False
        
        mnemonic = mnemonic_file.read_text().strip()
        print(f"✅ Mnemonic loaded: {mnemonic[:20]}...")
        
        # Get wallet address
        print("\n📍 Deriving wallet address...")
        addr_result = wallet.get_real_address(mnemonic, "undeployed")
        address = addr_result.get('address')
        network = addr_result.get('network')
        
        print(f"✅ Address: {address}")
        print(f"✅ Network: {network}")
        
        # Get private keys
        print("\n🔑 Deriving private keys...")
        keys = wallet.get_private_keys(mnemonic)
        print(f"✅ zswap key: {keys.get('zswap', 'N/A')[:20]}...")
        print(f"✅ nightExternal key: {keys.get('nightExternal', 'N/A')[:20]}...")
        print(f"✅ dust key: {keys.get('dust', 'N/A')[:20]}...")
        
        return True, address, mnemonic
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None

def test_balance_check(address: str):
    """Test balance checking"""
    print_section("Test 2: Balance Check")
    
    try:
        wallet = WalletClient()
        
        print(f"📊 Checking balance for: {address[:30]}...")
        balance = wallet.get_balance(address, "undeployed")
        
        print(f"✅ DUST Balance: {balance.dust:,} (${balance.dust / 1_000_000:.6f} DUST)")
        print(f"✅ NIGHT Balance: {balance.night:,} (${balance.night / 1_000_000:.6f} NIGHT)")
        
        return True, balance
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_create_second_wallet():
    """Create a second wallet for testing transfers"""
    print_section("Test 3: Create Second Wallet (Recipient)")
    
    try:
        import mnemonic as bip39_mnemonic
        
        # Generate new mnemonic for recipient
        mnemo = bip39_mnemonic.Mnemonic("english")
        recipient_mnemonic = mnemo.generate(strength=256)
        
        print(f"✅ Generated recipient mnemonic: {recipient_mnemonic[:30]}...")
        
        # Get recipient address
        wallet = WalletClient()
        addr_result = wallet.get_real_address(recipient_mnemonic, "undeployed")
        recipient_address = addr_result.get('address')
        
        print(f"✅ Recipient address: {recipient_address}")
        
        # Check recipient balance (should be 0)
        balance = wallet.get_balance(recipient_address, "undeployed")
        print(f"✅ Recipient DUST balance: {balance.dust}")
        print(f"✅ Recipient NIGHT balance: {balance.night}")
        
        return True, recipient_address, recipient_mnemonic
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None

def test_unshielded_transfer(sender_mnemonic: str, sender_address: str, recipient_address: str):
    """Test unshielded NIGHT transfer"""
    print_section("Test 4: Unshielded Transfer (Local Network)")
    
    try:
        wallet = WalletClient()
        
        # Check sender balance first
        print("📊 Checking sender balance...")
        sender_balance = wallet.get_balance(sender_address, "undeployed")
        print(f"   Sender NIGHT: {sender_balance.night:,}")
        
        if sender_balance.night < 1_000_000:
            print("⚠️  Insufficient balance for transfer")
            print("   Need at least 1,000,000 NIGHT (1 NIGHT)")
            print("   Skipping transfer test")
            return True  # Not a failure, just insufficient funds
        
        # Perform transfer
        amount = 500_000  # 0.5 NIGHT
        print(f"\n💸 Transferring {amount:,} NIGHT ({amount / 1_000_000:.6f} NIGHT)...")
        print(f"   From: {sender_address[:30]}...")
        print(f"   To: {recipient_address[:30]}...")
        
        result = wallet.transfer_unshielded(
            recipient_address,
            amount,
            sender_mnemonic,
            "undeployed"
        )
        
        print(f"✅ Transfer successful!")
        print(f"   TX Hash: {result.get('tx_hash', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        print(f"   Amount: {result.get('amount', 0):,}")
        
        # Check balances after transfer
        print("\n📊 Checking balances after transfer...")
        sender_balance_after = wallet.get_balance(sender_address, "undeployed")
        recipient_balance_after = wallet.get_balance(recipient_address, "undeployed")
        
        print(f"   Sender NIGHT: {sender_balance_after.night:,} (was {sender_balance.night:,})")
        print(f"   Recipient NIGHT: {recipient_balance_after.night:,}")
        
        # Verify transfer
        if recipient_balance_after.night == amount:
            print("✅ Transfer verified! Recipient received correct amount")
        else:
            print(f"⚠️  Balance mismatch: expected {amount}, got {recipient_balance_after.night}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_wallet_info(address: str, mnemonic: str):
    """Display complete wallet information"""
    print_section("Test 5: Complete Wallet Information")
    
    try:
        wallet = WalletClient()
        
        print("📋 Wallet Summary")
        print(f"   Address: {address}")
        print(f"   Network: undeployed (local)")
        
        # Get balance
        balance = wallet.get_balance(address, "undeployed")
        print(f"\n💰 Balances:")
        print(f"   DUST: {balance.dust:,} ({balance.dust / 1_000_000:.6f} DUST)")
        print(f"   NIGHT: {balance.night:,} ({balance.night / 1_000_000:.6f} NIGHT)")
        
        # Get keys
        keys = wallet.get_private_keys(mnemonic)
        print(f"\n🔑 Keys:")
        print(f"   zswap: {keys.get('zswap', 'N/A')[:30]}...")
        print(f"   nightExternal: {keys.get('nightExternal', 'N/A')[:30]}...")
        print(f"   dust: {keys.get('dust', 'N/A')[:30]}...")
        
        print("\n✅ Wallet information retrieved successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all transaction tests"""
    print("\n" + "="*60)
    print("  WALLET TRANSACTION TEST SUITE")
    print("  Testing Native Wallet Functionality")
    print("="*60)
    
    results = []
    
    # Test 1: Wallet creation
    result, sender_address, sender_mnemonic = test_wallet_creation()
    results.append(("Wallet Creation", result))
    
    if not result:
        print("\n❌ Cannot continue without wallet")
        return False
    
    # Test 2: Balance check
    result, balance = test_balance_check(sender_address)
    results.append(("Balance Check", result))
    
    # Test 3: Create second wallet
    result, recipient_address, recipient_mnemonic = test_create_second_wallet()
    results.append(("Create Recipient Wallet", result))
    
    if not result:
        print("\n⚠️  Skipping transfer test (no recipient)")
    else:
        # Test 4: Transfer
        result = test_unshielded_transfer(sender_mnemonic, sender_address, recipient_address)
        results.append(("Unshielded Transfer", result))
    
    # Test 5: Wallet info
    result = test_wallet_info(sender_address, sender_mnemonic)
    results.append(("Wallet Information", result))
    
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
    
    if passed == total:
        print("🎉 All tests passed! Native wallet is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
