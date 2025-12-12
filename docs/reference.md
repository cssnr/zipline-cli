---
icon: lucide/notebook-pen
---

# :lucide-notebook-pen: Reference

[![Zipline CLI](assets/images/logo.png){ align=right width=96 }](https://github.com/cssnr/zipline-cli?tab=readme-ov-file#readme)

## Environment Variables

Environment Variables are stored in the `.zipline` file in your home directory.

- Location: `~/.zipline` or `$HOME/.zipline`

| Variable         | Description                                                     |
| ---------------- | --------------------------------------------------------------- |
| `ZIPLINE_URL`    | URL to your Zipline Instance                                    |
| `ZIPLINE_TOKEN`  | Authorization Token from Zipline                                |
| `ZIPLINE_FORMAT` | Output Format. Variables: `{filename}`, `{url}` and `{raw_url}` |

See [.zipline.example](https://github.com/cssnr/zipline-cli/blob/master/.zipline.example) for an example `.zipline` file.

!!! danger "Deprecated Variables"

    Both `ZIPLINE_EXPIRE` and `ZIPLINE_EMBED` have been deprecated.
    These options will be restored in a future release.

You may override them by exporting the variables in your current environment
or using the corresponding [command line](#command-line) arguments.

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

For more details, view the [src/zipline.py](https://github.com/cssnr/zipline-cli/blob/master/src/zipline/zipline.py) file.

## Command Line

For more details see `zipline -h`.

```text
 Usage: zipline [OPTIONS] [FILES]...

 Zipline CLI

┌─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────┐
│   files      [FILES]...  Files...                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
┌─ Options ───────────────────────────────────────────────────────────────────────────────────────────────┐
│ --name                   -n           File Name (sent with upload).                             │
│ --url                    -u           Zipline URL. [env var: ZIPLINE_URL]                       │
│ --token,--authorization  -t,-a        Zipline token.                                            │
│                                       [env var: ZIPLINE_TOKEN, ZIPLINE_AUTHORIZATION]           │
│ --verbose                -v           Verbose Output (jq safe). [env var: ZIPLINE_VERBOSE]      │
│ --setup                  -S           Run interactive setup.                                    │
│ --info                   -I           Show saved information.                                   │
│ --version                -V           Show installed version.                                   │
│ --install-completion                  Install completion for the current shell.                 │
│ --show-completion                     Show completion for the current shell, to copy it or      │
│                                       customize the installation.                               │
│ --help                   -h           Show this message and exit.                               │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

&nbsp;

!!! question

    If you need **help** getting started or run into any issues, [support](support.md) is available!
