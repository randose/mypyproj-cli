# New Python project command. 
# 
# There is only one command in this file, but you can add more if you want, i.e. new_clitool, new_webapp, etc.
# If you do, make sure to remove the invoke_without_command arg in the typer.Typer() app initialization  on line 22, 
# and change the decorator for the new_pyproj() function to @app.command(name="pyproj").

from typing import Optional, Annotated
from enum import Enum
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

def write_pyproject_toml(input_env: str, input_path: str, input_name: str, input_version: str, input_test: bool = True):
    """
    Writes a list of strings to a file.
    Args:
        input_env (str): The type of environment to write the file for. Can be "pipenv" or "poetry".
        file_path (str): The path to the file to write.
        input_name (str): The import-safe name of the project.
        input_version (str): The version number of the project.
    """
    if input_env.lower() == "pipenv":
        vprint("Writing the setuptools-specific pyproject.toml file...")
        file_contents = [
            '[build-system]\n',
            'requires = ["setuptools"]\n',
            'build-backend = "setuptools.build_meta"\n\n',
            '[project]\n',
            f'name = "{input_name}"\n',
            f'version = "{input_version}"\n',
            'description = "A project."\n',
            'license = "MIT"\n',
            'authors = []\n',
            'readme = "README.md"\n',
            'dependencies = []\n\n'
        ]
        if input_test:
            file_contents.extend([
                '[project.optional-dependencies]\n',
                'dev = ["pytest"]\n\n'
            ])
        file_contents.extend([
            '[project.scripts]\n',
            f'{input_name} = "{input_name}.__main__:app" # This is optional, but it allows you to run your project from the command line\n'
        ])
        
    elif input_env.lower() == "poetry": # Finish this
        vprint("Writing the poetry-specific pyproject.toml file...")
        file_contents = [
            '[build-system]\n',
            'requires = ["poetry-core>=1.0.0"]\n',
            'build-backend = "poetry.core.masonry.api"\n\n',
            '[tool.poetry]\n',
            f'name = "{input_name}"\n',
            f'version = "{input_version}"\n',
            'description = "A project."\n',
            'license = "MIT"\n',
            'authors = []\n',
            'readme = "README.md"\n\n',
            '[tool.poetry.dependencies]\n\n'
        ]
        if input_test:
            file_contents.extend([
                '[tool.poetry.group.test.dependencies]\n',
                'pytest = "*"\n\n'
            ])
        file_contents.extend([
            '[tool.poetry.scripts]\n',
            f'{input_name} = "{input_name}.__main__:app" # This is optional, but it allows you to run your project from the command line\n'
        ])
        
    with open(os.path.join(input_path, "pyproject.toml"), "w") as f:
        f.writelines(file_contents)
    vprint("[bold green]pyproject.toml file written.[/bold green]\n")
#################################################################################################################################

# DEFINE THE ENVIRONMENT OPTIONS ################################################################################################

class Env(str, Enum):
    pipenv = "pipenv"
    poetry = "poetry"
valid_envs = [
    ("pipenv", "Use 'pipenv' to manage the environment and 'build' to build the project."),
    ("poetry", "Use 'poetry' to manage the environment and build the project.")
]
def complete_env(incomplete: str):
    """
    Autocompletion function for the --env option.
    """
    completions = []
    for env, help_text in valid_envs:
        if env.startswith(incomplete):
            completion_item = (env, help_text)
            completions.append(completion_item)
    return completions

### NEW PY COMMAND ##############################################################################################################
@app.callback() # Revert this to app.command() if/when adding more subcommands
def new_pyproj(
    project_name: Annotated[str, typer.Argument(help="Name of the Python project.")],
    directory: Annotated[Optional[str], typer.Argument(help="Directory to create the Python project.")] = os.getcwd(),
    env: Annotated[Optional[Env], typer.Option(case_sensitive=False, autocompletion=complete_env, help="Select the build tool and environment manager.")] = Env.pipenv,
    test: Annotated[Optional[bool], typer.Option(help="Install the 'pytest' package as a dev dependency, and set up a tests directory for easy testing.")] = True,
    verbose: Annotated[Optional[bool], typer.Option("--verbose", "-v", help="Enable verbose output.")] = False
):
    """
    Create a new Python project.
    """
    global verbose_global
    verbose_global = verbose
    
    startup_text = f"""Creating new Python project...
    Project name: [bold blue]{project_name}[/bold blue]
    Directory: [bold yellow]{os.path.abspath(directory)}[/]
    env: [bold italic purple]{env.value.lower()}[/]
    Test: [bold italic green]{test}[/]"""
    
    print(Panel(startup_text, title="MyPyProj CLI Tool", expand=False, border_style="bold blue"))
    
    ## INSTALLED DEPENDENCY CHECKS #################################################################
    vprint("Checking if Python is installed...")
    # Check if Python is installed
    if shutil.which("python") is None:
        # If it isn't, print an error message and exit
        console_err.print("[bold red]Python is not installed. Please install Python.[/bold red]")
        raise typer.Exit()
    vprint("Python is installed.\n")
    
    # Check if pipenv is installed
    if env.value.lower() == "pipenv":
        vprint("Checking if pipenv is installed...")
        if shutil.which("pipenv") is None:
            # If it isn't, print an error message and exit
            console_err.print(Panel("pipenv is not installed. Please install pipenv. https://pipenv.pypa.io/en/latest/", expand=False, style="bold red"))
            raise typer.Exit()
        vprint("pipenv is installed.\n")
    elif env.value.lower() == "poetry":
        vprint("Checking if poetry is installed...")
        if shutil.which("poetry") is None:
            # If it isn't, print an error message and exit
            console_err.print(Panel("poetry is not installed. Please install poetry. https://python-poetry.org/", expand=False, style="bold red"))
            raise typer.Exit()
        vprint("poetry is installed.\n")
    ################################################################################################
    
    ## PROJECT NAME AND PATH CHECK #################################################################
    vprint("Checking if the project name is valid...")
    # Check if the project name is valid
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]{0,212}[a-z0-9]$", project_name):
        console_err.print(f"[bold red]Project name {project_name} is an invalid Python package name. Please choose a different name.[/bold red]")
        raise typer.Exit()
    vprint(f"[bold green]Project name {project_name} is valid.[/bold green]\n")
    
    project_path = os.path.abspath(os.path.join(directory, project_name))
    
    vprint("Checking if the project path already exists...")
    # Check if the directory exists
    if os.path.exists(project_path):
        # If it does, print an error message and exit
        console_err.print(f"[bold red]Project {project_name} already exists at {os.path.abspath(directory)}. Please choose a different name or directory.[/bold red]")
        raise typer.Exit()
    vprint(f"[bold green]Project path {project_path} is available.[/bold green]\n")
    ################################################################################################

    ## PROJECT CREATION ############################################################################
    vprint("Creating project directory...")
    os.makedirs(project_path)
    vprint(f"[bold green]Project directory {project_path} created.[/bold green]\n")

    # PROJECT STRUCTURE
    vprint(Panel("Creating project structure...", expand=False, style="bold"))
    vprint("Creating import-safe package name...")
    project_name_safe = project_name.replace("-", "_")
    vprint(f"Import-safe package name is [bold yellow]{project_name_safe}[/bold yellow].\n")
    
    # Create the src directory
    vprint("Creating [bold green]src[/bold green] directory...")
    os.makedirs(os.path.join(project_path, "src", project_name_safe))
    vprint("[bold green]src directory created.[/bold green]\n")
    
    vprint("Initializing project version number...")
    project_version = "0.1.0"
    vprint(f"Project version number is {project_version}.\n")
    
    # Create the __init__.py file
    vprint("Creating [bold yellow]__init__.py[/bold yellow] file...")
    with open(os.path.join(project_path, "src", project_name_safe, "__init__.py"), "w") as f:
        f.writelines([f"# Path: src\\{project_name_safe}\\__init__.py\n\n",
                        "from importlib.metadata import version\n\n",
                        "__app_name__ = __name__\n",
                        "__version__ = version(__name__)\n",
        ])
    vprint("[bold green]__init__.py file created.[/bold green]\n")
    
    # Create the tests directory
    if test:
        vprint("Creating tests directory...")
        os.makedirs(os.path.join(project_path, "tests"))
        vprint("[bold green]Tests directory created.[/bold green]\n")
    
    # WRITE THE PYPROJECT.TOML FILE ################################################################
    write_pyproject_toml(env.value, project_path, project_name_safe, project_version, test)
    ################################################################################################
    
    # WRITE THE SCRIPTS ############################################################################
    vprint("Writing build and install scripts...")
    if os.name == "nt":
        vprint("Detected [bold blue]Windows[/bold blue].\n")
        script_ext = ".bat"
    else:
        vprint("Detected [bold blue]Linux/MacOS[\bold blue].\n")
        script_ext = ".sh"

    if env.value.lower() == "pipenv":
        build_script = ["pipenv run python -m build\n"]
        install_script = [f"cd {os.path.join('src', project_name_safe)}\n",
                          "pipenv install --editable .\n",
                          f"cd {os.path.join('..', '..')}"]
    elif env.value.lower() == "poetry":
        build_script = ["poetry build\n"]
        install_script = ["poetry install\n"]

    vprint("Writing build script...")
    with open(os.path.join(project_path, f"build{script_ext}"), "w") as f:
        f.writelines(build_script)
    vprint(f"[bold green]Build script 'build{script_ext}' written.[/bold green]\n")
    if os.name != "nt":
        vprint("Making build script executable...")
        try:
            os.chmod(os.path.join(project_path, f"build{script_ext}"), 0o755)
        except PermissionError:
            console_err.print(f"[bold red]Unable to make build script executable. Please make it executable manually.[/bold red]")
        else:
            vprint(f"[bold green]Build script 'build{script_ext}' made executable.[/bold green]\n")
    vprint("Writing install script...")
    with open(os.path.join(project_path, f"install{script_ext}"), "w") as f:
        f.writelines(install_script)
    vprint(f"[bold green]Install script 'install{script_ext}' written.[/bold green]\n")
    if os.name != "nt":
        vprint("Making install script executable...")
        try:
            os.chmod(os.path.join(project_path, f"install{script_ext}"), 0o755)
        except PermissionError:
            console_err.print(f"[bold red]Unable to make install script executable. Please make it executable manually.[/bold red]")
        else:
            vprint(f"[bold green]Install script 'install{script_ext}' made executable.[/bold green]\n")
    ################################################################################################        
        
    # WRITE THE README.MD FILE #####################################################################
    vprint("Generating README.md file...")
    readme_lines = [f"# {project_name}\n\n", 
                      "This project is awesome.\n\n",
                      "## Installation\n\n",
                      "## Building\n\n",
                      "To build this project:\n\n",
                      "1. Ensure the information is correct in the pyproject.toml file.\n",
                      "2. Enter ```build``` in terminal to activate the build script and build the project.\n\n",
                      "## Usage\n\n",
                      "## Contributing\n\n",
                      "## License\n\n",
                      "## Project Status\n\n",
                      "## Acknowledgements\n\n"]
    vprint("README.md file generated.\n")
        
    # Write the README.md file
    vprint("Writing README.md file...")
    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.writelines(readme_lines)
    vprint("[bold green]README.md file written.[/bold green]\n")
    ################################################################################################
    
    # CREATE THE .GITIGNORE FILE ###################################################################
    vprint("Creating .gitignore file...")
    with open(os.path.join(project_path, ".gitignore"), "w") as f:
        f.writelines([".vscode\n",
                      ".venv\n",
                      "__pycache__\n",
                      "*.egg-info\n",
                      "dist\n",
                      "build\n",])
    vprint("[bold green].gitignore file created.[/bold green]\n")
    
    print(Panel("Project structure created.", expand=False, style="bold green"))
    ################################################################################################
    
    # CREATE THE VIRTUAL ENVIRONMENT ###############################################################
    if env.value.lower() == "pipenv":
        # Set the PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT settings
        vprint("Setting PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT environment variables...\n")
        os.environ["PIPENV_IGNORE_VIRTUALENVS"] = "1"
        os.environ["PIPENV_IN_PROJECT"] = "1"
        
        pipenv_commands = ["pipenv", "install", "build"]
                
        with console.status("Creating virtual environment with pipenv...", spinner="pong"):
            try:
                vprint("Running pipenv install command...")
                # Run the pipenv install command
                result = subprocess.run(pipenv_commands, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            except Exception as e:
                console_err.print(Panel(result.stderr, title=f"Error: {e}", expand=False))
                raise typer.Exit()
        # Print the output of the pipenv install command
        vprint(Panel(result.stdout, title="Pipenv", expand=False))
        print("Successfully created virtual environment with [bold italic purple]pipenv[/].")
        
        if test:
        # add pytest as a dev dependency
            with console.status("Installing dev dependency with pipenv...", spinner="pong"):
                try:
                    vprint("Installing pytest as a dev dependency with pipenv...")
                    # Install pytest
                    subprocess.run(["pipenv", "install", "--dev", "pytest"], cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)   
                except Exception as e:
                    console_err.print(Panel(result.stderr, title=f"Error: {e}", expand=False))
                    raise typer.Exit()
                
            # Print the output of the pipenv install command
            print("Successfully installed dev dependency [bold yellow]'pytest'[/] with [bold italic purple]pipenv[/].")
            vprint(Panel(result.stdout, title="Pipenv", expand=False))
            
        # Reset the PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT settings
        vprint("Resetting PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT environment variables...")
        del os.environ["PIPENV_IGNORE_VIRTUALENVS"]
        del os.environ["PIPENV_IN_PROJECT"]
        vprint("[bold green]PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT environment variables reset.[/bold green]\n")
        
    elif env.value.lower() == "poetry":
        poetry_commands = ["poetry", "install"]
                
        with console.status("Creating virtual environment with [bold italic purple]poetry[/]...", spinner="pong"):
            try:
                vprint("Running poetry install command...")
                # Run the poetry install command
                result = subprocess.run(poetry_commands, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            except Exception as e:
                console_err.print(Panel(result.stderr, title=f"Error: {e}", expand=False))
                raise typer.Exit()
            else:
                # Print the output of the pipenv install command
                vprint(Panel(result.stdout, title="Poetry", expand=False))
        print("Successfully created virtual environment with [bold italic purple]poetry[/].")
    ################################################################################################
    
    # SUCCESS ######################################################################################
    print("")
    print(Panel(f"Python project [bold blue]{project_name}[/] created at [bold yellow]{os.path.abspath(project_path)}[/].", title="Success", expand=False, border_style="bold green"))

#################################################################################################################################