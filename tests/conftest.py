"""Test configuration for midnight-sdk."""

import pytest
from unittest.mock import Mock, MagicMock
from midnight_sdk import MidnightClient
from midnight_sdk.models import Balance, ZKProof


@pytest.fixture
def midnight_client():
    """Create a mocked MidnightClient for testing."""
    client = MidnightClient(network="local")
    
    # Mock the status method
    client.status = Mock(return_value={
        "node": True,
        "indexer": True,
        "prover": True
    })
    
    # Mock wallet methods
    client.wallet.generate_address = Mock(return_value="mn_preprod1test123")
    client.wallet.get_balance = Mock(return_value=Balance(dust=1000000, night=0))
    
    # Mock prover methods
    client.prover.generate_proof = Mock(return_value=ZKProof(
        proof="test_proof_hash",
        public_outputs={"verified": True},
        circuit_id="test:circuit"
    ))
    
    # Mock indexer methods
    mock_state = Mock()
    mock_state.address = "test_address"
    mock_state.data = {}
    mock_state.block_height = 100
    mock_state.state = {}
    client.indexer.get_contract_state = Mock(return_value=mock_state)
    
    # Mock contracts methods
    mock_contract = Mock()
    mock_contract.address = "addr123"
    mock_contract.circuit_ids = ["post", "increment"]
    
    # Mock contract call to return TransactionResult
    from midnight_sdk.models import TransactionResult
    mock_tx_result = TransactionResult(
        tx_hash="0x123abc",
        status="pending",
        block_height=None
    )
    mock_contract.call = Mock(return_value=mock_tx_result)
    
    # Mock state method
    mock_contract.state = Mock(return_value=mock_state)
    
    client.contracts.load = Mock(return_value=mock_contract)
    client.contracts.deploy = Mock(return_value=mock_contract)
    
    return client


@pytest.fixture
def sample_compact_contract(tmp_path):
    """Create a sample Compact contract file for testing."""
    contract_content = """
pragma language_version >= 0.20.0;
import CompactStandardLibrary;

export ledger counter: Counter;

export circuit increment(): [] {
    counter.increment(1);
}

export circuit post(message: Bytes<32>): [] {
    counter.increment(1);
}
"""
    contract_file = tmp_path / "test_contract.compact"
    contract_file.write_text(contract_content)
    return str(contract_file)


@pytest.fixture
def mock_wallet():
    """Create a mock wallet for testing."""
    wallet = Mock()
    wallet.address = "mn_preprod1test123"
    wallet.private_key = "test_private_key"
    wallet.sign = Mock(return_value="test_signature")
    return wallet


@pytest.fixture
def mock_prover():
    """Create a mock prover for testing."""
    prover = Mock()
    prover.generate_proof = Mock(return_value=ZKProof(
        proof="test_proof",
        public_outputs={},
        circuit_id="test"
    ))
    prover.is_alive = Mock(return_value=True)
    return prover


@pytest.fixture
def mock_indexer():
    """Create a mock indexer for testing."""
    indexer = Mock()
    indexer.url = "http://localhost:8088"
    indexer.is_alive = Mock(return_value=True)
    return indexer
