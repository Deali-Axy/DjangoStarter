import os
import shutil

current_path = os.path.abspath('.')

exclude_path = [
    os.path.join(current_path, '.idea'),
    os.path.join(current_path, '.git'),
    os.path.join(current_path, 'venv'),
]


def is_exclude(path: str):
    for item in exclude_path:
        if path.startswith(item):
            return True

    return False


def run():
    for root, dirs, files in os.walk(current_path):
        root: str

        if is_exclude(root):
            continue

        for item in dirs:
            dir_path = os.path.join(root, item)

            if item == '__pycache__':
                print(f'delete: {dir_path}')
                shutil.rmtree(dir_path)


if __name__ == '__main__':
    run()
