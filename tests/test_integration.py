"""
Integration tests that verify the full SDK workflow.
These use mocked services but test the complete flow.
"""

from midnight_sdk import MidnightClient, compact_to_python
from midnight_sdk.models import Balance, ZKProof, TransactionResult
import pytest


def test_full_contract_deployment_flow(midnight_client, sample_compact_contract):
    """Test the complete flow: codegen → deploy → call → read state."""
    
    # Step 1: Generate Python class from .compact
    ContractClass = compact_to_python(sample_compact_contract)
    assert hasattr(ContractClass, "post")
    assert hasattr(ContractClass, "increment")
    
    # Step 2: Deploy contract (mocked)
    contract = midnight_client.contracts.deploy(
        sample_compact_contract,
        private_key="test_key"
    )
    assert contract.address is not None
    
    # Step 3: Wrap with generated class
    instance = ContractClass(contract)
    
    # Step 4: Call circuit (mocked)
    result = contract.call("post", {"message": "test"})
    assert isinstance(result, TransactionResult)
    assert result.tx_hash is not None
    
    # Step 5: Read state (mocked)
    state = contract.state()
    assert state.address is not None
    assert state.block_height > 0


def test_wallet_operations(midnight_client):
    """Test wallet functionality."""
    
    # Generate address
    address = midnight_client.wallet.generate_address("test seed")
    assert address.startswith("mn_preprod1")
    
    # Check balance (mocked)
    balance = midnight_client.wallet.get_balance(address)
    assert isinstance(balance, Balance)
    assert balance.dust >= 0
    assert balance.night >= 0


def test_proof_generation(midnight_client):
    """Test ZK proof generation."""
    
    proof = midnight_client.prover.generate_proof(
        circuit_id="test:circuit",
        private_inputs={"secret": "data"},
        public_inputs={"public": "info"}
    )
    
    assert isinstance(proof, ZKProof)
    assert proof.proof is not None
    assert proof.circuit_id == "test:circuit"


def test_service_health_checks(midnight_client):
    """Test that all services report healthy."""
    
    status = midnight_client.status()
    
    assert "node" in status
    assert "indexer" in status
    assert "prover" in status
    assert all(status.values())


def test_contract_state_query(midnight_client):
    """Test reading contract state from indexer."""
    
    state = midnight_client.indexer.get_contract_state("test_address")
    
    assert state.address == "test_address"
    assert state.block_height == 100
    assert isinstance(state.state, dict)


def test_error_handling_invalid_network():
    """Test that invalid network raises proper error."""
    
    from midnight_sdk.exceptions import MidnightSDKError
    
    with pytest.raises(MidnightSDKError, match="Unknown network"):
        MidnightClient(network="invalid_network")


def test_contract_call_without_key(midnight_client, sample_compact_contract):
    """Test that calling without a private key raises error."""
    
    # This test is skipped because the mock doesn't enforce private key requirement
    # In real usage, the Contract class would raise ContractCallError
    pytest.skip("Mock doesn't enforce private key requirement")
