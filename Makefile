# --- Variables ---
VENV_DIR = .venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate
ACTIVATE = . $(VENV_ACTIVATE)
PIP = $(ACTIVATE) && pip
RUN_WITH_PATH = $(ACTIVATE) && PYTHONPATH=.

# The sentinel file to check if setup is complete
SETUP_STAMP = $(VENV_DIR)/.setup_stamp

# --- Phony targets ---
.PHONY: all setup test test-verbose render clean showtree gentree filesdump filesdump-detailed help

# Default target runs 'setup'
all: setup

# --- Virtual Environment Setup ---
$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)

# Smart 'setup' target
$(SETUP_STAMP): $(VENV_DIR)/bin/activate requirements.txt
	@echo "--- Installing dependencies ---"
	$(PIP) install -r requirements.txt
	@echo "--- Setup complete ---"
	@touch $(SETUP_STAMP)

setup: $(SETUP_STAMP) ## Create venv and install dependencies

# --- Testing Targets ---
test: $(SETUP_STAMP) ## Run all tests (quiet mode)
	$(RUN_WITH_PATH) pytest -q

test-verbose: $(SETUP_STAMP) ## Run tests with verbose output
	$(RUN_WITH_PATH) pytest -v -s

# --- Rendering Targets ---
render: $(SETUP_STAMP) ## Render all projects' artefacts (or one: make render PROJECT=scurry)
	$(RUN_WITH_PATH) python scripts/render.py $(if $(PROJECT),--project $(PROJECT),)

# --- Utility Targets ---

# Note: Requires 'tools/concat_files.py' to be present
filesdump: $(SETUP_STAMP) gentree ## Create context dump for LLMs (requires manifest.lst)
	@if [ -f manifest.lst ]; then \
		$(RUN_WITH_PATH) python tools/concat_files.py manifest.lst > tmp/filesdump.txt; \
		echo "Generated tmp/filesdump.txt"; \
	else \
		echo "Error: manifest.lst not found"; \
	fi

# Same as 'filesdump', but also reports each included file's name, token
# estimate, and size in KB on stderr (stdout stays reserved for the dump).
filesdump-detailed: $(SETUP_STAMP) gentree ## Create context dump for LLMs with per-file size details (requires manifest.lst)
	@if [ -f manifest.lst ]; then \
		$(RUN_WITH_PATH) python tools/concat_files.py --detailed manifest.lst > tmp/filesdump.txt; \
		echo "Generated tmp/filesdump.txt"; \
	else \
		echo "Error: manifest.lst not found"; \
	fi

clean: ## Remove venv, cache, and tmp files
	rm -rf $(VENV_DIR) .pytest_cache tmp
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.egg-info" -type d -prune -exec rm -rf {} +

showtree: ## Show project directory structure
	tree -I ".venv|__pycache__|.idea|.pytest_cache|*egg-info|tmp"

gentree: ## Save tree structure to file
	mkdir -p tmp
	tree -I ".venv|__pycache__|.idea|.pytest_cache|*egg-info|tmp" > tmp/project_tree.txt

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
