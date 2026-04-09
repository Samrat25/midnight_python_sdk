from midnight_sdk.proof import ProofClient
from midnight_sdk.models import ZKProof
import pytest


def test_proof_client_initialization():
    client = ProofClient()
    assert client.url == "http://localhost:6300"


def test_proof_client_custom_url():
    client = ProofClient(url="http://custom:7000")
    assert client.url == "http://custom:7000"


def test_proof_client_strips_trailing_slash():
    client = ProofClient(url="http://localhost:6300/")
    assert client.url == "http://localhost:6300"
