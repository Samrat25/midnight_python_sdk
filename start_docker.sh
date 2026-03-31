#!/bin/bash
# Start Midnight services using Docker

echo "🌙 Starting Midnight Services with Docker"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Choose which docker-compose to use
if [ -f "docker-compose.real.yml" ] && [ "$1" == "--real" ]; then
    echo "Using real Midnight Docker images..."
    COMPOSE_FILE="docker-compose.real.yml"
else
    echo "Using local mock services..."
    COMPOSE_FILE="docker-compose.local.yml"
fi

echo "Compose file: $COMPOSE_FILE"
echo ""

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose -f $COMPOSE_FILE down 2>/dev/null

# Build and start services
echo ""
echo "Building and starting services..."
docker-compose -f $COMPOSE_FILE up -d --build

# Wait for services to be healthy
echo ""
echo "Waiting for services to be healthy..."
sleep 5

# Check service status
echo ""
echo "Checking service status..."
docker-compose -f $COMPOSE_FILE ps

echo ""
echo "=========================================="
echo "✓ Services started!"
echo ""
echo "Check status with:"
echo "  midnight-py status"
echo ""
echo "View logs with:"
echo "  docker-compose -f $COMPOSE_FILE logs -f"
echo ""
echo "Stop services with:"
echo "  docker-compose -f $COMPOSE_FILE down"
echo "=========================================="
