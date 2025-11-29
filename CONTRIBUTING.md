# Contributing

- [Workflow](#Workflow)
- [Setup](#Setup)
- [Formatting](#Formatting)
- [Testing](#Testing)
- [Building](#Building)
- [Documentation](#Documentation)

This is a basic contributing guide and is a work in progress.

## Workflow

[![Fork](https://badges.cssnr.com/static/fork?lucide=git-fork&style=for-the-badge&color=3674a7)](https://github.com/cssnr/zipline-cli/fork)

1. Fork the repository.
2. Create a branch in your fork!
3. Make your changes, see [Setup](#Setup).
4. Test your changes, see [Testing](#Testing).
5. Commit and push your changes.
6. Create a PR to this repository.
7. Verify all the tests pass, fix the issues.
8. Make sure to keep your branch up-to-date.

If you need help with anything, [let us know](#readme-ov-file)...

## Setup

Clone the repository, change into the directory and run.

```shell
python -m pip install -U pip
python -m pip install --group dev
```

Install the project as an editable.

```shell
python -m pip install -e .
```

## Formatting

Black is used to format python code.

Prettier is used to format yaml, json and md.

```shell
npm install -g prettier
npx prettier --check .
npx prettier --write .
```

For details on linters see the [pyproject.toml](pyproject.toml) and [.github/workflows/lint.yaml](.github/workflows/lint.yaml).

## Testing

First [Setup](#Setup) the project, then run.

Note: The test only runs on GitHub Actions. See [.github/workflows/test.yaml](.github/workflows/test.yaml)

## Building

Build the project locally.

```shell
python -m pip install -U pip
python -m pip install --group dev
python -m build
```

Install the built package.

```shell
python -m pip install dist/zipline_cli-0.0.1-py3-none-any.whl
```

The default version is `0.0.1` unless you set the environment variable `GITHUB_REF_NAME`.

See [src/actions/\_\_init\_\_.py](src/zipline/__init__.py) for more details.

## Publishing

Create a pre-release on GitHub to publish to [test.pypi.org](https://test.pypi.org/).

To install from the test index, use the following command.

```shell
python -m pip install --pre -U --extra-index-url https://test.pypi.org/simple/ zipline-cli
```

- https://test.pypi.org/p/zipline-cli

## Documentation

The docs are built with Zensical.

```shell
python -m pip install -U zensical
zensical serve
```

Then visit: http://localhost:8000/

You can also build the docs locally.

```shell
zensical build
```

This builds the docs to the `sites` folder. It should run on any static site.

```shell
docker run --rm -p 8000:80 --name docker-static -v "./site:/static" ghcr.io/cssnr/docker-nginx-static:latest
```

Then visit: http://localhost:8000/
