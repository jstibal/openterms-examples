.PHONY: install install-dev test syntax-check clean

install:
	pip install "openterms-py>=0.3.1"

install-dev:
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v

syntax-check:
	python -m unittest discover -s tests -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
