#!/usr/bin/env python3
"""
Fix Docker conflicts and start Midnight services properly.
"""

import subprocess
import sys
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

console = Console()


def run_command(cmd, description, check=False):
    """Run a command and show output."""
    console.print(f"→ {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            console.print(result.stdout.strip())
        return result.returncode == 0
    except Exception as e:
        console.print(f"[yellow]⚠ {e}[/yellow]")
        return False


def stop_and_remove_containers():
    """Stop and remove all midnight containers."""
    console.print("\n[bold]Cleaning up existing containers...[/bold]")
    
    # Stop all midnight containers
    run_command(
        'docker ps -a --filter "name=midnight" -q | ForEach-Object { docker stop $_ }',
        "Stopping midnight containers"
    )
    
    # Remove all midnight containers
    run_command(
        'docker ps -a --filter "name=midnight" -q | ForEach-Object { docker rm $_ }',
        "Removing midnight containers"
    )
    
    # Also remove any testcontainers
    run_command(
        'docker ps -a --filter "name=testcontainers" -q | ForEach-Object { docker rm -f $_ }',
        "Removing testcontainers"
    )
    
    console.print("✓ Containers cleaned up")


def start_midnight_services():
    """Start midnight-local-dev services."""
    console.print("\n[bold]Starting Midnight services...[/bold]")
    console.print("[yellow]This will open in a new window...[/yellow]\n")
    
    # Start in new window
    subprocess.Popen(
        ["cmd", "/c", "start", "cmd", "/k", "cd ../midnight-local-dev && npm start"],
        shell=True
    )
    
    console.print("✓ Services starting in new window")
    console.print("[yellow]⏳ Waiting 45 seconds for services to initialize...[/yellow]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Starting services...", total=45)
        for i in range(45):
            time.sleep(1)
            progress.update(task, advance=1)


def check_services():
    """Check if services are running."""
    console.print("\n[bold]Checking service status...[/bold]\n")
    
    result = subprocess.run(
        ["midnight-py", "status"],
        capture_output=True,
        text=True
    )
    
    console.print(result.stdout)
    
    return "ONLINE" in result.stdout


def show_wallet_info():
    """Show wallet information."""
    console.print("\n[bold]Your Wallet Information:[/bold]\n")
    
    console.print(f"[bold]Address:[/bold] [cyan]mn_addr_undeployed1zaa268rc7sjz0ctscrsy7mp2ne7khfz8wu2uqsu4msfvxnlt6qfsmfrhr0[/cyan]")
    console.print(f"[bold]Mnemonic:[/bold] (from mnemonic.txt)")
    
    # Read mnemonic
    try:
        with open("mnemonic.txt") as f:
            mnemonic = f.read().strip()
        console.print(f"  {mnemonic[:50]}...")
    except:
        pass


def show_next_steps(services_ready):
    """Show what to do next."""
    console.rule("[bold]Next Steps")
    
    if not services_ready:
        console.print("\n[yellow]⚠ Services are still starting...[/yellow]\n")
        console.print("1. Wait another minute")
        console.print("2. Check status: [cyan]midnight-py status[/cyan]")
        console.print("3. If still offline, check the midnight-local-dev window for errors\n")
    else:
        console.print("\n[green]✓ Services are ready![/green]\n")
        console.print("1. Fund your wallet:")
        console.print("   • In the midnight-local-dev window, choose option [1]")
        console.print("   • Your mnemonic from mnemonic.txt will be used\n")
        
        console.print("2. Check balance:")
        console.print("   [cyan]midnight-py balance mn_addr_undeployed1zaa268rc7sjz0ctscrsy7mp2ne7khfz8wu2uqsu4msfvxnlt6qfsmfrhr0[/cyan]\n")
        
        console.print("3. Run the demo:")
        console.print("   [cyan]python examples/real_demo.py[/cyan]\n")


def main():
    """Main fix and start flow."""
    console.print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         🌙  Fix & Start Midnight Services  🌙             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Clean up containers
    stop_and_remove_containers()
    
    # Show wallet info
    show_wallet_info()
    
    # Start services
    start_midnight_services()
    
    # Check services
    services_ready = check_services()
    
    # Show next steps
    show_next_steps(services_ready)
    
    if services_ready:
        console.print("\n[bold green]🎉 Ready to go![/bold green]")
    else:
        console.print("\n[yellow]⏳ Services still starting... be patient![/yellow]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]✗ Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)
