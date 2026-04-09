from midnight_sdk.codegen import compact_to_python, parse_compact_circuits
from midnight_sdk.exceptions import CompactParseError
import pytest


def test_parse_circuits(sample_compact_contract):
    circuits = parse_compact_circuits(sample_compact_contract)
    assert "post" in circuits
    assert "increment" in circuits


def test_compact_to_python_generates_class(sample_compact_contract):
    ContractClass = compact_to_python(sample_compact_contract)
    assert hasattr(ContractClass, "post")
    assert hasattr(ContractClass, "increment")
    assert hasattr(ContractClass, "state")


def test_generated_method_is_callable(sample_compact_contract, midnight_client):
    ContractClass = compact_to_python(sample_compact_contract)
    contract_mock = midnight_client.contracts.load("addr123", ["post", "increment"])
    instance = ContractClass(contract_mock)
    assert callable(instance.post)
    assert callable(instance.increment)


def test_raises_on_empty_compact(tmp_path):
    empty = tmp_path / "empty.compact"
    empty.write_text("pragma language_version >= 1.0.0;")
    with pytest.raises(CompactParseError, match="No exported circuits"):
        compact_to_python(str(empty))
