from .proof import ProofClient
from .wallet import WalletClient
from .indexer import IndexerClient
from .models import ContractState, TransactionResult, ZKProof
from .exceptions import ContractDeployError, ContractCallError


class Contract:
    """
    Represents a deployed Midnight smart contract.
    
    Use ContractClient.deploy() or ContractClient.load() to get an instance.
    Don't instantiate this directly.
    """

    def __init__(
        self,
        address: str,
        circuit_ids: list[str],
        wallet: WalletClient,
        prover: ProofClient,
        indexer: IndexerClient,
        private_key: str | None = None,
    ):
        self.address = address
        self.circuit_ids = circuit_ids
        self._wallet = wallet
        self._prover = prover
        self._indexer = indexer
        self._private_key = private_key

    def call(
        self,
        circuit_name: str,
        private_inputs: dict | None = None,
        public_inputs: dict | None = None,
    ) -> TransactionResult:
        """
        Call a circuit function on this contract.
        
        1. Generates a ZK proof for the circuit
        2. Builds a transaction with the proof
        3. Signs and submits the transaction
        """
        if circuit_name not in self.circuit_ids:
            raise ContractCallError(
                f"Circuit '{circuit_name}' not found. "
                f"Available: {self.circuit_ids}"
            )

        # Step 1: Generate ZK proof
        proof: ZKProof = self._prover.generate_proof(
            circuit_id=f"{self.address}:{circuit_name}",
            private_inputs=private_inputs or {},
            public_inputs=public_inputs or {},
        )

        # Step 2: Build transaction
        tx = {
            "contractAddress": self.address,
            "circuit": circuit_name,
            "proof": proof.proof,
            "publicInputs": public_inputs or {},
            "publicOutputs": proof.public_outputs,
        }

        # Step 3: Sign
        if not self._private_key:
            raise ContractCallError("No private key set. Call contract.set_key(key) first.")
        signed = self._wallet.sign_transaction(tx, self._private_key)

        # Step 4: Submit
        return self._wallet.submit_transaction(signed)

    def state(self) -> ContractState:
        """Read the current public on-chain state of this contract."""
        return self._indexer.get_contract_state(self.address)

    def set_key(self, private_key: str) -> "Contract":
        """Set the private key used for signing. Returns self for chaining."""
        self._private_key = private_key
        return self


class ContractClient:
    """Factory for deploying and loading Midnight contracts."""

    def __init__(
        self,
        wallet: WalletClient,
        prover: ProofClient,
        indexer: IndexerClient,
    ):
        self._wallet = wallet
        self._prover = prover
        self._indexer = indexer

    def deploy(
        self,
        contract_path: str,
        constructor_args: dict | None = None,
        private_key: str | None = None,
    ) -> Contract:
        """
        Deploy a .compact contract to the network.
        Returns a Contract instance at the deployed address.
        """
        from .codegen import parse_compact_circuits
        import httpx

        circuits = parse_compact_circuits(contract_path)

        try:
            http = httpx.Client()
            response = http.post(
                f"{self._wallet.url}/contracts/deploy",
                json={
                    "contractPath": contract_path,
                    "constructorArgs": constructor_args or {},
                },
            )
            response.raise_for_status()
        except Exception as e:
            raise ContractDeployError(f"Deployment failed: {e}")

        address = response.json()["contractAddress"]
        return Contract(
            address=address,
            circuit_ids=circuits,
            wallet=self._wallet,
            prover=self._prover,
            indexer=self._indexer,
            private_key=private_key,
        )

    def load(self, address: str, circuit_ids: list[str]) -> Contract:
        """Load an already-deployed contract by address."""
        return Contract(
            address=address,
            circuit_ids=circuit_ids,
            wallet=self._wallet,
            prover=self._prover,
            indexer=self._indexer,
        )
