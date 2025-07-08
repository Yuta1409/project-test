from datetime import datetime
from uuid import uuid4
from enum import Enum

class Priority(Enum):
    # TODO: Définissez les priorités (LOW, MEDIUM, HIGH, URGENT)
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    URGENT = 'URGENT'

class Status(Enum):
    # TODO: Définissez les statuts (TODO, IN_PROGRESS, DONE, CANCELLED)
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    CANCELLED = 'CANCELLED'

class Task:
    """Une tâche avec toutes ses propriétés."""

    def __init__(self, title, description = "", priority=Priority.MEDIUM, status=Status.TODO):
        # TODO: Validez les paramètres
        # - title non vide
        # - priority est bien une Priority
        if not title:
            raise ValueError("Le titre de la tâche ne peut pas être vide.")
        if not isinstance(priority, Priority):
            raise ValueError("La priorité doit être une instance de Priority.")
        if not isinstance(status, Status):
            raise ValueError("Le statut doit être une instance de Status.")

        # TODO: Initialisez les attributs
        # - id unique (utilisez time.time() ou uuid)
        # - created_at avec datetime.now()
        # - status à TODO par défaut
        # - project_id à None
        self.id = uuid4()
        self.title = title
        self.description = description
        self.priority = priority
        self.created_at = datetime.now()
        self.status = status
        self.project_id = None
    
    def mark_completed(self):
        # TODO: Changez le statut à DONE
        if self.status != Status.IN_PROGRESS:
            raise ValueError("La tâche doit être en cours pour être marquée comme terminée.")
        self.status = Status.DONE
        # TODO: Ajoutez completed_at avec datetime.now()
        self.completed_at = datetime.now()

    def update_priority(self, new_priority):
        # TODO: Validez et mettez à jour la priorité
        if not isinstance(new_priority, Priority):
            raise ValueError("La nouvelle priorité doit être une instance de Priority.")
        self.priority = new_priority

    def assign_to_project(self, project_id):
        # TODO: Assignez la tâche à un projet
        if not project_id:
            raise ValueError("L'ID du projet ne peut pas être vide.")
        self.project_id = project_id

    def to_dict(self):
        # TODO: Retournez un dictionnaire pour la sérialisation JSON
        # Gérez la conversion des Enum et datetime
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.name,  # Convertit l'Enum en string
            "created_at": self.created_at.isoformat(),  # Convertit datetime en string ISO
            "status": self.status.value,  # Convertit l'Enum en string
            "project_id": self.project_id,
        }
        if hasattr(self, 'completed_at'):
            data['completed_at'] = self.completed_at.isoformat()
        return data
        
    @classmethod
    def from_dict(cls, data):
        # TODO: Créez une Task depuis un dictionnaire
        # Gérez la conversion des string vers Enum et datetime
        if not isinstance(data, dict):
            raise ValueError("Les données doivent être un dictionnaire.")
        title = data.get("title")
        description = data.get("description", "")
        priority = Priority[data.get("priority", "MEDIUM")]
        task = cls(title, description, priority)
        task.id = data.get("id", str(uuid4()))
        task.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        task.status = Status(data.get("status", "TODO"))
        task.project_id = data.get("project_id")
        if 'completed_at' in data:
            task.completed_at = datetime.fromisoformat(data['completed_at'])
        return task

