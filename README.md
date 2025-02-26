[![Release](https://github.com/cssnr/zipline-cli/actions/workflows/release.yaml/badge.svg)](https://github.com/cssnr/zipline-cli/actions/workflows/release.yaml)
[![Test](https://github.com/cssnr/zipline-cli/actions/workflows/test.yaml/badge.svg)](https://github.com/cssnr/zipline-cli/actions/workflows/test.yaml)
[![Lint](https://github.com/cssnr/zipline-cli/actions/workflows/lint.yaml/badge.svg)](https://github.com/cssnr/zipline-cli/actions/workflows/lint.yaml)
[![Codacy](https://img.shields.io/codacy/grade/1eee626c47fa4e6fb8b1ed3efdd3e518?logo=codacy&logoColor=white&label=Codacy&color=31c754)](https://app.codacy.com/gh/cssnr/zipline-cli/dashboard)
[![Issues](https://img.shields.io/github/issues-raw/cssnr/zipline-cli?logo=github&logoColor=white&label=Issues&color=31c754)](https://github.com/cssnr/zipline-cli/issues)
[![PyPI](https://img.shields.io/pypi/v/zipline-cli?logo=python&logoColor=white&label=PyPI)](https://pypi.org/project/zipline-cli/)
[![GitHub Release Version](https://img.shields.io/github/v/release/cssnr/zipline-cli?logo=github)](https://github.com/cssnr/zipline-cli/releases/latest)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/cssnr/zipline-cli?logo=github&logoColor=white&label=updated)](https://github.com/cssnr/zipline-cli/graphs/commit-activity)
[![GitHub Top Language](https://img.shields.io/github/languages/top/cssnr/zipline-cli?logo=htmx&logoColor=white)](https://github.com/cssnr/zipline-cli)
[![GitHub Repo Stars](https://img.shields.io/github/stars/cssnr/zipline-cli?style=flat&logo=github&logoColor=white)](https://github.com/cssnr/zipline-cli/stargazers)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=github&logoColor=white&label=org%20stars)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)
[![](https://repository-images.githubusercontent.com/661201286/8dfadbc8-94c0-4eaa-88bd-7ee351859510)](https://github.com/cssnr/zipline-cli)

# Zipline CLI

- [Quick Start](#Quick-Start)
- [Install](#Install)
- [Usage](#Usage)
- [Environment Variables](#Environment-Variables)
- [API Reference](#API-Reference)
- [Support](#Support)

Python 3 CLI Uploader for Zipline v3 and Django Files.
Zipline CLI is currently functional and **Under Active Development**.  
Please open a [Feature Request](https://github.com/cssnr/zipline-cli/discussions/new?category=feature-requests)
for new features and submit an [Issue](https://github.com/cssnr/zipline-cli/issues/new)
for any bugs you find.

- Zipline: [https://zipline.diced.tech/](https://zipline.diced.tech/)
- Django Files: [https://django-files.github.io/](https://django-files.github.io/)

> [!IMPORTANT]  
> An update for Zipline v4 is currently in progress.  
> Zipline-CLI v1 "should" work with both Zipline v3 and v4.

```python
# v4: Add url to line 104: ["url"]
return ZipURL(r.json()["files"][0]["url"])
```

## Quick Start

```shell
python3 -m pip install zipline-cli
zipline --setup
```

## Install

From PyPi using pip:

```shell
python3 -m pip install zipline-cli
```

From GitHub using pip:

```shell
python3 -m pip install git+https://github.com/cssnr/zipline-cli.git
```

From Source using pip:

```shell
git clone https://github.com/cssnr/zipline-cli.git
python3 -m pip install -e zipline-cli
```

From Source using setuptools:

```shell
git clone https://github.com/cssnr/zipline-cli.git
cd zipline-cli
python3 setup.py install
```

### Uninstall

To completely remove from any above install methods:

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

## Environment Variables

Environment Variables are stored in the `.zipline` file in your home directory.

- Location: `~/.zipline` or `$HOME/.zipline`

| Variable       | Description                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------- |
| ZIPLINE_URL    | URL to your Zipline Instance                                                                      |
| ZIPLINE_TOKEN  | Authorization Token from Zipline                                                                  |
| ZIPLINE_EMBED  | Set this enable Embed on your uploads                                                             |
| ZIPLINE_FORMAT | Output Format after upload. Variables: `{filename}`, `{url}` and `{raw_url}`                      |
| ZIPLINE_EXPIRE | Zipline: https://zipline.diced.tech/docs/guides/upload-options#image-expiration                   |
| ZIPLINE_EXPIRE | Django Files: https://github.com/onegreyonewhite/pytimeparse2#pytimeparse2-time-expression-parser |

See [.zipline.example](.zipline.example) for an example `.zipline` file.

You may override them by exporting the variables in your current environment
or using the corresponding command line arguments. Use `zipline -h` for more info.

## API Reference

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

# Support

For general help or to request a feature, see:

- Q&A Discussion: https://github.com/cssnr/zipline-cli/discussions/categories/q-a
- Request a Feature: https://github.com/cssnr/zipline-cli/discussions/categories/feature-requests

If you are experiencing an issue/bug or getting unexpected results, you can:

- Report an Issue: https://github.com/cssnr/zipline-cli/issues
- Chat with us on Discord: https://discord.gg/wXy6m2X8wY
- Provide General
  Feedback: [https://cssnr.github.io/feedback/](https://cssnr.github.io/feedback/?app=Portainer%20Zipline%20CLI)
