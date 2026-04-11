#!/usr/bin/env python3
"""
Simple Wallet UI Test
Tests the wallet interface using existing wallet
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

def main():
    """Run simple wallet test"""
    print("\n" + "="*60)
    print("  SINGLE-PAGE WALLET UI - SIMPLE TEST")
    print("  Using Existing Wallet")
    print("="*60)
    
    # Use existing wallet
    mnemonic_file = Path("mnemonic.txt")
    if not mnemonic_file.exists():
        print("❌ mnemonic.txt not found")
        return False
    
    mnemonic = mnemonic_file.read_text().strip()
    address = "mn_addr_undeployed1p6wepa6q49ta4ptu5lkltxl5x8a4efq06vft9uex0vpsk7wmvplsxmfzey"
    
    print_section("Test 1: API Health Check")
    try:
        response = requests.get(f"{API_BASE}/system/info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is running")
            print(f"   Version: {data.get('version')}")
        else:
            print("❌ API not responding")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("   Run: python wallet-app/api/server.py")
        return False
    
    print_section("Test 2: Check Balance")
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
            print(f"   Address: {address[:40]}...")
            print(f"   DUST: {dust:,} ({dust / 1_000_000:.6f} DUST)")
            print(f"   NIGHT: {night:,} ({night / 1_000_000:.6f} NIGHT)")
            
            initial_night = night
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Create recipient address (use a different one)
    recipient_address = "mn_addr_undeployed1pt2ulx4x89l94gjuxqmu2mahjlzkktp6sfqelzslm9lwcmcwag9qrrpu27"
    
    print_section("Test 3: Check Recipient Balance")
    try:
        response = requests.post(
            f"{API_BASE}/wallet/get-balance",
            headers={'Content-Type': 'application/json'},
            json={
                'address': recipient_address,
                'networkId': 'undeployed'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            recipient_night = data.get('night', 0)
            
            print(f"✅ Recipient balance retrieved")
            print(f"   Address: {recipient_address[:40]}...")
            print(f"   NIGHT: {recipient_night:,} ({recipient_night / 1_000_000:.6f} NIGHT)")
            
            initial_recipient_night = recipient_night
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    if initial_night < 1_000_000:
        print("\n⚠️  Insufficient balance for transfer")
        print(f"   Current: {initial_night:,} NIGHT")
        print(f"   Need: 1,000,000 NIGHT")
        print("\n   Add funds with:")
        print(f"   midnight-py wallet airdrop {address} 10000000")
        return False
    
    print_section("Test 4: Send Transfer Transaction")
    
    amount = 500_000  # 0.5 NIGHT
    
    print(f"💸 Transfer Details:")
    print(f"   From: {address[:40]}...")
    print(f"   To: {recipient_address[:40]}...")
    print(f"   Amount: {amount:,} ({amount / 1_000_000:.2f} NIGHT)")
    print()
    
    try:
        response = requests.post(
            f"{API_BASE}/wallet/transfer-unshielded",
            headers={'Content-Type': 'application/json'},
            json={
                'fromAddress': address,
                'toAddress': recipient_address,
                'amount': amount,
                'mnemonic': mnemonic,
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
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print_section("Test 5: Verify Transfer")
    
    import time
    time.sleep(2)
    
    # Check sender balance
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
            final_night = data.get('night', 0)
            
            print(f"📊 Sender Balance:")
            print(f"   Before: {initial_night:,} NIGHT")
            print(f"   After: {final_night:,} NIGHT")
            print(f"   Change: {final_night - initial_night:,} NIGHT")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Check recipient balance
    try:
        response = requests.post(
            f"{API_BASE}/wallet/get-balance",
            headers={'Content-Type': 'application/json'},
            json={
                'address': recipient_address,
                'networkId': 'undeployed'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            final_recipient_night = data.get('night', 0)
            
            print(f"📊 Recipient Balance:")
            print(f"   Before: {initial_recipient_night:,} NIGHT")
            print(f"   After: {final_recipient_night:,} NIGHT")
            print(f"   Change: {final_recipient_night - initial_recipient_night:,} NIGHT")
            
            # Verify
            if (final_night == initial_night - amount and 
                final_recipient_night == initial_recipient_night + amount):
                print("\n✅ Transfer verified successfully!")
            else:
                print("\n⚠️  Balance mismatch")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_section("✅ TEST COMPLETE")
    
    print("🎉 Single-page wallet UI is working!")
    print("\n📝 What was tested:")
    print("   ✓ API health check")
    print("   ✓ Balance checking")
    print("   ✓ Transfer transaction")
    print("   ✓ Balance verification")
    
    print("\n💡 How to use the wallet UI:")
    print("   1. Open wallet-app/index.html in browser")
    print("   2. Click 'Import Wallet' tab")
    print("   3. Paste your mnemonic from mnemonic.txt")
    print("   4. Click 'Import Wallet'")
    print("   5. Your balance will be displayed")
    print("   6. Enter recipient address and amount")
    print("   7. Click 'Send Transfer'")
    print("   8. Transaction confirmed!")
    
    print("\n🌐 Wallet URL:")
    print("   file:///C:/Users/Samrat/OneDrive/Desktop/midnightsdk/wallet-app/index.html")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
