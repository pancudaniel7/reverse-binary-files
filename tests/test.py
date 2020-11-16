from pathlib import Path


def change_file_path_name(file_path):
    print(Path(file_path).name)


change_file_path_name('/usr/home/test.txt')
