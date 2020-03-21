import os
import sys
import pkg_resources
from typing import List


PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))

# folder that holds all
# the data of the package
PACKAGE_DATA_PATH = None
if sys.platform == 'linux':
    PACKAGE_DATA_PATH = os.path.join(os.getenv('HOME'), '.git-repo')
elif sys.platform == 'win32':
    PACKAGE_DATA_PATH = os.path.join(os.getenv('LOCALAPPDATA'), '.git-repo')

LOG_FILE_PATH = os.path.join(PACKAGE_DATA_PATH, 'git-repo.log')

GITIGNORE_STORE_PATH = os.path.join(PACKAGE_DATA_PATH, 'gitignore')

CONFIG_FILE_PATH = os.path.join(PACKAGE_DATA_PATH, 'git-repo.config')
