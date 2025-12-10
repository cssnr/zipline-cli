import io
import os
import sys
from importlib.metadata import version
from typing import List, Optional, TextIO

import click
import typer
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from . import __doc__ as package_doc
from . import _utils as utils
from .zipline import Zipline, ZipURL


env_file = utils.get_env()
dotenv_loaded = load_dotenv(dotenv_path=env_file)

app = typer.Typer(pretty_exceptions_show_locals=False, rich_markup_mode="rich")

state = {"verbose": False}


def vprint(*objects: str):
    if state.get("verbose"):
        print(*objects, file=sys.stderr)


def format_output(filename: str, url: ZipURL) -> str:
    zipline_format = os.environ.get("ZIPLINE_FORMAT", "{filename}\n{url}\n{raw_url}")
    return zipline_format.format(filename=filename, url=url, raw_url=url.raw)


def run_setup(_url: str) -> None:
    # NOTE: Overhaul and update to typer/click/rich methods...
    env_file.touch()
    print(f"Setting up Environment File: [bold cyan]{env_file.absolute()}")
    url = typer.prompt("Zipline URL", default=_url).strip()
    token = typer.prompt("Zipline Authorization Token").strip()
    if not url or not token:
        raise click.ClickException("Missing URL or Token.")
    output = f"ZIPLINE_URL={url}\nZIPLINE_TOKEN={token}\n"
    embed = typer.confirm("Enabled Embed?", default=True)
    output += f"ZIPLINE_EMBED={embed}\n"
    expire = typer.prompt("Default Expire?", default="").strip().lower()
    if expire:
        output += f"ZIPLINE_EXPIRE={expire}\n"
    with open(env_file, "w") as f:
        f.write(output)
    print(f"Setup Complete. Variables Saved to: [bold green]{env_file.absolute()}")


def opt_info(value: bool):
    if value:
        table = Table(title="App Information")
        # Head
        table.add_column("Item", style="bold magenta", no_wrap=True)
        table.add_column("Value", style="bold cyan")
        # Body
        table.add_row("Zipline Version", version("zipline-cli"))
        table.add_row("Config File", str(env_file.absolute()))
        table.add_row("Config Loaded", str(dotenv_loaded))
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
    _embed: Annotated[
        Optional[bool], typer.Option("-E", "--embed", help="Enable Embed.", envvar="ZIPLINE_EMBED")
    ] = False,
    _expire: Annotated[
        str, typer.Option("-e", "-x", "--expire", "--expires_at", help="File Expiration.", envvar="ZIPLINE_EXPIRE")
    ] = "",
    _url: Annotated[str, typer.Option("-u", "--url", help="Zipline URL.", envvar="ZIPLINE_URL")] = "",
    _token: Annotated[
        str, typer.Option("-t", "-a", "--token", "--authorization", help="Zipline token.", envvar="ZIPLINE_TOKEN")
    ] = "",
    _verbose: Annotated[Optional[bool], typer.Option("-v", "--verbose", help="Verbose Output (jq safe).")] = False,
    _setup: Annotated[Optional[bool], typer.Option("-S", "--setup", help="Run interactive setup.")] = None,
    _info: Annotated[
        Optional[bool], typer.Option("-I", "--info", callback=opt_info, help="Show saved information.")
    ] = None,
    _version: Annotated[
        Optional[bool], typer.Option("-V", "--version", callback=opt_version, help="Show installed version.")
    ] = None,
):
    """Zipline CLI"""
    if _verbose:
        state["verbose"] = _verbose

    url = _url
    vprint(f"url: {url}")
    token = _token
    vprint(f"token: {token[-12:]}")
    expire = _expire
    vprint(f"expire: {expire}")
    embed = _embed
    vprint(f"embed: {embed}")

    if _setup or (not url and not token):
        print("[bold red]Error![/bold red] Missing --url or --token, Entering Setup.")
        run_setup(url)
        raise typer.Exit()

    zipline = Zipline(url, authorization=token)

    if not files:
        content: str = sys.stdin.read().rstrip("\n") + "\n"
        text_f: TextIO = io.StringIO(content)
        name = f"{utils.gen_rand(8)}.txt"
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
