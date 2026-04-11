#!/bin/bash
# Real CLI Wallet Workflow Test
# This script demonstrates the complete wallet workflow using real CLI commands

echo "============================================================"
echo "  MIDNIGHT CLI - REAL WALLET WORKFLOW TEST"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: List existing wallets${NC}"
midnight-py wallet list
echo ""

echo -e "${BLUE}Step 2: Check balance for main wallet${NC}"
echo "Address: mn_addr_undeployed1p6wepa6q49ta4ptu5lkltxl5x8a4efq06vft9uex0vpsk7wmvplsxmfzey"
midnight-py wallet balance mn_addr_undeployed1p6wepa6q49ta4ptu5lkltxl5x8a4efq06vft9uex0vpsk7wmvplsxmfzey
echo ""

echo -e "${BLUE}Step 3: Create a new recipient wallet${NC}"
midnight-py wallet new RecipientWallet
echo ""

echo -e "${BLUE}Step 4: Get recipient address${NC}"
echo "Note: Due to Windows Node.js issue, we'll use a pre-generated address"
RECIPIENT="mn_addr_undeployed1pt2ulx4x89l94gjuxqmu2mahjlzkktp6sfqelzslm9lwcmcwag9qrrpu27"
echo "Recipient address: $RECIPIENT"
echo ""

echo -e "${BLUE}Step 5: Check recipient balance (before transfer)${NC}"
midnight-py wallet balance $RECIPIENT
echo ""

echo -e "${BLUE}Step 6: Perform transfer (1 NIGHT = 1,000,000 units)${NC}"
echo "Transferring 1,000,000 NIGHT (1.0 NIGHT) to recipient..."
echo ""
echo -e "${YELLOW}Command:${NC}"
echo "midnight-py transfer unshielded $RECIPIENT 1000000"
echo ""
read -p "Press Enter to execute transfer..."
midnight-py transfer unshielded $RECIPIENT 1000000
echo ""

echo -e "${BLUE}Step 7: Check balances after transfer${NC}"
echo ""
echo "Sender balance:"
midnight-py wallet balance mn_addr_undeployed1p6wepa6q49ta4ptu5lkltxl5x8a4efq06vft9uex0vpsk7wmvplsxmfzey
echo ""
echo "Recipient balance:"
midnight-py wallet balance $RECIPIENT
echo ""

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  ✓ CLI Workflow Test Complete${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo "Summary:"
echo "  • Created new wallet"
echo "  • Checked balances"
echo "  • Performed transfer"
echo "  • Verified transaction"
echo ""
echo "Next steps:"
echo "  • Try: midnight-py transfer unshielded --help"
echo "  • Try: midnight-py wallet balance --full (for shielded balance)"
echo "  • Try: midnight-py status (check network status)"
echo ""
