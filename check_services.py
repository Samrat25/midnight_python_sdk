#!/usr/bin/env python3
"""
Quick script to check if Midnight services are ready.
Run this to verify everything is working.
"""

import subprocess
import time
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()


def check_service_status():
    """Check if services are running."""
    console.print("\n[bold]Checking Midnight Services...[/bold]\n")
    
    result = subprocess.run(
        ["midnight-py", "status", "--network", "local"],
        capture_output=True,
        text=True
    )
    
    console.print(result.stdout)
    
    if "ONLINE" in result.stdout:
        return True
    return False


def check_wallet():
    """Check wallet info."""
    console.print("\n[bold]Checking Wallet...[/bold]\n")
    
    wallet_file = Path(".wallet_info.json")
    if wallet_file.exists():
        with open(wallet_file) as f:
            wallet_info = json.load(f)
        
        console.print(f"[bold]Address:[/bold] [cyan]{wallet_info['address']}[/cyan]")
        console.print(f"[bold]Private Key:[/bold] {wallet_info['private_key'][:16]}...")
        
        # Try to check balance
        try:
            result = subprocess.run(
                ["midnight-py", "balance", wallet_info['address']],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                console.print("\n[bold]Balance:[/bold]")
                console.print(result.stdout)
                
                if "0" in result.stdout and "DUST" in result.stdout:
                    console.print("[yellow]⚠ Wallet needs funding![/yellow]")
                    console.print("Fund it in the midnight-local-dev window (option 1)")
                    return False
                else:
                    console.print("[green]✓ Wallet is funded![/green]")
                    return True
        except:
            console.print("[yellow]⚠ Could not check balance (services may not be ready)[/yellow]")
            return False
    else:
        console.print("[red]✗ Wallet info not found[/red]")
        return False


def show_next_steps(services_ready, wallet_funded):
    """Show what to do next."""
    console.print("\n")
    console.rule("[bold]Status Summary")
    
    table = Table(show_header=True)
    table.add_column("Check", style="bold")
    table.add_column("Status")
    table.add_column("Action")
    
    # Services
    if services_ready:
        table.add_row(
            "Services",
            "[green]✓ ONLINE[/green]",
            "Ready to use"
        )
    else:
        table.add_row(
            "Services",
            "[yellow]⏳ STARTING[/yellow]",
            "Wait 1-2 minutes, then run this script again"
        )
    
    # Wallet
    if wallet_funded:
        table.add_row(
            "Wallet",
            "[green]✓ FUNDED[/green]",
            "Ready to deploy contracts"
        )
    else:
        table.add_row(
            "Wallet",
            "[yellow]⚠ NEEDS FUNDING[/yellow]",
            "Fund in midnight-local-dev window (option 1)"
        )
    
    console.print(table)
    
    # Next steps
    console.print("\n[bold]Next Steps:[/bold]\n")
    
    if not services_ready:
        console.print("1. Wait for services to start (1-2 minutes)")
        console.print("2. Run this script again: [cyan]python check_services.py[/cyan]\n")
    elif not wallet_funded:
        console.print("1. Go to the midnight-local-dev window")
        console.print("2. Choose option [1] to fund wallet")
        console.print("3. Run this script again: [cyan]python check_services.py[/cyan]\n")
    else:
        console.print("[green]✓ Everything is ready![/green]\n")
        console.print("Run the demo:")
        console.print("  [cyan]python examples/real_demo.py[/cyan]\n")


def main():
    """Main check flow."""
    console.print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         🌙  Midnight Services Check  🌙                   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    services_ready = check_service_status()
    wallet_funded = check_wallet()
    
    show_next_steps(services_ready, wallet_funded)
    
    if services_ready and wallet_funded:
        console.print("\n[bold green]🎉 Ready for hackathon![/bold green]")
        return 0
    else:
        console.print("\n[yellow]⏳ Setup in progress...[/yellow]")
        return 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Check interrupted.[/yellow]")
        exit(1)
    except Exception as e:
        console.print(f"\n[red]✗ Check failed: {e}[/red]")
        import traceback
        traceback.print_exc()
        exit(1)
