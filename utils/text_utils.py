def translate_text(text, target_lang="ar"):
    """
    Dummy function for translation. For this project, we'll assume the LLM
    handles basic multi-language understanding.
    """
    return text

def clean_text(text):
    """Cleans text by removing extra whitespace and special characters."""
    if not isinstance(text, str):
        return ""
    text = ' '.join(text.split())
    return text