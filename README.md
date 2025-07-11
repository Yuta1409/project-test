# Task Manager Project

Ce projet est un gestionnaire de tâches simple écrit en Python. Il permet de créer, gérer, filtrer et sauvegarder des tâches avec différents statuts et priorités.

## Fonctionnalités
- Ajouter, supprimer et rechercher des tâches
- Filtrer les tâches par statut ou priorité
- Sauvegarder et charger les tâches depuis un fichier JSON
- Statistiques sur les tâches

## Installation

1. **Cloner le dépôt**

```bash
git clone <url-du-repo>
cd project-test
```

2. **Créer un environnement virtuel (optionnel mais recommandé)**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

## Utilisation

### Exemple d'utilisation dans un script Python

```python
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status

# Créer un gestionnaire de tâches
tm = TaskManager()

# Ajouter une tâche
task_id = tm.add_task("Ma première tâche", "Description", Priority.HIGH, Status.TODO)

# Sauvegarder les tâches
tm.save_to_file()

# Charger les tâches
tm.load_from_file()

# Afficher les statistiques
stats = tm.get_statistics()
print(stats)
```

### Lancer les tests

```bash
pytest
```

## Structure du projet

- `src/task_manager/` : Code source principal
- `tests/` : Tests unitaires et d'intégration
- `requirements.txt` : Dépendances Python
- `demo.py` : Exemple d'utilisation

## Auteur
- Yan ROGER

---