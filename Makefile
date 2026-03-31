.PHONY: install test lint format clean docker-up docker-down demo

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=midnight_py

lint:
	ruff check midnight_py/ tests/
	mypy midnight_py/

format:
	ruff format midnight_py/ tests/ examples/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-up:
	docker-compose up -d
	@echo "Waiting for services to start..."
	@sleep 5
	midnight-py status

docker-down:
	docker-compose down

demo:
	python examples/bulletin_board.py

check: lint test
	@echo "✓ All checks passed!"
