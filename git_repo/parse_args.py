import os
import sys
import argparse
# make root dir visible
# for importing
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
my_code_dir = os.path.dirname(parent_dir)
sys.path.insert(0, my_code_dir)

from . import config as cfg
from . import utils
from git_repo.utils import list_gitignore_choices


def _preproccess_args(args: argparse.Namespace) -> argparse.Namespace:
    """Modifies and completes missed arguments.

    Arguments:
        args {argparse.Namespace} -- raw arguments.

    Returns:
        argparse.Namespace -- preprocessed arguments.
    """
    if args.token is None:
        args.token = utils.get_config('github.token')

    return args


def _parse_init(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('init')
    parser.add_argument(
        'name',
        help='name of git repository.'
    )
    parser.add_argument(
        '-l', '--language',
        help='language of the repository.'
    )


def _parse_config(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('config')
    parser.add_argument(
        '-l', '--list',
        help='list the configurations.',
        action='store_true'
    )
    parser.add_argument(
        '-t', '--token',
        help='github access token.'
    )


def _parse_delete(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('delete')
    parser.add_argument(
        'path',
        help='path to the repo to delete.'
    )
    parser.add_argument(
        '-r', '--remote',
        help='delete only remote repo, but hold local one.',
        action='store_true'
    )
    parser.add_argument(
        '-l', '--local',
        help='delete only local repo, but hold remote one.',
        action='store_true'
    )


def _parse_rename(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('rename')
    parser.add_argument('path', help='path ot the repository to rename.')
    parser.add_argument('new_name', help='new name to set.')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--token',
        help='access token to use.'
    )

    subparsers = parser.add_subparsers(dest='command')
    _parse_init(subparsers)
    _parse_delete(subparsers)
    _parse_config(subparsers)
    _parse_rename(subparsers)

    args = parser.parse_args()
    args = _preproccess_args(args)
    return args


if __name__ == "__main__":
    args = parse_args()
