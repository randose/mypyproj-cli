# Init file. Path: src\randose\__init__.py

from importlib.metadata import version

__app_name__ = __name__
__version__ = version(__name__)

from .main import app
__all__ = [app]