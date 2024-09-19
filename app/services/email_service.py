class EmailService:
    """
    Mock service for sending email notifications.
    """

    def __init__(self, logger):
        self.logger = logger

    def send_status_change_email(self, to_email: str, task_title: str, old_status: str, new_status: str):
        """
        Sends an email notification to the responsible person when the task status changes.
        """
        # Here would be the real email sending. For now, we are just logging.
        self.logger.info(f"Sending email to {to_email}:")
        self.logger.info(f"Task title: {task_title}")
        self.logger.info(f"Status changed from '{old_status}' to '{new_status}'")
        print(
            f"Mock email sent to {to_email}: Task '{task_title}' status changed from '{old_status}' to '{new_status}'"
        )
