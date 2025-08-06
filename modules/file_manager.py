import os
import shutil
import zipfile
from config import DEFAULT_SCAN_PATH
from utils.helper_functions import find_files

class FileManager:
    def find_file(self, filename, search_path=None):
        """Finds a file on the local machine."""
        path_to_search = search_path if search_path else DEFAULT_SCAN_PATH
        if not os.path.isdir(path_to_search):
            return "Invalid search path provided."
        
        matches = find_files(filename, path_to_search)
        
        if matches:
            return f"Found the following files:\n" + "\n".join(matches)
        else:
            return f"File '{filename}' not found in '{path_to_search}'."

    def organize_files(self, directory=None):
        """Organizes files in a directory into sub-folders based on type."""
        path_to_organize = directory if directory else DEFAULT_SCAN_PATH
        if not os.path.isdir(path_to_organize):
            return "Invalid directory path provided."
        
        file_types = {
            'Images': ('.jpg', '.jpeg', '.png', '.gif'),
            'Documents': ('.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx'),
            'Videos': ('.mp4', '.mov', '.avi'),
            'Code': ('.py', '.js', '.html', '.css'),
            'Others': ()
        }
        
        for root, _, files in os.walk(path_to_organize):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isdir(file_path):
                    continue

                moved = False
                for folder, extensions in file_types.items():
                    if file.lower().endswith(extensions):
                        dest_folder = os.path.join(path_to_organize, folder)
                        os.makedirs(dest_folder, exist_ok=True)
                        try:
                            shutil.move(file_path, dest_folder)
                            moved = True
                            break
                        except shutil.Error as e:
                            # File with same name exists, add a unique suffix
                            new_file_path = os.path.join(dest_folder, file)
                            base, ext = os.path.splitext(new_file_path)
                            counter = 1
                            while os.path.exists(f"{base}_{counter}{ext}"):
                                counter += 1
                            shutil.move(file_path, f"{base}_{counter}{ext}")
                            moved = True
                            break
                
                if not moved:
                    others_folder = os.path.join(path_to_organize, 'Others')
                    os.makedirs(others_folder, exist_ok=True)
                    try:
                        shutil.move(file_path, others_folder)
                    except shutil.Error:
                        new_file_path = os.path.join(others_folder, file)
                        base, ext = os.path.splitext(new_file_path)
                        counter = 1
                        while os.path.exists(f"{base}_{counter}{ext}"):
                            counter += 1
                        shutil.move(file_path, f"{base}_{counter}{ext}")
        
        return f"Files in '{path_to_organize}' have been organized."

    def compress_folder(self, folder_path, output_name='compressed_archive'):
        """Compresses a folder into a zip file."""
        if not os.path.isdir(folder_path):
            return "Invalid folder path provided."
        
        try:
            output_path = shutil.make_archive(output_name, 'zip', folder_path)
            return f"Folder '{folder_path}' compressed successfully to '{output_path}'."
        except Exception as e:
            return f"Error compressing folder: {e}"

    def decompress_file(self, file_path, output_dir=None):
        """Decompresses a zip file."""
        if not os.path.isfile(file_path) or not file_path.endswith('.zip'):
            return "Invalid file path or not a zip file."
        
        output_directory = output_dir if output_dir else os.path.dirname(file_path)
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(output_directory)
            return f"File '{file_path}' decompressed successfully to '{output_directory}'."
        except Exception as e:
            return f"Error decompressing file: {e}"