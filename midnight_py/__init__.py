"""midnight-py: The first Python SDK for the Midnight blockchain."""

from .client import MidnightClient
from .models import Balance, ZKProof, TransactionResult, ContractState
from .exceptions import (
    MidnightSDKError,
    ProofGenerationError,
    ContractDeployError,
    ContractCallError,
    WalletError,
    CompactParseError,
)
from .codegen import compact_to_python

__version__ = "0.1.0"
__all__ = [
    "MidnightClient",
    "compact_to_python",
    "Balance",
    "ZKProof",
    "TransactionResult",
    "ContractState",
    "MidnightSDKError",
    "ProofGenerationError",
    "ContractDeployError",
    "ContractCallError",
    "WalletError",
    "CompactParseError",
]
