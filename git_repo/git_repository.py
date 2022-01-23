import os
import github
import git
import shutil
from github import Github, BadCredentialsException
from typing import Iterable
from .utils import BeautifulFormatter, BeautifulLogger
from . import utils


class GitRepository:
    def __init__(self, name, access_token=None, local_path=None):
        self.path = os.path.abspath(
            name) if local_path is None else os.path.abspath(local_path)
        if local_path is None:
            self.local_name = self.path.split(os.path.sep)[-1]
        else:
            self.local_name = name
        try:
            local_repo = git.Repo(self.path)
            origin = local_repo.remote('origin')
            origin_url = next(origin.urls)
            self.remote_name = origin_url.split(
                os.path.sep)[-1].split('.git')[0]
        except git.GitError:
            self.remote_name = os.path.abspath(name).split(os.path.sep)[-1]

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
            gitignore_file.writelines(gitignore)

        self.logger.info('Making initial commit...')
        local_repo.git.add('.')
        local_repo.git.commit(m='"Initial commit"')
        if hasattr(self, 'github'):
            user = self.github.get_user()

            # get unique name for github repo
            self.logger.info('Checking the name...')
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
            'Repository "{}/{}" has been created.'.format(self.local_name, self.remote_name))

    def delete(self):
        self.delete_remote()
        self.delete_local()

    def delete_local(self):
        """Delete the repository on local machine but hold on remote"""
        if os.path.exists(self.path):
            self.logger.info('Removing the repository locally...')
            shutil.rmtree(self.path)
            self.logger.info(
                'Repository has been successfully deleted locally.')
        else:
            self.logger.error(
                "Cannot remove the repository. It doesn't exist locally.")

    def delete_remote(self):
        """Delete the repository on remote but hold locally."""
        user = self.github.get_user()
        self.logger.info(
            'Trying to delete repository {} on remote...'.format(self.remote_name))
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

    @staticmethod
    def check_token(access_token):
        try:
            github = Github(access_token)
            user = github.get_user()
            _ = user.name
        except BadCredentialsException:
            return False
        return True

    def __open_in_local_repo(self, filename, mode):
        """
            Like open(...), but 
            with the repo folder as cwd.
        """
        filename = os.path.join(self.path, filename)
        return open(filename, mode)


