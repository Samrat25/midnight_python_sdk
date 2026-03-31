#!/bin/bash
# Stop Midnight Docker services

echo "🌙 Stopping Midnight Services"
echo "=============================="
echo ""

# Stop local services
if [ -f "docker-compose.local.yml" ]; then
    echo "Stopping local services..."
    docker-compose -f docker-compose.local.yml down
fi

# Stop real services
if [ -f "docker-compose.real.yml" ]; then
    echo "Stopping real services..."
    docker-compose -f docker-compose.real.yml down
fi

echo ""
echo "✓ All services stopped"
