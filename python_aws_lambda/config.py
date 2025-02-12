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

def get_default_database_url():
    """Determine the default database URL based on the environment."""
    if os.getenv("ENV") == "production":
        return os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    else:
        return "sqlite:///./test.db"

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
    db_type: str = "sqlite"  # "sqlite" or "postgresql"
    db_url: str = Field(default_factory=get_default_database_url)
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_name: Optional[str] = None

@dataclass()
class ProjectConfig:
    root = APP_ROOT
    database: DatabaseSettings

from sqlalchemy import create_engine

def load_database_settings():
    """Load database settings from the .env file."""
    db_type = os.getenv("DB_TYPE", "sqlite")
    db_url = os.getenv("DATABASE_URL", get_default_database_url())
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # Create the database engine based on the db_type
    if db_type == "postgresql":
        engine = create_engine(
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
    else:
        engine = create_engine(db_url)

    return DatabaseSettings(
        db_type=db_type,
        db_url=db_url,
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_port=int(db_port) if db_port else None,
        db_name=db_name,
    ), engine
    """Load database settings from the .env file."""
    db_type = os.getenv("DB_TYPE", "sqlite")
    db_url = os.getenv("DATABASE_URL", get_default_database_url())
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    return DatabaseSettings(
        db_type=db_type,
        db_url=db_url,
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_port=int(db_port) if db_port else None,
        db_name=db_name,
    )

def load_settings():
  database_settings, engine = load_database_settings()
  return {
    "database": load_database_settings(),
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
        run=RunSettings(),
        **settings,
    )

    return config

config = load_config()
