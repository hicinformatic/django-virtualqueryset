"""JSONQuerySet for JSON data sources."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .base import InMemoryQuerySet


class JSONQuerySet(InMemoryQuerySet):
    """QuerySet for JSON data (files or dicts).

    Loads data from JSON files or dictionaries and provides QuerySet interface.

    Example:
        class Product(models.Model):
            name = models.CharField(max_length=255)
            price = models.DecimalField()
            
            objects = JSONQuerySetManager('data/products.json')
            
            class Meta:
                managed = False
    """

    def __init__(
        self,
        model=None,
        data: Optional[List[Any]] = None,
        json_source: Optional[Union[str, Path, Dict]] = None,
        json_path: Optional[str] = None,
        query=None,
        using=None,
        hints=None,
    ):
        """Initialize with JSON source.

        Args:
            model: Django model class
            data: List of data (if already loaded)
            json_source: Path to JSON file, JSON string, or dict
            json_path: JSONPath-like string to extract nested data (e.g., 'results.items')
            query: Django Query object
            using: Database alias (unused)
            hints: Query hints (unused)
        """
        self.json_source = json_source
        self.json_path = json_path

        if data is None and json_source:
            data = self._load_json()

        super().__init__(
            model=model, data=data, query=query, using=using, hints=hints
        )

    def _load_json(self) -> List[Any]:
        """Load data from JSON source.

        Returns:
            List of data from JSON
        """
        if not self.json_source:
            return []

        try:
            if isinstance(self.json_source, dict):
                data = self.json_source
            elif isinstance(self.json_source, (str, Path)):
                path = Path(self.json_source)
                if path.exists() and path.is_file():
                    with path.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                else:
                    data = json.loads(str(self.json_source))
            else:
                return []

            if self.json_path:
                data = self._extract_json_path(data, self.json_path)

            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                return []

        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            return []

    def _extract_json_path(self, data: Any, path: str) -> Any:
        """Extract data using simple dot-notation path.

        Args:
            data: JSON data
            path: Dot-separated path (e.g., 'results.items')

        Returns:
            Extracted data
        """
        parts = path.split(".")
        current = data

        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list) and part.isdigit():
                current = current[int(part)]
            else:
                return None

        return current

    def reload(self):
        """Reload data from JSON source."""
        data = self._load_json()
        return self.__class__(
            self.model,
            data,
            self.json_source,
            self.json_path,
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

