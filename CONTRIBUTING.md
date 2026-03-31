# Contributing to midnight-py

Thanks for your interest in contributing! This is a hackathon project that we hope grows into a production-ready SDK.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/midnight-py`
3. Install in dev mode: `pip install -e ".[dev]"`
4. Create a branch: `git checkout -b feature/your-feature`

## Development Setup

```bash
# Install dependencies
pip install -e ".[dev]"

# Start Midnight services (optional, tests work without)
docker-compose up -d

# Run tests
pytest tests/ -v

# Run linter
ruff check midnight_py/ tests/

# Format code
ruff format midnight_py/ tests/

# Type check
mypy midnight_py/
```

## Project Structure

```
midnight_py/
├── client.py        # Main entry point
├── wallet.py        # Wallet operations
├── contract.py      # Contract deployment & calls
├── proof.py         # ZK proof generation
├── indexer.py       # On-chain state queries
├── codegen.py       # .compact → Python codegen
├── models.py        # Pydantic data models
├── exceptions.py    # Custom exceptions
├── cli.py           # CLI commands
└── pytest_plugin.py # Test fixtures
```

## Code Style

We use:
- **ruff** for linting and formatting (88 char line length)
- **mypy** for type checking
- **Pydantic v2** for data validation
- **Type hints** everywhere

Example:

```python
def generate_proof(
    self,
    circuit_id: str,
    private_inputs: dict,
    public_inputs: dict | None = None,
) -> ZKProof:
    """
    Generate a ZK proof for a circuit.
    
    Args:
        circuit_id: Circuit identifier
        private_inputs: Secret data
        public_inputs: Public data (optional)
    
    Returns:
        ZKProof with proof string and outputs
    """
    ...
```

## Testing

All new features need tests:

```python
def test_your_feature(midnight_client):
    """Test description."""
    # Use the midnight_client fixture (fully mocked)
    result = midnight_client.some_method()
    assert result is not None
```

Run tests:

```bash
# All tests
pytest tests/ -v

# Specific test
pytest tests/test_client.py::test_client_creates_with_preprod -v

# With coverage
pytest tests/ --cov=midnight_py
```

## Adding New Features

### 1. New Client Method

Add to the appropriate client class:

```python
# midnight_py/wallet.py
def new_method(self, param: str) -> Result:
    """Docstring explaining what it does."""
    try:
        response = self._http.post(...)
        response.raise_for_status()
    except httpx.ConnectError:
        raise MidnightConnectionError("Service", self.url)
    
    return Result(**response.json())
```

### 2. New Model

Add to `models.py`:

```python
class NewModel(BaseModel):
    field1: str
    field2: int = 0
    field3: Optional[datetime] = None
```

### 3. New Exception

Add to `exceptions.py`:

```python
class NewError(MidnightSDKError):
    """Description of when this is raised."""
```

### 4. New CLI Command

Add to `cli.py`:

```python
@app.command()
def new_command(
    arg: str = typer.Argument(..., help="Description"),
    option: str = typer.Option("default", help="Description"),
):
    """Command description."""
    client = MidnightClient()
    result = client.some_method(arg)
    rprint(f"Result: {result}")
```

## Documentation

- Add docstrings to all public functions/classes
- Update README.md if adding major features
- Add examples to `examples/` for complex features
- Update ARCHITECTURE.md for architectural changes

## Pull Request Process

1. Update tests to cover your changes
2. Run `make check` (lint + tests)
3. Update documentation
4. Write a clear PR description:
   - What does this change?
   - Why is it needed?
   - How was it tested?

## Commit Messages

Use clear, descriptive commits:

```
feat: add async proof generation
fix: handle connection timeout in wallet client
docs: update quickstart guide
test: add integration test for contract deployment
refactor: simplify codegen regex patterns
```

## Areas for Contribution

### High Priority

- [ ] Real BIP39 mnemonic support
- [ ] Hardware wallet integration (Ledger/Trezor)
- [ ] Proof caching to avoid regeneration
- [ ] Batch transaction submission
- [ ] Better error messages with recovery hints

### Medium Priority

- [ ] Contract event listeners with type safety
- [ ] WASM-based client-side proof generation
- [ ] GraphQL query builder
- [ ] Transaction history queries
- [ ] Gas estimation

### Nice to Have

- [ ] Jupyter notebook examples
- [ ] VS Code extension for .compact files
- [ ] Contract deployment wizard
- [ ] Performance benchmarks
- [ ] Docker-free local development

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

## Code of Conduct

Be respectful, inclusive, and constructive. This is a learning project and everyone is welcome.

---

Thanks for contributing! 🌙
