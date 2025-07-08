#!/usr/bin/env python3
"""
Démonstration du module TaskManager
"""
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status
from src.task_manager.services import EmailService

def main():
    print("=== Démonstration TaskManager ===\n")
    
    # TODO: Créez un gestionnaire
    manager = TaskManager("tasks.json")
    print("Gestionnaire de tâches créé.\n")

    # TODO: Ajoutez plusieurs tâches avec différentes priorités
    task1_id = manager.add_task("Tâche 1", "Description de la tâche 1", Priority.HIGH, Status.TODO)
    task2_id = manager.add_task("Tâche 2", "Description de la tâche 2", Priority.MEDIUM, Status.IN_PROGRESS)
    task3_id = manager.add_task("Tâche 3", "Description de la tâche 3", Priority.LOW, Status.DONE)
    print(f"Tâches ajoutées : {task1_id}, {task2_id}, {task3_id}\n")

    # TODO: Marquez certaines comme terminées
    task1 = manager.get_task(task1_id)
    if task1:
        task1.status = Status.IN_PROGRESS  # Ajouté : passer en cours
        task1.mark_completed()
        print(f"Tâche {task1_id} marquée comme terminée.\n")
        
    # TODO: Affichez les statistiques
    completed_tasks = sum(1 for t in manager.tasks if t.status == Status.DONE)
    print(f"Nombre de tâches terminées : {completed_tasks}\n")
    # TODO: Sauvegardez dans un fichier
    manager.save_to_file()
    print("Tâches sauvegardées dans 'tasks.json'.\n")
    # TODO: Rechargez et vérifiez
    manager.load_from_file()
    print("Tâches rechargées depuis 'tasks.json'.\n")

    print("Démo terminée avec succès !")

if __name__ == "__main__":
    main()