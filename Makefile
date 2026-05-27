.PHONY: test coverage lint security install clean

install:
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -q --tb=short

test-verbose:
	python -m pytest tests/ -v --tb=short

coverage:
	python -m pytest tests/ --cov=pareto_tournament --cov-report=term-missing --cov-fail-under=75

lint:
	ruff check pareto_tournament/ tests/

format:
	ruff format pareto_tournament/ tests/

type-check:
	mypy pareto_tournament/ --ignore-missing-imports

security:
	bandit -r pareto_tournament/ tests/
	pip-audit --desc .

dev: install lint type-check test

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/
