#!/usr/bin/env python3
"""
Stop all Midnight services
"""

import os
import sys
import signal
from pathlib import Path


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("  🌙 Stopping Midnight Services")
    print("=" * 60 + "\n")
    
    pid_file = Path(".service_pids.txt")
    
    if not pid_file.exists():
        print("No running services found (.service_pids.txt not found)")
        return 0
    
    # Read PIDs
    with open(pid_file, "r") as f:
        lines = f.readlines()
    
    stopped = 0
    for line in lines:
        if ":" in line:
            name, pid_str = line.strip().split(":")
            try:
                pid = int(pid_str)
                print(f"Stopping {name} (PID: {pid})...")
                
                if sys.platform == "win32":
                    # Windows
                    os.system(f"taskkill /F /PID {pid} >nul 2>&1")
                else:
                    # Unix-like
                    os.kill(pid, signal.SIGTERM)
                
                print(f"  ✓ {name} stopped")
                stopped += 1
            except (ValueError, ProcessLookupError, PermissionError) as e:
                print(f"  ⚠ Could not stop {name}: {e}")
    
    # Remove PID file
    pid_file.unlink()
    
    print(f"\n✓ Stopped {stopped} service(s)")
    print("=" * 60 + "\n")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
