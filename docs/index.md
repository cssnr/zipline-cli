---
icon: lucide/rocket
---

# :lucide-rocket: Get Started

[![Zipline CLI](assets/images/logo.png){ align=right width=96 }](https://github.com/cssnr/zipline-cli?tab=readme-ov-file#readme)

[![PyPI Version](https://img.shields.io/pypi/v/zipline-cli?logo=pypi&logoColor=white&label=pypi)](https://pypi.org/project/zipline-cli/)
[![TOML Python Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcssnr%2Fzipline-cli%2Frefs%2Fheads%2Fmaster%2Fpyproject.toml&query=%24.project.requires-python&logo=python&logoColor=white&label=python)](https://github.com/cssnr/zipline-cli?tab=readme-ov-file#readme)
[![PyPI Downloads](https://img.shields.io/pypi/dm/zipline-cli?logo=pypi&logoColor=white)](https://pypistats.org/packages/zipline-cli)
[![Workflow Test](https://img.shields.io/github/actions/workflow/status/cssnr/zipline-cli/test.yaml?logo=cachet&label=test)](https://github.com/cssnr/zipline-cli/actions/workflows/test.yaml)
[![GitHub Repo Size](https://img.shields.io/github/repo-size/cssnr/zipline-cli?logo=bookstack&logoColor=white&label=repo%20size)](https://github.com/cssnr/zipline-cli?tab=readme-ov-file#readme)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/cssnr/zipline-cli?logo=github&label=updated)](https://github.com/cssnr/zipline-cli/pulse)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/cssnr/zipline-cli?logo=github)](https://github.com/cssnr/zipline-cli/issues)
[![GitHub Discussions](https://img.shields.io/github/discussions/cssnr/zipline-cli?logo=github)](https://github.com/cssnr/zipline-cli/discussions)
[![GitHub Forks](https://img.shields.io/github/forks/cssnr/zipline-cli?style=flat&logo=github)](https://github.com/cssnr/zipline-cli/forks)
[![GitHub Repo Stars](https://img.shields.io/github/stars/cssnr/zipline-cli?style=flat&logo=github)](https://github.com/cssnr/zipline-cli/stargazers)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=github&label=org%20stars)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-72a5f2?logo=kofi&label=support)](https://ko-fi.com/cssnr)

Python 3 CLI File Uploader for [Diced/Zipline](https://github.com/diced/zipline) v3/v4 Upload Server and [Django Files](https://github.com/django-files/django-files).

- Zipline: [https://zipline.diced.tech/](https://zipline.diced.tech/)
- Django Files: [https://django-files.github.io/](https://django-files.github.io/)

**To get started [Install](#install) the cli and view the [Usage](#usage).**

If you run into any issues, [support](support.md) is available.

## Quick Start

```shell
python3 -m pip install zipline-cli
zipline --setup
```

Next, review the [Usage](#usage) and [Environment Variables](reference.md#environment-variables) reference.

## Install

From PyPI: https://pypi.org/p/zipline-cli

=== "pip"

    ```shell
    python -m pip install zipline-cli
    ```

=== "uv"

    ```shell
    uv add zipline-cli
    ```

=== "requirements.txt"

    ``` text
    zipline-cli
    ```

=== "pyproject.toml"

    ``` toml
    dependencies = ["zipline-cli"]
    ```

From GitHub using pip.

```shell
python3 -m pip install git+https://github.com/cssnr/zipline-cli.git
```

From Source using pip.

```shell
git clone https://github.com/cssnr/zipline-cli.git
python3 -m pip install zipline-cli
```

Uninstall.

```shell
python3 -m pip uninstall zipline-cli
```

## Usage

Setup Zipline URL and Token:

```shell
zipline --setup
```

Upload a File:

```shell
zipline test.txt
```

Upload Multiple Files:

```shell
zipline file1.txt file2.txt
```

Create Text File from Input

```shell
cat test.txt | zipline
```

Create Text File from Clipboard

```shell
zipline
# Paste or Type contents, followed by a newline, then Ctrl+D (Ctrl+Z on Windows)
```

For more options, see the [Environment Variables](reference.md#environment-variables) reference.

[:lucide-notebook-pen: Environment Variables](reference.md#environment-variables){ .md-button .md-button--primary }

&nbsp;

!!! question

    If you need **help** getting started or run into any issues, [support](support.md) is available!
