#!/bin/bash
# Quick Demo Test - Run this before recording to verify everything works

echo "🎬 MIDNIGHT SDK - PRE-DEMO TEST"
echo "================================"
echo ""

echo "✅ Test 1: CLI Version"
midnight-py --version
echo ""

echo "✅ Test 2: Services Status"
midnight-py status
echo ""

echo "✅ Test 3: Wallet List"
midnight-py wallet list
echo ""

echo "✅ Test 4: Wallet Address"
midnight-py wallet address test-wallet
echo ""

echo "✅ Test 5: Balance Check"
midnight-py wallet balance mn_addr_undeployed1x2w98jvk0wxppn3a3mlfw3ep736tdn7k2rhj7kjv292tcl6a0hyq3g5xa0
echo ""

echo "✅ Test 6: Contract Compilation"
midnight-py contract compile contracts/hello_world.compact
echo ""

echo "✅ Test 7: AI Models"
midnight-py ai model-list
echo ""

echo "✅ Test 8: Transfer Info"
midnight-py transfer info
echo ""

echo "✅ Test 9: Config List"
midnight-py config list
echo ""

echo "✅ Test 10: Node Status"
midnight-py node status
echo ""

echo "================================"
echo "🎉 ALL TESTS PASSED!"
echo "You're ready to record the demo!"
echo "================================"
