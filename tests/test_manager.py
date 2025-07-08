import pytest
from unittest.mock import patch, mock_open
import json
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status

import pytest

@pytest.mark.unit
class TestTaskManagerBasics:
    """Tests basiques du gestionnaire"""
    def setup_method(self):
        """Fixture : gestionnaire de test"""
        # TODO: Créez self.manager avec un fichier temporaire
        self.manager = TaskManager()
        self.manager.storage_file = "test_tasks.json"

    def test_add_task_returns_id(self):
        """Test ajout tâche retourne un ID"""
        # TODO: Ajoutez une tâche
        # TODO: Vérifiez que l'ID est retourné
        # TODO: Vérifiez que la tâche est dans la liste
        task_id = self.manager.add_task("Test Task", "Description", Priority.HIGH)
        print(f"Task ID: {task_id}")
        task = self.manager.get_task(task_id)
        assert task is not None 
        assert task.title == "Test Task"
        assert task.description == "Description"

    def test_get_task_existing(self):
        """Test récupération tâche existante"""
        # TODO: Ajoutez une tâche
        # TODO: Récupérez-la par ID
        # TODO: Vérifiez les propriétés
        task_id = self.manager.add_task("Test Task", "Description", Priority.HIGH)
        task = self.manager.get_task(task_id)
        assert task is not None
        assert task.title == "Test Task"
        assert task.description == "Description"

    def test_get_task_nonexistent_returns_none(self):
        """Test récupération tâche inexistante"""
        # TODO: Cherchez une tâche avec un ID bidon
        # TODO: Vérifiez que None est retourné
        task = self.manager.get_task("nonexistent-id")
        assert task is None

@pytest.mark.unit
class TestTaskManagerFiltering:
    """Tests de filtrage des tâches"""
    def setup_method(self):
        """Fixture : gestionnaire avec plusieurs tâches"""
        self.manager = TaskManager("test_tasks.json")
        # TODO: Ajoutez 3-4 tâches avec différents statuts/priorités
        self.manager.add_task("Task 1", "Description 1", Priority.HIGH, Status.TODO)
        self.manager.add_task("Task 2", "Description 2", Priority.MEDIUM, Status.IN_PROGRESS)
        self.manager.add_task("Task 3", "Description 3", Priority.LOW, Status.DONE)
        self.manager.add_task("Task 4", "Description 4", Priority.HIGH, Status.TODO)

    def test_get_task_by_status(self):
        """Test filtrage par statut"""
        # TODO: Filtrez les tâches TODO
        # TODO: Vérifiez le nombre et les propriétés
        tasks = self.manager.get_tasks_by_status(Status.TODO)
        assert len(tasks) == 2  
        assert all(task.status == Status.TODO for task in tasks if task.title == "Task 1" or task.title == "Task 4")
        assert all(task.status == Status.IN_PROGRESS for task in tasks if task.title == "Task 2")
        assert all(task.status == Status.DONE for task in tasks if task.title == "Task 3")
        
    def test_get_task_by_priority(self):
        """Test filtrage par priorité"""
        # TODO: Filtrez les tâches HIGH proirity
        # TODO: Vérifiez le résultat
        tasks = self.manager.get_tasks_by_priority(Priority.HIGH)
        assert len(tasks) == 2
        assert all(task.priority == Priority.HIGH for task in tasks if task.title == "Task 1" or task.title == "Task 4")
        assert all(task.priority == Priority.MEDIUM for task in tasks if task.title == "Task 2")
        assert all(task.priority == Priority.LOW for task in tasks if task.title == "Task 3")

@pytest.mark.unit
class TestTaskManagerPersistence:
    """Tests de sauvegarde/chargement avec mocks"""
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")
        # TODO: Ajoutez quelques tâches de test
        self.manager.add_task("Task 1", "Description 1", Priority.HIGH, status=Status.TODO)
        
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_success(self, mock_json_dump, mock_file):
        """Test sauvegarde réussie"""
        # TODO: Appelez save_to_file()
        # TODO: Vérifiez que le fichier est ouvert en écriture
        # TODO: Vérifiez que json.dump est appelé
        self.manager.save_to_file()
        mock_file.assert_called_once_with("test_tasks.json", 'w', encoding='utf-8')
        mock_json_dump.assert_called_once()
        assert mock_json_dump.call_args[0][0] == [task.to_dict() for task in self.manager.tasks]
        
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('json.load')
    def test_load_from_file_success(self, mock_json_load, mock_file):
        """Test chargement réussi"""
        # TODO: Configurez mock_json_load pour retourner des données de test
        # TODO: Appelez load_from_file()
        # TODO: Vérifiez que les tâches sont chargées
        mock_json_load.return_value = [
            {"title": "Task 1", "description": "Description 1", "priority": Priority.HIGH.name, "status": Status.TODO.name}
        ]
        self.manager.load_from_file()
        mock_file.assert_called_once_with("test_tasks.json", 'r', encoding='utf-8')
        assert len(self.manager.tasks) == 1
        assert self.manager.tasks[0].title == "Task 1"
        assert self.manager.tasks[0].description == "Description 1"
        assert self.manager.tasks[0].priority == Priority.HIGH
        assert self.manager.tasks[0].status == Status.TODO

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_from_nonexistent_file(self, mock_file):
        """Test chargement fichier inexistant"""
        # TODO: Appelez load_from_file()
        # TODO: Vérifiez que ça ne plante pas
        # TODO: Vérifiez que la liste reste vide
        manager = TaskManager("test_tasks.json")
        manager.load_from_file()
        mock_file.assert_called_once_with("test_tasks.json", 'r', encoding='utf-8')
        assert len(manager.tasks) == 0  # La liste des tâches doit rester vide
        