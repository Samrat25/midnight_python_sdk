#!/usr/bin/env python3
"""Debug balance query to see actual response"""

import httpx
import json
from rich import print as rprint

ADDRESS = "mn_addr_undeployed1zaa268rc7sjz0ctscrsy7mp2ne7khfz8wu2uqsu4msfvxnlt6qfsmfrhr0"

rprint(f"\n[bold]Debugging balance query for:[/bold]")
rprint(f"[cyan]{ADDRESS}[/cyan]\n")

try:
    response = httpx.post(
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
    
    rprint(f"[bold]Status Code:[/bold] {response.status_code}")
    rprint(f"\n[bold]Raw Response:[/bold]")
    rprint(response.text)
    
    rprint(f"\n[bold]Parsed JSON:[/bold]")
    data = response.json()
    rprint(json.dumps(data, indent=2))
    
    if "data" in data:
        rprint(f"\n[bold]Data field:[/bold] {data['data']}")
        if data["data"] and "walletBalance" in data["data"]:
            bal = data["data"]["walletBalance"]
            rprint(f"\n[bold green]✓ Balance found![/bold green]")
            rprint(f"  DUST:  {bal.get('dust', 0)}")
            rprint(f"  NIGHT: {bal.get('night', 0)}")
        else:
            rprint(f"\n[yellow]walletBalance is null or missing[/yellow]")
    
    if "errors" in data:
        rprint(f"\n[bold red]GraphQL Errors:[/bold red]")
        for error in data["errors"]:
            rprint(f"  {error}")
            
except Exception as e:
    rprint(f"\n[red]Exception: {type(e).__name__}: {e}[/red]")
    import traceback
    traceback.print_exc()
