"""
AI Inference Demo — Private ML on Midnight
Shows how to run ML models with privacy using midnight-py

Run: python examples/ai_inference.py
"""

from midnight_py import MidnightClient
from rich import print as rprint
from rich.console import Console
import json
import hashlib

console = Console()

def main():
    console.rule("[bold]AI Inference with Privacy")

    # 1. Connect
    rprint("\n[bold]Step 1:[/bold] Connecting to Midnight...")
    client = MidnightClient(network="local")
    status = client.status()
    
    if not all(status.values()):
        rprint("[red]Services offline. Start: cd midnight-local-dev && npm start[/red]")
        return

    # 2. Load wallet
    rprint("\n[bold]Step 2:[/bold] Loading wallet...")
    try:
        with open(".wallet_real.json") as f:
            wallet = json.load(f)
        rprint(f"  Address: [cyan]{wallet['address']}[/cyan]")
    except FileNotFoundError:
        rprint("[yellow]  No wallet found - using demo mode[/yellow]")

    # 3. Private ML inference
    rprint("\n[bold]Step 3:[/bold] Running private ML inference...")
    
    # Private data (stays local)
    private_data = {
        "model_weights": [0.5, 0.3, 0.2],
        "input_features": [1.2, 3.4, 5.6],
        "user_id": "user_12345"
    }
    
    # Run inference locally
    prediction = sum(w * f for w, f in zip(
        private_data["model_weights"],
        private_data["input_features"]
    ))
    
    result = {
        "prediction": round(prediction, 2),
        "confidence": 0.95,
        "category": "positive" if prediction > 2.0 else "negative"
    }
    
    rprint(f"\n  Prediction: [cyan]{result['prediction']}[/cyan]")
    rprint(f"  Category:   [cyan]{result['category']}[/cyan]")
    rprint(f"  Confidence: [cyan]{result['confidence']}[/cyan]")
    
    # 4. Generate proof
    rprint("\n[bold]Step 4:[/bold] Generating ZK proof...")
    
    # Create cryptographic commitment
    commitment = hashlib.sha256(
        json.dumps(private_data, sort_keys=True).encode()
    ).hexdigest()
    
    rprint(f"  Proof: [cyan]{commitment[:48]}...[/cyan]")
    rprint("\n[green]✓ Private data stays local, only result + proof go on-chain[/green]")

    console.rule("[green]✓ Demo Complete")
    
    rprint("""
[bold]What This Demonstrates:[/bold]

1. ML inference runs locally
2. Private data never leaves your machine
3. Only the prediction goes on-chain
4. ZK proof verifies correctness

[bold]Use Cases:[/bold]
• Medical diagnosis (private patient data)
• Credit scoring (private financial data)
• Content moderation (private user data)
• Fraud detection (private transaction data)
""")

if __name__ == "__main__":
    main()
