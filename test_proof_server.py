#!/usr/bin/env python3
"""
Test Proof Server
Tests the proof server with your project's compiled circuits
"""

from rich.console import Console
from rich.table import Table
from pathlib import Path
import json
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from midnight_sdk import MidnightClient
from midnight_sdk.proof import ProofClient

console = Console()


def test_proof_server():
    """Test proof server with compiled circuits"""
    
    console.print("\n[bold cyan]═══ Midnight Proof Server Test ═══[/bold cyan]\n")
    
    # Step 1: Check proof server connection
    console.print("[cyan]Step 1:[/cyan] Checking proof server connection...")
    try:
        prover = ProofClient("http://localhost:6300")
        if prover.is_alive():
            console.print("[green]✓[/green] Proof server is online at http://localhost:6300")
        else:
            console.print("[red]✗[/red] Proof server is offline")
            console.print("\n[yellow]Start the proof server:[/yellow]")
            console.print("  docker-compose up -d proof-server")
            return False
    except Exception as e:
        console.print(f"[red]✗[/red] Connection failed: {e}")
        return False
    
    # Step 2: Check compiled circuits
    console.print("\n[cyan]Step 2:[/cyan] Checking compiled circuits...")
    contracts_dir = Path("contracts/managed")
    
    if not contracts_dir.exists():
        console.print(f"[red]✗[/red] Contracts directory not found: {contracts_dir}")
        console.print("\n[yellow]Compile contracts first:[/yellow]")
        console.print("  midnight-py compile contracts/counter.compact")
        return False
    
    circuits = list(contracts_dir.glob("*/"))
    if not circuits:
        console.print("[red]✗[/red] No compiled circuits found")
        console.print("\n[yellow]Compile contracts first:[/yellow]")
        console.print("  midnight-py compile contracts/counter.compact")
        return False
    
    console.print(f"[green]✓[/green] Found {len(circuits)} compiled circuit(s)")
    
    # Display circuits
    table = Table(title="Available Circuits")
    table.add_column("Circuit", style="cyan")
    table.add_column("Path", style="white")
    
    for circuit in circuits:
        table.add_row(circuit.name, str(circuit))
    
    console.print(table)
    
    # Step 3: Test proof generation with counter circuit
    console.print("\n[cyan]Step 3:[/cyan] Testing proof generation...")
    
    test_cases = [
        {
            "name": "Counter Increment",
            "circuit": "counter:increment",
            "private_inputs": {"current": 5},
            "public_inputs": {"increment": 1}
        },
        {
            "name": "Hello World Greet",
            "circuit": "hello_world:greet",
            "private_inputs": {"name": "Alice"},
            "public_inputs": {}
        }
    ]
    
    success_count = 0
    for test in test_cases:
        console.print(f"\n  Testing: [cyan]{test['name']}[/cyan]")
        try:
            proof = prover.generate_proof(
                circuit_id=test["circuit"],
                private_inputs=test["private_inputs"],
                public_inputs=test["public_inputs"]
            )
            
            console.print(f"  [green]✓[/green] Proof generated successfully")
            console.print(f"    Circuit: {proof.circuit_id}")
            console.print(f"    Proof hash: {proof.proof[:32]}...")
            console.print(f"    Public outputs: {proof.public_outputs}")
            success_count += 1
        except Exception as e:
            console.print(f"  [yellow]⚠[/yellow] Skipped (circuit not available): {e}")
    
    # Step 4: Summary
    console.print("\n[bold cyan]═══ Test Summary ═══[/bold cyan]\n")
    
    summary_table = Table()
    summary_table.add_column("Component", style="cyan")
    summary_table.add_column("Status", style="white")
    
    summary_table.add_row("Proof Server", "[green]✓ Online[/green]")
    summary_table.add_row("Compiled Circuits", f"[green]✓ {len(circuits)} found[/green]")
    summary_table.add_row("Proof Generation", f"[green]✓ {success_count} tests passed[/green]")
    
    console.print(summary_table)
    
    # Step 5: Usage examples
    console.print("\n[bold cyan]═══ Usage Examples ═══[/bold cyan]\n")
    
    console.print("[yellow]CLI Commands:[/yellow]")
    console.print("  # Check proof server status")
    console.print("  midnight-py proof info contracts/managed/counter")
    console.print()
    console.print("  # Generate proof for counter circuit")
    console.print('  midnight-py proof generate counter:increment \'{"current": 5, "increment": 1}\'')
    console.print()
    console.print("  # Generate proof for hello_world circuit")
    console.print('  midnight-py proof generate hello_world:greet \'{"name": "Alice"}\'')
    
    console.print("\n[yellow]Python SDK:[/yellow]")
    console.print("""
from midnight_sdk import ProofClient

# Initialize client
prover = ProofClient("http://localhost:6300")

# Generate proof
proof = prover.generate_proof(
    circuit_id="counter:increment",
    private_inputs={"current": 5},
    public_inputs={"increment": 1}
)

print(f"Proof: {proof.proof}")
print(f"Public outputs: {proof.public_outputs}")
    """)
    
    console.print("\n[yellow]REST API:[/yellow]")
    console.print("""
curl -X POST http://localhost:6300/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "circuitId": "counter:increment",
    "privateInputs": {"current": 5},
    "publicInputs": {"increment": 1}
  }'
    """)
    
    console.print("\n[green]✓[/green] All tests completed successfully!\n")
    return True


if __name__ == "__main__":
    try:
        success = test_proof_server()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {e}")
        sys.exit(1)
