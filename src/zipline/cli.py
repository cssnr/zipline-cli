import io
import os
import secrets
import string
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any, List, Optional, TextIO

import typer
from click import ClickException
from dotenv import find_dotenv, load_dotenv
from rich import print
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from . import __doc__ as package_doc
from .zipline import Zipline, ZipURL


app = typer.Typer(pretty_exceptions_show_locals=False, rich_markup_mode="rich")


def get_env(file_name: str = ".zipline-test") -> Path:
    # NOTE: Remove `find_dotenv` and use central config file...
    env_file = Path(os.path.expanduser("~")) / file_name
    if os.path.isfile(env_file):
        return env_file
    dotenv_file = find_dotenv(filename=file_name)
    if dotenv_file:
        dotenv_path = Path(dotenv_file)
        return dotenv_path
    return env_file


def get_config(values: List[str], arg: Any, req: bool = False, cast: type = str):
    if arg or arg == 0 or arg is False:
        return arg
    for value in values:
        result = os.environ.get(f"ZIPLINE_{value.upper()}", "")
        if result:
            return cast(result)
    if req:
        error = f"Missing required argument: --{values[0]} (see also --help and --setup)"
        raise ClickException(error)
    return None


def gen_rand(length: int = 4) -> str:
    r = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return "".join(r)


def format_output(filename: str, url: ZipURL) -> str:
    zipline_format = os.environ.get("ZIPLINE_FORMAT", "{filename}\n{url}\n{raw_url}")
    return zipline_format.format(filename=filename, url=url, raw_url=url.raw)


def run_setup(env_file: Path) -> None:
    # NOTE: Overhaul and update to typer/click/rich methods...
    env_file.touch()
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
        output += f"ZIPLINE_EXPIRE={expire}\n"
    with open(env_file, "w") as f:
        f.write(output)
    print(f"Setup Complete. Variables Saved to: {env_file.absolute()}")


def opt_info(value: bool):
    if value:
        env_file = get_env()
        env = load_dotenv(dotenv_path=env_file)
        table = Table(title="App Information")
        # Head
        table.add_column("Item", style="bold magenta", no_wrap=True)
        table.add_column("Value", style="bold cyan")
        # Body
        table.add_row("Zipline Version", version("zipline-cli"))
        table.add_row("Config File", str(env_file.absolute()))
        table.add_row("Config Loaded", str(env))
        table.add_row("Server URL", os.environ.get("ZIPLINE_URL", ""))
        table.add_row("Token (ends in)", os.environ.get("ZIPLINE_TOKEN", "")[-10:])
        table.add_row("Expire", os.environ.get("ZIPLINE_EXPIRE", ""))
        table.add_row("Embed", os.environ.get("ZIPLINE_EMBED", ""))
        table.add_row("Results Format", repr(os.environ.get("ZIPLINE_FORMAT", "{url}\n{raw_url}"))[1:-1])
        console = Console()
        console.print(table)
        raise typer.Exit()


def opt_version(value: bool):
    if value:
        print(package_doc, file=sys.stderr)
        print(version("zipline-cli"))
        raise typer.Exit()


@app.command(epilog="Docs: https://zipline-cli.cssnr.com/")
def main(
    files: Annotated[Optional[List[str]], typer.Argument(help="AI is RETARDED")] = None,
    _embed: Annotated[Optional[bool], typer.Option("-E", "--embed", help="Enable Embed.")] = False,
    _expire: Annotated[str, typer.Option("-e", "-x", "--expire", "--expires_at", help="File Expiration.")] = "",
    _url: Annotated[str, typer.Option("-u", "--url", help="Zipline URL.")] = "",
    _token: Annotated[str, typer.Option("-t", "-a", "--token", "--authorization", help="Zipline token.")] = "",
    _setup: Annotated[Optional[bool], typer.Option("-S", "--setup", help="Run interactive setup.")] = None,
    _info: Annotated[
        Optional[bool], typer.Option("-I", "--info", callback=opt_info, help="Show saved information.")
    ] = None,
    _version: Annotated[
        Optional[bool], typer.Option("-V", "--version", callback=opt_version, help="Show installed version.")
    ] = None,
):
    """Zipline CLI"""
    # App Directory
    # app_dir = typer.get_app_dir('zipline-cli')
    # print(f"app_dir: {app_dir}")
    # Launch App
    # typer.launch("https://zipline-cli.cssnr.com/")

    print(f"_setup: {_setup}")
    env_file = get_env()
    print(f"env_file: {env_file}")
    env = load_dotenv(dotenv_path=env_file)
    print(f"env: {env}")
    print("--------------------")

    # print(f"_token: {_token}")
    url = get_config(["url"], _url)
    print(f"url: {url}")
    token = get_config(["token", "authorization"], _token)
    print(f"token: {token}")
    expire = get_config(["expire", "expire_at"], _expire)
    print(f"expire: {expire}")
    embed = get_config(["expire", "expire_at"], _embed, cast=bool)
    print(f"embed: {embed}")
    print("--------------------")

    if _setup or (not url and not token):
        print("Missing --url or --token, Entering Setup.")
        run_setup(env_file)
        raise typer.Exit()

    zipline = Zipline(url, authorization=token)

    print(f"files: {files}")

    if not files:
        content: str = sys.stdin.read().rstrip("\n") + "\n"
        text_f: TextIO = io.StringIO(content)
        name = f"{gen_rand(8)}.txt"
        zip_url: ZipURL = zipline.send_file(name, text_f)
        print(format_output(name, zip_url))
        raise typer.Exit()

    exit_code = 1
    for name in files:
        if not os.path.isfile(name):
            print(f"Warning: File Not Found: {name}")
            continue
        with open(name, "rb") as f:
            zip_url2: ZipURL = zipline.send_file(name, f)
            print(format_output(name, zip_url2))
            exit_code = 0
    sys.exit(exit_code)


if __name__ == "__main__":
    app()
