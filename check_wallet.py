#!/usr/bin/env python3
"""Check wallet balance"""

from midnight_py import MidnightClient
import json
from rich import print as rprint

# Load wallet info
with open('.wallet_info.json') as f:
    wallet_info = json.load(f)

client = MidnightClient(network='local')

rprint(f"\n[bold]Wallet Address:[/bold] [cyan]{wallet_info['address']}[/cyan]")
rprint(f"[bold]Network:[/bold] {wallet_info['network']}")

try:
    balance = client.wallet.get_balance(wallet_info['address'])
    rprint(f"\n[bold green]✓ Wallet Balance:[/bold green]")
    rprint(f"  NIGHT: [cyan]{balance.night:,}[/cyan]")
    rprint(f"  DUST:  [cyan]{balance.dust:,}[/cyan]")
    
    if balance.night >= 50000000000:
        rprint(f"\n[bold green]✓ Wallet is funded! You received 50,000,000,000 NIGHT tokens.[/bold green]")
    else:
        rprint(f"\n[yellow]⚠ Wallet has {balance.night} NIGHT (expected 50,000,000,000)[/yellow]")
        
except Exception as e:
    rprint(f"\n[red]✗ Error checking balance: {e}[/red]")
