import os
import shutil
from multiprocessing import Pool
from collections import defaultdict
from tqdm import tqdm

def get_file_extension(file_path):
    return os.path.splitext(file_path)[1].lower()

def copy_files_and_directories(root, files, target_directory):
    for file in files:
        source_path = os.path.join(root, file)
        extension = get_file_extension(file)
        if extension:
            target_dir = os.path.join(target_directory, extension.lstrip('.'))
            if not os.path.exists(target_dir):
                try:
                    os.makedirs(target_dir)
                except OSError as e:
                    print(f"Error creating directory {target_dir}: {str(e)}")
                    continue
            target_path = os.path.join(target_dir, file)
            base, ext = os.path.splitext(target_path)
            i = 1
            while os.path.exists(target_path):
                target_path = f"{base}_{i}{ext}"
                i += 1
            try:
                shutil.copy2(source_path, target_path)
            except IOError as e:
                print(f"Error copying file {source_path}: {str(e)}")
                continue

    for dir in os.listdir(root):
        source_path = os.path.join(root, dir)
        if os.path.isdir(source_path):
            target_dir = os.path.join(target_directory, dir)
            base, ext = os.path.splitext(target_dir)
            i = 1
            while os.path.exists(target_dir):
                target_dir = f"{base}_{i}{ext}"
                i += 1
            try:
                shutil.copytree(source_path, target_dir)
            except OSError as e:
                print(f"Error copying directory {source_path}: {str(e)}")
                continue

def copy_files_by_extension(directory, target_directory):
    for root, dirs, files in tqdm(os.walk(directory), desc="Copying files", unit="files"):
        extensions = set()
        for file in files:
            extension = get_file_extension(file)
            if extension:
                extensions.add(extension)
        for extension in extensions:
            target_dir = os.path.join(target_directory, extension.lstrip('.'))
            if not os.path.exists(target_dir):
                try:
                    os.makedirs(target_dir)
                except OSError as e:
                    print(f"Error creating directory {target_dir}: {str(e)}")
                    continue
            files_with_extension = [file for file in files if get_file_extension(file) == extension]
            copy_files_and_directories(root, files_with_extension, target_directory)

def get_distinct_file_extensions(directory):
    extensions = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            extension = get_file_extension(file)
            if extension:
                extensions.add(extension)
    return extensions

if __name__ == '__main__':
    directory = input("Enter the directory path: ")
    target_directory = input("Enter the target directory path: ")

    extensions = get_distinct_file_extensions(directory)

    for extension in extensions:
        target_dir = os.path.join(target_directory, extension.lstrip('.'))
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except OSError as e:
                print(f"Error creating directory {target_dir}: {str(e)}")
                continue

    copy_files_by_extension(directory, target_directory)
