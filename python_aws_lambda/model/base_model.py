from sqlalchemy.orm import declarative_base
import json
from sqlalchemy import inspect

Base = declarative_base()

"""
BaseModel class for SQLAlchemy models with JSON serialization.

This class provides a base for other models, enabling them to be serialized
to JSON format, which is useful for API responses and other JSON-based
interactions.

Attributes:
    __abstract__ (bool): Indicates that this is an abstract base class.
"""

class BaseModel(Base):
    __abstract__ = True

    def to_dict(self):
        """Convert model instance to a dictionary."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def to_json(self):
        """Convert model instance to JSON."""
        return json.dumps(self.to_dict())
