# Pax

Pax is a command line tool that helps create and manage Python projects. It is built using Python and the Typer library, and relies on ```pipenv``` to manage virtual environments.

## Building

To build the CLI, you need to have Python 3.10 installed. Use the Pipfile and Pipfile.lock to generate a new virtual environment with Pipenv and install the dependencies:

```bash
pipenv install
```

Then, you can use the handy build script (build.bat for Windows & build.sh for MacOS/Linux) to build the package using the configuration defined in the pyproject.toml file. Simply run:

```bash
build
```

This will generate a dist folder with the wheel (.whl) file inside. You can use this wheel file to install the CLI globally.

## Installation

It is recommended to use pipx, rather than pip, to install Python command line tools. When you use pipx, you are not installing dependencies to your system's main Python installation, which could potentially cause issues with other projects. You can learn how to install pipx here: [pipx](https://pypa.github.io/pipx/).

Once you have pipx installed, you can install pax using the wheel file generated in the previous step:

```bash
pipx install path/to/whl_file
```

## Usage

```bash
pax COMMAND [ARGS] [OPTIONS] ...
```

## Commands

The available commands are:
- new: Create a new project
  - ARG project_name: Name of the Python project. [required]
  - ARG directory: Directory to create the Python project. [default: .]
  - OPTION --env: Select the build tool and environment manager. [default: pipenv]
  - OPTION --test: Install the 'pytest' package as a dev dependency, and set up a tests directory for easy testing. [default: True]
  - verbose --verbose, -v: Enable verbose output. [default: False]
- <b>NOT YET IMPLEMENTED</b> add: Add a new dependency to the project
  - ARG dependency: Name of the dependency to add. [required]
  - ARG directory: Directory of the project to add the dependency to. [default: .]
  - OPTION --version: Version of the dependency to add. [default: latest]
  - OPTION --dev: Add the dependency as a dev dependency. [default: False]
- <b>NOT YET IMPLEMENTED</b> remove: Remove a dependency from the project
  - ARG dependency: Name of the dependency to remove. [required]
  - ARG directory: Directory of the project to remove the dependency from. [default: .]