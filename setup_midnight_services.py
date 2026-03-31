#!/usr/bin/env python3
"""
Complete setup for Midnight services using the official midnight-local-dev.
This script will clone, install, and start everything automatically.
"""

import subprocess
import sys
import time
import json
import os
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

console = Console()


def run_command(cmd, description, cwd=None, check=True, capture=True, shell=True):
    """Run a command and show output."""
    console.print(f"→ {description}...")
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=shell,
                check=check,
                capture_output=True,
                text=True,
                cwd=cwd
            )
            return result
        else:
            result = subprocess.run(cmd, shell=shell, check=check, cwd=cwd)
            return result
    except subprocess.CalledProcessError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        if e.stderr:
            console.print(e.stderr)
        return None


def check_prerequisites():
    """Check if required tools are installed."""
    console.print("\n[bold]Checking prerequisites...[/bold]")
    
    # Check Node.js
    result = run_command("node --version", "Checking Node.js")
    if not result:
        console.print("[red]✗ Node.js not found. Please install Node.js 18+[/red]")
        console.print("Download from: https://nodejs.org/")
        return False
    console.print(f"✓ Node.js {result.stdout.strip()}")
    
    # Check npm
    result = run_command("npm --version", "Checking npm")
    if not result:
        console.print("[red]✗ npm not found[/red]")
        return False
    console.print(f"✓ npm {result.stdout.strip()}")
    
    # Check git
    result = run_command("git --version", "Checking git")
    if not result:
        console.print("[red]✗ git not found. Please install git[/red]")
        return False
    console.print(f"✓ {result.stdout.strip()}")
    
    return True


def clone_midnight_local_dev():
    """Clone the midnight-local-dev repository."""
    console.print("\n[bold]Setting up midnight-local-dev...[/bold]")
    
    local_dev_path = Path("../midnight-local-dev")
    
    if local_dev_path.exists():
        console.print("✓ midnight-local-dev already exists")
        return str(local_dev_path.absolute())
    
    console.print("Cloning midnight-local-dev repository...")
    result = run_command(
        "git clone https://github.com/midnightntwrk/midnight-local-dev.git",
        "Cloning repository",
        cwd="..",
        capture=False
    )
    
    if result and result.returncode == 0:
        console.print("✓ Repository cloned")
        return str(local_dev_path.absolute())
    else:
        console.print("[red]✗ Failed to clone repository[/red]")
        return None


def install_dependencies(local_dev_path):
    """Install npm dependencies."""
    console.print("\n[bold]Installing dependencies...[/bold]")
    console.print("[yellow]This may take a few minutes...[/yellow]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Installing npm packages...", total=None)
        
        result = run_command(
            "npm install",
            "Installing dependencies",
            cwd=local_dev_path,
            capture=False
        )
        
        progress.update(task, completed=True)
    
    if result and result.returncode == 0:
        console.print("✓ Dependencies installed")
        return True
    else:
        console.print("[red]✗ Failed to install dependencies[/red]")
        return False


def load_mnemonic():
    """Load mnemonic from file."""
    mnemonic_file = Path("mnemonic.txt")
    if mnemonic_file.exists():
        mnemonic = mnemonic_file.read_text().strip()
        console.print(f"✓ Loaded mnemonic from mnemonic.txt")
        return mnemonic
    else:
        console.print("[yellow]⚠ mnemonic.txt not found, using default[/yellow]")
        return "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art"


def create_wallet_config(local_dev_path):
    """Create wallet configuration file."""
    console.print("\n[bold]Creating wallet configuration...[/bold]")
    
    mnemonic = load_mnemonic()
    
    # Create config directory if it doesn't exist
    config_dir = Path(local_dev_path) / "config"
    config_dir.mkdir(exist_ok=True)
    
    # Create wallet config
    wallet_config = {
        "mnemonic": mnemonic,
        "network": "undeployed"
    }
    
    config_file = config_dir / "wallet.json"
    with open(config_file, "w") as f:
        json.dump(wallet_config, f, indent=2)
    
    console.print(f"✓ Wallet config created at {config_file}")
    
    # Also create wallet info in our directory
    try:
        from midnight_py import MidnightClient
        
        client = MidnightClient(network="local")
        wallet_info = client.wallet.generate_from_mnemonic(mnemonic, "undeployed")
        
        console.print(f"✓ Address: [cyan]{wallet_info['address']}[/cyan]")
        console.print(f"✓ Private key: {wallet_info['private_key'][:16]}...")
        
        # Save wallet info
        with open(".wallet_info.json", "w") as f:
            json.dump(wallet_info, f, indent=2)
        
        console.print("✓ Wallet info saved to .wallet_info.json")
        return wallet_info
    except Exception as e:
        console.print(f"[yellow]⚠ Could not generate wallet info: {e}[/yellow]")
        return None


def start_services_background(local_dev_path):
    """Start midnight services in the background."""
    console.print("\n[bold]Starting Midnight services...[/bold]")
    console.print("[yellow]Services will run in the background...[/yellow]")
    
    # Create a start script
    if sys.platform == "win32":
        start_script = Path(local_dev_path) / "start_services.bat"
        with open(start_script, "w") as f:
            f.write("@echo off\n")
            f.write("cd /d %~dp0\n")
            f.write("npm start\n")
        
        # Start in new window
        subprocess.Popen(
            ["cmd", "/c", "start", "cmd", "/k", str(start_script)],
            cwd=local_dev_path
        )
    else:
        start_script = Path(local_dev_path) / "start_services.sh"
        with open(start_script, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("cd \"$(dirname \"$0\")\"\n")
            f.write("npm start\n")
        
        os.chmod(start_script, 0o755)
        
        # Start in background
        subprocess.Popen(
            ["bash", str(start_script)],
            cwd=local_dev_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    console.print("✓ Services starting in new window...")
    console.print("[yellow]⏳ Waiting for services to be ready (30 seconds)...[/yellow]")
    time.sleep(30)


def wait_for_services():
    """Wait for services to be ready."""
    console.print("\n[bold]Checking service status...[/bold]")
    
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            result = subprocess.run(
                ["midnight-py", "status", "--network", "local"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "ONLINE" in result.stdout:
                console.print("✓ Services are ready!")
                console.print(result.stdout)
                return True
        except:
            pass
        
        if attempt < max_attempts - 1:
            console.print(f"⏳ Attempt {attempt + 1}/{max_attempts}... waiting...")
            time.sleep(5)
    
    console.print("[yellow]⚠ Services may need more time to start[/yellow]")
    console.print("Check status with: [cyan]midnight-py status[/cyan]")
    return False


def show_next_steps(wallet_info, local_dev_path):
    """Show what to do next."""
    console.rule("[bold green]Setup Complete!")
    
    console.print("\n[bold]Midnight services are starting![/bold]\n")
    
    if wallet_info:
        console.print(f"[bold]Wallet Address:[/bold] [cyan]{wallet_info['address']}[/cyan]")
        console.print(f"[bold]Private Key:[/bold] {wallet_info['private_key'][:16]}...\n")
    
    console.print("[bold]Services running in:[/bold]")
    console.print(f"  {local_dev_path}\n")
    
    console.print("[bold]Next steps:[/bold]\n")
    
    console.print("1. Fund your wallet:")
    console.print("   • In the midnight-local-dev window, choose option [1]")
    console.print("   • Your mnemonic is already configured\n")
    
    console.print("2. Check services:")
    console.print("   [cyan]midnight-py status[/cyan]\n")
    
    console.print("3. Check balance:")
    if wallet_info:
        console.print(f"   [cyan]midnight-py balance {wallet_info['address']}[/cyan]\n")
    
    console.print("4. Run the real demo:")
    console.print("   [cyan]python examples/real_demo.py[/cyan]\n")
    
    console.print("[bold]Useful commands:[/bold]")
    console.print(f"  • View logs: [cyan]cd {local_dev_path} && npm run logs[/cyan]")
    console.print(f"  • Stop services: [cyan]cd {local_dev_path} && npm run stop[/cyan]")
    console.print(f"  • Restart: [cyan]cd {local_dev_path} && npm start[/cyan]\n")
    
    console.print("[bold green]Ready for hackathon! 🚀🌙[/bold green]")


def main():
    """Main setup flow."""
    console.print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         🌙  Midnight Services Setup  🌙                   ║
    ║                                                           ║
    ║         Official midnight-local-dev Setup                 ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check prerequisites
    if not check_prerequisites():
        console.print("\n[red]Please install missing prerequisites and try again.[/red]")
        sys.exit(1)
    
    # Clone midnight-local-dev
    local_dev_path = clone_midnight_local_dev()
    if not local_dev_path:
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies(local_dev_path):
        sys.exit(1)
    
    # Create wallet config
    wallet_info = create_wallet_config(local_dev_path)
    
    # Start services
    start_services_background(local_dev_path)
    
    # Wait for services
    wait_for_services()
    
    # Show next steps
    show_next_steps(wallet_info, local_dev_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Setup interrupted.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]✗ Setup failed: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)
