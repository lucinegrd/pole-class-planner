# Détection de Python
ifeq ($(shell python3 --version >/dev/null 2>&1; echo $$?),0)
    PYTHON = python3
else ifeq ($(shell python --version >/dev/null 2>&1; echo $$?),0)
    PYTHON = python
else
    $(error "Python non trouvé. Veuillez installer Python 3.x")
endif

# Variables d'environnement
VENV = .venv
VENV_BIN = $(VENV)/bin
ifeq ($(OS),Windows_NT)
    VENV_BIN = $(VENV)/Scripts
    PYTHON_VENV = $(VENV_BIN)/python.exe
    RM = rd /s /q
else
    PYTHON_VENV = $(VENV_BIN)/python
    RM = rm -rf
endif

.PHONY: install test clean

# Cible par défaut
all: venv install

# Créer l'environnement virtuel
venv:
	@echo "Création de l'environnement virtuel avec $(PYTHON)..."
	$(PYTHON) -m venv $(VENV)
	@echo "Environnement virtuel créé dans le dossier $(VENV)"
	@echo "Pour l'activer manuellement:"
ifeq ($(OS),Windows_NT)
	@echo "  $(VENV_BIN)/activate.bat"
else
	@echo "  source $(VENV_BIN)/activate"
endif

# Installation des dépendances dans l'environnement virtuel
install: venv
	@echo "Installation des dépendances..."
	$(PYTHON_VENV) -m pip install --upgrade pip
	$(PYTHON_VENV) -m pip install -r requirements-dev.txt
	$(PYTHON_VENV) -m pip install flake8 pylint black pytest pytest-cov

# Supprimer l'environnement virtuel
clean-venv:
	$(RM) $(VENV)

run:
	python app.py

test:
	PYTHONPATH=. $(VENV_BIN)/pytest tests/ -v


test-unit:
	PYTHONPATH=. $(VENV_BIN)/pytest tests/unit/ -v

test-integration:
	PYTHONPATH=. $(VENV_BIN)/pytest tests/integration/ -v

test-e2e:
	PYTHONPATH=. $(VENV_BIN)/pytest tests/e2e/ -v

coverage:
	PYTHONPATH=. $(VENV_BIN)/pytest --cov=./ --cov-report=term-missing

coverage-html:
	pytest --cov=./ --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

coverage-xml:
	pytest --cov=./ --cov-report=xml
	@echo "Coverage report generated in coverage.xml"


clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

reset-db:
	rm -f database.db
	python3 seed.py
