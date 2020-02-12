import os
import sys
from typing import List
from . import config as cfg


def read_gitignore_template(name: str) -> List[str]:
    files = os.listdir(cfg.GITIGNORE_STORE_PATH)
    for file in files:
        gitignore_path = os.path.join(cfg.GITIGNORE_STORE_PATH, file)
        gitignore_name, ext = os.path.splitext(gitignore_path)
        if ext != '.gitignore':
            continue
        if gitignore_name == name:
            with open(gitignore_path, 'r') as gitignore_file:
                gitignore_template = gitignore_file.readlines()
            return gitignore_template
    return None
