#!/usr/bin/env python3
"""
Verification script to check midnight-py installation.
Run this after installation to ensure everything works.
"""

import sys
from rich.console import Console
from rich.table import Table

console = Console()


def check_imports():
    """Check that all modules can be imported."""
    console.print("\n[bold]Checking imports...[/bold]")
    
    try:
        import midnight_py
        from midnight_py import (
            MidnightClient,
            compact_to_python,
            Balance,
            ZKProof,
            TransactionResult,
        )
        console.print("✓ All imports successful", style="green")
        console.print(f"  Version: {midnight_py.__version__}")
        return True
    except ImportError as e:
        console.print(f"✗ Import failed: {e}", style="red")
        return False


def check_dependencies():
    """Check that all dependencies are installed."""
    console.print("\n[bold]Checking dependencies...[/bold]")
    
    deps = {
        "httpx": "HTTP client",
        "websockets": "WebSocket support",
        "pydantic": "Data validation",
        "typer": "CLI framework",
        "rich": "Terminal formatting",
    }
    
    all_ok = True
    for module, description in deps.items():
        try:
            __import__(module)
            console.print(f"✓ {module:12} - {description}", style="green")
        except ImportError:
            console.print(f"✗ {module:12} - {description}", style="red")
            all_ok = False
    
    return all_ok


def check_cli():
    """Check that CLI is available."""
    console.print("\n[bold]Checking CLI...[/bold]")
    
    import subprocess
    try:
        result = subprocess.run(
            ["midnight-py", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            console.print("✓ CLI command available", style="green")
            return True
        else:
            console.print("✗ CLI command failed", style="red")
            return False
    except Exception as e:
        console.print(f"✗ CLI check failed: {e}", style="red")
        return False


def check_tests():
    """Check if tests can run."""
    console.print("\n[bold]Checking test setup...[/bold]")
    
    try:
        import pytest
        console.print("✓ pytest installed", style="green")
        
        # Check if fixtures are available
        from midnight_py.pytest_plugin import midnight_client
        console.print("✓ pytest fixtures available", style="green")
        return True
    except ImportError as e:
        console.print(f"✗ Test setup incomplete: {e}", style="red")
        return False


def check_examples():
    """Check if example files exist."""
    console.print("\n[bold]Checking examples...[/bold]")
    
    from pathlib import Path
    
    examples = [
        "examples/bulletin_board.py",
        "examples/private_vote.py",
        "examples/ai_inference.py",
    ]
    
    all_ok = True
    for example in examples:
        if Path(example).exists():
            console.print(f"✓ {example}", style="green")
        else:
            console.print(f"✗ {example} not found", style="red")
            all_ok = False
    
    return all_ok


def check_contracts():
    """Check if sample contracts exist."""
    console.print("\n[bold]Checking contracts...[/bold]")
    
    from pathlib import Path
    
    if Path("contracts/bulletin_board.compact").exists():
        console.print("✓ Sample contract available", style="green")
        return True
    else:
        console.print("✗ Sample contract not found", style="red")
        return False


def main():
    console.rule("[bold]midnight-py Installation Verification")
    
    checks = [
        ("Imports", check_imports),
        ("Dependencies", check_dependencies),
        ("CLI", check_cli),
        ("Tests", check_tests),
        ("Examples", check_examples),
        ("Contracts", check_contracts),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            console.print(f"\n[red]Error in {name}: {e}[/red]")
            results[name] = False
    
    # Summary
    console.print("\n")
    console.rule("[bold]Summary")
    
    table = Table(show_header=True)
    table.add_column("Check", style="bold")
    table.add_column("Status")
    
    for name, passed in results.items():
        status = "[green]✓ PASS[/green]" if passed else "[red]✗ FAIL[/red]"
        table.add_row(name, status)
    
    console.print(table)
    
    # Overall result
    all_passed = all(results.values())
    console.print()
    if all_passed:
        console.print("[bold green]✅ All checks passed! midnight-py is ready to use.[/bold green]")
        console.print("\nNext steps:")
        console.print("  1. Start services: [cyan]docker-compose up -d[/cyan]")
        console.print("  2. Check status: [cyan]midnight-py status[/cyan]")
        console.print("  3. Run tests: [cyan]pytest tests/ -v[/cyan]")
        console.print("  4. Try examples: [cyan]python examples/bulletin_board.py[/cyan]")
        return 0
    else:
        console.print("[bold red]❌ Some checks failed. Please fix the issues above.[/bold red]")
        console.print("\nTry:")
        console.print("  [cyan]pip install -e '.[dev]'[/cyan]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
