from typing import Optional
import typer

from pax import __app_name__, __version__
from .commands import new_app

app = typer.Typer(no_args_is_help=True)
app.add_typer(new_app, name="new", help="Create a new Python project.")

# Global options #
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
        is_eager=True,
        help="Show version and exit."
    ),
) -> None:
    return
# End Global options #