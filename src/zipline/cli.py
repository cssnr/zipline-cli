import os
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any, List, Optional

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

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    pretty_exceptions_show_locals=False,
    rich_markup_mode="rich",
)

state = {"verbose": False}


def vprint(*objects: Any, **kwargs):
    if state.get("verbose"):
        print(*objects, file=sys.stderr, **kwargs)


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


def info_callback(value: bool):
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


def version_callback(value: bool):
    if value:
        print(package_doc, file=sys.stderr)
        print(version("zipline-cli"))
        raise typer.Exit()


@app.command(epilog="Docs: https://zipline-cli.cssnr.com/")
def main(
    files: Annotated[Optional[List[Path]], typer.Argument(help="Files...", exists=True, dir_okay=False)] = None,
    _embed: Annotated[
        Optional[bool], typer.Option("-E", "--embed", help="Enable Embed.", envvar="ZIPLINE_EMBED")
    ] = False,
    _expire: Annotated[
        str,
        typer.Option(
            "-e", "-x", "--expire", "--expires_at", metavar="", help="File Expiration.", envvar="ZIPLINE_EXPIRE"
        ),
    ] = "",
    _url: Annotated[str, typer.Option("-u", "--url", metavar="", help="Zipline URL.", envvar="ZIPLINE_URL")] = "",
    _token: Annotated[
        str,
        typer.Option(
            "-t",
            "-a",
            "--token",
            "--authorization",
            metavar="",
            help="Zipline token.",
            envvar=["ZIPLINE_TOKEN", "ZIPLINE_AUTHORIZATION"],
        ),
    ] = "",
    _verbose: Annotated[Optional[bool], typer.Option("-v", "--verbose", help="Verbose Output (jq safe).")] = False,
    _setup: Annotated[Optional[bool], typer.Option("-S", "--setup", help="Run interactive setup.")] = None,
    _info: Annotated[
        Optional[bool], typer.Option("-I", "--info", callback=info_callback, help="Show saved information.")
    ] = None,
    _version: Annotated[
        Optional[bool], typer.Option("-V", "--version", callback=version_callback, help="Show installed version.")
    ] = None,
):
    """Zipline CLI"""
    if _verbose:
        state["verbose"] = _verbose

    vprint(f"{_url=}", f"{_token[-12:]=}", f"{_expire=}", f"{_embed=}", sep="\n")

    if _setup or not _url and not _token:
        print("[bold red]Error![/bold red] Missing --url or --token, Entering Setup.")
        run_setup(_url)
        raise typer.Exit()

    zipline = Zipline(_url, authorization=_token)

    if not files:
        name: str = f"{utils.gen_rand(8)}.txt"
        zip_url: ZipURL = zipline.send_file(name, click.get_text_stream("stdin"))
        print(format_output(name, zip_url))
        raise typer.Exit()

    exit_code = 1
    for file in files:
        vprint(
            f"Uploading: [green bold]{click.format_filename(file.name)}[/green bold] - [cyan bold]{file.absolute()}"
        )
        with open(file, "rb") as f:
            zip_url_: ZipURL = zipline.send_file(file.name, f)
        print(format_output(file.name, zip_url_))
        exit_code = 0
    raise typer.Exit(exit_code)


if __name__ == "__main__":
    app()
