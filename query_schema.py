#!/usr/bin/env python3
"""Query the GraphQL schema to find available queries"""

import httpx
import json
from rich import print as rprint

try:
    # Introspection query to get schema
    response = httpx.post(
        "http://127.0.0.1:8088/api/v3/graphql",
        json={
            "query": """
            {
              __schema {
                queryType {
                  fields {
                    name
                    description
                    args {
                      name
                      type {
                        name
                        kind
                      }
                    }
                  }
                }
              }
            }
            """
        },
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    
    data = response.json()
    
    if "data" in data and data["data"]:
        fields = data["data"]["__schema"]["queryType"]["fields"]
        
        rprint("\n[bold]Available GraphQL Queries:[/bold]\n")
        
        # Look for wallet/balance related queries
        for field in fields:
            name = field["name"]
            if "wallet" in name.lower() or "balance" in name.lower() or "account" in name.lower():
                rprint(f"[cyan]{name}[/cyan]")
                if field.get("description"):
                    rprint(f"  {field['description']}")
                if field.get("args"):
                    rprint(f"  Args: {[arg['name'] for arg in field['args']]}")
                rprint()
        
        rprint("\n[bold]All available queries:[/bold]\n")
        for field in fields:
            rprint(f"  • {field['name']}")
            
except Exception as e:
    rprint(f"[red]Error: {e}[/red]")
    import traceback
    traceback.print_exc()
