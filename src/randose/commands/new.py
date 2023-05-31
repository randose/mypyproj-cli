from typing import Optional, Annotated
import typer
from rich import print
import os
import shutil
import subprocess
import re

app = typer.Typer()

@app.command(name="py")
def new_py(
    project_name: Annotated[str, typer.Argument(help="Name of the Python project.")],
    directory: Annotated[Optional[str], typer.Argument(help="Directory to create the Python project.")] = os.getcwd(),
    pipenv: Annotated[Optional[bool], typer.Option(help="Set up a new pipenv virtual environment.")] = True,
    build: Annotated[Optional[bool], typer.Option(help="Install the 'build' package, and set up a pyproject.toml file for easy deployment and distribution.")] = True,
    test: Annotated[Optional[bool], typer.Option(help="Install the 'pytest' package, and set up a tests directory for easy testing.")] = True,
    verbose: Annotated[Optional[bool], typer.Option("--verbose", "-v", help="Print verbose output.")] = False
):
    """
    Create a new Python project.
    """
    
    print("Creating new Python project...")
    
    if verbose:
        print(f"Project name: {project_name}")
        print(f"Directory: {directory}")
        print(f"Pipenv: {pipenv}")
        print(f"Build: {build}")
        print(f"Test: {test}")
        print(f"Verbose: {verbose}")
        
    if verbose:
        print("Checking if Python is installed...")
    # Check if Python is installed
    if shutil.which("python") is None:
        # If it isn't, print an error message and exit
        print("[bold red]Python is not installed. Please install Python.[/bold red]")
        raise typer.Exit()
    
    if verbose:
        print("Checking if pipenv is installed...")
    # Check if pipenv is installed
    if pipenv and shutil.which("pipenv") is None:
        # If it isn't, print an error message and exit
        print("[bold red]pipenv is not installed. Please install pipenv.[/bold red]")
        raise typer.Exit()
    
    if verbose:
        print("Checking if the project name is valid...")
    # Check if the project name is valid
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]{0,212}[a-z0-9]$", project_name):
        print(f"[bold red]Project name {project_name} is an invalid Python package name. Please choose a different name.[/bold red]")
        raise typer.Exit()
    if verbose: print(f"[bold green]Project name {project_name} is valid.[/bold green]")
    
    project_path = os.path.abspath(os.path.join(directory, project_name))
    
    if verbose:
        print("Checking if the project path already exists...")
    # Check if the directory exists
    if os.path.exists(project_path):
        # If it does, print an error message and exit
        print(f"[bold red]Project {project_name} already exists at {os.path.abspath(directory)}. Please choose a different name or directory.[/bold red]")
        raise typer.Exit()
    if verbose: print(f"[bold green]Project path {project_path} is available.[/bold green]")

    if verbose: print("Creating project directory...")
    # If it doesn't, create the project directory
    os.makedirs(project_path)
    if verbose: print(f"[bold green]Project directory {project_path} created.[/bold green]")

    # PROJECT STRUCTURE
    if verbose: print("Creating project structure...")
    if verbose: print("Creating import-safe package name...")
    project_name_safe = project_name.replace("-", "_")
    if verbose: print(f"Import-safe package name is [bold yellow]{project_name_safe}[/bold yellow].")
    
    # Create the src directory
    if verbose: print("Creating [bold green]src[/bold green] directory...")
    os.makedirs(os.path.join(project_path, "src", project_name_safe))
    if verbose: print("[bold green]src directory created.[/bold green]")
    
    if build:
        if verbose: print("Initializing project version number...")
        project_version = "0.1.0"
        if verbose: print(f"Project version number is {project_version}.")
        # Create the __init__.py file
        if verbose: print("Creating __init__.py file...")
        with open(os.path.join(project_path, "src", project_name_safe, "__init__.py"), "w") as f:
            f.writelines([f"# Path: src\\{project_name_safe}\\__init__.py\n\n",
                           "from importlib.metadata import version\n\n",
                           "__app_name__ = __name__\n",
                           "__version__ = version(__name__)\n",
            ])
        if verbose: print("__init__.py file created.")
        
        # Create the tests directory
        if test:
            if verbose: print("Creating tests directory...")
            os.makedirs(os.path.join(project_path, "tests"))
            if verbose: print("Tests directory created.")
        
        # Write the pyproject.toml file
        if verbose: print("Writing pyproject.toml file...")
        with open(os.path.join(project_path, "pyproject.toml"), "w") as f:
            f.writelines(['[build-system]\n',
                          'requires = ["setuptools"]\n',
                          'build-backend = "setuptools.build_meta"\n\n',
                          '[project]\n',
                          f'name = "{project_name_safe}"\n',
                          f'version = "{project_version}"\n',
                          'description = "A project."\n',
                          'license = "MIT"\n',
                          'authors = ["Daniel Rosenwald"]\n',
                          'readme = "README.md"\n',
                          'dependencies = []\n\n',
                          '[project.optional-dependencies]\n',
                          'dev = ["pytest"]\n\n',
                          '[project.scripts]\n',
                          f'{project_name_safe} = "{project_name_safe}.__main__:app" # This is optional, but it allows you to run your project from the command line\n'
                        ])
        if verbose: print("pyproject.toml file written.")
        
        # Write the build script
        if verbose: print("Writing build script...")
        if os.name == "win32":
            if verbose: print("Detected Windows. Writing build.bat file...")
            with open(os.path.join(project_path, "build.bat"), "w") as f:
                f.write("python -m build")
        else:
            if os.name == "posix":
                if verbose: print("Detected Linux. Writing build.sh file...")
            elif os.name == "darwin":
                if verbose: print("Detected MacOS. Writing build.sh file...")     
            with open(os.path.join(project_path, "build.sh"), "w") as f:
                f.write("python -m build")
        if verbose: print("Build script written.")
        
        
        
    # Create the README.md base text
    if verbose: print("Generating README.md file...")
    readme_lines = [f"# {project_name}\n\n", 
                      "This project is awesome.\n\n",
                      "## Installation\n\n",
                      "## Usage\n\n",
                      "## Contributing\n\n",
                      "## License\n\n",
                      "## Project Status\n\n",
                      "## Acknowledgements\n\n"]
    
    # Add build-specific content to the README.md lines
    if build:
        readme_lines = readme_lines[:2] + ["## Building\n\n",
                    "To build this project:\n\n",
                    "1. Ensure the information is correct in the pyproject.toml file.\n",
                    "2. Ensure the virtual environment is active.\n",
                    "3. Build it\n\n",
                    "    If on Windows: simply run ```build``` in the cmd prompt to activate the build.bat script.\n",
                    "    If on MacOS/Unix: run ```python -m build``` in terminal\n\n"] + readme_lines[2:]
        
    # Write the README.md file
    if verbose: print("Writing README.md file...")
    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.writelines(readme_lines)
    if verbose: print("README.md file written.")
    
    # Create the .gitignore file
    if verbose: print("Creating .gitignore file...")
    with open(os.path.join(project_path, ".gitignore"), "w") as f:
        f.writelines([".vscode\n",
                      ".venv\n",
                      "__pycache__\n",
                      "*.egg-info\n",
                      "dist\n",
                      "build\n",])
    if verbose: print(".gitignore file created.")
    
    print("Project structure created.")
    
    # Create the virtual environment
    if pipenv:
        print("Creating virtual environment...")
        # Set the PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT settings
        if verbose: print("Setting PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT environment variables...")
        os.environ["PIPENV_IGNORE_VIRTUALENVS"] = "1"
        os.environ["PIPENV_IN_PROJECT"] = "1"
        
        pipenv_commands = ["pipenv", "install"]
        if build:
            # Add the build package to the pipenv install command
            pipenv_commands.append("build")
            if verbose: print("Added build package to pipenv install command.")
            
        try:
            if verbose: print("Running pipenv install command...")
            # Run the pipenv install command
            result = subprocess.run(pipenv_commands, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            print(f"Error: {e}")
            print(result.stderr)
            raise typer.Exit()
        else:
            # Print the output of the pipenv install command
            print("Successfully created virtual environment with pipenv.")
            if verbose: print(f"Standard Output: {result.stdout}")
        
        # add pytest as a dev dependency
        if test:
            try:
                if verbose: print("Installing pytest as a dev dependency with pipenv...")
                # Install pytest
                subprocess.run(["pipenv", "install", "--dev", "pytest"], cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)   
            except Exception as e:
                print(f"Error: {e}")
                print(result.stderr)
                raise typer.Exit()
            else:
                # Print the output of the pipenv install command
                print("Successfully installed dev dependency 'pytest' with pipenv.")
                if verbose: print(f"Standard Output: {result.stdout}")
        
        # Reset the PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT settings
        if verbose: print("Resetting PIPENV_IGNORE_VIRTUALENVS and PIPENV_IN_PROJECT environment variables...")
        del os.environ["PIPENV_IGNORE_VIRTUALENVS"]
        del os.environ["PIPENV_IN_PROJECT"]

    else:
        if test:
            print("Warning: You have chosen not to use pipenv, but you have chosen to install pytest. This will not work without pipenv. Please install pytest manually.")    

    # Print a success message
    print(f"Python project {project_name} created at {os.path.abspath(project_path)}.")

#########

audio_plugins_path = r"C:\\Users\\daniel\\dev\\projects\\personal\\audio-plugins"

@app.command(name="vst")
def new_vst(
    project_name: Annotated[str, typer.Argument(help="Name of the JUCE project.")],
    directory: Annotated[Optional[str], typer.Argument(help="Directory to create the JUCE project.")] = audio_plugins_path,
):
    """
    Create a new JUCE VST Plugin project from the template.
    """
        
    # Check if the directory exists
    project_path = os.path.join(directory, project_name)
    if os.path.exists(project_path):
        # If it does, print an error message and exit
        print(f"Project {project_name} already exists at {directory}. Please choose a different name or directory.")
        raise typer.Exit()

    # # If it doesn't, create the project directory
    # os.makedirs(project_path)
    
    # Copy the Template project files to the new project directory
    shutil.copytree(os.path.join(audio_plugins_path, "Template"), project_path, symlinks=True)
    
    # # Check if a remnant JUCE symlink directory exists
    # if os.path.exists(os.path.join(project_path, "JUCE")):
    #     # If it does, delete it
    #     os.rmdir(os.path.join(project_path, "JUCE"))
        
    # # Create a symbolic link to the JUCE directory (as an administrator)
    # os.system('Powershell -Command "& { New-Item -ItemType SymbolicLink -Path ' + os.path.join(project_path, "JUCE") + ' -Target ' + os.path.join(audio_plugins_path, "JUCE") + ' -Verb RunAs } "')
    
    # Print a success message
    print(f"VST Plugin project {project_name} created at {os.path.abspath(project_path)}.")
