#!/usr/bin/env python3
"""
Test Single-Page Wallet UI
Tests the wallet interface by simulating API calls
"""

import sys
import requests
import json
from pathlib import Path

API_BASE = 'http://127.0.0.1:8000'

def print_section(title: str):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_api_health():
    """Test if API is running"""
    print_section("Test 1: API Health Check")
    
    try:
        response = requests.get(f"{API_BASE}/system/info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is running")
            print(f"   Version: {data.get('version')}")
            print(f"   SDK Version: {data.get('sdkVersion')}")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        print("   Make sure to run: python wallet-app/api/server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_generate_mnemonic():
    """Test mnemonic generation"""
    print_section("Test 2: Generate Mnemonic")
    
    try:
        response = requests.post(
            f"{API_BASE}/wallet/generate-mnemonic",
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            mnemonic = data.get('mnemonic')
            words = mnemonic.split()
            
            print(f"✅ Mnemonic generated")
            print(f"   Words: {len(words)}")
            print(f"   Preview: {' '.join(words[:3])}...")
            
            return mnemonic
        else:
            print(f"❌ Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_address(mnemonic: str):
    """Test address derivation"""
    print_section("Test 3: Derive Address from Mnemonic")
    
    try:
        response = requests.post(
            f"{API_BASE}/wallet/get-address",
            headers={'Content-Type': 'application/json'},
            json={
                'mnemonic': mnemonic,
                'networkId': 'undeployed'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            address = data.get('address')
            
            print(f"✅ Address derived")
            print(f"   Address: {address}")
            
            return address
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_balance(address: str):
    """Test balance check"""
    print_section("Test 4: Check Balance")
    
    try:
        response = requests.post(
            f"{API_BASE}/wallet/get-balance",
            headers={'Content-Type': 'application/json'},
            json={
                'address': address,
                'networkId': 'undeployed'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            dust = data.get('dust', 0)
            night = data.get('night', 0)
            
            print(f"✅ Balance retrieved")
            print(f"   DUST: {dust:,} ({dust / 1_000_000:.6f} DUST)")
            print(f"   NIGHT: {night:,} ({night / 1_000_000:.6f} NIGHT)")
            
            return {'dust': dust, 'night': night}
        else:
            print(f"❌ Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_add_funds(address: str):
    """Add funds to wallet for testing"""
    print_section("Test 5: Add Test Funds")
    
    try:
        # Use the node API directly to add funds
        response = requests.post(
            'http://127.0.0.1:9944/balance',
            json={
                'address': address,
                'dust': 10_000_000,
                'night': 10_000_000
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Funds added")
            print(f"   DUST: 10,000,000 (10 DUST)")
            print(f"   NIGHT: 10,000,000 (10 NIGHT)")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_transfer(sender_mnemonic: str, sender_address: str, recipient_address: str):
    """Test transfer transaction"""
    print_section("Test 6: Send Transfer Transaction")
    
    amount = 1_000_000  # 1 NIGHT
    
    print(f"💸 Transfer Details:")
    print(f"   From: {sender_address[:40]}...")
    print(f"   To: {recipient_address[:40]}...")
    print(f"   Amount: {amount:,} ({amount / 1_000_000:.2f} NIGHT)")
    print()
    
    try:
        response = requests.post(
            f"{API_BASE}/wallet/transfer-unshielded",
            headers={'Content-Type': 'application/json'},
            json={
                'fromAddress': sender_address,
                'toAddress': recipient_address,
                'amount': amount,
                'mnemonic': sender_mnemonic,
                'networkId': 'undeployed'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            tx_hash = data.get('txHash', 'N/A')
            status = data.get('status', 'N/A')
            
            print(f"✅ Transfer successful!")
            print(f"   TX Hash: {tx_hash}")
            print(f"   Status: {status}")
            
            return tx_hash
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_verify_transfer(sender_address: str, recipient_address: str, initial_sender: int, initial_recipient: int):
    """Verify transfer by checking balances"""
    print_section("Test 7: Verify Transfer")
    
    import time
    time.sleep(2)  # Wait for balance update
    
    # Check sender balance
    sender_balance = test_get_balance(sender_address)
    if not sender_balance:
        return False
    
    print()
    
    # Check recipient balance
    recipient_balance = test_get_balance(recipient_address)
    if not recipient_balance:
        return False
    
    print()
    print("📊 Balance Changes:")
    print(f"   Sender:")
    print(f"     Before: {initial_sender:,} NIGHT")
    print(f"     After: {sender_balance['night']:,} NIGHT")
    print(f"     Change: {sender_balance['night'] - initial_sender:,} NIGHT")
    
    print(f"   Recipient:")
    print(f"     Before: {initial_recipient:,} NIGHT")
    print(f"     After: {recipient_balance['night']:,} NIGHT")
    print(f"     Change: {recipient_balance['night'] - initial_recipient:,} NIGHT")
    
    # Verify
    expected_sender = initial_sender - 1_000_000
    expected_recipient = initial_recipient + 1_000_000
    
    if sender_balance['night'] == expected_sender and recipient_balance['night'] == expected_recipient:
        print("\n✅ Transfer verified successfully!")
        return True
    else:
        print("\n⚠️  Balance mismatch detected")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  SINGLE-PAGE WALLET UI TEST")
    print("  Testing API Integration")
    print("="*60)
    
    # Test 1: API Health
    if not test_api_health():
        print("\n❌ API is not running. Please start it first:")
        print("   python wallet-app/api/server.py")
        return False
    
    # Test 2: Generate mnemonic
    sender_mnemonic = test_generate_mnemonic()
    if not sender_mnemonic:
        return False
    
    # Test 3: Get sender address
    sender_address = test_get_address(sender_mnemonic)
    if not sender_address:
        return False
    
    # Test 4: Check initial balance
    initial_balance = test_get_balance(sender_address)
    if initial_balance is None:
        return False
    
    # Test 5: Add funds
    if not test_add_funds(sender_address):
        return False
    
    # Check balance after funding
    print_section("Verify Funds Added")
    funded_balance = test_get_balance(sender_address)
    if not funded_balance:
        return False
    
    # Create recipient wallet
    print_section("Create Recipient Wallet")
    recipient_mnemonic = test_generate_mnemonic()
    if not recipient_mnemonic:
        return False
    
    recipient_address = test_get_address(recipient_mnemonic)
    if not recipient_address:
        return False
    
    recipient_initial = test_get_balance(recipient_address)
    if recipient_initial is None:
        return False
    
    # Test 6: Transfer
    tx_hash = test_transfer(sender_mnemonic, sender_address, recipient_address)
    if not tx_hash:
        return False
    
    # Test 7: Verify
    success = test_verify_transfer(
        sender_address,
        recipient_address,
        funded_balance['night'],
        recipient_initial['night']
    )
    
    # Summary
    print_section("Test Summary")
    
    if success:
        print("✅ All tests passed!")
        print("\n📝 What was tested:")
        print("   1. API health check")
        print("   2. Mnemonic generation")
        print("   3. Address derivation")
        print("   4. Balance checking")
        print("   5. Fund addition")
        print("   6. Transfer transaction")
        print("   7. Balance verification")
        
        print("\n🎉 Single-page wallet UI is working correctly!")
        print("\nYou can now:")
        print("   • Open wallet-app/index.html in browser")
        print("   • Import wallet with mnemonic")
        print("   • Check balances")
        print("   • Send transfers")
        
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
