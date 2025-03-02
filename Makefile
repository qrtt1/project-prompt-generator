.PHONY: setup check build test release clean

VENV = venv
PYTHON = $(VENV)/bin/python

# Create venv if not exist, upgrade pip, and install required packages.
setup:
	test -d $(VENV) || python -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"
	$(PYTHON) -m pip install build twine

# Verify that the Python executable is from the venv.
check:
	@$(PYTHON) -c "import sys; print('Python executable:', sys.executable)"

# Run tests
test:
	$(PYTHON) -m pytest

# Run tests with coverage report
coverage:
	$(PYTHON) -m pytest --cov=prompts tests/

build: setup
	$(PYTHON) -m build

release: build
	$(PYTHON) -m twine upload dist/*

clean:
	rm -rf build dist *.egg-info
