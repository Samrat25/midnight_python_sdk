"""
midnight-py CLI — interact with Midnight from the terminal.

Commands:
    midnight-py status           — check all services
    midnight-py deploy <file>    — deploy a .compact contract
    midnight-py call <addr> <fn> — call a circuit function
    midnight-py state <addr>     — read contract state
    midnight-py balance <addr>   — get wallet balance
"""

import typer
import json
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from .client import MidnightClient

app = typer.Typer(
    name="midnight-py",
    help="Python CLI for the Midnight blockchain",
    no_args_is_help=True,
)
console = Console()


@app.command()
def status(network: str = typer.Option("local", help="Network to connect to")):
    """Check if all Midnight services are running."""
    client = MidnightClient(network=network)
    result = client.status()

    table = Table(title=f"Midnight Services ({network})")
    table.add_column("Service", style="bold")
    table.add_column("Status")
    table.add_column("URL")

    cfg = {"node": client.wallet.url, "indexer": client.indexer.url, "prover": client.prover.url}
    for service, alive in result.items():
        icon = "[green]✓ ONLINE[/green]" if alive else "[red]✗ OFFLINE[/red]"
        table.add_row(service.capitalize(), icon, cfg[service])

    console.print(table)


@app.command()
def deploy(
    contract: str = typer.Argument(..., help="Path to .compact file"),
    network: str = typer.Option("local"),
    key: str = typer.Option(..., help="Private key for signing"),
):
    """Deploy a .compact contract to Midnight."""
    rprint(f"[bold]Deploying[/bold] {contract} to {network}...")
    client = MidnightClient(network=network)
    deployed = client.contracts.deploy(contract, private_key=key)
    rprint(f"[green]✓ Deployed at:[/green] {deployed.address}")


@app.command()
def call(
    address: str = typer.Argument(..., help="Contract address"),
    circuit: str = typer.Argument(..., help="Circuit function name"),
    args: str = typer.Option("{}", help="JSON public inputs"),
    private: str = typer.Option("{}", help="JSON private inputs"),
    key: str = typer.Option(..., help="Private key for signing"),
    network: str = typer.Option("local"),
):
    """Call a circuit function on a deployed contract."""
    client = MidnightClient(network=network)
    contract = client.get_contract(address, [circuit])
    contract.set_key(key)
    result = contract.call(
        circuit_name=circuit,
        public_inputs=json.loads(args),
        private_inputs=json.loads(private),
    )
    rprint(f"[green]TX Hash:[/green] {result.tx_hash}")
    rprint(f"[green]Status:[/green]  {result.status}")


@app.command()
def state(
    address: str = typer.Argument(..., help="Contract address"),
    network: str = typer.Option("local"),
):
    """Read the current on-chain state of a contract."""
    client = MidnightClient(network=network)
    contract_state = client.indexer.get_contract_state(address)
    rprint(f"[bold]Contract:[/bold] {address}")
    rprint(f"[bold]Block:[/bold]    {contract_state.block_height}")
    rprint(f"[bold]State:[/bold]")
    console.print_json(json.dumps(contract_state.state))


@app.command()
def balance(
    address: str = typer.Argument(..., help="Wallet address"),
    network: str = typer.Option("local"),
):
    """Get token balances for a wallet address."""
    client = MidnightClient(network=network)
    bal = client.wallet.get_balance(address)
    rprint(f"[bold]DUST:[/bold]  {bal.dust:,}")
    rprint(f"[bold]NIGHT:[/bold] {bal.night:,}")


def main():
    app()
