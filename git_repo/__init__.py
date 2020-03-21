"""
    Tools for creating git repository.

    If a repo exists on remote then it
    will be cloned here. Otherwise it will
    be created and uploaded.
"""

import argparse
import os
import sys
from github import Github
import github
import git
import shutil
import logging
from colored import fg, bg, attr
from typing import Iterable

# make root dir visible
# for importing
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
my_code_dir = os.path.dirname(parent_dir)
sys.path.insert(0, my_code_dir)

from . import config as cfg
from . import utils
from .utils import BeautifulFormatter, BeautifulLogger
from .parse_args import parse_args


class GitRepository:
    def __init__(self, name, access_token=None):
        self.path = name
        self.local_name = name.split(os.path.sep)[-1]
        self.remote_name = None
        self.logger = utils.BeautifulLogger()
        if access_token:
            self.github = Github(access_token)

    def create_and_upload(self, gitignore: Iterable = None, readme: Iterable = None):
        if os.path.exists(self.local_name):
            self.logger.error(
                'Local repository with name {} already exists.'.format(self.path))
            return None

        gitignore = gitignore if gitignore is not None else []
        readme = readme if readme is not None else ['# ' + self.local_name]

        # Create local repo
        self.logger.info('Initializing local repository...')
        repo_path = os.path.join(os.getcwd(), self.path)
        if not os.path.exists(repo_path):
            os.mkdir(repo_path)
        local_repo = git.Repo.init(repo_path)

        # Create README for the repo
        self.logger.info('Creating README...')
        with self.__open_in_local_repo('README.md', 'w+') as readme:
            readme.writelines(readme)

        # Create .gitignore
        self.logger.info('Creating .gitignore...')
        with self.__open_in_local_repo('.gitignore', 'w+') as gitignore_file:
            for element in gitignore:
                print(element, file=gitignore_file)

        self.logger.info('Making initial commit...')
        local_repo.git.add('.')
        local_repo.git.commit(m='"Initial commit"')
        if hasattr(self, 'github'):
            user = self.github.get_user()

            # get unique name for github repo
            self.logger.info('Checking the name...')
            self.remote_name = self.local_name
            repos = [repo.name for repo in user.get_repos()]
            while self.remote_name in repos:
                self.logger.error('Repository name is not free.')
                self.remote_name = input('Please, enter a new name for repo: ')

            # Create private remote repo
            self.logger.info('Creating the new repository on remote...')
            github_repo = user.create_repo(self.remote_name)
            github_repo.edit(private=True)

            # Push to remote
            self.logger.info('Pushing the repository to remote...')
            local_repo.git.remote('add', 'origin', github_repo.clone_url)

            # Setup a local tracking branch of a remote branch
            self.logger.info('Setting up upstream to remote master...')
            local_repo.git.push('-u', 'origin', 'master')

        self.logger.info(
            'Repository "{}" has been created.'.format(self.local_name))

    def delete(self):
        self.delete_remote()
        self.delete_local()

    def delete_local(self):
        """Delete the repository on local machine but hold on remote"""
        if os.path.exists(self.local_name):
            self.logger.info('Removing the repository locally...')
            shutil.rmtree(self.local_name)
            self.logger.info(
                'Repository has been successfully deleted locally.')
        else:
            self.logger.error(
                "Cannot remove the repository. It doesn't exist locally.")

    def delete_remote(self):
        """Delete the repository on remote but hold locally."""
        user = self.github.get_user()
        self.logger.info('Trying to delete repository on remote...')
        try:
            if self.remote_name is None:
                user.get_repo(self.local_name).delete()
            else:
                user.get_repo(self.remote_name).delete()
        except github.GithubException:
            self.logger.error(
                "Cannot remove the repository. It doesn't exist on remote."
            )
        else:
            self.logger.info(
                'Repository has been successfully deleted on remote.')

    def rename(self, new_name):
        user = self.github.get_user()
        self.logger.info('Trying to rename repository on remote...')
        try:
            if self.remote_name is None:
                user.get_repo(self.local_name).edit(name=new_name)
            else:
                user.get_repo(self.remote_name).edit(name=new_name)
        except github.GithubException:
            self.logger.error(
                "Cannot rename the repository. It doesn't exist on remote."
            )
        else:
            self.logger.info(
                'Repository has been successfully renamed on remote.')
        if os.path.exists(self.local_name):
            self.logger.info('Renaming the repository locally...')
            os.rename(self.local_name, new_name)
            self.local_name = new_name
            self.logger.info(
                'Repository has been successfully renamed locally.')

    def __open_in_local_repo(self, filename, mode):
        """
            Like open(...), but 
            with the repo folder as cwd.
        """
        filename = os.path.join(self.local_name, filename)
        return open(filename, mode)


def handle_config(args):
    if args.list:
        print('\n'.join(utils.get_config()))
    elif args.token:
        utils.set_config('github.token', args.token)


def handle_init(args):
    gr = GitRepository(
        name=args.name,
        access_token=args.token
    )

    # TODO: language-specific template
    gr.create_and_upload(
        gitignore=utils.read_gitignore_template('default')
    )


def handle_delete(args):
    gr = GitRepository(
        name=args.path,
        access_token=args.token
    )
    if args.remote:
        gr.delete_remote()
    elif args.local:
        gr.delete_local()
    else:
        gr.delete()


def handle_rename(args):
    gr = GitRepository(
        name=args.path,
        access_token=args.token
    )
    gr.rename(args.new_name)


def main():
    args = parse_args()
    {
        'config': handle_config,
        'init': handle_init,
        'delete': handle_delete,
        'rename': handle_rename
    }[args.command](args)


if __name__ == "__main__":
    main()
