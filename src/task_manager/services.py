import smtplib, csv
from datetime import datetime
from src.task_manager.task import Task, Status, Priority

class EmailService:
    """Service pour envoyer des emails."""
    # TODO: Stockez la configuration SMTP
    def __init__(self, smtp_server="smtp@gmail.com", port=587, username="test", password="test"):
        self.smtp_server = smtp_server
        self.smtp_port = port
        self.username = username
        self.password = password

    def send_task_reminder(self, email, task_title, due_date):
        # TODO: Simulez l'envoi d'un email de rappel
        # TODO: Levez une exception si email invalide
        # TODO: Retournez True si succès
        if not self.is_valid_email(email):
            raise ValueError("Adresse email invalide")
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                message = f"Subject: Rappel de tâche\n\nVous avez une tâche '{task_title}' à faire avant le {due_date}."
                server.sendmail(self.username, email, message)
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")
            return False

    def is_valid_email(self, email):
        """Valide simplement le format de l'email."""
        import re
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def send_completion_notification(self, email, task_title):
        # TODO: Simulez l'envoi d'un email de confirmation
        email_confirmation = f"Subject: Confirmation de tâche terminée\n\nLa tâche '{task_title}' a été marquée comme terminée."
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, email, email_confirmation)
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")
            return False

class ReportService:
    """Service de génération de rapports"""
    def generate_daily_report(self, tasks, date=None):
        from datetime import datetime
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.status == Status.DONE)
        pending_tasks = total_tasks - completed_tasks
        return {
            "date": date,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
        }
        return report

    def export_tasks_csv(self, tasks, filename):
        # TODO: Exportez les tâches en CSV
        # TODO: Gérez les erreurs d'écriture
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'title', 'description', 'priority', 'status', 'created_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for task in tasks:
                    writer.writerow({
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'priority': task.priority.name,
                        'status': task.status.value,
                        'created_at': task.created_at.isoformat()
                    })
        except IOError as e:
            print(f"Erreur lors de l'écriture du fichier CSV : {e}")
            return False
        return True
