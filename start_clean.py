#!/usr/bin/env python3
"""
Clean start script for Midnight services.
Removes all conflicts and starts fresh.
"""

import subprocess
import sys
import time
import json
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import print as rprint

console = Console()

WALLET_ADDRESS = "mn_addr_undeployed1zaa268rc7sjz0ctscrsy7mp2ne7khfz8wu2uqsu4msfvxnlt6qfsmfrhr0"


def run_cmd(cmd, description=None, check=False):
    """Run a command."""
    if description:
        console.print(f"→ {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return result
    except Exception as e:
        if description:
            console.print(f"[yellow]⚠ {e}[/yellow]")
        return None


def clean_docker():
    """Clean all Docker containers and networks."""
    console.print("\n[bold]Step 1: Cleaning Docker environment...[/bold]")
    
    # Stop all containers
    run_cmd('docker ps -q | ForEach-Object { docker stop $_ }', "Stopping all containers")
    
    # Remove midnight containers
    run_cmd('docker ps -a --filter "name=midnight" -q | ForEach-Object { docker rm -f $_ }', 
            "Removing midnight containers")
    
    # Remove testcontainers
    run_cmd('docker ps -a --filter "name=testcontainers" -q | ForEach-Object { docker rm -f $_ }',
            "Removing testcontainers")
    
    # Prune networks
    run_cmd('docker network prune -f', "Cleaning networks")
    
    # Prune volumes
    run_cmd('docker volume prune -f', "Cleaning volumes")
    
    console.print("✓ Docker environment cleaned\n")


def update_demo_with_correct_address():
    """Update the demo file with the correct wallet address."""
    console.print("[bold]Step 2: Updating demo with your wallet address...[/bold]")
    
    demo_file = Path("examples/real_demo.py")
    if demo_file.exists():
        try:
            content = demo_file.read_text(encoding='utf-8')
            console.print(f"✓ Demo already configured to use mnemonic.txt")
            console.print(f"✓ Your address: [cyan]{WALLET_ADDRESS}[/cyan]\n")
        except Exception as e:
            console.print(f"[yellow]⚠ Could not read demo file: {e}[/yellow]\n")
    else:
        console.print("[yellow]⚠ Demo file not found[/yellow]\n")


def start_services():
    """Start midnight-local-dev services."""
    console.print("[bold]Step 3: Starting Midnight services...[/bold]")
    console.print("[yellow]A new window will open with the services...[/yellow]\n")
    
    # Start in new window
    subprocess.Popen(
        ["cmd", "/c", "start", "cmd", "/k", "cd ../midnight-local-dev && npm start"],
        shell=True
    )
    
    console.print("✓ Services starting in new window\n")
    
    # Wait with progress bar
    console.print("[yellow]⏳ Waiting for services to initialize (60 seconds)...[/yellow]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Starting...", total=60)
        for i in range(60):
            time.sleep(1)
            progress.update(task, advance=1)
    
    console.print()


def check_services():
    """Check if services are running."""
    console.print("[bold]Step 4: Checking service status...[/bold]\n")
    
    result = run_cmd("midnight-py status")
    if result:
        console.print(result.stdout)
        return "ONLINE" in result.stdout
    return False


def check_balance():
    """Check wallet balance."""
    console.print(f"\n[bold]Step 5: Checking wallet balance...[/bold]\n")
    
    result = run_cmd(f"midnight-py balance {WALLET_ADDRESS}")
    if result and result.returncode == 0:
        console.print(result.stdout)
        
        if "0" in result.stdout or result.stdout.strip() == "":
            console.print("[yellow]⚠ Wallet needs funding[/yellow]")
            return False
        else:
            console.print("[green]✓ Wallet is funded![/green]")
            return True
    else:
        console.print("[yellow]⚠ Could not check balance (services may not be ready)[/yellow]")
        return False


def show_instructions(services_ready, wallet_funded):
    """Show what to do next."""
    console.rule("[bold]Setup Status")
    
    console.print()
    
    # Status table
    from rich.table import Table
    table = Table(show_header=True)
    table.add_column("Component", style="bold")
    table.add_column("Status")
    
    if services_ready:
        table.add_row("Services", "[green]✓ ONLINE[/green]")
    else:
        table.add_row("Services", "[yellow]⏳ STARTING[/yellow]")
    
    if wallet_funded:
        table.add_row("Wallet", "[green]✓ FUNDED[/green]")
    else:
        table.add_row("Wallet", "[yellow]⚠ NEEDS FUNDING[/yellow]")
    
    console.print(table)
    console.print()
    
    # Instructions
    console.print("[bold]Your Wallet:[/bold]")
    console.print(f"  Address: [cyan]{WALLET_ADDRESS}[/cyan]")
    console.print(f"  Mnemonic: (from mnemonic.txt)\n")
    
    if not services_ready:
        console.print("[bold yellow]⏳ Services Still Starting[/bold yellow]\n")
        console.print("Wait another minute, then check:")
        console.print("  [cyan]midnight-py status[/cyan]\n")
        console.print("If services don't start, check the midnight-local-dev window for errors.\n")
    
    elif not wallet_funded:
        console.print("[bold yellow]⚠ Fund Your Wallet[/bold yellow]\n")
        console.print("In the midnight-local-dev window:")
        console.print("  1. Choose option [1] to fund wallet")
        console.print("  2. Your mnemonic from mnemonic.txt will be used")
        console.print("  3. Wait for 'Funding complete' message\n")
        console.print("Then check balance:")
        console.print(f"  [cyan]midnight-py balance {WALLET_ADDRESS}[/cyan]\n")
    
    else:
        console.print("[bold green]✓ Everything Ready![/bold green]\n")
        console.print("Run the demo:")
        console.print("  [cyan]python examples/real_demo.py[/cyan]\n")
        console.print("Or deploy your own contract:")
        console.print("  [cyan]midnight-py deploy contracts/bulletin_board.compact --key YOUR_KEY[/cyan]\n")


def save_wallet_info():
    """Save wallet info for easy access."""
    wallet_info = {
        "address": WALLET_ADDRESS,
        "mnemonic_file": "mnemonic.txt",
        "network": "local"
    }
    
    with open(".wallet_info.json", "w") as f:
        json.dump(wallet_info, f, indent=2)
    
    console.print("✓ Wallet info saved to .wallet_info.json\n")


def main():
    """Main flow."""
    console.print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         🌙  Midnight Clean Start  🌙                      ║
    ║                                                           ║
    ║         Fresh setup with your wallet                      ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Clean Docker
    clean_docker()
    
    # Update demo
    update_demo_with_correct_address()
    
    # Save wallet info
    save_wallet_info()
    
    # Start services
    start_services()
    
    # Check services
    services_ready = check_services()
    
    # Check balance
    wallet_funded = False
    if services_ready:
        wallet_funded = check_balance()
    
    # Show instructions
    show_instructions(services_ready, wallet_funded)
    
    if services_ready and wallet_funded:
        console.print("\n[bold green]🎉 Ready for hackathon![/bold green]")
        return 0
    else:
        console.print("\n[yellow]⏳ Setup in progress... follow the steps above[/yellow]")
        return 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted.[/yellow]")
        exit(1)
    except Exception as e:
        console.print(f"\n[red]✗ Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        exit(1)
