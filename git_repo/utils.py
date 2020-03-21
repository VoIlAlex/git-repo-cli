import os
import sys
from typing import List, Any
from . import config as cfg
import shutil
import logging
from colored import fg, bg, attr


class BeautifulFormatter(logging.Formatter):

    warning_color = fg('yellow')
    error_color = fg('red')
    critical_color = fg('red')
    info_color = fg('green')
    debug_color = fg('grey_93')
    default_color = fg('white')
    reset_color = attr('reset')

    def __init__(self):
        logging.Formatter.__init__(self,
                                   fmt='[%(asctime)s] %(levelname)s: %(message)s',
                                   datefmt='%m/%d/%Y %I:%M:%S %p'
                                   )

    def format(self, record):
        def set_color(color):
            self._fmt = '[%(asctime)s] ' + color + '%(levelname)s' + \
                self.reset_color + ': %(message)s'
        original_format = self._fmt

        if record.levelno == logging.DEBUG:
            set_color(self.debug_color)
        elif record.levelno == logging.INFO:
            set_color(self.info_color)
        elif record.levelno == logging.WARNING:
            set_color(self.warning_color)
        elif record.levelno == logging.ERROR:
            set_color(self.error_color)
        elif record.levelno == logging.CRITICAL:
            set_color(self.critical_color)

        record = logging.Formatter.format(self, record)
        self._fmt = original_format
        return record

    @staticmethod
    def create_formatter(color):
        return logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s',
                                 datefmt='%m/%d/%Y %I:%M:%S %p')


class BeautifulLogger:
    logger = None

    def __new__(cls):
        if BeautifulLogger.logger is None:
            BeautifulLogger.logger = logging.getLogger(__name__)
            BeautifulLogger.logger.handlers.clear()
            BeautifulLogger.logger.setLevel(logging.DEBUG)

            # logging to file
            logging_handler = logging.FileHandler(cfg.LOG_FILE_PATH)
            logging_handler.setFormatter(
                BeautifulFormatter.create_formatter(BeautifulFormatter.default_color))
            logging_handler.setLevel(logging.DEBUG)
            BeautifulLogger.logger.addHandler(logging_handler)

            # logging to console
            logging_console_handler = logging.StreamHandler()
            logging_console_handler.setFormatter(BeautifulFormatter())
            logging_console_handler.setLevel(logging.DEBUG)
            BeautifulLogger.logger.addHandler(logging_console_handler)
        return BeautifulLogger.logger


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


def list_gitignore_choices():
    files = os.listdir(cfg.GITIGNORE_STORE_PATH)
    gitignore_files = [f for f in files if os.path.splitext(f)[
        0] == '.gitignore']
    return gitignore_files


def save_gitignore_template(file: str) -> None:
    file_without_ext, file_ext = os.path.splitext(file)
    if file_ext != '.gitignore':
        BeautifulLogger().error("Template should have .gitignore extension.")
        exit(1)

    folder_path, file_name = os.path.split(file_without_ext)
    template_file_path = os.path.join(
        cfg.GITIGNORE_STORE_PATH, file_name, '.gitignore')
    shutil.copyfile(file, template_file_path)


def get_config(key: str = None):
    with open(cfg.CONFIG_FILE_PATH, 'r') as config_file:
        if key is None:
            return config_file.readlines()
        else:
            for line in config_file:
                config_key, config_value = line.split('=')
                if config_key == key:
                    return config_value


def set_config(key: str, value: Any):
    with open(cfg.CONFIG_FILE_PATH, 'r') as config_file:
        config_content = config_file.readlines()

    for i, line in enumerate(config_content):
        config_key, config_value = line.split('=')
        if config_key == key:
            new_line = '='.join([config_key, value])
            config_content[i] = new_line
            break
    else:
        config_content.append('='.join([key, value]))

    with open(cfg.CONFIG_FILE_PATH, 'w') as config_file:
        config_file.truncate()
        config_file.writelines(config_content)
