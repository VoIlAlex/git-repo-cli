from distutils.core import setup
from setuptools import find_packages
from setuptools.command.install import install
import pkg_resources
import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path)

import git_repo.config as cfg


class PostInstallCommand(install):
    def run(self):
        # setup package data folder
        package_data_path = cfg.PACKAGE_DATA_PATH
        if not os.path.exists(package_data_path):
            os.makedirs(package_data_path)

        # setup configuration file
        config_file_path = cfg.CONFIG_FILE_PATH
        if not os.path.exists(config_file_path):
            with open(config_file_path, 'w+') as f:
                pass

        # setup logging
        log_file_path = os.path.dirname(cfg.LOG_FILE_PATH)
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w+') as f:
                pass

        # setup gitignore templates
        templates_folder = cfg.GITIGNORE_STORE_PATH
        if not os.path.exists(templates_folder):
            os.makedirs(templates_folder)

        default_gitignore = pkg_resources.resource_filename(
            'git_repo',
            'gitignore/default.gitignore'
        )
        with open(default_gitignore, 'r') as f_in:
            default_gitignore_content = f_in.readlines()
            current_default_gitignore_path = os.path.join(
                templates_folder, 'default.gitignore')
            with open(current_default_gitignore_path, 'w+') as f_out:
                f_out.writelines(default_gitignore_content)

        install.run(self)


setup(
    name='git-repo-cli',         # How you named your package folder (MyLib)
    packages=find_packages('.'),   # Chose the same as "name"
    # Start with a small number and increase it with every change you make
    version='1.0.0',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Utils to easily create/delete/rename repository.',
    author='Ilya Vouk',                   # Type in your name
    author_email='ilya.vouk@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/VoIlAlex/git-repo',
    # I explain this later on
    download_url='https://github.com/VoIlAlex/git-repo/archive/v1.0.0.tar.gz',
    # Keywords that define your package best
    keywords=['VCS', 'Git', 'GitHub', 'utility', 'cli'],
    scripts=['bin/git-repo'],
    install_requires=[            # I get to this in a second
        'PyGithub',
        'GitPython',
        'colored'
    ],
    cmdclass={
        'install': PostInstallCommand
    },
    package_data={
        'git_repo': ['gitignore/default.gitignore']
    },
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which python versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
