[![Discord](https://img.shields.io/discord/899171661457293343?color=7289da&label=discord&logo=discord&logoColor=white&style=flat)](https://discord.gg/wXy6m2X8wY)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1eee626c47fa4e6fb8b1ed3efdd3e518)](https://app.codacy.com/gh/cssnr/zipline-cli/dashboard)
[![PyPI](https://img.shields.io/pypi/v/zipline-cli)](https://pypi.org/project/zipline-cli/)
[![](https://repository-images.githubusercontent.com/661201286/8dfadbc8-94c0-4eaa-88bd-7ee351859510)](https://zipline.diced.tech/)
# Zipline CLI

Python 3 CLI Uploader for Zipline.

*   Zipline: [https://zipline.diced.tech/](https://zipline.diced.tech/)

This is currently a **WIP** and not complete, but has some useful functions.

## Install

From PyPi using pip:
```text
python -m pip install zipline-cli
```

From GitHub using pip:
```text
python -m pip install git+https://github.com/cssnr/zipline-cli.git
```

From Source using setuptools:
```text
git clone https://github.com/cssnr/zipline-cli.git
cd zipline-cli
python setup.py install
```

Uninstall:
```text
python -m pip uninstall zipline-cli
```

## CLI Usage

You will need a Zipline URL and Token to use the utility.

Setup Zipline URL and Token:
```bash
zipline --setup
```

Upload a File:
```bash
zipline test.txt
```

Create Text File from Input
```bash
cat test.txt | zipline 
```

Create Text File from Text
```bash
zipline
# type or paste contents followed by Ctrl+D (Ctrl+Z on Windows)
```

## Environment Variables

Environment Variables are stored in the `.zipline` file in your home directory.

*   Location: `~/.zipline`

| Variable       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| ZIPLINE_URL    | URL to your Zipline Instance                                                |
| ZIPLINE_TOKEN  | Authorization Token from Zipline                                            |
| ZIPLINE_EMBED  | Set this enable Embed on your uploads                                       |
| ZIPLINE_EXPIRE | See: https://zipline.diced.tech/docs/guides/upload-options#image-expiration |

You may also override them by exporting the variables in your current environment.

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

## Additional Information

> If you have more questions, concerns, or comments? 
> Join our [Discord](https://discord.gg/wXy6m2X8wY) for more information...
