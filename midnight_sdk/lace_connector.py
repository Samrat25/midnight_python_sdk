"""
Lace Wallet Connector for Python CLI

This module provides integration with the Lace wallet browser extension,
allowing Python developers to connect their Lace wallet to the CLI.

Based on Midnight DApp Connector API v4.0.1
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from .models import Balance
from .exceptions import WalletError


class LaceConnector:
    """
    Connect to Lace wallet via Node.js bridge.
    
    Since Lace wallet is a browser extension, we use a Node.js script
    to access window.midnight.mnLace and bridge it to Python.
    """
    
    def __init__(self, network: str = "preprod"):
        self.network = network
        self._bridge_script = Path(__file__).parent.parent / "scripts" / "wallet" / "lace_bridge.mjs"

    def _run(self, *args, timeout: int = 10) -> dict:
        """
        Run a lace_bridge command and return parsed JSON from stdout.
        The bridge always writes JSON to stdout before any error exit,
        so we parse stdout first and ignore stderr instruction text.
        """
        from midnight_sdk.wallet import _find_node_executable
        try:
            node = _find_node_executable()
        except Exception:
            node = "node"

        result = subprocess.run(
            [node, str(self._bridge_script), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
        )
        stdout = result.stdout.strip()
        if stdout:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                pass
        raise WalletError(
            "Lace wallet is a browser extension and cannot be accessed from the CLI directly. "
            "Open the Lace extension in your browser to view balances and addresses."
        )
    
    def is_available(self) -> bool:
        """Check if Lace wallet is installed and accessible."""
        try:
            data = self._run("check", timeout=5)
            return data.get("available", False)
        except Exception:
            return False

    def get_wallet_info(self) -> Dict[str, str]:
        """Get Lace wallet name, icon, and API version."""
        return self._run("info", timeout=5)

    def connect(self) -> Dict[str, Any]:
        """Connect to Lace wallet."""
        return self._run("connect", self.network, timeout=30)

    def get_balance(self) -> Balance:
        """
        Get real wallet balance using the Midnight wallet SDK.
        Reads shielded NIGHT balance that the indexer cannot see.
        Requires MNEMONIC env var or mnemonic.txt / config/prepod.mnemonic.txt.
        """
        import os
        from midnight_sdk.wallet import _find_node_executable

        # Resolve mnemonic
        mnemonic = os.environ.get("MNEMONIC", "")
        if not mnemonic:
            for candidate in ["mnemonic.txt", "config/prepod.mnemonic.txt", "prepod.mnemonic.txt"]:
                p = Path(__file__).parent.parent / candidate
                if p.exists():
                    mnemonic = p.read_text().strip()
                    break

        if not mnemonic:
            raise WalletError(
                "No mnemonic found. Set MNEMONIC env var or create mnemonic.txt"
            )

        script = Path(__file__).parent.parent / "scripts" / "utilities" / "get_real_balance.mjs"
        if not script.exists():
            raise WalletError(f"get_real_balance.mjs not found at {script}")

        try:
            node = _find_node_executable()
        except Exception:
            node = "node"

        try:
            result = subprocess.run(
                [node, str(script)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=75,
                env={**os.environ, "MNEMONIC": mnemonic, "NETWORK": self.network},
            )
            # Script writes success JSON to stdout, error JSON to stderr
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if stdout:
                try:
                    data = json.loads(stdout)
                    if "error" not in data:
                        return Balance(
                            dust=int(data.get("dust", 0)),
                            night=int(data.get("night", 0)),
                        )
                except json.JSONDecodeError:
                    pass

            # Check stderr for JSON error
            if stderr:
                # stderr may have log lines before the JSON — find last JSON line
                for line in reversed(stderr.splitlines()):
                    line = line.strip()
                    if line.startswith("{"):
                        try:
                            err = json.loads(line)
                            if "error" in err:
                                raise WalletError(err["error"])
                        except json.JSONDecodeError:
                            pass
                        break

            raise WalletError("Could not retrieve balance from wallet SDK")
        except subprocess.TimeoutExpired:
            raise WalletError("Wallet SDK timed out after 130s — check your network connection")

    def get_addresses(self) -> Dict[str, str]:
        """Get wallet addresses from Lace wallet."""
        return self._run("addresses", self.network, timeout=30)

    def get_configuration(self) -> Dict[str, str]:
        """Get service configuration from Lace wallet."""
        return self._run("config", self.network, timeout=10)


def check_lace_wallet() -> bool:
    """
    Quick check if Lace wallet is available.
    
    Returns:
        True if Lace wallet is installed and accessible
    """
    connector = LaceConnector()
    return connector.is_available()


def get_lace_balance(network: str = "preprod") -> Optional[Balance]:
    """
    Get balance from Lace wallet.
    
    Args:
        network: Network to query (preprod, testnet, mainnet)
    
    Returns:
        Balance object or None if Lace wallet is not available
    """
    connector = LaceConnector(network=network)
    if not connector.is_available():
        return None
    
    try:
        connector.connect()
        return connector.get_balance()
    except WalletError:
        return None
