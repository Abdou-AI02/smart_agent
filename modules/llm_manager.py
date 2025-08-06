import ollama
from config import OLLAMA_MODEL, OLLAMA_HOST

class LLMManager:
    def __init__(self):
        self.client = ollama.Client(host=OLLAMA_HOST)

    def generate_response(self, prompt, history=[]):
        """
        Generates a response from the local LLM.
        Args:
            prompt (str): The user's prompt.
            history (list): List of dictionaries, each with 'role' and 'content' for conversation context.
        Returns:
            str: The LLM's response.
        """
        messages = []
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat(model=OLLAMA_MODEL, messages=messages, stream=False)
            return response['message']['content']
        except ollama.ResponseError as e:
            return f"Error connecting to Ollama or model not found: {e}. Please ensure Ollama server is running and '{OLLAMA_MODEL}' is downloaded."
        except Exception as e:
            return f"An unexpected error occurred with LLM: {e}"