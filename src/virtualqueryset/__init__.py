"""Django VirtualQuerySet - QuerySet-like objects not backed by a database."""

__version__ = "0.1.1"

default_app_config = "virtualqueryset.apps.VirtualQuerySetConfig"

# QuerySets can be imported at module level
from .queryset.base import InMemoryQuerySet
from .queryset.config import ConfigQuerySet
from .queryset.api import APIQuerySet
from .queryset.json_qs import JSONQuerySet
from .queryset.cached import CachedQuerySet

# Managers can be imported at module level
from .managers import (
    VirtualManager,
    ConfigQuerySetManager,
    APIQuerySetManager,
    JSONQuerySetManager,
    CachedQuerySetManager,
)

# Models should NOT be imported at module level (Django not ready yet)
# Import them as: from virtualqueryset.models import VirtualModel

__all__ = [
    # QuerySets
    "InMemoryQuerySet",
    "ConfigQuerySet",
    "APIQuerySet",
    "JSONQuerySet",
    "CachedQuerySet",
    # Managers
    "VirtualManager",
    "ConfigQuerySetManager",
    "APIQuerySetManager",
    "JSONQuerySetManager",
    "CachedQuerySetManager",
]
