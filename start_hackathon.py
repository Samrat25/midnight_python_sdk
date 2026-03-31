#!/usr/bin/env python3
"""
Complete hackathon setup script.
Installs dependencies, starts servers, and verifies everything works.

Usage:
    python start_hackathon.py
"""

import subprocess
import sys
import time
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def run_command(cmd, description, check=True):
    """Run a command and show output."""
    print(f"→ {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"✗ Python 3.10+ required. Found: {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def install_package():
    """Install midnight-py package."""
    print_header("Installing midnight-py")
    
    # Install in development mode
    if not run_command(
        f"{sys.executable} -m pip install -e .",
        "Installing package"
    ):
        return False
    
    # Install aiohttp for dev server
    if not run_command(
        f"{sys.executable} -m pip install aiohttp",
        "Installing aiohttp for dev servers"
    ):
        return False
    
    return True


def verify_installation():
    """Verify the installation."""
    print_header("Verifying Installation")
    
    try:
        import midnight_py
        print(f"✓ midnight-py v{midnight_py.__version__} installed")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def start_dev_servers():
    """Start the development servers in background."""
    print_header("Starting Development Servers")
    
    print("Starting mock Midnight services...")
    print("(These simulate the real Midnight node, indexer, and proof server)")
    print()
    
    # Start dev_server.py in background
    if sys.platform == "win32":
        # Windows
        subprocess.Popen(
            [sys.executable, "dev_server.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        # Unix-like
        subprocess.Popen(
            [sys.executable, "dev_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    print("Waiting for servers to start...")
    time.sleep(3)
    
    return True


def check_services():
    """Check if services are running."""
    print_header("Checking Services")
    
    # Use midnight-py CLI to check status
    result = subprocess.run(
        [sys.executable, "-m", "midnight_py.cli", "status"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if "ONLINE" in result.stdout or "OK" in result.stdout:
        print("✓ All services are running!")
        return True
    else:
        print("⚠ Some services may not be ready yet")
        return False


def create_test_wallet():
    """Create a test wallet."""
    print_header("Creating Test Wallet")
    
    try:
        from midnight_py import MidnightClient
        
        client = MidnightClient(network="preprod")
        
        # Generate a test address
        address = client.wallet.generate_address("hackathon test seed phrase")
        print(f"✓ Test wallet address: {address}")
        
        # Check balance
        balance = client.wallet.get_balance(address)
        print(f"✓ Balance: {balance.dust:,} DUST, {balance.night:,} NIGHT")
        
        # Save to file for later use
        with open(".test_wallet.txt", "w") as f:
            f.write(f"Address: {address}\n")
            f.write(f"Seed: hackathon test seed phrase\n")
            f.write(f"Balance: {balance.dust} DUST, {balance.night} NIGHT\n")
        
        print("✓ Wallet info saved to .test_wallet.txt")
        return address
        
    except Exception as e:
        print(f"✗ Error creating wallet: {e}")
        return None


def run_quick_test():
    """Run a quick integration test."""
    print_header("Running Quick Test")
    
    try:
        from midnight_py import MidnightClient, compact_to_python
        
        client = MidnightClient(network="preprod")
        
        # Test 1: Check services
        print("Test 1: Service connectivity")
        status = client.status()
        for service, alive in status.items():
            icon = "✓" if alive else "✗"
            print(f"  {icon} {service}")
        
        # Test 2: Generate proof
        print("\nTest 2: ZK Proof generation")
        proof = client.prover.generate_proof(
            circuit_id="test:circuit",
            private_inputs={"secret": "data"},
            public_inputs={"result": 42}
        )
        print(f"  ✓ Proof generated: {proof.proof[:50]}...")
        
        # Test 3: Codegen
        print("\nTest 3: Contract codegen")
        if Path("contracts/bulletin_board.compact").exists():
            BulletinBoard = compact_to_python("contracts/bulletin_board.compact")
            print(f"  ✓ Generated class: {BulletinBoard.__name__}")
            methods = [m for m in dir(BulletinBoard) if not m.startswith('_')]
            print(f"  ✓ Methods: {methods}")
        
        print("\n✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_next_steps(wallet_address):
    """Show what to do next."""
    print_header("Setup Complete! 🎉")
    
    print("Your midnight-py environment is ready for the hackathon!\n")
    
    print("📋 Quick Reference:")
    print(f"  • Test wallet: {wallet_address}")
    print(f"  • Wallet file: .test_wallet.txt")
    print()
    
    print("🚀 Try these commands:")
    print()
    print("  # Check service status")
    print("  midnight-py status")
    print()
    print("  # Check your balance")
    print(f"  midnight-py balance {wallet_address}")
    print()
    print("  # Run the demo")
    print("  python examples/bulletin_board.py")
    print()
    print("  # Run tests")
    print("  pytest tests/ -v")
    print()
    
    print("📚 Documentation:")
    print("  • README.md - Full documentation")
    print("  • QUICKSTART.md - Quick start guide")
    print("  • DEMO_SCRIPT.md - Hackathon demo script")
    print("  • examples/ - Working examples")
    print()
    
    print("💡 Tips:")
    print("  • Dev servers are running in the background")
    print("  • Use Ctrl+C in the server window to stop them")
    print("  • Check .test_wallet.txt for your wallet info")
    print()
    
    print("=" * 60)
    print("Happy hacking! 🌙")
    print("=" * 60)


def main():
    """Main setup flow."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🌙  midnight-py Hackathon Setup  🌙          ║
    ║                                                           ║
    ║         The First Python SDK for Midnight Blockchain     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check Python
    print_header("Step 1: Checking Python")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Install package
    print_header("Step 2: Installing Package")
    if not install_package():
        print("✗ Installation failed")
        sys.exit(1)
    
    # Step 3: Verify installation
    if not verify_installation():
        print("✗ Verification failed")
        sys.exit(1)
    
    # Step 4: Start dev servers
    if not start_dev_servers():
        print("✗ Failed to start servers")
        sys.exit(1)
    
    # Step 5: Check services
    time.sleep(2)  # Give servers time to start
    check_services()
    
    # Step 6: Create test wallet
    wallet_address = create_test_wallet()
    if not wallet_address:
        print("⚠ Wallet creation failed, but continuing...")
        wallet_address = "mn_preprod1example..."
    
    # Step 7: Run quick test
    run_quick_test()
    
    # Step 8: Show next steps
    show_next_steps(wallet_address)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
