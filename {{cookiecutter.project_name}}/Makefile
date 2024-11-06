.PHONY: translations-extract translations-init translations-compile translations-update help

# Variables
LOCALES_DIR = app/locales
POT_FILE = $(LOCALES_DIR)/messages.pot
PYDANTIC_POT = $(LOCALES_DIR)/pydantic_messages.pot
BABEL_CONFIG = babel.cfg

# Help target
help:
	@echo "Translation management commands:"
	@echo "  make translations-extract     Extract translatable strings to POT file"
	@echo "  make translations-init LANG=xx  Initialize new language (e.g., LANG=ru)"
	@echo "  make translations-compile     Compile translation messages"
	@echo "  make translations-update      Update all existing translations with new strings"
	@echo "  make translations-all LANG=xx  Run complete translation workflow for new language"

# Ensure pydantic messages exist
ensure-pydantic-messages:
	@if [ ! -f "$(PYDANTIC_POT)" ]; then \
		echo "Error: $(PYDANTIC_POT) not found. Please create this file with your Pydantic messages first."; \
		exit 1; \
	fi

# Extract translatable strings
translations-extract: ensure-pydantic-messages
	@echo "Extracting translatable strings..."
	@mkdir -p $(LOCALES_DIR)
	python scripts/extract_messages.py
	@echo "Strings extracted to $(POT_FILE)"

# Initialize a new language
translations-init:
	@if [ -z "$(LANG)" ]; then \
		echo "Error: LANG parameter is required. Usage: make translations-init LANG=xx"; \
		exit 1; \
	fi
	@echo "Initializing translations for language: $(LANG)"
	pybabel init -i $(POT_FILE) -d $(LOCALES_DIR) -l $(LANG)
	@echo "Translation files created for $(LANG)"

# Compile translation messages
translations-compile:
	@echo "Compiling translation messages..."
	pybabel compile -d $(LOCALES_DIR)
	@echo "Translations compiled successfully"

# Update existing translations with new strings
translations-update:
	@echo "Updating existing translations..."
	pybabel update -i $(POT_FILE) -d $(LOCALES_DIR)
	@echo "Translations updated successfully"

# Complete workflow for new language
translations-all: translations-extract
	@if [ -z "$(LANG)" ]; then \
		echo "Error: LANG parameter is required. Usage: make translations-all LANG=xx"; \
		exit 1; \
	fi
	@make translations-init LANG=$(LANG)
	@make translations-compile
	@echo "Complete translation workflow finished for $(LANG)"