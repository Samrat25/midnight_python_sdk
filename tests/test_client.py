from midnight_sdk import MidnightClient
from midnight_sdk.exceptions import MidnightSDKError
import pytest


def test_client_creates_with_preprod():
    client = MidnightClient(network="preprod")
    assert client.network == "preprod"
    assert client.wallet is not None
    assert client.indexer is not None
    assert client.prover is not None


def test_client_raises_on_unknown_network():
    with pytest.raises(MidnightSDKError, match="Unknown network"):
        MidnightClient(network="fakenet")


def test_status_returns_dict(midnight_client):
    result = midnight_client.status()
    assert "node" in result
    assert "indexer" in result
    assert "prover" in result


def test_status_all_services_up(midnight_client):
    result = midnight_client.status()
    assert all(result.values())
