#!/bin/bash
# Comprehensive CLI Test Script

echo "================================"
echo "Midnight SDK CLI Test Suite"
echo "================================"
echo ""

# Test 1: Version
echo "Test 1: Version"
midnight-py --version
echo ""

# Test 2: System Status
echo "Test 2: System Status"
midnight-py status
echo ""

# Test 3: System Info
echo "Test 3: System Info"
midnight-py system info
echo ""

# Test 4: Config List
echo "Test 4: Config List"
midnight-py config list
echo ""

# Test 5: Wallet List
echo "Test 5: Wallet List"
midnight-py wallet list
echo ""

# Test 6: Wallet Address
echo "Test 6: Wallet Address (test-wallet)"
midnight-py wallet address test-wallet
echo ""

# Test 7: Wallet Balance
echo "Test 7: Wallet Balance"
midnight-py wallet balance mn_addr_undeployed1x2w98jvk0wxppn3a3mlfw3ep736tdn7k2rhj7kjv292tcl6a0hyq3g5xa0
echo ""

# Test 8: Contract List
echo "Test 8: Contract List"
midnight-py contract list
echo ""

# Test 9: Contract Compile
echo "Test 9: Contract Compile"
midnight-py contract compile contracts/hello_world.compact
echo ""

# Test 10: Node Status
echo "Test 10: Node Status"
midnight-py node status
echo ""

# Test 11: AI Model List
echo "Test 11: AI Model List"
midnight-py ai model-list
echo ""

# Test 12: Transfer Info
echo "Test 12: Transfer Info"
midnight-py transfer info
echo ""

# Test 13: TX List
echo "Test 13: TX List"
midnight-py tx list
echo ""

# Test 14: Config Get
echo "Test 14: Config Get Active Profile"
midnight-py config get active_profile
echo ""

# Test 15: Explorer Help
echo "Test 15: Explorer Help"
midnight-py explorer --help
echo ""

echo "================================"
echo "All Tests Completed!"
echo "================================"
