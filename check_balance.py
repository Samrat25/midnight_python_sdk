#!/usr/bin/env python3
"""Quick balance checker for your wallet"""

import httpx
from rich import print as rprint

ADDRESS = "mn_addr_undeployed1zaa268rc7sjz0ctscrsy7mp2ne7khfz8wu2uqsu4msfvxnlt6qfsmfrhr0"

rprint(f"\n[bold]Checking balance for:[/bold]")
rprint(f"[cyan]{ADDRESS}[/cyan]\n")

try:
    r = httpx.post(
        "http://127.0.0.1:8088/api/v3/graphql",
        json={
            "query": """
            query GetBalance($address: String!) {
                walletBalance(address: $address) {
                    dust
                    night
                }
            }
            """,
            "variables": {"address": ADDRESS},
        },
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    
    if "data" in data and data["data"] and data["data"].get("walletBalance"):
        bal = data["data"]["walletBalance"]
        dust = int(bal.get("dust", 0))
        night = int(bal.get("night", 0))
        
        rprint(f"[bold]Balance:[/bold]")
        rprint(f"  DUST:  [green]{dust:,}[/green]")
        rprint(f"  NIGHT: [green]{night:,}[/green]\n")
        
        if dust > 0 and night > 0:
            rprint("[bold green]✓ Wallet is FUNDED! Ready to run demo.[/bold green]")
            rprint("\nRun: [cyan]python examples/private_ml_demo.py[/cyan]\n")
        else:
            rprint("[bold red]✗ Wallet needs funding.[/bold red]")
            rprint("\nSee: [cyan]FUND_WALLET_NOW.md[/cyan] for instructions.\n")
    else:
        rprint("[yellow]Could not read balance from indexer.[/yellow]")
        rprint("Make sure midnight-local-dev is running.\n")
        
except httpx.ConnectError:
    rprint("[red]✗ Cannot connect to indexer at http://127.0.0.1:8088[/red]")
    rprint("Make sure midnight-local-dev is running:\n")
    rprint("  cd ../midnight-local-dev && npm start\n")
except Exception as e:
    rprint(f"[red]Error: {e}[/red]\n")
