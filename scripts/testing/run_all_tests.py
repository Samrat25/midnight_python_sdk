#!/usr/bin/env python3
"""
Run all midnight-py tests and demos
Shows everything that's working
"""

from rich.console import Console
from rich import print as rprint
import subprocess
import sys

console = Console()

def run_script(name, command):
    """Run a script and report results"""
    console.rule(f"[bold cyan]{name}")
    rprint()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=False,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            rprint(f"\n[bold green]✓ {name} - SUCCESS[/bold green]\n")
            return True
        else:
            rprint(f"\n[bold red]✗ {name} - FAILED (exit code {result.returncode})[/bold red]\n")
            return False
    except subprocess.TimeoutExpired:
        rprint(f"\n[bold yellow]⚠ {name} - TIMEOUT[/bold yellow]\n")
        return False
    except Exception as e:
        rprint(f"\n[bold red]✗ {name} - ERROR: {e}[/bold red]\n")
        return False

def main():
    console.rule("[bold]🌙 midnight-py — Complete Test Suite")
    rprint("\n[dim]Running all tests and demos...[/dim]\n")
    
    tests = [
        ("Service Status Check", "python check_services.py"),
        ("CLI Status Command", "midnight-py status"),
        ("Private ML Simple Demo", "python examples/private_ml_simple.py"),
        ("AI Inference Demo", "python examples/ai_inference.py"),
        ("Private Voting Demo", "python examples/private_vote.py"),
        ("Bulletin Board (Auto-Codegen)", "python examples/bulletin_board.py"),
    ]
    
    results = []
    
    for name, command in tests:
        success = run_script(name, command)
        results.append((name, success))
    
    # Summary
    console.rule("[bold]Test Summary")
    rprint()
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        icon = "[green]✓[/green]" if success else "[red]✗[/red]"
        rprint(f"  {icon} {name}")
    
    rprint()
    rprint(f"[bold]Results: {passed}/{total} tests passed[/bold]")
    
    if passed == total:
        rprint("\n[bold green]🎉 All tests passed![/bold green]\n")
    else:
        rprint(f"\n[bold yellow]⚠ {total - passed} test(s) failed[/bold yellow]\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Tests interrupted.[/yellow]")
        sys.exit(1)
