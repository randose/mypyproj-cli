from typing import Optional
import typer

from randose import __app_name__, __version__
from .commands import new

app = typer.Typer()
app.add_typer(new.app, name="new")

def _version_callback(value: bool):
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True
    ),
) -> None:
    return