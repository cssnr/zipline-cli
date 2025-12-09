[![PyPI Version](https://img.shields.io/pypi/v/zipline-cli?logo=pypi&logoColor=white&label=pypi)](https://pypi.org/project/zipline-cli/)
[![GitHub Release Version](https://img.shields.io/github/v/release/cssnr/zipline-cli?logo=github)](https://github.com/cssnr/zipline-cli/releases)
[![TOML Python Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcssnr%2Fzipline-cli%2Frefs%2Fheads%2Fmaster%2Fpyproject.toml&query=%24.project.requires-python&logo=python&logoColor=white&label=python)](https://github.com/cssnr/zipline-cli?tab=readme-ov-file#readme)
[![PyPI Downloads](https://img.shields.io/pypi/dm/zipline-cli?logo=pypi&logoColor=white)](https://pypistats.org/packages/zipline-cli)
[![Pepy Total Downloads](https://img.shields.io/pepy/dt/zipline-cli?logo=pypi&logoColor=white&label=total)](https://clickpy.clickhouse.com/dashboard/zipline-cli)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1eee626c47fa4e6fb8b1ed3efdd3e518)](https://app.codacy.com/gh/cssnr/zipline-cli/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=cssnr_zipline-cli&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=cssnr_zipline-cli)
[![Workflow Test](https://img.shields.io/github/actions/workflow/status/cssnr/zipline-cli/test.yaml?logo=cachet&label=test)](https://github.com/cssnr/zipline-cli/actions/workflows/test.yaml)
[![Workflow Lint](https://img.shields.io/github/actions/workflow/status/cssnr/zipline-cli/lint.yaml?logo=cachet&label=lint)](https://github.com/cssnr/zipline-cli/actions/workflows/lint.yaml)
[![Workflow Release](https://img.shields.io/github/actions/workflow/status/cssnr/zipline-cli/release.yaml?logo=cachet&label=release)](https://github.com/cssnr/zipline-cli/actions/workflows/release.yaml)
[![Deployment PyPi](https://img.shields.io/github/deployments/cssnr/zipline-cli/pypi?logo=pypi&logoColor=white&label=pypi)](https://pypi.org/project/zipline-cli/)
[![Deployment Docs](https://img.shields.io/github/deployments/cssnr/zipline-cli/docs?logo=materialformkdocs&logoColor=white&label=docs)](https://zipline-cli.cssnr.com/)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/cssnr/zipline-cli?logo=github&label=updated)](https://github.com/cssnr/zipline-cli/graphs/commit-activity)
[![GitHub Repo Size](https://img.shields.io/github/repo-size/cssnr/zipline-cli?logo=bookstack&logoColor=white&label=repo%20size)](https://github.com/cssnr/zipline-cli)
[![GitHub Top Language](https://img.shields.io/github/languages/top/cssnr/zipline-cli?logo=htmx&logoColor=white)](https://github.com/cssnr/zipline-cli?tab=readme-ov-file#readme)
[![GitHub Contributors](https://img.shields.io/github/contributors-anon/cssnr/zipline-cli?logo=github)](https://github.com/cssnr/zipline-cli/graphs/contributors)
[![GitHub Discussions](https://img.shields.io/github/discussions/cssnr/cloudflare-purge-cache-action?logo=github)](https://github.com/cssnr/cloudflare-purge-cache-action/discussions)
[![GitHub Forks](https://img.shields.io/github/forks/cssnr/zipline-cli?style=flat&logo=github)](https://github.com/cssnr/zipline-cli/forks)
[![GitHub Repo Stars](https://img.shields.io/github/stars/cssnr/zipline-cli?style=flat&logo=github)](https://github.com/cssnr/zipline-cli/stargazers)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=github&label=org%20stars)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-72a5f2?logo=kofi&label=support)](https://ko-fi.com/cssnr)
[![](https://repository-images.githubusercontent.com/661201286/8dfadbc8-94c0-4eaa-88bd-7ee351859510)](https://zipline-cli.cssnr.com/)

# Zipline CLI

<a title="Zipline CLI" href="https://zipline-cli.cssnr.com/" target="_blank">
<img alt="Zipline CLI" align="right" width="128" height="auto" src="https://zipline-cli.cssnr.com/assets/images/logo.png"></a>

- [Quick Start](#quick-start)
- [Install](#install)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Support](#support)
- [Contributing](#contributing)

Python 3 CLI File Uploader for [Diced/Zipline](https://github.com/diced/zipline) v3/v4 Upload Server and [Django Files](https://github.com/django-files/django-files).

- Zipline: [https://zipline.diced.sh/](https://zipline.diced.sh/)
- Django Files: [https://django-files.github.io/](https://django-files.github.io/)

> [!TIP]  
> If you have any trouble getting started, [support is available](#support).  
> You can also [request new features](https://github.com/cssnr/zipline-cli/discussions/new?category=feature-requests)
> or report any [issues](https://github.com/cssnr/zipline-cli/issues/new).

> [!WARNING]  
> This branch contains the latest changes for [pre-releases](https://github.com/cssnr/zipline-cli/releases).  
> For the current version see this [README.md](https://github.com/cssnr/zipline-cli/tree/0.2.3).

## Quick Start<a id="quick-start"></a>

```shell
python -m pip install zipline-cli
zipline --setup
```

[![View Documentation](https://img.shields.io/badge/view_documentation-blue?style=for-the-badge&logo=googledocs&logoColor=white)](https://zipline-cli.cssnr.com/)

## Install<a id="install"></a>

From PyPI: https://pypi.org/p/zipline-cli

```shell
python -m pip install zipline-cli
```

From GitHub using pip.

```shell
python -m pip install git+https://github.com/cssnr/zipline-cli.git
```

From Source using pip.

```shell
git clone https://github.com/cssnr/zipline-cli.git
python -m pip install zipline-cli
```

Uninstall.

```shell
python -m pip uninstall zipline-cli
```

## Usage<a id="usage"></a>

> [!TIP]  
> View the [Getting Started](https://zipline-cli.cssnr.com/) guide online.

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

## Environment Variables<a id="environment-variables"></a>

Environment Variables are stored in the `.zipline` file in your home directory.

- Location: `~/.zipline` or `$HOME/.zipline`

| Variable         | Description                                                                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ZIPLINE_URL`    | URL to your Zipline Instance                                                                                                                                                                     |
| `ZIPLINE_TOKEN`  | Authorization Token from Zipline                                                                                                                                                                 |
| `ZIPLINE_EMBED`  | Set this enable Embed on your uploads                                                                                                                                                            |
| `ZIPLINE_FORMAT` | Output Format. Variables: `{filename}`, `{url}` and `{raw_url}`                                                                                                                                  |
| `ZIPLINE_EXPIRE` | Reference: [Zipline](https://zipline.diced.sh/docs/guides/upload-options#image-expiration) / [Django Files](https://github.com/onegreyonewhite/pytimeparse2#pytimeparse2-time-expression-parser) |

See [.zipline.example](.zipline.example) for an example `.zipline` file.

You may override them by exporting the variables in your current environment
or using the corresponding command line arguments.

```shell
zipline -h
```

## API Reference<a id="api-reference"></a>

Initialize the class with your Zipline URL.
Everything else is a header passed as a kwarg.
The API does not yet support environment variables.

Zipline Token/Authorization is a header kwarg and can be passed as follows:

```python
from zipline import Zipline
zipline = Zipline('ZIPLINE_URL', authorization='ZIPLINE_TOKEN')
```

Upload a File

```python
from zipline import Zipline
zipline = Zipline('ZIPLINE_URL', authorization='ZIPLINE_TOKEN')
with open('text.txt') as f:
    url = zipline.send_file('test.txt', f)
print(url)
```

# Support<a id="support"></a>

For general help or to request a feature, see:

- Q&A Discussion: https://github.com/cssnr/zipline-cli/discussions/categories/q-a
- Request a Feature: https://github.com/cssnr/zipline-cli/discussions/categories/feature-requests
- Chat with us on Discord: https://discord.gg/wXy6m2X8wY

If you are experiencing an issue/bug or getting unexpected results, you can:

- Report an Issue: https://github.com/cssnr/zipline-cli/issues
- Provide General Feedback: [https://cssnr.github.io/feedback/](https://cssnr.github.io/feedback/?app=zipline-cli)
- Chat with us on Discord: https://discord.gg/wXy6m2X8wY

# Contributing<a id="contributing"></a>

All contributions are welcome including [bug reports](https://github.com/cssnr/zipline-cli/issues),
[feature requests](https://github.com/cssnr/zipline-cli/discussions/categories/feature-requests),
or [pull requests](https://github.com/cssnr/zipline-cli/discussions) (please start a discussion).

See the [CONTRIBUTING.md](#contributing-ov-file) for more details.

More Zipline Projects:

- [Zipline CLI](https://zipline-cli.cssnr.com/) - [Source Code](https://github.com/cssnr/zipline-cli?tab=readme-ov-file#readme)
- [Zipline Web Extension](https://zipline-extension.cssnr.com/) - [Source Code](https://github.com/cssnr/zipline-extension?tab=readme-ov-file#readme)
- [Zipline Android Application](https://zipline-android.cssnr.com/) - [Source Code](https://github.com/cssnr/zipline-android?tab=readme-ov-file#readme)

Please consider making a donation to support the development of this project
and [additional](https://cssnr.com/) open source projects.

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cssnr)

For a full list of current projects visit: [https://cssnr.github.io/](https://cssnr.github.io/)
