from .parse_args import parse_args
from .git_repository import GitRepository
from . import utils

def handle_config(args):
    if args.list:
        print('\n'.join(utils.get_config()))
    elif args.token:
        utils.set_config('github.token', args.token)


def handle_init(args):
    gr = GitRepository(
        name=args.name,
        access_token=args.token,
        local_path=args.folder
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


def cli():
    args = parse_args()
    {
        'config': handle_config,
        'init': handle_init,
        'delete': handle_delete,
        'rename': handle_rename
    }[args.command](args)


if __name__ == "__main__":
    cli()
