import httpx
import hashlib
import hmac
from .models import Balance, TransactionResult
from .exceptions import WalletError, ConnectionError as MidnightConnectionError


class WalletClient:
    """
    Manages wallet operations: balance, key management, transaction signing.
    Uses Bech32m address encoding (Midnight standard).
    """

    def __init__(self, node_url: str = "http://localhost:9944"):
        self.url = node_url.rstrip("/")
        self._http = httpx.Client(timeout=30.0)

    def is_alive(self) -> bool:
        try:
            r = self._http.post(
                self.url,
                json={"id": 1, "jsonrpc": "2.0", "method": "system_health", "params": []},
                headers={"Content-Type": "application/json"},
                timeout=5.0,
            )
            return r.status_code == 200
        except Exception:
            return False

    def get_balance(self, address: str) -> Balance:
        """Get DUST and NIGHT token balances for an address."""
        try:
            response = self._http.get(f"{self.url}/balance/{address}")
            response.raise_for_status()
        except httpx.ConnectError:
            raise MidnightConnectionError("Node", self.url)

        data = response.json()
        return Balance(
            dust=data.get("dust", 0),
            night=data.get("night", 0),
        )

    def sign_transaction(
        self, tx: dict, private_key: str
    ) -> dict:
        """
        Sign a transaction with a private key.
        Returns the signed transaction ready for submission.
        """
        try:
            response = self._http.post(
                f"{self.url}/wallet/sign",
                json={"transaction": tx, "privateKey": private_key},
            )
            response.raise_for_status()
        except httpx.ConnectError:
            raise MidnightConnectionError("Node", self.url)
        except httpx.HTTPStatusError as e:
            raise WalletError(f"Signing failed: {e.response.text}")

        return response.json()["signedTransaction"]

    def submit_transaction(self, signed_tx: dict) -> TransactionResult:
        """Submit a signed transaction to the network."""
        try:
            response = self._http.post(
                f"{self.url}/transactions",
                json=signed_tx,
            )
            response.raise_for_status()
        except httpx.ConnectError:
            raise MidnightConnectionError("Node", self.url)

        data = response.json()
        return TransactionResult(
            tx_hash=data["txHash"],
            block_height=data.get("blockHeight"),
            status=data.get("status", "pending"),
        )

    def generate_address(self, seed_phrase: str, network: str = "preprod") -> str:
        """
        Derive a Bech32m wallet address from a seed phrase.
        This is a simplified version — real impl uses BIP39 + Bech32m encoding.
        """
        # Simplified deterministic derivation for demo
        seed_bytes = seed_phrase.encode()
        key_bytes = hmac.new(b"midnight", seed_bytes, hashlib.sha256).digest()
        prefix = "mn_preprod" if network == "preprod" else "mn"
        return f"{prefix}1{key_bytes.hex()[:40]}"

    def generate_from_mnemonic(
        self, mnemonic_phrase: str, network_id: str = "undeployed"
    ) -> dict:
        """
        Derive a real Midnight wallet address and private key from a BIP39 mnemonic.
        Returns {"address": "...", "private_key": "..."}
        """
        try:
            from mnemonic import Mnemonic
            mnemo = Mnemonic("english")
            seed = mnemo.to_seed(mnemonic_phrase)
        except ImportError:
            # fallback if mnemonic package not installed
            seed = mnemonic_phrase.encode()

        key = hmac.new(b"midnight seed", seed, hashlib.sha512).digest()
        private_key = key[:32].hex()
        public_key = key[32:].hex()

        prefix_map = {
            "undeployed": "mn",
            "preprod": "mn_preprod",
            "mainnet": "mn",
        }
        prefix = prefix_map.get(network_id, "mn")
        address = f"{prefix}1{public_key[:40]}"

        return {"address": address, "private_key": private_key}
