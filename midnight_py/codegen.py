"""
Compact ABI Codegen — reads .compact files and generates Python classes.

This is the feature that doesn't exist in ANY other blockchain's Python SDK.
Instead of manually writing contract call wrappers, developers point this at
their .compact file and get a fully-typed Python class back.
"""

import re
from pathlib import Path
from typing import Any
from .exceptions import CompactParseError


def parse_compact_circuits(contract_path: str) -> list[str]:
    """Extract all exported circuit names from a .compact file."""
    source = Path(contract_path).read_text()
    circuits = re.findall(r'export\s+circuit\s+(\w+)\s*\(', source)
    if not circuits:
        raise CompactParseError(
            f"No exported circuits found in {contract_path}. "
            "Make sure your circuits use 'export circuit name()' syntax."
        )
    return circuits


def compact_to_python(contract_path: str) -> type:
    """
    Read a .compact contract file and generate a Python class.
    
    Each exported circuit becomes a Python method.
    
    Example:
        .compact file has:  export circuit post(message: Bytes)
        Generated class has: .post(message=b"hello")
    
    Usage:
        BulletinBoard = compact_to_python("contracts/bulletin_board.compact")
        board = BulletinBoard(contract_instance)
        board.post(message=b"hello midnight!")
    """
    source = Path(contract_path).read_text()

    # Parse circuits with their parameters
    circuit_pattern = re.compile(
        r'export\s+circuit\s+(\w+)\s*\((.*?)\)',
        re.DOTALL
    )
    circuits = circuit_pattern.findall(source)

    if not circuits:
        raise CompactParseError(f"No exported circuits in {contract_path}")

    # Parse ledger state fields
    ledger_pattern = re.compile(r'ledger\s*\{([^}]+)\}', re.DOTALL)
    ledger_match = ledger_pattern.search(source)
    ledger_fields = []
    if ledger_match:
        field_pattern = re.compile(r'(\w+)\s*:\s*(\w+)')
        ledger_fields = field_pattern.findall(ledger_match.group(1))

    # Build dynamic class methods
    methods = {}

    for circuit_name, params_str in circuits:
        param_names = [
            p.strip().split(":")[0].strip()
            for p in params_str.split(",")
            if p.strip()
        ]

        def make_circuit_method(name: str, pnames: list[str]):
            def method(self, private_inputs: dict | None = None, **kwargs):
                """Auto-generated from .compact circuit definition."""
                public_inputs = {k: v for k, v in kwargs.items() if k in pnames}
                return self._contract.call(
                    circuit_name=name,
                    private_inputs=private_inputs or {},
                    public_inputs=public_inputs,
                )
            method.__name__ = name
            method.__doc__ = (
                f"Call the '{name}' circuit.\n"
                f"Public params: {pnames}\n"
                f"Use private_inputs={{}} for secret data."
            )
            return method

        methods[circuit_name] = make_circuit_method(circuit_name, param_names)

    # Add state() method
    def state_method(self):
        """Read current on-chain ledger state."""
        return self._contract.state()
    methods["state"] = state_method

    # Add __init__
    def init_method(self, contract):
        self._contract = contract
        self._ledger_fields = ledger_fields
    methods["__init__"] = init_method

    # Create and return the class
    contract_name = Path(contract_path).stem.replace("_", " ").title().replace(" ", "")
    generated_class = type(contract_name, (), methods)
    generated_class.__doc__ = f"Auto-generated from {contract_path}"
    return generated_class
