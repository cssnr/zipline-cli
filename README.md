[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=Discord)](https://discord.gg/wXy6m2X8wY)
[![PyPI](https://img.shields.io/github/issues-raw/cssnr/zipline-cli?logo=github&logoColor=white&label=Issues)](https://github.com/cssnr/zipline-cli/issues)
[![Codacy Badge](https://img.shields.io/codacy/grade/1eee626c47fa4e6fb8b1ed3efdd3e518?logo=codacy&logoColor=white&label=Codacy)](https://app.codacy.com/gh/cssnr/zipline-cli/dashboard)
[![PyPI](https://img.shields.io/pypi/v/zipline-cli?logo=python&logoColor=white&label=PyPi)](https://pypi.org/project/zipline-cli/)
[![](https://repository-images.githubusercontent.com/661201286/8dfadbc8-94c0-4eaa-88bd-7ee351859510)](https://github.com/cssnr/zipline-cli)
# Zipline CLI

Python 3 CLI Uploader for Zipline.
Zipline CLI is currently functional and **Under Active Development**.  
Please open a [Feature Request](https://github.com/cssnr/zipline-cli/discussions/new?category=feature-requests)
for new features and submit an [Issue](https://github.com/cssnr/zipline-cli/issues)
for any bugs you find.

*   Zipline Docs: [https://zipline.diced.tech/](https://zipline.diced.tech/)

## Table of Contents

*   [Quick Start](#quick-start)
*   [Install](#install)
*   [CLI Usage](#cli-usage)
*   [Environment Variables](#environment-variables)
*   [Python API Reference](#python-api-reference)
*   [Additional Information](#additional-information)

## Quick Start

```bash
python3 -m pip install zipline-cli
zipline --setup
```

## Install

From PyPi using pip:
```bash
python3 -m pip install zipline-cli
```

From GitHub using pip:
```bash
python3 -m pip install git+https://github.com/cssnr/zipline-cli.git
```

From Source using pip:
```bash
git clone https://github.com/cssnr/zipline-cli.git
python3 -m pip install -e zipline-cli
```

From Source using setuptools:
```bash
git clone https://github.com/cssnr/zipline-cli.git
cd zipline-cli
python3 setup.py install
```

### Uninstall

To completely remove from any above install methods:
```bash
python3 -m pip uninstall zipline-cli
```

## CLI Usage

Setup Zipline URL and Token:
```bash
zipline --setup
```

Upload a File:
```bash
zipline test.txt
```

Upload Multiple Files:
```bash
zipline file1.txt file2.txt
```

Create Text File from Input
```bash
cat test.txt | zipline 
```

Create Text File from Clipboard
```bash
zipline
# Paste or Type contents, followed by a newline, then Ctrl+D (Ctrl+Z on Windows)
```

## Environment Variables

Environment Variables are stored in the `.zipline` file in your home directory.

*   Location: `~/.zipline` or `$HOME/.zipline`

| Variable       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| ZIPLINE_URL    | URL to your Zipline Instance                                                |
| ZIPLINE_TOKEN  | Authorization Token from Zipline                                            |
| ZIPLINE_EMBED  | Set this enable Embed on your uploads                                       |
| ZIPLINE_EXPIRE | See: https://zipline.diced.tech/docs/guides/upload-options#image-expiration |

You may override them by exporting the variables in your current environment
or using the corresponding command line arguments. See `-h` for more info.

## Python API Reference

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

## Additional Information

Still have questions, concerns, or comments?

*   [Feature Requests](https://github.com/cssnr/zipline-cli/discussions/categories/feature-requests)
*   [Helpdesk Q&A](https://github.com/cssnr/zipline-cli/discussions/categories/helpdesk-q-a)
*   [Discord](https://discord.gg/wXy6m2X8wY)

> Zipline Guide: Hit That Fresh Nar Nar: [youtube.com/watch?v=bJHYo2aGWgE](https://www.youtube.com/watch?v=bJHYo2aGWgE)
