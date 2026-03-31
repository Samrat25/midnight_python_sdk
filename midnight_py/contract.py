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
        
        This requires:
        1. Compact compiler installed (npm install -g @midnight-ntwrk/compact-compiler)
        2. Contract compiled to managed/ directory
        3. Proof server running (docker run -p 6300:6300 midnightntwrk/proof-server)
        4. Wallet with NIGHT + DUST tokens
        
        Returns a Contract instance at the deployed address.
        """
        import subprocess
        import json
        from pathlib import Path
        
        from .codegen import parse_compact_circuits

        # Check if contract is compiled
        contract_name = Path(contract_path).stem
        managed_dir = Path("contracts/managed") / contract_name
        contract_js = managed_dir / "contract" / "index.js"
        
        if not contract_js.exists():
            raise ContractDeployError(
                f"Contract not compiled!\n\n"
                f"Run: compact compile {contract_path} {managed_dir}\n\n"
                f"This requires:\n"
                f"  1. Install Compact compiler: npm install -g @midnight-ntwrk/compact-compiler\n"
                f"  2. Compile your contract: compact compile {contract_path} {managed_dir}\n"
                f"  3. Verify {contract_js} exists\n"
            )

        circuits = parse_compact_circuits(contract_path)

        # For now, we need to use the TypeScript SDK for deployment
        # because it requires complex ZK proof generation and wallet integration
        raise ContractDeployError(
            f"Contract deployment requires the full Midnight TypeScript SDK.\n\n"
            f"Your contract is compiled at: {managed_dir}\n\n"
            f"To deploy, use the TypeScript SDK:\n"
            f"  1. Install dependencies: npm install @midnight-ntwrk/midnight-js-contracts\n"
            f"  2. Create deploy.ts script (see Midnight docs)\n"
            f"  3. Run: tsx deploy.ts\n\n"
            f"midnight-py can interact with deployed contracts using:\n"
            f"  contract = client.get_contract(address, {circuits})\n"
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
