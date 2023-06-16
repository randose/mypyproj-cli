# Add dependency command. 
# 
# There is only one command in this file, but you can add more if you want, i.e. new_clitool, new_webapp, etc.
# If you do, make sure to remove the invoke_without_command arg in the typer.Typer() app initialization on line 21, 
# and change the decorator for the add_cmd() function to @app.command().

from typing import Optional, Annotated
import os
import shutil
import subprocess
import re

import typer
from rich import print
from rich.console import Console
from rich.panel import Panel

console = Console() # Used for normal output
console_err = Console(stderr=True) # Used for error output

app = typer.Typer(no_args_is_help=True, add_completion=True, invoke_without_command=True) # Remove invoke_without_command=True if/when adding more subcommands

## HELPER FUNCTIONS #############################################################################################################
def vprint(message: str):
    """
    Prints a message if verbose is True.
    Args:
        message (str): The message to print.
    """
    global verbose_global
    if verbose_global:
        print(message)
#################################################################################################################################

### ADD DEPENDENCY COMMAND ######################################################################################################
@app.callback() # Revert this to app.command() if/when adding more subcommands
def add_cmd(
    package_name: Annotated[str, typer.Argument(help="Name of the package to add to the project.")],
    directory: Annotated[Optional[str], typer.Argument(help="Directory of the Python project to add the package to.")] = os.getcwd(),
    dev: Annotated[Optional[bool], typer.Option("--dev", "-d", help="Add the package as a dev dependency.")] = False,
    verbose: Annotated[Optional[bool], typer.Option("--verbose", "-v", help="Enable verbose output.")] = False
):
    """
    Add a dependency to your Python project.
    """
    global verbose_global
    verbose_global = verbose
    
    ## ARGUMENT CHECKS #############################################################################
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"[bold red]Path {directory} does not exist.")
        raise typer.Exit()
    
    # Check if the directory is a directory
    if not os.path.isdir(directory):
        print(f"[bold red]Path {directory} is not a directory.")
        raise typer.Exit()
    
    # Check if the directory contains a pax-created Python project
    if not os.path.exists(os.path.join(directory, "pyproject.toml")) or not os.path.exists(os.path.join(directory, "Pipfile")):
        print(f"[bold red]Directory {directory} does not contain a recognizable Python project.")
        raise typer.Exit()
    ################################################################################################
    
    project_name = os.path.basename(directory)
    with console.status(f"""Adding {"dev" if dev else ""} dependency [bold yellow]{package_name}[/] to project [bold blue]{project_name}[/]...""", spinner="pong"):
        
        ## INSTALLED CHECKS ########################################################################
        vprint("Checking if Python is installed...")
        # Check if Python is installed
        if shutil.which("python") is None:
            # If it isn't, print an error message and exit
            console_err.print("[bold red]Python installation not found. Please install Python or make sure it's on your PATH.")
            raise typer.Exit()
        vprint("Python is installed.\n")
        
        # Check if pipenv is installed
        vprint("Checking if pipenv is installed...")
        if shutil.which("pipenv") is None:
            # If it isn't, print an error message and exit
            console_err.print("[bold red]pipenv is not installed. Please install pipenv. https://pipenv.pypa.io/en/latest/")
            raise typer.Exit()
        vprint("pipenv is installed.\n")
        ############################################################################################

        ## ADD DEPENDENCY ##########################################################################
        os.environ["PIPENV_IGNORE_VIRTUALENVS"] = "1"
        os.environ["PIPENV_IN_PROJECT"] = "1"
        
        pipenv_commands = ["pipenv", "install", package_name]
        pipenv_commands.insert(2, "--dev") if dev else None
            
        try:
            vprint("Running pipenv install command...")
            # Run the pipenv install command
            result = subprocess.run(pipenv_commands, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            console_err.print(Panel(result.stderr, title=f"Error: {e}", expand=False))
            raise typer.Exit()
        # Print the output of the pipenv install command
        vprint(Panel(result.stdout, title="pipenv", expand=False))
        vprint(f"Successfully added package {package_name} with [bold italic purple]pipenv[/].\n")

        ## ADD PACKAGE TO PYPROJECT.TOML ###########################################################
        # TODO: Add the package to the pyproject.toml file
    
   
        # Reset the PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT settings
        vprint("Resetting PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT environment variables...")
        del os.environ["PIPENV_IGNORE_VIRTUALENVS"]
        del os.environ["PIPENV_IN_PROJECT"]
        vprint("[bold green]PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT environment variables reset.[/bold green]\n")    
    ################################################################################################
    
    # SUCCESS ######################################################################################
    print("")
    print(Panel(f"""{"Dev dependency" if dev else "Dependency"} {package_name} successfully added to project [bold blue]{project_name}[/].""", title="Success", expand=False, border_style="bold green"))

#################################################################################################################################