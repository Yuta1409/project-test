import json 
from typing import List, Optional
from .task import Task, Priority, Status

class TaskManager:
    """Gestionnaire principal des tâches."""
    
    def __init__(self, storage_file = "tasks.json"):
        # TODO: Initialisez une liste des tâches et le fichier de stockage
        self.tasks: List[Task] = []
        self.storage_file = storage_file

  
    def add_task(self, title, description="", priority=Priority.MEDIUM, status=Status.TODO):
        # TODO: Créez et ajoutez une nouvelle tâche
        # TODO: Retournez l'ID de la tâche créée
        new_task = Task(title, description, priority, status)
        self.tasks.append(new_task)
        return new_task.id

    def get_task(self, task_id) -> Optional[Task]:
        # TODO: Trouvez une tâche par son ID
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        # TODO: Filtrez les tâches par statut
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        # TODO: Filtrez les tâches par priorité
        return [task for task in self.tasks if task.priority == priority]

    def delete_task(self, task_id) -> bool:
        # TODO: Supprimez une tâche
        # TODO: Retournez True si trouvée et supprimée, False sinon
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False

    def save_to_file(self, filename=None):
        # TODO: Sauvegardez toutes les tâches en JSON
        # TODO: Gérez les erreurs d'écriture
        if filename is None:
            filename = self.storage_file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des tâches : {e}")

    def load_from_file(self, filename=None):
        # TODO: Chargez les tâches depuis JSON
        # TODO: Gérez le cas du fichier inexistant
        if filename is None:
            filename = self.storage_file
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(task) for task in tasks_data]
        except FileNotFoundError:
            print(f"Fichier {filename} non trouvé. Aucune tâche chargée.")
        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON dans {filename} : {e}")
            self.tasks = []

    def get_statistics(self):
        # TODO: Retournez un dictionnaire avec :
        # - total_tasks
        # - completed_tasks
        # - tasks_by_priority (dict)
        # - tasks_by_status (dict)
        total_tasks = len(self.tasks)
        completed_tasks = len(self.get_tasks_by_status(Status.DONE))
        tasks_by_priority = {priority: len(self.get_tasks_by_priority(priority)) for priority in Priority}
        tasks_by_status = {status: len(self.get_tasks_by_status(status)) for status in Status}

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "tasks_by_priority": tasks_by_priority,
            "tasks_by_status": tasks_by_status
        }