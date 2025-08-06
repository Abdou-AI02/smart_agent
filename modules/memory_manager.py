import os
from config import MEMORY_FILE, MAX_MEMORY_SIZE
from utils.helper_functions import load_json, save_json

class MemoryManager:
    def __init__(self):
        self.memory = self._load_memory()

    def _load_memory(self):
        """Loads conversation memory from file."""
        return load_json(MEMORY_FILE, default_value={"conversations": []})

    def _save_memory(self):
        """Saves current conversation memory to file."""
        save_json(MEMORY_FILE, self.memory)

    def add_message(self, role, content):
        """Adds a message to the conversation memory."""
        self.memory["conversations"].append({"role": role, "content": content})
        if len(self.memory["conversations"]) > MAX_MEMORY_SIZE * 2:
            self.memory["conversations"] = self.memory["conversations"][-MAX_MEMORY_SIZE*2:]
        self._save_memory()

    def get_history(self):
        """Returns the current conversation history for the LLM."""
        return self.memory["conversations"]

    def clear_memory(self):
        """Clears all conversation memory."""
        self.memory = {"conversations": []}
        self._save_memory()
        print("Memory cleared.")