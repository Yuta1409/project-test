import json 
from typing import List, Optional
from .task import Task, Priority, Status

class TaskManager:
    """Gestionnaire principal des tâches."""
    
    def __init__(self):
        # TODO: Initialisez une liste des tâches et le fichier de stockage
        self.tasks: List[Task] = []
        self.storage_file = "tasks.json"

  