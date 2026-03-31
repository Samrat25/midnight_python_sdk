#!/usr/bin/env python3
"""
Start all Midnight services without Docker
Runs the mock servers directly using Python
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_port(port):
    """Check if a port is in use"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0


def start_server(name, script_path, port):
    """Start a server in the background"""
    print(f"Starting {name} on port {port}...")
    
    # Check if port is already in use
    if check_port(port):
        print(f"  ⚠ Port {port} already in use. Skipping {name}.")
        return None
    
    # Start the server
    if sys.platform == "win32":
        # Windows
        process = subprocess.Popen(
            [sys.executable, script_path],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    else:
        # Unix-like
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    print(f"  ✓ {name} started (PID: {process.pid})")
    return process


def wait_for_service(port, timeout=10):
    """Wait for a service to be ready"""
    import socket
    start_time = time.time()
    while time.time() - start_time < timeout:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        if result == 0:
            return True
        time.sleep(0.5)
    return False


def main():
    """Main entry point"""
    print_header("🌙 Starting Midnight Services")
    
    # Check if server files exist
    node_server = Path("docker/node/server.py")
    indexer_server = Path("docker/indexer/server.py")
    proof_server = Path("docker/proof/server.py")
    
    if not all([node_server.exists(), indexer_server.exists(), proof_server.exists()]):
        print("❌ Server files not found!")
        print("Make sure you're in the midnightsdk directory.")
        return 1
    
    # Start services
    processes = []
    
    # Start Node
    node_proc = start_server("Midnight Node", str(node_server), 9944)
    if node_proc:
        processes.append(("Node", node_proc))
    
    # Start Indexer
    indexer_proc = start_server("Midnight Indexer", str(indexer_server), 8088)
    if indexer_proc:
        processes.append(("Indexer", indexer_proc))
    
    # Start Proof Server
    proof_proc = start_server("Midnight Proof Server", str(proof_server), 6300)
    if proof_proc:
        processes.append(("Proof Server", proof_proc))
    
    # Wait for services to be ready
    print("\nWaiting for services to be ready...")
    time.sleep(3)
    
    # Check service health
    print_header("Service Status")
    
    services = [
        ("Node", 9944),
        ("Indexer", 8088),
        ("Proof Server", 6300)
    ]
    
    all_ready = True
    for name, port in services:
        if wait_for_service(port, timeout=5):
            print(f"  ✓ {name:20} http://127.0.0.1:{port}")
        else:
            print(f"  ✗ {name:20} OFFLINE")
            all_ready = False
    
    # Save PIDs for later cleanup
    if processes:
        with open(".service_pids.txt", "w") as f:
            for name, proc in processes:
                f.write(f"{name}:{proc.pid}\n")
        print(f"\n✓ Service PIDs saved to .service_pids.txt")
    
    # Final status
    print_header("Services Started!")
    
    if all_ready:
        print("✅ All services are running!\n")
        print("Check status:")
        print("  midnight-py status\n")
        print("Run demo:")
        print("  python examples/bulletin_board.py\n")
        print("Stop services:")
        print("  python stop_services.py\n")
    else:
        print("⚠ Some services failed to start.")
        print("Check the console windows for errors.\n")
    
    return 0 if all_ready else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
