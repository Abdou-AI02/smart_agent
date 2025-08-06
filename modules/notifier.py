from plyer import notification
import platform

class Notifier:
    """A simple class to handle desktop notifications."""

    def __init__(self):
        # Check if platform supports notifications
        self.supported = platform.system() in ['Linux', 'Windows', 'Darwin']

    def send_notification(self, title, message):
        """Sends a desktop notification."""
        if not self.supported:
            print(f"Notification: {title} - {message}")
            return
            
        try:
            notification.notify(
                title=title,
                message=message,
                app_name='Smart Agent',
                timeout=10,
            )
        except Exception as e:
            print(f"Failed to send notification: {e}")