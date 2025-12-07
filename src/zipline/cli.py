import argparse
import io
import os
import re
import secrets
import string
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any, List, Optional, TextIO

from decouple import config
from dotenv import find_dotenv, load_dotenv

from zipline.zipline import Zipline, ZipURL

from . import __doc__ as package_doc


def run() -> None:
    zipline_file = ".zipline"
    env_file = Path(os.path.expanduser("~")) / zipline_file
    dotenv_path = env_file if os.path.isfile(env_file) else find_dotenv(filename=zipline_file)
    env = load_dotenv(dotenv_path=dotenv_path)

    parser = argparse.ArgumentParser(description="Zipline CLI.", epilog="Docs: https://zipline-cli.cssnr.com/")
    parser.add_argument("files", metavar="file(s)", type=str, nargs="*", help="file(s) to upload")
    parser.add_argument("-s", "--setup", action="store_true", default=False, help="run the interactive setup")
    parser.add_argument(
        "-u", "--url", metavar="ZIPLINE_URL", type=str, default=get_default(["url"]), help="Zipline server url"
    )
    parser.add_argument(
        "-a",
        "-t",
        "--authorization",
        "--token",
        metavar="ZIPLINE_TOKEN",
        type=str,
        default=get_default(["token", "authorization"]),
        help="Zipline access token or ZIPLINE_TOKEN",
    )
    parser.add_argument(
        "-e",
        "-x",
        "--expires_at",
        "--expire",
        type=str,
        default=get_default(["expire", "expire_at"]),
        help="1d, 2w, etc. See: https://zipline.diced.sh/docs/guides/ms",
    )
    parser.add_argument(
        "-E",
        "--embed",
        action="store_true",
        default=get_default(["embed"], False, bool),
        help="enable embeds on uploads",
    )
    parser.add_argument("-i", "--info", action="store_true", help="show application information")
    parser.add_argument("-V", "--version", action="store_true", help="show the installed version")
    args = parser.parse_args()

    if args.version:
        print(package_doc, file=sys.stderr)
        print(version("zipline-cli"))
        return

    if args.info:
        print(f"Zipline Version:  {version('zipline-cli')}")
        print(f"Config File:      {env_file.absolute()}")
        print(f"Server URL:       {config('ZIPLINE_URL', '')}")
        print(f"Token (ends in):  {config('ZIPLINE_TOKEN', '')[-10:]}")
        print(f"Expire:           {config('ZIPLINE_EXPIRE', '')}")
        print(f"Embed:            {config('ZIPLINE_EMBED', '')}")
        zipline_format = config("ZIPLINE_FORMAT", "{url}\n{raw_url}")
        print(f"URL Format::\n{zipline_format}")
        return

    if args.setup:
        setup(env_file)
        return

    if not env and not args.url and not args.authorization and not os.path.isfile(env_file):
        env_file.touch()
        print("First Run Detected, Entering Setup.")
        setup(env_file)
        return

    if not args.url:
        parser.print_help()
        exit_error(parser, "Missing URL. Use --setup or specify --url")

    if not args.authorization:
        parser.print_help()
        exit_error(parser, "Missing Token. Use --setup or specify --token")

    if args.expires_at:
        args.expires_at = args.expires_at.strip().lower()
        match = re.search(r"^(\d+)(?:ms|s|m|h|d|w|y)$", args.expires_at)
        if not match:
            parser.print_help()
            exit_error(parser, f"Invalid Expire Format: {args.expires_at}.")

    zipline = Zipline(**vars(args))

    if not args.files:
        content: str = sys.stdin.read().rstrip("\n") + "\n"
        text_f: TextIO = io.StringIO(content)
        name = f"{gen_rand(8)}.txt"
        url: ZipURL = zipline.send_file(name, text_f)
        print(format_output(name, url))
        return

    exit_code = 1
    for name in args.files:
        if not os.path.isfile(name):
            print(f"Warning: File Not Found: {name}")
            continue
        # mode: Literal["r", "rb"] = get_mode(name)
        with open(name, "rb") as f:
            # name, ext = os.path.splitext(os.path.basename(filename))
            # ext = f'.{ext}' if ext else ''
            # name = f'{name}-{gen_rand(8)}{ext}'
            # url: str = zipline.send_file(name, f)
            zip_url: ZipURL = zipline.send_file(name, f)
            print(format_output(name, zip_url))
            exit_code = 0
    sys.exit(exit_code)


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


def get_default(
    values: List[str],
    default: Optional[Any] = None,
    cast: type = str,
    pre: str = "ZIPLINE_",
    suf: str = "",
) -> Optional[str]:
    """
    Get Default Environment Variable from List of values
    :param values: List of Values to Check
    :param default: Default Value if None
    :param cast: Type to Cast Value
    :param pre: Environment Variable Prefix
    :param suf: Environment Variable Suffix
    :return: Environment Variable or None
    """
    for value in values:
        result = config(f"{pre}{value.upper()}{suf}", "", cast)
        if result:
            return result
    return default


def format_output(filename: str, url: ZipURL) -> str:
    """
    Format URL Output
    :param filename: Original or File Name
    :param url: ZipURL to Format
    :return: Formatted Output
    """
    zipline_format = config("ZIPLINE_FORMAT", "{filename}\n{url}\n{raw_url}")
    return zipline_format.format(filename=filename, url=url, raw_url=url.raw)


def gen_rand(length: int = 4) -> str:
    """
    Generate Random Streng
    :param length: Length of String
    :return: Random String
    """
    r = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return "".join(r)


def exit_error(arg_parser: argparse.ArgumentParser, message: str, print_help=True):
    # print(f"\033[31;1merror: \033[33;1m{message}\033[0m", file=sys.stderr, end="\n\n")
    print(f"error: {message}", file=sys.stderr, end="\n\n")
    if print_help:
        arg_parser.print_help(sys.stderr)
    sys.exit(1)


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
