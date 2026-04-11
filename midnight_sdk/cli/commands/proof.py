"""ZK proof generation and verification commands."""

import typer
from rich.console import Console
from pathlib import Path
import json

from ...client import MidnightClient
from ...config import ConfigManager

app = typer.Typer(help="ZK proof generation and verification")
console = Console()


@app.command("generate")
def proof_generate(
    circuit: str = typer.Argument(..., help="Circuit name"),
    inputs: str = typer.Argument(..., help="JSON inputs"),
    output: Path = typer.Option(None, "--output", "-o", help="Output proof file"),
    profile: str = typer.Option(None, "--profile", "-p", help="Network profile"),
):
    """Generate ZK proof for circuit."""
    try:
        inputs_dict = json.loads(inputs)
    except json.JSONDecodeError:
        console.print("[red]Invalid JSON inputs[/red]")
        raise typer.Exit(1)
    
    config_mgr = ConfigManager()
    config_mgr.load()
    profile_obj = config_mgr.get_profile(profile)
    
    try:
        with console.status("[cyan]Generating proof..."):
            client = MidnightClient(network=profile_obj.name)
            proof = client.prover.generate_proof(circuit, inputs_dict)
        
        # Convert ZKProof to dict
        proof_dict = {
            "proof": proof.proof,
            "publicOutputs": proof.public_outputs,
            "circuitId": proof.circuit_id
        }
        
        if output:
            output.write_text(json.dumps(proof_dict, indent=2))
            console.print(f"[green]✓[/green] Proof saved to {output}")
        else:
            console.print(json.dumps(proof_dict, indent=2))
    except Exception as e:
        console.print(f"[red]Proof generation failed: {e}[/red]")
        raise typer.Exit(1)


@app.command("verify")
def proof_verify(
    proof_file: Path = typer.Argument(..., help="Proof file"),
    profile: str = typer.Option(None, "--profile", "-p", help="Network profile"),
):
    """Verify ZK proof."""
    if not proof_file.exists():
        console.print(f"[red]File not found: {proof_file}[/red]")
        raise typer.Exit(1)
    
    try:
        proof = json.loads(proof_file.read_text())
    except json.JSONDecodeError:
        console.print("[red]Invalid JSON file[/red]")
        raise typer.Exit(1)
    
    config_mgr = ConfigManager()
    config_mgr.load()
    profile_obj = config_mgr.get_profile(profile)
    
    try:
        client = MidnightClient(network=profile_obj.name)
        is_valid = client.prover.verify_proof(proof)
        
        if is_valid:
            console.print("[green]✓[/green] Proof is valid")
        else:
            console.print("[red]✗[/red] Proof is invalid")
            raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Verification failed: {e}[/red]")
        raise typer.Exit(1)


@app.command("info")
def proof_info(
    circuit: str = typer.Argument(..., help="Circuit path or name"),
    profile: str = typer.Option(None, "--profile", "-p", help="Network profile"),
):
    """Show circuit information."""
    from rich.table import Table
    
    circuit_path = Path(circuit)
    if not circuit_path.exists():
        console.print(f"[red]Circuit not found: {circuit}[/red]")
        console.print("[dim]Hint: Provide path to compiled circuit (e.g., contracts/managed/hello_world)[/dim]")
        raise typer.Exit(1)
    
    # Show basic circuit info
    table = Table(title=f"Circuit: {circuit_path.name}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Path", str(circuit_path))
    table.add_row("Exists", "✓ Yes" if circuit_path.exists() else "✗ No")
    
    # Check for circuit files
    if circuit_path.is_dir():
        files = list(circuit_path.glob("*"))
        table.add_row("Files", str(len(files)))
        for f in files[:5]:  # Show first 5 files
            table.add_row("", f"  • {f.name}")
    
    console.print(table)
    console.print("\n[dim]Note: Detailed circuit analysis requires proof server integration[/dim]")
