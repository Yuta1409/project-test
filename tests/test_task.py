import pytest
from uuid import uuid4
from datetime import datetime
from src.task_manager.task import Task, Priority, Status

class TestTaskCreation:
    """Test de création de tâche."""

    def test_create_task_minimal(self):
        """Test de création d'une tâche avec les paramètres minimaux."""
        task = Task(title="Tâche minimale")
        assert task.title == "Tâche minimale"
        assert task.description == ""
        assert task.priority == Priority.MEDIUM
        assert isinstance(task.created_at, datetime)
        assert task.status == Status.TODO
        assert task.project_id is None

    def test_create_task_complete(self):
        """Test de création d'une tâche avec tous les paramètres."""
        task = Task(
            title="Tâche complète",
            description="Ceci est une tâche complète.",
            priority=Priority.HIGH
        )
        assert task.title == "Tâche complète"
        assert task.description == "Ceci est une tâche complète."
        assert task.priority == Priority.HIGH
        assert isinstance(task.created_at, datetime)
        assert task.status == Status.TODO
        assert task.project_id is None
    
    def test_create_task_empty_title_raises_error(self):
        """Test titre vide lève une erreur"""
        # TODO: Utilisez pytest.raises pour tester l'exception
        with pytest.raises(ValueError, match="Le titre de la tâche ne peut pas être vide."):
            Task(title="")
    
    def test_create_task_invalid_priority_raises_error(self):
        """Test priorité invalide lève une erreur"""
        # TODO: Testez avec un mauvais type de priorité
        with pytest.raises(ValueError, match="La priorité doit être une instance de Priority."):
            Task(title="Tâche invalide", priority="INVALID_PRIORITY")

class TestTaskOperations:
    """Tests des opérations sur les tâches"""

    def setup_method(self):
        """Fixture : tâche de test"""
        # TODO: Créez self.task pour les tests
        self.task = Task(title="Tâche de test", description="Description de la tâche", priority=Priority.MEDIUM)

    def test_mark_completed_changes_status(self):
        """Test marquage comme terminée"""
        # TODO: Marquez la tâche comme terminée
        # TODO: Vérifiez le changement de statut
        # TODO: Vérifiez que completed_at est défini
        self.task.status = Status.IN_PROGRESS
        self.task.mark_completed()
        assert self.task.status == Status.DONE
        assert hasattr(self.task, 'completed_at')

    def test_update_priority_valid(self):
        """Test mise à jour priorité valide"""
        # TODO: Changez la priorité
        # TODO: Vérifiez le changement
        new_priority = Priority.LOW
        self.task.update_priority(new_priority)
        assert self.task.priority == new_priority

    def test_assign_to_project(self):
        """Test assignation à un projet"""
        # TODO: Assignez à un projet
        # TODO: Vérifiez l'assignation
        project_id = "12345"
        self.task.assign_to_project(project_id)
        assert self.task.project_id == project_id

class TestTaskSerialization:
    """Tests de sérialisation JSON"""

    def setup_method(self):
        # TODO: Créez une tâche complexe avec tous les attributs
        self.task = Task(
            title="Tâche complexe",
            description="Description de la tâche complexe",
            priority=Priority.HIGH
        )
        self.task.status = Status.IN_PROGRESS
        self.task.project_id = "12345"
        self.task.mark_completed()  # Pour tester completed_at
        self.task.completed_at = datetime.now()

    def test_to_dict_contains_all_fields(self):
        """Test conversion en dictionnaire"""
        # TODO: Convertissez en dict
        # TODO: Vérifiez que tous les champs sont présents
        # TODO: Vérifiez que les types sont sérialisables (str pour Enum/datetime)
        task_dict = self.task.to_dict()
        assert isinstance(task_dict, dict)
        assert "id" in task_dict
        assert "title" in task_dict
        assert "description" in task_dict
        assert "priority" in task_dict
        assert "created_at" in task_dict
        assert "status" in task_dict
        assert "project_id" in task_dict
        assert "completed_at" in task_dict
        assert isinstance(task_dict["priority"], str)
        assert isinstance(task_dict["created_at"], str)

    def test_from_dict_recreates_task(self):
        """Test recréation depuis dictionnaire"""
        # TODO: Convertissez en dict puis recréez
        # TODO: Vérifiez que les deux tâches sont équivalentes
        task_dict = self.task.to_dict()
        recreated_task = Task.from_dict(task_dict)
        assert recreated_task.title == self.task.title
        assert recreated_task.description == self.task.description
        assert recreated_task.priority == self.task.priority
        assert recreated_task.created_at == self.task.created_at
        assert recreated_task.status == self.task.status
        assert recreated_task.project_id == self.task.project_id
        assert hasattr(recreated_task, 'completed_at') 
        assert recreated_task.completed_at == self.task.completed_at