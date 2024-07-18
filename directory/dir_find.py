import os

# Get directory and search for file
def find_file(file_name, search_path):
    for root, files in os.walk(search_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            return file_path
    return None