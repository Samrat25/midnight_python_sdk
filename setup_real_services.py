#!/usr/bin/env python3
"""
Setup script for real Midnight Docker services.
This will start all services and fund your wallet.
"""

import subprocess
import sys
import time
import json
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

console = Console()


def run_command(cmd, description, check=True, capture=True):
    """Run a command and show output."""
    console.print(f"→ {description}...")
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                check=check,
                capture_output=True,
                text=True
            )
            return result
        else:
            result = subprocess.run(cmd, shell=True, check=check)
            return result
    except subprocess.CalledProcessError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        if e.stderr:
            console.print(e.stderr)
        return None


def check_docker():
    """Check if Docker is installed and running."""
    console.print("\n[bold]Checking Docker...[/bold]")
    
    result = run_command("docker --version", "Checking Docker installation")
    if not result:
        console.print("[red]✗ Docker not found. Please install Docker Desktop.[/red]")
        console.print("Download from: https://www.docker.com/products/docker-desktop")
        return False
    
    console.print(f"✓ {result.stdout.strip()}")
    
    result = run_command("docker info", "Checking Docker daemon", check=False)
    if not result or result.returncode != 0:
        console.print("[red]✗ Docker daemon not running. Please start Docker Desktop.[/red]")
        return False
    
    console.print("✓ Docker daemon is running")
    return True


def stop_existing_services():
    """Stop any existing Midnight services."""
    console.print("\n[bold]Stopping existing services...[/bold]")
    
    # Stop dev_server.py if running
    if sys.platform == "win32":
        run_command("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq dev_server*\"", 
                   "Stopping dev_server.py", check=False)
    else:
        run_command("pkill -f dev_server.py", "Stopping dev_server.py", check=False)
    
    # Stop docker containers
    run_command("docker-compose -f docker-compose.real.yml down", 
               "Stopping Docker containers", check=False)
    
    console.print("✓ Existing services stopped")


def pull_images():
    """Pull Docker images (this may take a while)."""
    console.print("\n[bold]Pulling Docker images...[/bold]")
    console.print("[yellow]This may take 5-10 minutes on first run...[/yellow]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Pulling images...", total=None)
        
        result = run_command(
            "docker-compose -f docker-compose.real.yml pull",
            "Pulling images",
            capture=False
        )
        
        progress.update(task, completed=True)
    
    if result and result.returncode == 0:
        console.print("✓ Images pulled successfully")
        return True
    else:
        console.print("[yellow]⚠ Some images may not be available yet[/yellow]")
        console.print("[yellow]Falling back to midnight-local-dev setup...[/yellow]")
        return False


def start_services():
    """Start Docker services."""
    console.print("\n[bold]Starting Midnight services...[/bold]")
    
    result = run_command(
        "docker-compose -f docker-compose.real.yml up -d",
        "Starting containers",
        capture=False
    )
    
    if not result or result.returncode != 0:
        return False
    
    console.print("✓ Services started")
    return True


def wait_for_services():
    """Wait for services to be healthy."""
    console.print("\n[bold]Waiting for services to be ready...[/bold]")
    
    services = {
        "Node": "http://127.0.0.1:9944",
        "Indexer": "http://127.0.0.1:8088/api/v3/graphql",
        "Proof Server": "http://127.0.0.1:6300",
    }
    
    max_wait = 60  # seconds
    start_time = time.time()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for service, url in services.items():
            task = progress.add_task(f"Waiting for {service}...", total=None)
            
            while time.time() - start_time < max_wait:
                try:
                    import httpx
                    client = httpx.Client(timeout=5.0)
                    
                    if "graphql" in url:
                        response = client.post(url, json={"query": "{ __typename }"})
                    else:
                        response = client.get(f"{url.rstrip('/')}/health")
                    
                    if response.status_code == 200:
                        progress.update(task, completed=True)
                        console.print(f"✓ {service} is ready")
                        break
                except:
                    pass
                
                time.sleep(2)
            else:
                console.print(f"[yellow]⚠ {service} not ready yet (may need more time)[/yellow]")


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


def create_wallet():
    """Create wallet from mnemonic."""
    console.print("\n[bold]Creating wallet...[/bold]")
    
    mnemonic = load_mnemonic()
    
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
        console.print(f"[red]✗ Error creating wallet: {e}[/red]")
        return None


def check_services_status():
    """Check if services are running."""
    console.print("\n[bold]Checking service status...[/bold]")
    
    result = run_command("midnight-py status --network local", "Checking services", capture=False)
    return result and result.returncode == 0


def show_next_steps(wallet_info):
    """Show what to do next."""
    console.rule("[bold green]Setup Complete!")
    
    console.print("\n[bold]Your Midnight environment is ready![/bold]\n")
    
    if wallet_info:
        console.print(f"[bold]Wallet Address:[/bold] [cyan]{wallet_info['address']}[/cyan]")
        console.print(f"[bold]Private Key:[/bold] {wallet_info['private_key'][:16]}...\n")
    
    console.print("[bold]Next steps:[/bold]\n")
    console.print("1. Check services:")
    console.print("   [cyan]midnight-py status[/cyan]\n")
    
    console.print("2. Check your balance:")
    if wallet_info:
        console.print(f"   [cyan]midnight-py balance {wallet_info['address']}[/cyan]\n")
    
    console.print("3. Run the real demo:")
    console.print("   [cyan]python examples/real_demo.py[/cyan]\n")
    
    console.print("[bold]Docker containers:[/bold]")
    console.print("  • View logs: [cyan]docker-compose -f docker-compose.real.yml logs -f[/cyan]")
    console.print("  • Stop: [cyan]docker-compose -f docker-compose.real.yml down[/cyan]")
    console.print("  • Restart: [cyan]docker-compose -f docker-compose.real.yml restart[/cyan]\n")
    
    console.print("[bold green]Ready for hackathon! 🚀🌙[/bold green]")


def fallback_to_local_dev():
    """Provide instructions for midnight-local-dev."""
    console.rule("[yellow]Alternative Setup")
    
    console.print("\n[bold]Docker images not available yet.[/bold]")
    console.print("Use the official midnight-local-dev instead:\n")
    
    console.print("[bold]Setup:[/bold]")
    console.print("1. Clone midnight-local-dev:")
    console.print("   [cyan]git clone https://github.com/midnightntwrk/midnight-local-dev[/cyan]")
    console.print("   [cyan]cd midnight-local-dev[/cyan]\n")
    
    console.print("2. Install and start:")
    console.print("   [cyan]npm install[/cyan]")
    console.print("   [cyan]npm start[/cyan]\n")
    
    console.print("3. Fund your wallet:")
    console.print("   • Choose option [1] in the menu")
    console.print("   • Enter your mnemonic from mnemonic.txt\n")
    
    console.print("4. Run the demo:")
    console.print("   [cyan]python examples/real_demo.py[/cyan]\n")


def main():
    """Main setup flow."""
    console.print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         🌙  Midnight Real Services Setup  🌙              ║
    ║                                                           ║
    ║              Docker-based Real Network                    ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check Docker
    if not check_docker():
        sys.exit(1)
    
    # Stop existing services
    stop_existing_services()
    
    # Try to pull and start Docker services
    console.print("\n[bold]Attempting to use Docker containers...[/bold]")
    
    if pull_images():
        if start_services():
            wait_for_services()
            wallet_info = create_wallet()
            
            if check_services_status():
                show_next_steps(wallet_info)
            else:
                console.print("\n[yellow]⚠ Services started but not fully ready yet[/yellow]")
                console.print("Wait a minute and run: [cyan]midnight-py status[/cyan]")
        else:
            console.print("[red]✗ Failed to start services[/red]")
            fallback_to_local_dev()
    else:
        fallback_to_local_dev()


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
