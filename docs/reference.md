---
icon: lucide/notebook-pen
---

# :lucide-notebook-pen: Reference

[![Zipline CLI](assets/images/logo.png){ align=right width=96 }](https://github.com/cssnr/zipline-cli?tab=readme-ov-file#readme)

## Environment Variables

Environment Variables are stored in the `.zipline` file in your home directory.

- Location: `~/.zipline` or `$HOME/.zipline`

| Variable         | Description                                                                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ZIPLINE_URL`    | URL to your Zipline Instance                                                                                                                                                                     |
| `ZIPLINE_TOKEN`  | Authorization Token from Zipline                                                                                                                                                                 |
| `ZIPLINE_EMBED`  | Set this enable Embed on your uploads                                                                                                                                                            |
| `ZIPLINE_FORMAT` | Output Format. Variables: `{filename}`, `{url}` and `{raw_url}`                                                                                                                                  |
| `ZIPLINE_EXPIRE` | Reference: [Zipline](https://zipline.diced.sh/docs/guides/upload-options#image-expiration) / [Django Files](https://github.com/onegreyonewhite/pytimeparse2#pytimeparse2-time-expression-parser) |

See [.zipline.example](https://github.com/cssnr/zipline-cli/blob/master/.zipline.example) for an example `.zipline` file.

You may override them by exporting the variables in your current environment
or using the corresponding command line arguments.

```shell
zipline -h
```

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

&nbsp;

!!! question

    If you need **help** getting started or run into any issues, [support](support.md) is available!
