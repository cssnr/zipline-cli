# Contributing

- [Workflow](#Workflow)
- [Setup](#Setup)
- [Testing](#Testing)
- [Building](#Building)

> [!WARNING]  
> This guide is a work in progress and may not be complete.

This is a basic contributing guide and is a work in progress.

## Workflow

1. Fork the repository.
2. Create a branch in your fork!
3. Make your changes, see [Setup](#Setup).
4. Test your changes, see [Testing](#Testing).
5. Commit and push your changes.
6. Create a PR to this repository.
7. Verify all the tests pass, fix the issues.
8. Make sure to keep your branch up-to-date.

If you need help with anything, [let us know](https://github.com/cssnr/zipline-cli?tab=readme-ov-file#support)...

## Setup

Clone the repository, change into the directory and run:

```shell
python -m pip install -U pip
python -m pip install -Ur requirements.txt
```

Prettier is used to format yaml, json and md.

```shell
npm install -g prettier
```

## Testing

First [Setup](#Setup) the project, then run:

```shell
pytest -v
```

## Building

Build the project locally:

```shell
python -m pip install -U pip
python -m pip install -Ur requirements.txt
python -m build
```

Install the built package:

```shell
python -m pip install dist/zipline_cli-0.0.1-py3-none-any.whl
```

The default version is `0.0.1` unless you set the environment variable `GITHUB_REF_NAME`.
