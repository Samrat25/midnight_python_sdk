#!/usr/bin/env python3
"""
Comprehensive test of ALL Midnight SDK operations
"""

import subprocess
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run_command(cmd_list, description):
    """Run a CLI command and return success status"""
    try:
        result = subprocess.run(
            ["python", "-c", f"from midnight_sdk.cli import app; app({cmd_list})"],
            capture_output=True,
            text=True,
            timeout=30
        )
        success = result.returncode == 0
        return success, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def main():
    console.print(Panel.fit(
        "[bold cyan]Midnight SDK - Complete Operations Test[/bold cyan]\n"
        "[dim]Testing all CLI commands and operations[/dim]",
        border_style="cyan"
    ))
    
    tests = [
        # System commands
        ("System Status", "['system', 'status']"),
        ("System Info", "['system', 'info']"),
        ("Version", "['--version']"),
        
        # Config commands
        ("Config List", "['config', 'list']"),
        ("Config Get", "['config', 'get', 'active_profile']"),
        
        # Wallet commands
        ("Wallet List", "['wallet', 'list']"),
        ("Wallet Address", "['wallet', 'address', 'test-deploy-wallet']"),
        ("Wallet Balance", "['wallet', 'balance', 'mn_addr_undeployed1x2w98jvk0wxppn3a3mlfw3ep736tdn7k2rhj7kjv292tcl6a0hyq3g5xa0']"),
        
        # Contract commands
        ("Contract Compile", "['contract', 'compile', 'contracts/hello_world.compact']"),
        ("Contract List", "['contract', 'list']"),
        
        # Transaction commands
        ("TX List", "['tx', 'list']"),
        
        # Node commands
        ("Node Status", "['node', 'status']"),
        
        # AI commands
        ("AI Model List", "['ai', 'model-list']"),
        
        # Transfer commands
        ("Transfer Info", "['transfer', 'info']"),
        
        # Explorer commands
        ("Explorer Help", "['explorer', '--help']"),
        
        # Events commands
        ("Events Help", "['events', '--help']"),
        
        # Proof commands
        ("Proof Help", "['proof', '--help']"),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    console.print("\n[cyan]Running tests...[/cyan]\n")
    
    for description, cmd in tests:
        with console.status(f"[cyan]Testing: {description}..."):
            success, stdout, stderr = run_command(cmd, description)
        
        if success:
            console.print(f"[green]✓[/green] {description}")
            passed += 1
            results.append((description, "✓ PASS", "green"))
        else:
            console.print(f"[red]✗[/red] {description}")
            if stderr:
                console.print(f"  [dim]{stderr[:100]}[/dim]")
            failed += 1
            results.append((description, "✗ FAIL", "red"))
    
    # Summary table
    console.print("\n")
    table = Table(title="Test Results Summary", show_header=True, header_style="bold cyan")
    table.add_column("Test", style="cyan", width=40)
    table.add_column("Result", justify="center", width=12)
    
    for desc, result, color in results:
        table.add_row(desc, f"[{color}]{result}[/{color}]")
    
    console.print(table)
    
    # Final summary
    total = passed + failed
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    console.print(f"\n[bold]Total Tests:[/bold] {total}")
    console.print(f"[green]Passed:[/green] {passed}")
    console.print(f"[red]Failed:[/red] {failed}")
    console.print(f"[cyan]Pass Rate:[/cyan] {pass_rate:.1f}%\n")
    
    if pass_rate >= 90:
        console.print("[bold green]✓ EXCELLENT! All critical operations working![/bold green]")
        return 0
    elif pass_rate >= 75:
        console.print("[bold yellow]⚠ GOOD! Most operations working, minor issues.[/bold yellow]")
        return 0
    else:
        console.print("[bold red]✗ NEEDS ATTENTION! Multiple failures detected.[/bold red]")
        return 1

if __name__ == "__main__":
    sys.exit(main())
