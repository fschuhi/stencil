# haddolib — Makefile
#
# Cross-platform: macOS (native .venv) and Windows (native .venv-win, run from an
# MSYS2 / Git-Bash shell). GNU make sets OS=Windows_NT on Windows — including
# inside MSYS2 — so the block below flips only the things that actually differ:
# the venv dir, its bin/Scripts subdir, the Python launcher, and the reqs file.
#
# All targets and recipes are shared; coreutils (touch/rm/find/grep/awk) come
# from the POSIX shell on both sides.
#
# Note: on Windows, PYTHON = `py -3` so the venv is built by NATIVE Windows
# Python (required for PyXLL), not MSYS2's python. Override if needed, e.g.:
#   make setup PYTHON=python

# --- OS-specific variables ---
ifeq ($(OS),Windows_NT)
    VENV_DIR     = .venv-win
    VENV_BIN     = $(VENV_DIR)/Scripts
    PYTHON       = py -3
    REQUIREMENTS = requirements-win.txt
else
    VENV_DIR     = .venv
    VENV_BIN     = $(VENV_DIR)/bin
    PYTHON       = python3
    REQUIREMENTS = requirements.txt
endif

# --- Derived variables (shared) ---
VENV_ACTIVATE = $(VENV_BIN)/activate
ACTIVATE      = . $(VENV_ACTIVATE)
PIP           = $(ACTIVATE) && pip
RUN           = $(ACTIVATE) && python
SETUP_STAMP   = $(VENV_DIR)/.setup_stamp

# --- Phony targets ---
.PHONY: all setup test test-verbose clean showtree gentree filesdump help

all: setup

# --- Virtual Environment & Setup ---

$(VENV_ACTIVATE):
	$(PYTHON) -m venv $(VENV_DIR)

$(SETUP_STAMP): $(VENV_ACTIVATE) $(REQUIREMENTS) pyproject.toml
	@echo "--- Installing dependencies ($(REQUIREMENTS)) ---"
	$(PIP) install -r $(REQUIREMENTS)
	@echo "--- Installing project in editable mode ---"
	$(PIP) install -e .
	@echo "--- Setup complete ---"
	@touch $(SETUP_STAMP)

setup: $(SETUP_STAMP) ## Create venv and install dependencies

# --- Testing ---

test: $(SETUP_STAMP) ## Run all tests (quiet mode)
	$(RUN) -m pytest -q

test-verbose: $(SETUP_STAMP) ## Run tests with verbose output
	$(RUN) -m pytest -v -s

# --- Tools ---

# TBD

# --- Utilities ---

clean: ## Remove venv, cache, and tmp files
	rm -rf $(VENV_DIR) .pytest_cache tmp
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.egg-info" -type d -prune -exec rm -rf {} +

showtree: ## Show project directory structure (needs `tree`; mac-side)
	@tree -I ".venv|.venv-win|__pycache__|tmp|*.egg-info|.git|*.jpg" -L 3

gentree: ## Save tree to tmp/project_tree.txt (needs `tree`; mac-side)
	@mkdir -p tmp
	@tree -I ".venv|.venv-win|__pycache__|tmp|*.egg-info|.git|*.jpg|*_rejected.*" > tmp/project_tree.txt
	@echo "Project tree saved to tmp/project_tree.txt"

filesdump: gentree ## Create context dump for LLMs
	@echo "--- Generating filesdump ---"
	$(RUN) tools/concat_files.py manifest.lst > tmp/filesdump.txt
	@echo "Filesdump created at tmp/filesdump.txt"

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'