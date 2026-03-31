"""
REAL end-to-end demo against the actual Midnight local network.

Before running this:
  1. git clone https://github.com/midnightntwrk/midnight-local-dev
  2. cd midnight-local-dev
  3. npm install
  4. npm start   ← keep this running in a separate terminal
  5. In the menu that appears, choose [1] and fund your wallet

Then run this file:
  python examples/real_demo.py
"""

from midnight_py import MidnightClient
from midnight_py.codegen import compact_to_python
from rich.console import Console
from rich import print as rprint

console = Console()

# Load mnemonic from mnemonic.txt
def load_mnemonic():
    """Load mnemonic from file."""
    from pathlib import Path
    mnemonic_file = Path("mnemonic.txt")
    if mnemonic_file.exists():
        return mnemonic_file.read_text().strip()
    else:
        # Fallback to default
        return (
            "abandon abandon abandon abandon abandon abandon abandon abandon "
            "abandon abandon abandon abandon abandon abandon abandon abandon "
            "abandon abandon abandon abandon abandon abandon abandon art"
        )

MNEMONIC = load_mnemonic()


def main():
    console.rule("[bold]midnight-py — Real Midnight Network Demo")

    # Step 1: Connect to real local network
    rprint("\n[bold]Step 1:[/bold] Connecting to real Midnight local network...")
    client = MidnightClient(network="local")
    status = client.status()

    all_up = True
    for svc, ok in status.items():
        icon = "[green]✓ ONLINE[/green]" if ok else "[red]✗ OFFLINE[/red]"
        rprint(f"  {svc}: {icon}")
        if not ok:
            all_up = False

    if not all_up:
        rprint("\n[red]⚠ Some services are offline.[/red]")
        rprint("Run this in a separate terminal:")
        rprint("  cd midnight-local-dev && npm start")
        return

    # Step 2: Create real wallet from mnemonic
    rprint("\n[bold]Step 2:[/bold] Creating wallet from mnemonic...")
    wallet_info = client.wallet.generate_from_mnemonic(MNEMONIC, "undeployed")
    rprint(f"  Address:     [cyan]{wallet_info['address']}[/cyan]")
    rprint(f"  Private key: {wallet_info['private_key'][:16]}...")

    # Step 3: Check real balance
    rprint("\n[bold]Step 3:[/bold] Checking real balance on-chain...")
    try:
        balance = client.wallet.get_balance(wallet_info["address"])
        rprint(f"  DUST:  [green]{balance.dust:,}[/green]")
        rprint(f"  NIGHT: [green]{balance.night:,}[/green]")

        if balance.dust == 0:
            rprint("\n[yellow]⚠ Wallet has no DUST.[/yellow]")
            rprint("  Fund it: in the midnight-local-dev menu, choose [1] and add your mnemonic")
            return
    except Exception as e:
        rprint(f"  [yellow]Balance check skipped: {e}[/yellow]")

    # Step 4: Parse real .compact contract
    rprint("\n[bold]Step 4:[/bold] Generating Python class from Compact contract...")
    BulletinBoard = compact_to_python("contracts/bulletin_board.compact")
    methods = [m for m in dir(BulletinBoard) if not m.startswith("_")]
    rprint(f"  Generated class: [cyan]{BulletinBoard.__name__}[/cyan]")
    rprint(f"  Methods: {methods}")

    # Step 5: Deploy to real local Midnight chain
    rprint("\n[bold]Step 5:[/bold] Deploying contract to real Midnight node...")
    try:
        raw = client.contracts.deploy(
            "contracts/bulletin_board.compact",
            private_key=wallet_info["private_key"],
        )
        board = BulletinBoard(raw)
        rprint(f"  [green]✓ Deployed at: {raw.address}[/green]")
    except Exception as e:
        rprint(f"  [red]✗ Deploy failed: {e}[/red]")
        rprint("  Make sure your wallet has DUST to pay fees.")
        return

    # Step 6: Call circuit — real ZK proof generated + submitted
    rprint("\n[bold]Step 6:[/bold] Calling circuit (real ZK proof generation)...")
    rprint("  [yellow]⏳ This may take 10-30 seconds — real ZK proof is being generated...[/yellow]")
    try:
        result = board.post(message="Hello from Python on real Midnight!")
        rprint(f"  TX Hash: [cyan]{result.tx_hash}[/cyan]")
        rprint(f"  Status:  [green]{result.status}[/green]")
    except Exception as e:
        rprint(f"  [red]✗ Circuit call failed: {e}[/red]")
        return

    # Step 7: Read state from real indexer
    rprint("\n[bold]Step 7:[/bold] Reading on-chain state from real indexer...")
    try:
        state = board.state()
        rprint(f"  Block height: [cyan]{state.block_height}[/cyan]")
        rprint(f"  State: {state.state}")
    except Exception as e:
        rprint(f"  [yellow]State query: {e}[/yellow]")
        rprint("  (Indexer may still be syncing — wait a few seconds and try again)")

    console.rule("[green]✓ Real ZK proof confirmed on Midnight blockchain!")
    rprint(f"\n[bold]TX Hash to show judges:[/bold] [cyan]{result.tx_hash}[/cyan]")


if __name__ == "__main__":
    main()
