#!/usr/bin/env python3
"""Check if Midnight services are running"""

import socket
from rich import print as rprint
from rich.console import Console

console = Console()

def check_port(host, port, name):
    """Check if a port is listening"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

console.rule("[bold]Midnight Services Status")

services = [
    ("Node", "127.0.0.1", 9944),
    ("Indexer", "127.0.0.1", 8088),
    ("Prover", "127.0.0.1", 6300),
]

all_running = True

rprint()
for name, host, port in services:
    is_running = check_port(host, port, name)
    status = "[green]✓ RUNNING[/green]" if is_running else "[red]✗ NOT RUNNING[/red]"
    rprint(f"  {name:10} (port {port}): {status}")
    if not is_running:
        all_running = False

rprint()

if all_running:
    rprint("[bold green]✓ All services are running![/bold green]")
    rprint("\nYou can now:")
    rprint("  [cyan]python check_balance.py[/cyan]")
    rprint("  [cyan]python examples/private_ml_demo.py[/cyan]")
else:
    rprint("[bold red]✗ Some services are NOT running![/bold red]")
    rprint("\nStart them:")
    rprint("  [yellow]cd ../midnight-local-dev[/yellow]")
    rprint("  [yellow]npm start[/yellow]")
    rprint("\nOr see: [cyan]START_SERVICES.md[/cyan]")

rprint()
