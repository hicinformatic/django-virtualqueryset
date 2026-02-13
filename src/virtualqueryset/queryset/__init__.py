from typing import Any, Iterable

from django.db import models
from django.db.models.query import QuerySet
from django.db.models.sql import Query

from .data import DataMixin
from .filter import FilterMixin
from .order import OrderMixin


def create_dynamic_model(data):
    """Create a dynamic model based on the first data item."""
    if not data:
        return None
    
    first_item = data[0] if isinstance(data, list) else next(iter(data), None)
    if first_item is None:
        return None
    
    # If it's a dict, extract fields from keys
    if isinstance(first_item, dict):
        fields = {}
        for key in first_item.keys():
            fields[key] = models.CharField(max_length=255)
        
        # Create a dynamic model class
        attrs = {
            '__module__': 'virtualqueryset.models',
            'Meta': type('Meta', (), {
                'managed': False,
                'app_label': 'virtualqueryset',
            }),
            **fields
        }
        return type('DynamicModel', (models.Model,), attrs)
    
    return None


class VirtualQuerySet(DataMixin, FilterMixin, OrderMixin, QuerySet):
    def __init__(
        self, model=None, data: Iterable[Any] | None = None, query=None, using=None, hints=None
    ):
        # Create dynamic model if none provided and data contains dicts
        if model is None and data:
            model = create_dynamic_model(data)
        
        if query is None and model is not None:
            query = Query(model)
        super().__init__(model=model, query=query, using=using, hints=hints)
        self._result_cache = self._from_data(data or [])
        self._prefetch_done = True

    def _clone(self):
        query = self.query.clone() if self.query else None
        return self.__class__(
            model=self.model,
            data=list(self._result_cache),
            query=query,
            using=self._db,
            hints=self._hints,
        )

    def __getitem__(self, k):
        if isinstance(k, slice):
            query = self.query.clone() if self.query else None
            return self.__class__(
                model=self.model,
                data=self._result_cache[k],
                query=query,
                using=self._db,
                hints=self._hints,
            )
        return self._result_cache[k]

    def all(self):
        return self._clone()

    def count(self):
        return len(self._result_cache)

    def exists(self):
        return len(self._result_cache) > 0

    def first(self):
        return self._result_cache[0] if self._result_cache else None

    def last(self):
        return self._result_cache[-1] if self._result_cache else None

    def values(self, *fields):
        """Return a list of dictionaries with the specified fields."""
        if not fields:
            # If no fields specified, return all attributes as dict
            return [
                {key: getattr(obj, key) for key in dir(obj) if not key.startswith('_')}
                for obj in self._result_cache
            ]
        return [{field: getattr(obj, field, None) for field in fields} for obj in self._result_cache]

    def values_list(self, *fields, flat=False):
        """Return a list of tuples with the specified fields."""
        if flat:
            if len(fields) != 1:
                raise TypeError("'flat' is not valid when values_list is called with more than one field.")
            return [getattr(obj, fields[0], None) for obj in self._result_cache]
        if not fields:
            return [tuple(getattr(obj, key, None) for key in dir(obj) if not key.startswith('_')) for obj in self._result_cache]
        return [tuple(getattr(obj, field, None) for field in fields) for obj in self._result_cache]

    def none(self):
        """Return an empty QuerySet."""
        query = self.query.clone() if self.query else None
        return self.__class__(
            model=self.model,
            data=[],
            query=query,
            using=self._db,
            hints=self._hints,
        )

    def __len__(self):
        return len(self._result_cache)
