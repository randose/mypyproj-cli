# MyPyProj CLI

This is a command line tool that helps create and manage Python projects. It is built using Python and the Typer library.

## Building

To build the CLI, you need to have Python 3.10 installed. Use the Pipfile and Pipfile.lock to generate a new virtual environment with Pipenv and install the dependencies:

```bash
pipenv install
```

Then, you can use the handy build script (build.bat for Windows & build.sh for MacOS/Linux) to build the package using the configuration defined in the pyproject.toml file. Simply run:

```bash
build
```

This will generate a dist folder with the wheel file inside. You can use this wheel file to install the CLI globally.

## Installation

We want to be able to call the CLI from anywhere on our system. However, it's best not to directly install any packages directly to our main Python library, as it can cause dependency issues with other projects on our system. Pipx solves this problem. It is a package manager like pip, but instead installs packages to isolated environments, while still making them available globally. If you don't have pipx installed, you can get it here: [pipx](https://pypa.github.io/pipx/).

Once you have pipx installed, you can install MyPyProj using the wheel file generated in the previous step:

```bash
pipx install path/to/whl_file
```

## Usage

```bash
mypyproj COMMAND [ARGS] [OPTIONS] ...
```

## Commands

The available commands available are:
- new: Create a new project
  - pyproject: Create a new Python project
    - ARG project_name: Name of the Python project. [required]
    - ARG directory: Directory to create the Python project. [default: .]
    - OPTION --env: Select the build tool and environment manager. [default: pipenv]
    - OPTION --test: Install the 'pytest' package as a dev dependency, and set up a tests directory for easy testing. [default: True]
    - verbose --verbose, -v: Enable verbose output. [default: False]
- add: Add a new dependency to the project TODO: Implement this
  - ARG dependency: Name of the dependency to add. [required]
  - ARG directory: Directory of the project to add the dependency to. [default: .]
  - OPTION --version: Version of the dependency to add. [default: latest]
  - OPTION --dev: Add the dependency as a dev dependency. [default: False]
- remove: Remove a dependency from the project