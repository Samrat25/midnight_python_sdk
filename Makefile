.PHONY: install test lint format clean docker-up docker-down demo

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=midnight_sdk

lint:
	ruff check midnight_sdk/ tests/
	mypy midnight_sdk/

format:
	ruff format midnight_sdk/ tests/ examples/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-up:
	docker-compose up -d
	@echo "Waiting for services to start..."
	@sleep 5
	midnight-sdk status

docker-down:
	docker-compose down

demo:
	python examples/bulletin_board.py

check: lint test
	@echo "✓ All checks passed!"
