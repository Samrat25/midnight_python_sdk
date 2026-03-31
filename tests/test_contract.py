from midnight_py.contract import Contract
from midnight_py.exceptions import ContractCallError
import pytest


def test_contract_call_validates_circuit_name(midnight_client):
    contract = Contract(
        address="test_addr",
        circuit_ids=["valid_circuit"],
        wallet=midnight_client.wallet,
        prover=midnight_client.prover,
        indexer=midnight_client.indexer,
    )
    
    with pytest.raises(ContractCallError, match="Circuit 'invalid' not found"):
        contract.call("invalid", {}, {})


def test_contract_set_key_returns_self(midnight_client):
    contract = Contract(
        address="test_addr",
        circuit_ids=[],
        wallet=midnight_client.wallet,
        prover=midnight_client.prover,
        indexer=midnight_client.indexer,
    )
    
    result = contract.set_key("test_key")
    assert result is contract
    assert contract._private_key == "test_key"
