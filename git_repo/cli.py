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
    is_token_active = gr.check_token()
    if not is_token_active:
        print('Token is not valid.')
        return

    # TODO: language-specific template
    gr.create_and_upload(
        gitignore=utils.read_gitignore_template('default')
    )


def handle_delete(args):
    gr = GitRepository(
        name=args.path,
        access_token=args.token
    )
    is_token_active = gr.check_token()
    if not is_token_active:
        print('Token is not valid.')
        return
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
    is_token_active = gr.check_token()
    if not is_token_active:
        print('Token is not valid.')
        return
    gr.rename(args.new_name)


def handle_check_token(args):
    is_token_active = GitRepository.check_token(args.token)
    if not is_token_active:
        print('Token is not valid.')
        return


def cli():
    args = parse_args()
    {
        'config': handle_config,
        'init': handle_init,
        'delete': handle_delete,
        'rename': handle_rename,
        'check-token': handle_check_token,
    }[args.command](args)


if __name__ == "__main__":
    cli()
