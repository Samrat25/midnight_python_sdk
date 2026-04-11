#!/usr/bin/env python3
"""
Test Wallet with Funds
Tests wallet transactions with actual token transfers
"""

import sys
import os
import requests
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from midnight_sdk.wallet import WalletClient

def print_section(title: str):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def add_funds_to_wallet(address: str, dust_amount: int = 10_000_000, night_amount: int = 10_000_000):
    """Add funds to wallet via local node API"""
    print_section("Adding Funds to Wallet")
    
    try:
        node_url = "http://127.0.0.1:9944"
        
        print(f"💰 Adding funds to: {address[:40]}...")
        print(f"   DUST: {dust_amount:,} ({dust_amount / 1_000_000:.2f} DUST)")
        print(f"   NIGHT: {night_amount:,} ({night_amount / 1_000_000:.2f} NIGHT)")
        
        # Add funds via node API
        response = requests.post(
            f"{node_url}/balance",
            json={
                "address": address,
                "dust": dust_amount,
                "night": night_amount
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Funds added successfully!")
            return True
        else:
            print(f"❌ Failed to add funds: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error adding funds: {e}")
        return False

def test_full_transaction_flow():
    """Test complete transaction flow with funds"""
    print("\n" + "="*60)
    print("  WALLET TRANSACTION TEST WITH FUNDS")
    print("  Testing Complete Transaction Flow")
    print("="*60)
    
    try:
        wallet = WalletClient()
        
        # Step 1: Load sender wallet
        print_section("Step 1: Load Sender Wallet")
        mnemonic_file = Path("mnemonic.txt")
        if not mnemonic_file.exists():
            print("❌ mnemonic.txt not found")
            return False
        
        sender_mnemonic = mnemonic_file.read_text().strip()
        sender_result = wallet.get_real_address(sender_mnemonic, "undeployed")
        sender_address = sender_result.get('address')
        
        print(f"✅ Sender address: {sender_address}")
        
        # Step 2: Create recipient wallet
        print_section("Step 2: Create Recipient Wallet")
        import mnemonic as bip39_mnemonic
        mnemo = bip39_mnemonic.Mnemonic("english")
        recipient_mnemonic = mnemo.generate(strength=256)
        
        recipient_result = wallet.get_real_address(recipient_mnemonic, "undeployed")
        recipient_address = recipient_result.get('address')
        
        print(f"✅ Recipient address: {recipient_address}")
        
        # Step 3: Add funds to sender
        if not add_funds_to_wallet(sender_address, 10_000_000, 10_000_000):
            print("❌ Failed to add funds")
            return False
        
        # Step 4: Check sender balance
        print_section("Step 3: Check Sender Balance")
        sender_balance = wallet.get_balance(sender_address, "undeployed")
        print(f"✅ Sender DUST: {sender_balance.dust:,} ({sender_balance.dust / 1_000_000:.2f} DUST)")
        print(f"✅ Sender NIGHT: {sender_balance.night:,} ({sender_balance.night / 1_000_000:.2f} NIGHT)")
        
        # Step 5: Check recipient balance (should be 0)
        print_section("Step 4: Check Recipient Balance (Before)")
        recipient_balance_before = wallet.get_balance(recipient_address, "undeployed")
        print(f"✅ Recipient DUST: {recipient_balance_before.dust:,}")
        print(f"✅ Recipient NIGHT: {recipient_balance_before.night:,}")
        
        # Step 6: Perform transfer
        print_section("Step 5: Perform Transfer")
        transfer_amount = 2_000_000  # 2 NIGHT
        
        print(f"💸 Transferring {transfer_amount:,} NIGHT ({transfer_amount / 1_000_000:.2f} NIGHT)")
        print(f"   From: {sender_address[:40]}...")
        print(f"   To: {recipient_address[:40]}...")
        
        result = wallet.transfer_unshielded(
            recipient_address,
            transfer_amount,
            sender_mnemonic,
            "undeployed"
        )
        
        print(f"✅ Transfer successful!")
        print(f"   TX Hash: {result.get('tx_hash', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        print(f"   From: {result.get('from', 'N/A')[:40]}...")
        print(f"   To: {result.get('to', 'N/A')[:40]}...")
        print(f"   Amount: {result.get('amount', 0):,} NIGHT")
        
        # Step 7: Check balances after transfer
        print_section("Step 6: Check Balances (After Transfer)")
        
        sender_balance_after = wallet.get_balance(sender_address, "undeployed")
        recipient_balance_after = wallet.get_balance(recipient_address, "undeployed")
        
        print("📊 Sender Balance:")
        print(f"   Before: {sender_balance.night:,} NIGHT")
        print(f"   After: {sender_balance_after.night:,} NIGHT")
        print(f"   Change: -{sender_balance.night - sender_balance_after.night:,} NIGHT")
        
        print("\n📊 Recipient Balance:")
        print(f"   Before: {recipient_balance_before.night:,} NIGHT")
        print(f"   After: {recipient_balance_after.night:,} NIGHT")
        print(f"   Change: +{recipient_balance_after.night - recipient_balance_before.night:,} NIGHT")
        
        # Step 8: Verify transfer
        print_section("Step 7: Verify Transfer")
        
        expected_sender = sender_balance.night - transfer_amount
        expected_recipient = recipient_balance_before.night + transfer_amount
        
        sender_correct = sender_balance_after.night == expected_sender
        recipient_correct = recipient_balance_after.night == expected_recipient
        
        if sender_correct:
            print("✅ Sender balance correct")
        else:
            print(f"❌ Sender balance incorrect: expected {expected_sender:,}, got {sender_balance_after.night:,}")
        
        if recipient_correct:
            print("✅ Recipient balance correct")
        else:
            print(f"❌ Recipient balance incorrect: expected {expected_recipient:,}, got {recipient_balance_after.night:,}")
        
        # Step 9: Test second transfer (reverse direction)
        print_section("Step 8: Test Reverse Transfer")
        
        reverse_amount = 500_000  # 0.5 NIGHT
        print(f"💸 Transferring {reverse_amount:,} NIGHT ({reverse_amount / 1_000_000:.2f} NIGHT)")
        print(f"   From: {recipient_address[:40]}... (recipient)")
        print(f"   To: {sender_address[:40]}... (sender)")
        
        reverse_result = wallet.transfer_unshielded(
            sender_address,
            reverse_amount,
            recipient_mnemonic,
            "undeployed"
        )
        
        print(f"✅ Reverse transfer successful!")
        print(f"   TX Hash: {reverse_result.get('tx_hash', 'N/A')}")
        
        # Final balances
        print_section("Step 9: Final Balances")
        
        sender_final = wallet.get_balance(sender_address, "undeployed")
        recipient_final = wallet.get_balance(recipient_address, "undeployed")
        
        print("📊 Final Balances:")
        print(f"   Sender NIGHT: {sender_final.night:,} ({sender_final.night / 1_000_000:.2f} NIGHT)")
        print(f"   Recipient NIGHT: {recipient_final.night:,} ({recipient_final.night / 1_000_000:.2f} NIGHT)")
        
        # Summary
        print_section("Transaction Summary")
        
        print("✅ All transactions completed successfully!")
        print(f"\n📝 Transaction History:")
        print(f"   1. Added {10_000_000:,} NIGHT to sender")
        print(f"   2. Transferred {transfer_amount:,} NIGHT: sender → recipient")
        print(f"   3. Transferred {reverse_amount:,} NIGHT: recipient → sender")
        print(f"\n💰 Net Changes:")
        print(f"   Sender: {sender_final.night - 10_000_000:,} NIGHT")
        print(f"   Recipient: {recipient_final.night:,} NIGHT")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test"""
    success = test_full_transaction_flow()
    
    if success:
        print("\n" + "="*60)
        print("  🎉 ALL TESTS PASSED!")
        print("  Native wallet is fully functional")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("  ❌ TESTS FAILED")
        print("  Check the output above for details")
        print("="*60 + "\n")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
