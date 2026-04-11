#!/usr/bin/env python3
"""
Real CLI Wallet Demo
Demonstrates the complete wallet workflow using actual CLI commands
"""

import subprocess
import sys
import time

def run_command(cmd, description=""):
    """Run a CLI command and display output"""
    if description:
        print(f"\n{'='*60}")
        print(f"  {description}")
        print(f"{'='*60}\n")
    
    print(f"$ {cmd}\n")
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    return result.returncode == 0

def main():
    """Run the demo"""
    print("\n" + "="*60)
    print("  MIDNIGHT CLI - REAL WALLET WORKFLOW DEMO")
    print("="*60)
    
    # Step 1: List wallets
    run_command(
        "midnight-py wallet list",
        "Step 1: List All Wallets"
    )
    
    input("\nPress Enter to continue...")
    
    # Step 2: Check main wallet balance
    main_address = "mn_addr_undeployed1p6wepa6q49ta4ptu5lkltxl5x8a4efq06vft9uex0vpsk7wmvplsxmfzey"
    run_command(
        f"midnight-py wallet balance {main_address}",
        "Step 2: Check Main Wallet Balance"
    )
    
    input("\nPress Enter to continue...")
    
    # Step 3: Show transfer info
    run_command(
        "midnight-py transfer info",
        "Step 3: Transfer Information"
    )
    
    input("\nPress Enter to continue...")
    
    # Step 4: Create recipient wallet
    print("\n" + "="*60)
    print("  Step 4: Create Recipient Wallet")
    print("="*60)
    print("\nCreating a new wallet for testing transfers...")
    print("Note: Save the mnemonic that will be displayed!\n")
    
    input("Press Enter to create wallet...")
    run_command("midnight-py wallet new DemoRecipient")
    
    input("\nPress Enter to continue...")
    
    # Step 5: Use pre-generated recipient address (due to Windows Node.js issue)
    recipient_address = "mn_addr_undeployed1pt2ulx4x89l94gjuxqmu2mahjlzkktp6sfqelzslm9lwcmcwag9qrrpu27"
    
    print("\n" + "="*60)
    print("  Step 5: Check Recipient Balance (Before Transfer)")
    print("="*60)
    print(f"\nRecipient address: {recipient_address}\n")
    
    run_command(f"midnight-py wallet balance {recipient_address}")
    
    input("\nPress Enter to continue...")
    
    # Step 6: Perform transfer
    print("\n" + "="*60)
    print("  Step 6: Perform Transfer")
    print("="*60)
    print("\nTransferring 1,000,000 NIGHT (1.0 NIGHT) to recipient")
    print(f"From: {main_address[:40]}...")
    print(f"To: {recipient_address[:40]}...")
    print("\nAmount: 1,000,000 units = 1.0 NIGHT\n")
    
    input("Press Enter to execute transfer...")
    
    success = run_command(
        f"midnight-py transfer unshielded {recipient_address} 1000000"
    )
    
    if not success:
        print("\n⚠️  Transfer failed. This might be due to:")
        print("   • Insufficient balance")
        print("   • Network not running (docker-compose up)")
        print("   • Windows Node.js compatibility issue")
        return
    
    input("\nPress Enter to continue...")
    
    # Step 7: Check balances after transfer
    print("\n" + "="*60)
    print("  Step 7: Verify Transfer")
    print("="*60)
    
    print("\n📊 Sender Balance (After Transfer):")
    run_command(f"midnight-py wallet balance {main_address}")
    
    print("\n📊 Recipient Balance (After Transfer):")
    run_command(f"midnight-py wallet balance {recipient_address}")
    
    # Summary
    print("\n" + "="*60)
    print("  ✅ DEMO COMPLETE!")
    print("="*60)
    
    print("\n📝 What You Learned:")
    print("   1. List wallets: midnight-py wallet list")
    print("   2. Check balance: midnight-py wallet balance <address>")
    print("   3. Create wallet: midnight-py wallet new <name>")
    print("   4. Transfer: midnight-py transfer unshielded <recipient> <amount>")
    
    print("\n🔧 Additional Commands:")
    print("   • midnight-py wallet --help")
    print("   • midnight-py transfer --help")
    print("   • midnight-py status (check network)")
    print("   • midnight-py wallet balance --full (shielded balance)")
    
    print("\n💡 Tips:")
    print("   • 1 NIGHT = 1,000,000 units")
    print("   • DUST is non-transferable (generated from NIGHT)")
    print("   • Use --dry-run to simulate transfers")
    print("   • Balances update immediately on local network")
    
    print("\n🌐 Real Networks:")
    print("   • Preprod: midnight-py transfer unshielded <addr> <amt> -p preprod")
    print("   • Testnet: midnight-py transfer unshielded <addr> <amt> -p testnet")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(1)
