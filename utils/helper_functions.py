import json
import os
import hashlib
import shutil

def load_json(filepath, default_value={}):
    """Loads JSON data from a file."""
    if not os.path.exists(filepath):
        return default_value
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default_value

def save_json(filepath, data):
    """Saves JSON data to a file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_file_content(filepath):
    """Reads the content of a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error reading file: {e}"

def hash_file(filepath):
    """Calculates the SHA256 hash of a file."""
    try:
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as afile:
            buf = afile.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(65536)
        return hasher.hexdigest()
    except Exception:
        return None

def find_files(filename, search_path):
    """Searches for a file by name in a given directory and its subdirectories."""
    matches = []
    for root, _, files in os.walk(search_path):
        if filename in files:
            matches.append(os.path.join(root, filename))
    return matches