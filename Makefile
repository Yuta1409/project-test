# TODO: Créez les cibles suivantes :
# - install : installer les dépendances
# - test : lancer les tests
# - test-unit : seulement les tests unitaires
# - test-integration : seulement les tests d'intégration
# - coverage : couverture avec rapport HTML
# - clean : nettoyer les fichiers temporaires
# - lint : vérification syntaxique
# - all : séquence complète
.PHONY: install test test-unit test-integration coverage clean lint all

install:
    pip install -r requirements.txt

test:
    pytest

test-unit:
    pytest -m unit

test-integration:
    pytest -m integration

coverage:
    pytest --cov=src/task_manager --cov-report=html --cov-report=term-missing

clean:
    rm -rf .pytest_cache __pycache__ */__pycache__ htmlcov .coverage

lint:
    python -m py_compile src/task_manager/*.py

all: clean install lint test coverage