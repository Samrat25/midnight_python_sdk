from midnight_sdk.wallet import WalletClient
from midnight_sdk.models import Balance
import pytest


def test_generate_address_preprod():
    wallet = WalletClient()
    addr = wallet.generate_address("test seed phrase", network="preprod")
    assert addr.startswith("mn_preprod1")
    assert len(addr) > 20


def test_generate_address_mainnet():
    wallet = WalletClient()
    addr = wallet.generate_address("test seed phrase", network="mainnet")
    assert addr.startswith("mn1")


def test_generate_address_deterministic():
    wallet = WalletClient()
    addr1 = wallet.generate_address("same seed", network="preprod")
    addr2 = wallet.generate_address("same seed", network="preprod")
    assert addr1 == addr2
