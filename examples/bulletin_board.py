"""
Full end-to-end demo: deploy and use a BulletinBoard contract.
This is what you demo at the hackathon.

Run: python examples/bulletin_board.py
"""

from midnight_py import MidnightClient
from midnight_py.codegen import compact_to_python
from rich import print as rprint
from rich.console import Console

console = Console()

def main():
    console.rule("[bold]midnight-py Demo — BulletinBoard")

    # 1. Connect
    rprint("\n[bold]Step 1:[/bold] Connecting to Midnight local network...")
    client = MidnightClient(network="local")
    status = client.status()
    for svc, ok in status.items():
        icon = "[green]✓ OK[/green]" if ok else "[red]✗ OFFLINE[/red]"
        rprint(f"  {svc}: {icon}")
    
    if not all(status.values()):
        rprint("\n[red]⚠ Services not running! Start them with:[/red]")
        rprint("[yellow]  python start_services.py[/yellow]")
        return

    # 2. Create/load wallet
    rprint("\n[bold]Step 2:[/bold] Setting up wallet...")
    seed_phrase = "hackathon test seed phrase"
    address = client.wallet.generate_address(seed_phrase)
    rprint(f"  Wallet address: [cyan]{address}[/cyan]")
    
    balance = client.wallet.get_balance(address)
    rprint(f"  Balance: {balance.dust:,} DUST, {balance.night:,} NIGHT")

    # 3. Generate Python class from .compact file
    rprint("\n[bold]Step 3:[/bold] Generating Python class from Compact contract...")
    BulletinBoard = compact_to_python("contracts/bulletin_board.compact")
    rprint(f"  Generated class: [cyan]{BulletinBoard.__name__}[/cyan]")
    rprint(f"  Available methods: {[m for m in dir(BulletinBoard) if not m.startswith('_')]}")

    # 4. Deploy
    rprint("\n[bold]Step 4:[/bold] Deploying contract...")
    raw_contract = client.contracts.deploy(
        "contracts/bulletin_board.compact",
        private_key="test_private_key_for_demo",
    )
    board = BulletinBoard(raw_contract)
    rprint(f"  Deployed at: [green]{raw_contract.address}[/green]")

    # 5. Post a message (ZK proof auto-generated)
    rprint("\n[bold]Step 5:[/bold] Posting message with ZK proof...")
    raw_contract.set_key("test_private_key_for_demo")
    result = board.post(message="Hello from Python on Midnight!")
    rprint(f"  TX Hash: [cyan]{result.tx_hash}[/cyan]")
    rprint(f"  Status:  [green]{result.status}[/green]")

    # 6. Read state
    rprint("\n[bold]Step 6:[/bold] Reading on-chain state...")
    state = board.state()
    rprint(f"  Block: {state.block_height}")
    rprint(f"  State: {state.state}")

    console.rule("[green]✓ Done! Python on Midnight works.")


if __name__ == "__main__":
    main()
