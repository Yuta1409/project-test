import pytest

import pytest
from unittest.mock import patch, Mock, mock_open
from src.task_manager.services import EmailService, ReportService
from src.task_manager.task import Task, Priority, Status


@pytest.mark.unit
class TestEmailService:
    """Tests du service email avec mocks"""
    def setup_method(self):
        self.email_service = EmailService()
        self.email_service.smtp_server = "smtp.test.com"
        self.email_service.smtp_port = 587
        self.email_service.username = "TestUser"
        self.email_service.password = "TestPassword"

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_task_reminder_success(self, mock_smtp):
        """Test envoi rappel réussi"""
        mock_smtp_instance = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

        result = self.email_service.send_task_reminder(
            email="yan.roger@ynov.com",
            task_title="Test Task",
            due_date="2023-10-01"
        )
        mock_smtp_instance.sendmail.assert_called_once_with(
            self.email_service.username,
            "yan.roger@ynov.com",
            "Subject: Rappel de tâche\n\nVous avez une tâche 'Test Task' à faire avant le 2023-10-01."
        )
        assert result is True

    def test_send_task_reminder_invalid_email(self):
        """Test envoi avec email invalide"""
        with pytest.raises(ValueError, match="Adresse email invalide"):
            self.email_service.send_task_reminder(
                email="invalid-email",
                task_title="Test Task",
                due_date="2023-10-01"
            )


@pytest.mark.unit
class TestReportService:
    """Tests du service de rapports"""
    def setup_method(self):
        self.report_service = ReportService()
        self.tasks = [
            Task(title="Task 1", description="Description 1", priority=Priority.HIGH, status=Status.TODO),
            Task(title="Task 2", description="Description 2", priority=Priority.MEDIUM, status=Status.IN_PROGRESS),
            Task(title="Task 3", description="Description 3", priority=Priority.LOW, status=Status.DONE),
        ]

    @patch('src.task_manager.services.datetime')
    def test_generate_daily_report_fixed_date(self, mock_datetime):
        """Test génération rapport avec date fixe"""
        mock_datetime.now.return_value.date.return_value = "2023-10-01"
        report = self.report_service.generate_daily_report(self.tasks, date="2023-10-01")
        assert report['date'] == "2023-10-01"
        assert report['total_tasks'] == 3
        assert report['completed_tasks'] == 1
        assert report['pending_tasks'] == 2

    @patch('builtins.open', new_callable=mock_open)
    def test_export_tasks_csv(self, mock_file):
        """Test export CSV"""
        self.report_service.export_tasks_csv(self.tasks, "test_tasks.csv")
        mock_file.assert_called_once_with("test_tasks.csv", 'w', newline='', encoding='utf-8')
        handle = mock_file()
        handle.write.assert_called()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        assert "id,title,description,priority,status,created_at" in written_data
        assert "Task 1,Description 1,HIGH,TODO" in written_data
        assert "Task 3,Description 3,LOW,DONE" in written_data


# Test d'intégration exemple : export réel CSV (pas de mock)
@pytest.mark.integration
def test_export_tasks_csv_real(tmp_path):
    report_service = ReportService()
    tasks = [
        Task(title="Task 1", description="Description 1", priority=Priority.HIGH, status=Status.TODO),
        Task(title="Task 2", description="Description 2", priority=Priority.MEDIUM, status=Status.IN_PROGRESS),
    ]
    file_path = tmp_path / "tasks.csv"
    report_service.export_tasks_csv(tasks, str(file_path))
    assert file_path.exists()
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
        assert "Task 1" in content
        assert "Task 2" in content
