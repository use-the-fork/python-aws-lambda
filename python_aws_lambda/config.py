import json
import os
import site
import sys
from importlib import util
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Union,
)

from dataclasses_json import DataClassJsonMixin
from pydantic import Field
from pydantic.dataclasses import dataclass

BACKEND_ROOT = os.path.dirname(__file__)
PACKAGE_ROOT = os.path.dirname(os.path.dirname(BACKEND_ROOT))
TRANSLATIONS_DIR = os.path.join(BACKEND_ROOT, "translations")

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_ROOT_PATH = ""

@dataclass()
class RunSettings:
    # Name of the module (python file) used in the run command
    module_name: Optional[str] = None
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    root_path: str = DEFAULT_ROOT_PATH
    headless: bool = False
    watch: bool = False
    no_cache: bool = False
    debug: bool = False
    ci: bool = False

@dataclass()
class DatabaseSettings:
    transports: Optional[List[str]] = None
    enable_telemetry: bool = True
    # List of environment variables to be provided by each user to use the app. If empty, no environment variables will be asked to the user.
    user_env: Optional[List[str]] = None
    # Path to the local langchain cache database
    lc_cache_path: Optional[str] = None
    # Path to the local chat db
    # Duration (in seconds) during which the session is saved when the connection is lost
    session_timeout: int = 3600
    # Duration (in seconds) of the user session expiry
    user_session_timeout: int = 1296000  # 15 days
    # Enable third parties caching (e.g LangChain cache)
    cache: bool = False

@dataclass()
class ProjectConfig:
    root = APP_ROOT
    database: DatabaseSettings

def load_settings():
  features_settings = FeaturesSettings(**features_settings)

  ui_settings = UISettings(**ui_settings)

  code_settings = CodeSettings(action_callbacks={})

  return {
    "features": features_settings,
    "ui": ui_settings,
    "project": project_settings,
    "code": code_settings,
  }


def reload_config():
    """Reload the configuration from the config file."""
    global config
    if config is None:
        return

    settings = load_settings()

    config.features = settings["features"]
    config.code = settings["code"]
    config.ui = settings["ui"]
    config.project = settings["project"]


def load_config():

    settings = load_settings()

    config = ProjectConfig(
        chainlit_server=chainlit_server,
        run=RunSettings(),
        **settings,
    )

    return config

config = load_config()
