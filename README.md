# Git Repo CLI

Utils to easily create/delete/rename repository.

## Installation

To install git-repo-cli util type in your terminal:

```bash
pip install git-repo-cli
```

To use all the git-repo-cli functionality you should configure GitHub access token.

```bash
git-repo config --token <github-token>
```

Now you can use it.

## Usage

To make usage of the cli easier `git-repo` is used, instead of `git-repo-cli`.
To get help on usage you can always add --help flag to the command:

```bash
git-repo --help
```

### Initialize repository

To initialize repository type the following in the terminal:

```bash
git-repo init <repository-path>
```

It will create folder with name of `<repository-path>` folder and initialize it
locally and remotely.

If you use other name on remote you should use the following pattern:

```bash
git-repo init <repository-name> -f <repository-local-path>
```

It will create repository with name `<repository-name>` on remote and with path `<repository-local-path>` locally.

### Delete repository

To delete a repository use the following command:

```bash
git-repo delete <repository-path>
```

### Rename repository

To rename a repository use the following command:

```bash
git-repo rename <repository-path> <repository-new-name>
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[MIT](LICENSE.md)
