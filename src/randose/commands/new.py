from typing import Optional, Annotated
import typer
import os
import shutil
import subprocess

app = typer.Typer()

@app.command(name="pyproject")
def new_pyproject(
    project_name: Annotated[str, typer.Argument(help="Name of the Python project.")],
    directory: Annotated[Optional[str], typer.Argument(help="Directory to create the Python project.")] = os.getcwd(),
    pipenv: Annotated[Optional[bool], typer.Option(help="Set up a new pipenv virtual environment.")] = True,
    build: Annotated[Optional[bool], typer.Option(help="Install the 'build' package, and set up a pyproject.toml file for easy deployment and distribution.")] = True
):
    """
    Create a new Python project.
    """
    
    # Check if the directory exists
    project_path = os.path.join(directory, project_name)
    if os.path.exists(project_path):
        # If it does, print an error message and exit
        typer.echo(f"Project {project_name} already exists at {directory}. Please choose a different name or directory.", color=typer.colors.RED)
        raise typer.Exit()

    # If it doesn't, create the project directory
    os.makedirs(project_path)

    # PROJECT STRUCTURE
    
    # Create the src directory
    os.makedirs(os.path.join(project_path, "src", project_name))
    
    if build:
        project_version = "0.1.0"
        # Create the __init__.py file
        with open(os.path.join(project_path, "src", project_name, "__init__.py"), "w") as f:
            f.writelines([f"# Path: src\\{project_name}\\__init__.py\n\n",
                        f"__name__ = \"{project_name}\"\n",
                        f"__app_name__ = \"{project_name}\"\n",
                        f"__version__ = \"{project_version}\"\n",
            ])
            
        # Create the tests directory
        os.makedirs(os.path.join(project_path, "tests"))
        
        # Write the pyproject.toml file
        with open(os.path.join(project_path, "pyproject.toml"), "w") as f:
            f.writelines(['[build-system]\n',
                          'requires = ["setuptools"]\n',
                          'build-backend = "setuptools.build_meta"\n',
                          '\n',
                          '[project]\n',
                          f'name = "{project_name}"\n',
                          f'version = "{project_version}"\n',
                          'authors = [{name = "Daniel Rosenwald", email = "danielrosenwald@gmail.com"},]\n',
                          'description = "A project."\n',
                          'readme = "README.md"\n',
                          'requires-python = ">=3.10.0"\n',
                          'dependencies = []\n',
                          '\n',
                          '[project.scripts]\n',
                          f'{project_name} = "{project_name}.__main__:app" # This is optional, but it allows you to run your project from the command line\n'
                        ])
        
        # Write the build.bat file
        with open(os.path.join(project_path, "build.bat"), "w") as f:
            f.write("python -m build")
        
        
    # Create the README.md base text
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
                    "1. Ensure the information is correct in the pyproject.toml file and the top-level __init__.py file.\n",
                    "2. Ensure the virtual environment is active.\n",
                    "3. Build it\n\n",
                    "    If on Windows: simply run 'build' in the cmd prompt to activate the build.bat script.\n",
                    "    If on MacOS/Unix: run python -m build in terminal\n\n"] + readme_lines[2:]
        
    # Write the README.md file
    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.writelines(readme_lines)    
    
    # Create the .gitignore file
    with open(os.path.join(project_path, ".gitignore"), "w") as f:
        f.writelines([".vscode\n",
                      ".venv\n",
                      "__pycache__\n",
                      "*.egg-info\n",
                      "dist\n"])
            
    # Create the virtual environment
    if pipenv:
        pipenv_commands = ["pipenv", "install"]
        if build:
            pipenv_commands.append("build")
                
        subprocess.run(pipenv_commands, cwd=project_path)

    # Print a success message
    typer.echo(f"Python project {project_name} created at {os.path.abspath(project_path)}.", color=True)

#########

audio_plugins_path = r"C:\\Users\\daniel\\dev\\projects\\personal\\audio-plugins"

@app.command(name="vst-plugin")
def new_vst_plugin(
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
        typer.echo(f"Project {project_name} already exists at {directory}. Please choose a different name or directory.", color=typer.colors.RED)
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
    typer.echo(f"VST Plugin project {project_name} created at {os.path.abspath(project_path)}.", color=True)
