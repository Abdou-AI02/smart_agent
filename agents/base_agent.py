class BaseAgent:
    def __init__(self, name="BaseAgent"):
        self.name = name
        self.logs = []

    def add_log(self, message):
        """Adds a log message for tracking agent's operations."""
        self.logs.append(message)
        print(f"[{self.name} LOG]: {message}")

    def get_logs(self):
        """Returns all accumulated logs."""
        return "\n".join(self.logs)

    def clear_logs(self):
        """Clears all logs."""
        self.logs = []