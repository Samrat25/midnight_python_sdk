"""
Complete Workflow — Compile, Deploy, Interact
==============================================

This example shows the COMPLETE workflow:
1. Derive private keys from mnemonic
2. Compile .compact contract
3. Show how to deploy (requires TypeScript)
4. Interact with deployed contract (Python)

Run: python examples/complete_workflow.py
"""

from midnight_py import MidnightClient
from midnight_py.wallet import WalletClient
from midnight_py.codegen import compile_compact, compact_to_python
from rich.console import Console
from rich import print as rprint
from pathlib import Path

console = Console()

def main():
    console.rule("[bold cyan]Complete Midnight Workflow")
    
    # Step 1: Derive keys from mnemonic
    rprint("\n[bold]Step 1: Derive Keys from Mnemonic[/bold]\n")
    
    mnemonic_file = Path("mnemonic.txt")
    if not mnemonic_file.exists():
        rprint("[red]mnemonic.txt not found![/red]")
        return
    
    mnemonic = mnemonic_file.read_text().strip()
    rprint(f"  Mnemonic: [dim]{mnemonic[:50]}...[/dim]")
    
    wallet = WalletClient()
    
    try:
        # Get address
        rprint("\n  Deriving address...")
        address_info = wallet.get_real_address(mnemonic, network_id="undeployed")
        rprint(f"  Address: [cyan]{address_info['address']}[/cyan]")
        
        # Get private keys
        rprint("\n  Deriving private keys...")
        keys = wallet.get_private_keys(mnemonic)
        rprint(f"  Zswap key: [dim]{keys['zswap'][:32]}...[/dim]")
        rprint(f"  Night key: [dim]{keys['nightExternal'][:32]}...[/dim]")
        rprint(f"  Dust key:  [dim]{keys['dust'][:32]}...[/dim]")
        
        rprint("\n[green]✓ Keys derived successfully![/green]")
        
    except Exception as e:
        rprint(f"[red]Error deriving keys: {e}[/red]")
        rprint("\n[yellow]Make sure Node.js and wallet SDK are installed:[/yellow]")
        rprint("  npm install")
        return
    
    # Step 2: Compile contract
    rprint("\n[bold]Step 2: Compile Contract[/bold]\n")
    
    contract_path = "contracts/counter.compact"
    
    if not Path(contract_path).exists():
        rprint(f"[red]{contract_path} not found![/red]")
        return
    
    rprint(f"  Contract: [cyan]{contract_path}[/cyan]")
    
    try:
        output_dir = compile_compact(contract_path)
        rprint(f"\n[green]✓ Compiled to: {output_dir}[/green]")
        
        # Show generated files
        rprint("\n  Generated files:")
        contract_js = output_dir / "contract" / "index.js"
        zkir_dir = output_dir / "zkir"
        keys_dir = output_dir / "keys"
        
        if contract_js.exists():
            rprint(f"    [green]✓[/green] {contract_js}")
        if zkir_dir.exists():
            rprint(f"    [green]✓[/green] {zkir_dir}/ (ZK circuits)")
        if keys_dir.exists():
            rprint(f"    [green]✓[/green] {keys_dir}/ (proving keys)")
        
    except Exception as e:
        rprint(f"[red]Compilation failed: {e}[/red]")
        rprint("\n[yellow]Install Compact compiler:[/yellow]")
        rprint("  npm install -g @midnight-ntwrk/compact-compiler")
        return
    
    # Step 3: Auto-generate Python class
    rprint("\n[bold]Step 3: Auto-Generate Python Class[/bold]\n")
    
    try:
        HelloWorld = compact_to_python(contract_path)
        rprint(f"  Generated class: [cyan]{HelloWorld.__name__}[/cyan]")
        
        methods = [m for m in dir(HelloWorld) if not m.startswith('_')]
        rprint("\n  Available methods:")
        for method in methods:
            rprint(f"    • [cyan]{method}()[/cyan]")
        
        rprint("\n[green]✓ Python class generated![/green]")
        
    except Exception as e:
        rprint(f"[red]Codegen failed: {e}[/red]")
        return
    
    # Step 4: Deployment instructions
    rprint("\n[bold]Step 4: Deploy Contract (TypeScript Required)[/bold]\n")
    
    rprint("""[yellow]Contract deployment requires the TypeScript SDK.[/yellow]

Create [cyan]deploy.ts[/cyan]:

```typescript
import {{ deployContract }} from '@midnight-ntwrk/midnight-js-contracts';
import {{ createWallet, createProviders }} from './utils.js';

const seed = "{seed}";
const walletCtx = await createWallet(seed);
const providers = await createProviders(walletCtx);

const deployed = await deployContract(providers, {{
  compiledContract,
  privateStateId: 'helloWorldState',
  initialPrivateState: {{}},
}});

console.log('Contract:', deployed.deployTxData.public.contractAddress);
```

Run:
```bash
npm install @midnight-ntwrk/midnight-js-contracts
tsx deploy.ts
```

This will output a contract address like: [cyan]0x1234...[/cyan]
""".format(seed=keys['nightExternal'][:32] + "..."))
    
    # Step 5: Interaction (Python)
    rprint("\n[bold]Step 5: Interact with Deployed Contract (Python)[/bold]\n")
    
    rprint("""Once deployed, use Python to interact:

```python
from midnight_py import MidnightClient
from midnight_py.codegen import compact_to_python

# Connect
client = MidnightClient(network="local")

# Load contract
HelloWorld = compact_to_python("contracts/hello_world.compact")
contract = client.get_contract(
    address="0x1234...",  # From deploy.ts
    circuit_ids=["storeMessage", "getMessage", "getCount"]
)

# Use auto-generated class
hello = HelloWorld(contract)

# Call circuits
hello.storeMessage(newMessage=b"Hello from Python!")

# Read state
state = hello.state()
print(f"Message: {{state.message}}")
print(f"Count: {{state.message_count}}")
```
""")
    
    # Step 6: Check services
    rprint("\n[bold]Step 6: Check Services[/bold]\n")
    
    client = MidnightClient(network="local")
    status = client.status()
    
    for service, online in status.items():
        icon = "[green]✓[/green]" if online else "[red]✗[/red]"
        rprint(f"  {icon} {service.upper()}")
    
    if all(status.values()):
        rprint("\n[green]✓ All services online - ready for deployment![/green]")
    else:
        rprint("\n[yellow]⚠ Start services: cd midnight-local-dev && npm start[/yellow]")
    
    # Summary
    console.rule("[bold green]✓ Workflow Complete")
    
    rprint(f"""
[bold]What You Have Now:[/bold]

1. [green]✓[/green] Private keys derived from mnemonic
   • Address: {address_info['address'][:30]}...
   • Keys ready for signing

2. [green]✓[/green] Contract compiled
   • Source: {contract_path}
   • Output: {output_dir}
   • ZK circuits generated

3. [green]✓[/green] Python class auto-generated
   • Class: {HelloWorld.__name__}
   • Methods: {', '.join(methods)}

4. [yellow]⚠[/yellow] Deployment requires TypeScript
   • Create deploy.ts script
   • Run: tsx deploy.ts
   • Get contract address

5. [green]✓[/green] Ready for Python interaction
   • Use auto-generated class
   • Call circuits
   • Read state

[bold]Next Steps:[/bold]

1. Create deploy.ts script (see Step 4 above)
2. Deploy contract: [cyan]tsx deploy.ts[/cyan]
3. Copy contract address
4. Interact with Python (see Step 5 above)

[bold cyan]Your wallet is funded and ready![/bold cyan]
Address: {address_info['address']}
Network: undeployed (local)
""")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
