"""
pytest plugin for midnight-py.

Auto-registered via pyproject.toml entry point. Provides fixtures that mock
all 3 Midnight services — no Docker needed.

Usage in tests:
    def test_something(midnight_client, mock_proof_server):
        ...
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from .client import MidnightClient
from .models import ZKProof, TransactionResult, ContractState, Balance
from datetime import datetime


@pytest.fixture
def midnight_client():
    """
    A fully mocked MidnightClient.
    All services return realistic dummy data.
    No Docker, no network required.
    """
    client = MagicMock(spec=MidnightClient)
    
    # Create mock sub-clients
    client.wallet = MagicMock()
    client.indexer = MagicMock()
    client.prover = MagicMock()
    client.contracts = MagicMock()

    # Mock wallet
    client.wallet.is_alive.return_value = True
    client.wallet.get_balance.return_value = Balance(dust=1_000_000, night=100)
    client.wallet.sign_transaction.return_value = {"signed": True, "tx": {}}
    client.wallet.submit_transaction.return_value = TransactionResult(
        tx_hash="0xmocktxhash123",
        block_height=42,
        status="confirmed",
    )
    client.wallet.generate_address.return_value = "mn_preprod1mockedaddress123"
    client.wallet.generate_address.return_value = "mn_preprod1mockedaddress123"

    # Mock indexer
    client.indexer.is_alive.return_value = True
    client.indexer.get_contract_state.return_value = ContractState(
        address="mock_address",
        state={"value": "mock_state"},
        block_height=42,
    )

    # Mock prover
    client.prover.is_alive.return_value = True
    client.prover.generate_proof.return_value = ZKProof(
        proof="mock_proof_abc123xyz",
        public_outputs={"result": True},
        circuit_id="mock:circuit",
    )
    
    # Mock contracts
    mock_contract = MagicMock()
    mock_contract.address = "mock_contract_address"
    mock_contract.circuit_ids = ["post", "increment"]
    client.contracts.deploy.return_value = mock_contract
    client.contracts.load.return_value = mock_contract

    # Mock status
    client.status.return_value = {
        "node": True,
        "indexer": True,
        "prover": True,
    }

    return client


@pytest.fixture
def mock_proof_server():
    """Tracks proof generation calls."""
    server = MagicMock()
    server.proof_count = 0

    original_generate = server.generate_proof

    def counting_generate(*args, **kwargs):
        server.proof_count += 1
        return ZKProof(
            proof=f"proof_{server.proof_count}",
            public_outputs={},
            circuit_id=args[0] if args else "unknown",
        )

    server.generate_proof.side_effect = counting_generate
    return server


@pytest.fixture
def sample_compact_contract(tmp_path):
    """Creates a minimal .compact file for testing codegen."""
    contract_source = """
pragma language_version >= 1.0.0;
import CompactStandardLibrary;

ledger {
  counter: Counter;
  message: Bytes<256>;
}

export circuit post(message: Bytes<256>): [] {
  ledger.message = message;
}

export circuit increment(): [] {
  increment_counter(ledger.counter);
}
"""
    contract_file = tmp_path / "test_contract.compact"
    contract_file.write_text(contract_source)
    return str(contract_file)
