# Randose CLI

This is a CLI built by me to help me with my daily tasks. It is built using Python and the Typer library.

## Building

To build the CLI, you need to have Python 3.10 installed. Use the Pipfile and Pipfile.lock to generate a new virtual environment with Pipenv and install the dependencies:

```bash
pipenv install
```

Then, you can use the pyproject.toml file to build the CLI using the build command from the build package:

```bash
pipenv run python -m build
```

or, if you're on Windows, you can use the build.bat file:

```bash
build
```

This will generate a dist folder with the wheel file inside. You can use this wheel file to install the CLI globally.

## Installation

Because we want it available globally, but we also want to keep it isolated from the rest of the system, we will use [pipx](https://pypa.github.io/pipx/) to install it.

```bash
pipx install WHL_FILE
```

## Usage

```bash
randose COMMAND [ARGS] [OPTIONS] ...
```

## Commands

The available commands available are:
- new: Create a new project
  - pyproject: Create a new Python project
    - ARG project_name: Name of the Python project. [required]
    - ARG directory: Directory to create the Python project. [default: .]
    - OPTION --env: Select the build tool and environment manager. [default: pipenv]
    - OPTION --test: Install the 'pytest' package, and set up a tests directory for easy testing. [default: True]
  - vst-plugin: Create a new vst audio plugin project using the JUCE framework in C++ [not implemented]
    - ARG name: Name of the project [required]
    - ARG path: Path to create the project [default: .]
