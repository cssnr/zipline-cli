import argparse
import io
import mimetypes
import os
import re
import secrets
import string
import sys
from importlib.metadata import version
from pathlib import Path
from typing import IO, Any, Dict, List, Literal, Optional, TextIO

import requests
from binaryornot.check import is_binary
from decouple import config
from dotenv import find_dotenv, load_dotenv


class ZipURL(object):
    """
    Zipline URL Object
    :param file_url: str: Zipline File Display URL
    """

    __slots__ = ["url", "raw"]

    def __init__(self, file_url: str):
        self.url: str = file_url
        self.raw: str = self._get_raw(file_url)

    def __repr__(self):
        return f"<url={self.url} raw={self.raw}>"

    def __str__(self):
        return self.url

    @staticmethod
    def _get_raw(url: str) -> str:
        try:
            s = url.split("/", 4)
            return f"{s[0]}//{s[2]}/r/{s[4]}"
        except Exception:  # noqa
            return ""


class Zipline(object):
    """
    Zipline Python API
    :param base_url: str: Zipline URL
    :param kwargs: Zipline Headers
    """

    # noinspection SpellCheckingInspection
    allowed_headers = [
        # zipline v3
        "format",
        "image_compression_percent",
        "expires_at",
        "password",
        "zws",
        "embed",
        "max_views",
        "uploadtext",
        "authorization",
        "no_json",
        "x_zipline_filename",
        "original_name",
        "override_domain",
        # zipline v4
        "x-zipline-deletes-at",
        "x-zipline-format",
        "x-zipline-image-compression-percent",
        "x-zipline-password",
        "x-zipline-max-views",
        "x-zipline-no-json",
        "x-zipline-original-name",
        "x-zipline-folder",
        "x-zipline-filename",
        "x-zipline-domain",
        "x-zipline-file-extension",
    ]

    def __init__(self, url: str, **kwargs):
        self.base_url: str = url.rstrip("/")
        self._headers: Dict[str, str] = {}
        for header, value in kwargs.items():
            if header.lower() not in self.allowed_headers:
                continue
            if value is None:
                continue
            key = header.replace("_", "-").title()
            self._headers[key] = str(value)

    def send_file(self, file_name: str, file_object: IO, overrides: Optional[dict] = None) -> ZipURL:
        """
        Send File to Zipline
        TO-DO: Add timeout option to requests
        :param file_name: str: Name of File for files tuple
        :param file_object: TextIO: File to Upload
        :param overrides: dict: Header Overrides
        :return: str: File URL
        """
        url = self.base_url + "/api/upload"

        path = Path(file_name)
        if not path.is_file():
            raise ValueError(f"Not a File: {path.resolve()}")

        mime_type = get_type(file_name)
        files = {"file": (file_name, file_object, mime_type)}
        headers = self._headers | overrides if overrides else self._headers
        r = requests.post(url, headers=headers, files=files)  # nosec
        r.raise_for_status()
        data = r.json()["files"][0]
        if isinstance(data, dict):
            return ZipURL(data["url"])
        elif isinstance(data, list):
            return ZipURL(data[0])
        else:
            return ZipURL(data)


def get_type(file_name: str) -> str:
    # Deprecated since version 3.13: Passing a file path instead of URL is soft deprecated. Use guess_file_type() for this.
    # https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type
    mime_type, _ = mimetypes.guess_type(file_name, strict=False)
    if mime_type:
        return mime_type
    return "application/octet-stream" if is_binary(file_name) else "text/plain"


def get_mode(file_path: str, blocksize: int = 512) -> Literal["r", "rb"]:
    try:
        with open(file_path, "rb") as file:
            chunk = file.read(blocksize)
        chunk.decode("utf-8")
    except UnicodeDecodeError:
        return "rb"
    return "r"


def format_output(filename: str, url: ZipURL) -> str:
    """
    Format URL Output
    :param filename: str: Original or File Name
    :param url: ZipURL: ZipURL to Format
    :return: str: Formatted Output
    """
    zipline_format = config("ZIPLINE_FORMAT", "{filename}\n{url}\n{raw_url}")
    return zipline_format.format(filename=filename, url=url, raw_url=url.raw)


def gen_rand(length: int = 4) -> str:
    """
    Generate Random Streng at Given length
    :param length: int: Length of Random String
    :return: str: Random String
    """
    r = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return "".join(r)


def get_default(
    values: List[str],
    default: Optional[Any] = None,
    cast: type = str,
    pre: str = "ZIPLINE_",
    suf: str = "",
) -> Optional[str]:
    """
    Get Default Environment Variable from List of values
    :param values: list: List of Values to Check
    :param default: any: Default Value if None
    :param cast: type: Type to Cast Value
    :param pre: str: Environment Variable Prefix
    :param suf: str: Environment Variable Suffix
    :return: str: Environment Variable or None
    """
    for value in values:
        result = config(f"{pre}{value.upper()}{suf}", "", cast)
        if result:
            return result
    return default


def setup(env_file: Path) -> None:
    print("Setting up Environment File...")
    url = input("Zipline URL: ").strip()
    token = input("Zipline Authorization Token: ").strip()
    if not url or not token:
        raise ValueError("Missing URL or Token.")
    output = f"ZIPLINE_URL={url}\nZIPLINE_TOKEN={token}\n"
    embed = input("Enabled Embed? [Yes]/No: ").strip()
    if not embed or embed.lower() not in ["n", "o", "no", "noo"]:
        output += "ZIPLINE_EMBED=true\n"
    expire = input("Default Expire? [Blank for None]: ").strip().lower()
    if expire:
        match = re.search(r"^(\d+)(?:ms|s|m|h|d|w|y)$", expire)
        if not match:
            print(f"Warning: invalid expire format: {expire}. See --help")
        else:
            output += f"ZIPLINE_EXPIRE={expire}\n"
    with open(env_file, "w") as f:
        f.write(output)
    print(f"Setup Complete. Variables Saved to: {env_file}")
    sys.exit(0)


def run() -> None:
    zipline_file = ".zipline"
    env_file = Path(os.path.expanduser("~")) / zipline_file
    dotenv_path = env_file if os.path.isfile(env_file) else find_dotenv(filename=zipline_file)
    env = load_dotenv(dotenv_path=dotenv_path)

    parser = argparse.ArgumentParser(description="Zipline CLI.")
    parser.add_argument("files", metavar="Files", type=str, nargs="*", help="Files to Upload.")
    parser.add_argument("-s", "--setup", action="store_true", default=False, help="run the interactive setup")
    parser.add_argument("-i", "--info", action="store_true", help="show application information")
    parser.add_argument("-V", "--version", action="store_true", help="show the installed version")
    parser.add_argument("-u", "--url", type=str, default=get_default(["url"]), help="Zipline URL")
    parser.add_argument(
        "-a",
        "-t",
        "--authorization",
        "--token",
        type=str,
        default=get_default(["token", "authorization"]),
        help="Zipline Access Token for Authorization or ZIPLINE_TOKEN",
    )
    parser.add_argument(
        "-e",
        "-x",
        "--expires_at",
        "--expire",
        type=str,
        default=get_default(["expire", "expire_at"]),
        help="Ex: 1d, 2w. See: https://zipline.diced.tech/docs/guides/upload-options#image-expiration",
    )
    parser.add_argument(
        "--embed", action="store_true", default=get_default(["embed"], False, bool), help="Enable Embeds on Uploads."
    )
    args = parser.parse_args()

    if args.version:
        print(version("zipline-cli"))
        return

    if args.info:
        print(f"Zipline Version:  {version("zipline-cli")}")
        print(f"Config File:      {env_file.absolute()}")
        print(f"Server URL:       {config("ZIPLINE_URL", "")}")
        print(f"Token (ends in):  {config("ZIPLINE_TOKEN", "")[-12:]}")
        print(f"Expire:           {config("ZIPLINE_EXPIRE", "")}")
        print(f"Embed:            {config("ZIPLINE_EMBED", "")}")
        print(f"URL Format::\n{config("ZIPLINE_FORMAT", "")}")
        return

    if args.setup:
        setup(env_file)

    if not env and not args.url and not args.authorization and not os.path.isfile(env_file):
        env_file.touch()
        print("First Run Detected, Entering Setup.")
        setup(env_file)

    if not args.url:
        parser.print_help()
        raise ValueError("Missing URL. Use --setup or specify --url")

    if not args.authorization:
        parser.print_help()
        raise ValueError("Missing Token. Use --setup or specify --token")

    if args.expires_at:
        args.expires_at = args.expires_at.strip().lower()
        match = re.search(r"^(\d+)(?:ms|s|m|h|d|w|y)$", args.expires_at)
        if not match:
            parser.print_help()
            raise ValueError(f"Invalid Expire Format: {args.expires_at}.")

    zipline = Zipline(**vars(args))

    if not args.files:
        content: str = sys.stdin.read().rstrip("\n") + "\n"
        text_f: TextIO = io.StringIO(content)
        name = f"{gen_rand(8)}.txt"
        url: ZipURL = zipline.send_file(name, text_f)
        print(format_output(name, url))
        sys.exit(0)

    exit_code = 1
    for name in args.files:
        if not os.path.isfile(name):
            print(f"Warning: File Not Found: {name}")
            continue
        mode: Literal["r", "rb"] = get_mode(name)
        with open(name, mode) as f:
            # name, ext = os.path.splitext(os.path.basename(filename))
            # ext = f'.{ext}' if ext else ''
            # name = f'{name}-{gen_rand(8)}{ext}'
            # url: str = zipline.send_file(name, f)
            zip_url: ZipURL = zipline.send_file(name, f)
            print(format_output(name, zip_url))
            exit_code = 0
    sys.exit(exit_code)


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as error:
        print("\nError: {}".format(str(error)))
        sys.exit(1)


if __name__ == "__main__":
    main()
