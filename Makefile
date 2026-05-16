.PHONY: install test lint format validate drift clean help

PYTHON := python3
PIP    := pip

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  %-14s %s\n", $$1, $$2}'

install:  ## Install all dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

lint:  ## Run ruff linter
	ruff check integrations/ digital-twins/ tests/

format:  ## Run black formatter
	black integrations/ digital-twins/ tests/

format-check:  ## Check formatting without modifying files
	black --check integrations/ digital-twins/ tests/

test:  ## Run full pytest suite
	pytest tests/ -v --tb=short

validate:  ## Run IoT validator example
	$(PYTHON) integrations/iot-validator.py

drift:  ## Run drift detection example
	$(PYTHON) digital-twins/drift-detection.py

clean:  ## Remove __pycache__ and .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
