#!/bin/bash
# Quick setup script for midnight-sdk

set -e

echo "🌙 midnight-sdk Setup"
echo "===================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.10+ required. Found: $python_version"
    exit 1
fi
echo "✓ Python $python_version"

# Check Docker
echo ""
echo "Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not found. You'll need it to run Midnight services."
    echo "   Install from: https://docs.docker.com/get-docker/"
else
    echo "✓ Docker installed"
fi

# Install package
echo ""
echo "Installing midnight-sdk..."
pip install -e ".[dev]"
echo "✓ Package installed"

# Check installation
echo ""
echo "Verifying installation..."
python3 -c "import midnight_sdk; print(f'✓ midnight-sdk v{midnight_sdk.__version__}')"

# Run tests
echo ""
echo "Running tests..."
pytest tests/ -v --tb=short
echo "✓ Tests passed"

# Check services (if Docker is running)
if command -v docker &> /dev/null && docker info &> /dev/null; then
    echo ""
    echo "Starting Midnight services..."
    docker-compose up -d
    sleep 5
    
    echo ""
    echo "Checking service status..."
    midnight-sdk status || echo "⚠️  Services not ready yet. Run 'docker-compose up -d' and wait a minute."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Start services: docker-compose up -d"
echo "  2. Check status: midnight-sdk status"
echo "  3. Run example: python examples/bulletin_board.py"
echo "  4. Read docs: cat QUICKSTART.md"
echo ""
echo "Happy building! 🚀"
