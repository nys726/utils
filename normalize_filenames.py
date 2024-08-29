import os
import unicodedata

def normalize_and_rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            print("@@@@@@@:", filename)
            normalized_name = unicodedata.normalize('NFC', filename)
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, normalized_name)
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f'Renamed: {old_path} -> {new_path}')

directory_path = 'cam1/'
normalize_and_rename_files(directory_path)

