import httpx
from .models import ZKProof
from .exceptions import ProofGenerationError, ConnectionError as MidnightConnectionError


class ProofClient:
    """
    Talks to the Midnight proof server (default: http://localhost:6300).
    
    The proof server takes private inputs, runs a ZK circuit, and returns
    a cryptographic proof. The proof can be verified on-chain without
    revealing the private inputs.
    """

    def __init__(self, url: str = "http://localhost:6300"):
        self.url = url.rstrip("/")
        self._http = httpx.Client(timeout=120.0)  # proofs can take time

    def is_alive(self) -> bool:
        try:
            r = self._http.get(f"{self.url}/health", timeout=5.0)
            return r.status_code == 200
        except Exception:
            return False

    def generate_proof(
        self,
        circuit_id: str,
        private_inputs: dict,
        public_inputs: dict | None = None,
        circuit_files_dir: str | None = None,
    ) -> ZKProof:
        """
        Generate a ZK proof for a given circuit.
        
        Args:
            circuit_id: Identifier of the circuit (e.g. "BulletinBoard:post")
            private_inputs: Secret data — never leaves this machine
            public_inputs: Data that can be visible on-chain
            circuit_files_dir: Optional path to circuit files directory
            
        Returns:
            ZKProof with the proof string and public outputs
        """
        payload = {
            "circuitId": circuit_id,
            "privateInputs": private_inputs,
            "publicInputs": public_inputs or {},
        }
        if circuit_files_dir:
            payload["circuitFilesDir"] = circuit_files_dir

        try:
            response = self._http.post(
                f"{self.url}/prove",
                json=payload,
            )
            response.raise_for_status()
        except httpx.ConnectError:
            raise MidnightConnectionError("Proof Server", self.url)
        except httpx.HTTPStatusError as e:
            raise ProofGenerationError(
                f"Proof generation failed for '{circuit_id}': {e.response.text}"
            )

        data = response.json()
        return ZKProof(
            proof=data["proof"],
            public_outputs=data.get("publicOutputs", {}),
            circuit_id=circuit_id,
        )

    async def generate_proof_async(
        self,
        circuit_id: str,
        private_inputs: dict,
        public_inputs: dict | None = None,
    ) -> ZKProof:
        """Async version of generate_proof."""
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(
                    f"{self.url}/prove",
                    json={
                        "circuitId": circuit_id,
                        "privateInputs": private_inputs,
                        "publicInputs": public_inputs or {},
                    },
                )
                response.raise_for_status()
            except httpx.ConnectError:
                raise MidnightConnectionError("Proof Server", self.url)

        data = response.json()
        return ZKProof(
            proof=data["proof"],
            public_outputs=data.get("publicOutputs", {}),
            circuit_id=circuit_id,
        )

    def __del__(self):
        self._http.close()
