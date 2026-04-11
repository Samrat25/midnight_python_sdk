from midnight_sdk.wallet import WalletClient
from midnight_sdk.models import Balance
import pytest


def test_get_real_address_undeployed():
    """Test generating address for undeployed (local) network."""
    wallet = WalletClient()
    mnemonic = "test seed phrase word word word word word word word word word word word word word word word word word word word word word"
    result = wallet.get_real_address(mnemonic, "undeployed")
    assert "address" in result
    assert result["address"].startswith("mn_addr_undeployed1")


def test_get_real_address_returns_dict():
    """Test that get_real_address returns a dictionary with address key."""
    wallet = WalletClient()
    mnemonic = "test seed phrase word word word word word word word word word word word word word word word word word word word word word"
    result = wallet.get_real_address(mnemonic, "undeployed")
    assert isinstance(result, dict)
    assert "address" in result
    assert len(result["address"]) > 20


def test_get_real_address_deterministic():
    """Test that same mnemonic generates same address."""
    wallet = WalletClient()
    mnemonic = "same seed phrase word word word word word word word word word word word word word word word word word word word word word"
    result1 = wallet.get_real_address(mnemonic, "undeployed")
    result2 = wallet.get_real_address(mnemonic, "undeployed")
    assert result1["address"] == result2["address"]
