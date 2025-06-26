# Makefile for GitHub Checker project

.PHONY: all pot po mo i18n html sdist wheel clean clean_all test install

# Default target
all: i18n html wheel

# Configuration
PODEST = bot/locale
PROJECT_DIR = .

# Extract translatable strings
pot:
	pybabel extract -o $(PODEST)/bot.pot bot/

# Update Russian translations
po: pot
	pybabel update -l en_US.UTF-8 -D bot -i $(PODEST)/bot.pot -d $(PODEST)

# Compile translations
mo: po
	mkdir -p $(PODEST)/en_US.UTF-8/LC_MESSAGES
	pybabel compile -D bot -l en_US.UTF-8 -i $(PODEST)/en_US.UTF-8/LC_MESSAGES/bot.po -d $(PODEST)

# Build i18n (alias for mo)
i18n: mo

# Build documentation
html: i18n
	sphinx-build -M html docs docs/_build

# Create source distribution
sdist:
	python3 -m build -s

# Create wheel distribution
wheel: html
	python3 -m build -w

# Run tests
test: i18n
	python3 -m pytest

# Install for development
install:
	pipenv shell
	pipenv install

# Clean build artifacts
clean:
	rm -rf dist build *.egg-info
	rm -rf docs/_build
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -exec rm -rf {} +

# Full clean (including translations)
clean_all: clean
	rm -rf $(PODEST)/*.pot
	rm -rf $(PODEST)/*/LC_MESSAGES/*.mo
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +

# Help target
help:
	@echo "Available targets:"
	@echo "  all        - Build everything (default)"
	@echo "  pot        - Extract translatable strings"
	@echo "  po         - Update translation files"
	@echo "  mo         - Compile translations"
	@echo "  i18n       - Build internationalization files (alias for mo)"
	@echo "  html       - Build documentation"
	@echo "  sdist      - Create source distribution"
	@echo "  wheel      - Create wheel distribution"
	@echo "  test       - Run tests"
	@echo "  install    - Install for development"
	@echo "  clean      - Remove build artifacts"
	@echo "  clean_all  - Full clean including translations"