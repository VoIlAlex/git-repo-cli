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


def parse_args():
    DEFAULT_GITIGNORE = cfg.read_gitignore_template('default')
    DEFAULT_ACCESS_TOKEN = cfg.ACCESS_TOKEN

    parser = argparse.ArgumentParser()

    # TODO: split parser into subparsers
    # sp = parser.add_subparsers(dest='cmd')
    # for cmd in ['config']:
    #     sp.add_parser(cmd)

    parser.add_argument(
        'name',
        help='name of git repository'
    )

    parser.add_argument(
        '-i', '--ignore',
        help='elements to ignore by git',
        default=DEFAULT_GITIGNORE,
        action='append',
        required=False
    )
    parser.add_argument(
        '-ait', '--add-ignore-template',
        help='add specified file as new ignore template'
    )
    parser.add_argument(
        '-it', '--ignore-template',
        help='gitignore template to use',
        default=None,
        action='append'
    )
    parser.add_argument(
        '-t', '--access-token',
        help='username of github account',
        default=DEFAULT_ACCESS_TOKEN,
        required=False
    )
    parser.add_argument(
        '-d', '--delete',
        help='delete specified repo',
        action='store_true'
    )
    parser.add_argument(
        '-dr', '--delete-remote',
        help='delete repo on remote',
        action='store_true'
    )
    parser.add_argument(
        '-da', '--delete-all',
        help='delete repo on remote and locally',
        action='store_true'
    )
    parser.add_argument(
        '-r', '--rename',
        help='rename repo remotely and locally',
        metavar="NAME"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
