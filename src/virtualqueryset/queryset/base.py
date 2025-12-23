"""Base in-memory QuerySet implementation."""

from __future__ import annotations

from typing import Any, List, Optional

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.db.models.sql import Query


class InMemoryQuerySet(QuerySet):
    """Base QuerySet for in-memory data (not backed by database).

    Provides Django ORM-like API for arbitrary data sources:
    - Filtering with Django lookups (icontains, exact, in, etc.)
    - Ordering with field names and reverse
    - Slicing and iteration
    - get(), first(), last(), count(), exists()
    
    Useful for virtual models displayed in Django admin without database tables.
    """

    def __init__(
        self,
        model=None,
        data: Optional[List[Any]] = None,
        query=None,
        using=None,
        hints=None,
    ):
        """Initialize with in-memory data.

        Args:
            model: Django model class
            data: List of model instances or dictionaries
            query: Django Query object (created if None)
            using: Database alias (unused for in-memory)
            hints: Query hints (unused for in-memory)
        """
        if query is None and model is not None:
            query = Query(model)
        super().__init__(model=model, query=query, using=using, hints=hints)
        self._result_cache = list(data or [])
        self._prefetch_done = True

    def __len__(self):
        """Return count of cached results."""
        return len(self._result_cache)

    def __getitem__(self, k):
        """Support indexing and slicing."""
        if isinstance(k, slice):
            return self.__class__(
                self.model,
                self._result_cache[k],
                self.query.clone(),
                using=self._db,
                hints=self._hints,
            )
        return self._result_cache[k]

    def __iter__(self):
        """Iterate over cached results, applying ordering from query if present."""
        rslt = self._result_cache
        # Apply ordering from query.order_by if present (Django admin sets this)
        if hasattr(self.query, "order_by") and self.query.order_by:
            ordering = self.query.order_by
            if ordering:
                rslt = list(rslt)
                for field in reversed(ordering):
                    reverse = field.startswith("-")
                    field_name = field[1:] if reverse else field
                    
                    def get_field_value(obj):
                        """Get field value for sorting, handling None and strings."""
                        value = getattr(obj, field_name, None)
                        if value is None:
                            return ""
                        if isinstance(value, str):
                            return value.lower()
                        return value
                    
                    rslt.sort(key=get_field_value, reverse=reverse)
        return iter(rslt)

    def _clone(self):
        """Clone this queryset with copied data."""
        return self.__class__(
            self.model,
            list(self._result_cache),
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

    def all(self):
        """Return a clone of this queryset."""
        return self._clone()

    def count(self):
        """Return count of results."""
        return len(self._result_cache)

    def exists(self):
        """Return True if queryset has results."""
        return len(self._result_cache) > 0

    def first(self):
        """Return first result or None."""
        return self._result_cache[0] if self._result_cache else None

    def last(self):
        """Return last result or None."""
        return self._result_cache[-1] if self._result_cache else None

    def filter(self, *args, **kwargs):
        """Filter in-memory objects with Django lookup support.

        Supported lookups:
        - exact: field__exact=value or field=value
        - icontains: field__icontains=value (case-insensitive)
        - contains: field__contains=value (case-sensitive)
        - in: field__in=[values]
        - gt, gte, lt, lte: Comparison operators
        - isnull: field__isnull=True/False
        - startswith, istartswith: String prefix
        - endswith, iendswith: String suffix
        """
        rslt = self._result_cache

        def _value(obj, attr):
            """Get attribute value from object."""
            return getattr(obj, attr, "")

        for lookup, value in kwargs.items():
            if "__" in lookup:
                field_name, lookup_type = lookup.rsplit("__", 1)
                field_value_getter = lambda obj: _value(obj, field_name)

                if lookup_type == "icontains":
                    rslt = [
                        obj
                        for obj in rslt
                        if value.lower() in str(field_value_getter(obj)).lower()
                    ]
                elif lookup_type == "contains":
                    rslt = [
                        obj for obj in rslt if value in str(field_value_getter(obj))
                    ]
                elif lookup_type == "exact":
                    rslt = [obj for obj in rslt if field_value_getter(obj) == value]
                elif lookup_type == "in":
                    rslt = [obj for obj in rslt if field_value_getter(obj) in value]
                elif lookup_type == "gt":
                    rslt = [obj for obj in rslt if field_value_getter(obj) > value]
                elif lookup_type == "gte":
                    rslt = [obj for obj in rslt if field_value_getter(obj) >= value]
                elif lookup_type == "lt":
                    rslt = [obj for obj in rslt if field_value_getter(obj) < value]
                elif lookup_type == "lte":
                    rslt = [obj for obj in rslt if field_value_getter(obj) <= value]
                elif lookup_type == "isnull":
                    if value:
                        rslt = [
                            obj
                            for obj in rslt
                            if field_value_getter(obj) in (None, "")
                        ]
                    else:
                        rslt = [
                            obj
                            for obj in rslt
                            if field_value_getter(obj) not in (None, "")
                        ]
                elif lookup_type == "startswith":
                    rslt = [
                        obj
                        for obj in rslt
                        if str(field_value_getter(obj)).startswith(value)
                    ]
                elif lookup_type == "istartswith":
                    rslt = [
                        obj
                        for obj in rslt
                        if str(field_value_getter(obj)).lower().startswith(value.lower())
                    ]
                elif lookup_type == "endswith":
                    rslt = [
                        obj
                        for obj in rslt
                        if str(field_value_getter(obj)).endswith(value)
                    ]
                elif lookup_type == "iendswith":
                    rslt = [
                        obj
                        for obj in rslt
                        if str(field_value_getter(obj)).lower().endswith(value.lower())
                    ]
            else:
                rslt = [obj for obj in rslt if getattr(obj, lookup, None) == value]

        return self.__class__(
            self.model,
            rslt,
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

    def exclude(self, *args, **kwargs):
        """Exclude objects matching the given lookups."""
        filtered = self.filter(*args, **kwargs)
        excluded_ids = {id(obj) for obj in filtered._result_cache}
        rslt = [obj for obj in self._result_cache if id(obj) not in excluded_ids]
        return self.__class__(
            self.model,
            rslt,
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

    def order_by(self, *fields):
        """Sort in-memory objects by specified fields.

        Args:
            *fields: Field names to sort by. Prefix with '-' for descending.
                    Example: order_by('name', '-created_at')
        """
        rslt = list(self._result_cache)
        for field in reversed(fields):
            reverse = field.startswith("-")
            field_name = field[1:] if reverse else field
            
            def get_field_value(obj):
                """Get field value for sorting, handling None and strings."""
                value = getattr(obj, field_name, None)
                if value is None:
                    return ""
                if isinstance(value, str):
                    return value.lower()
                return value
            
            rslt.sort(key=get_field_value, reverse=reverse)
        
        # Update query.order_by to preserve ordering for subsequent operations
        cloned_query = self.query.clone()
        if hasattr(cloned_query, "order_by"):
            cloned_query.order_by = list(fields)
        
        return self.__class__(
            self.model,
            rslt,
            cloned_query,
            using=self._db,
            hints=self._hints,
        )

    def reverse(self):
        """Reverse the ordering of the queryset."""
        rslt = list(reversed(self._result_cache))
        return self.__class__(
            self.model,
            rslt,
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

    def get(self, **kwargs):
        """Get a single object matching the given lookups.

        Raises:
            ObjectDoesNotExist: If no object matches
            MultipleObjectsReturned: If multiple objects match
        """
        rslt = self._result_cache
        for attr, value in kwargs.items():
            rslt = [obj for obj in rslt if getattr(obj, attr) == value]

        if len(rslt) == 1:
            return rslt[0]

        if not rslt:
            model_name = self.model.__name__ if self.model else "Object"
            raise ObjectDoesNotExist(f"{model_name} matching query does not exist.")

        model_name = self.model.__name__ if self.model else "Object"
        raise MultipleObjectsReturned(
            f"get() returned more than one {model_name} -- it returned {len(rslt)}!"
        )

    def values(self, *fields):
        """Return dictionaries instead of model instances.

        Args:
            *fields: Field names to include. If empty, include all fields.
        """
        if not fields:
            return [
                {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
                for obj in self._result_cache
            ]

        return [
            {field: getattr(obj, field, None) for field in fields}
            for obj in self._result_cache
        ]

    def values_list(self, *fields, flat=False):
        """Return tuples of values instead of model instances.

        Args:
            *fields: Field names to include
            flat: If True and only one field, return flat list of values
        """
        if flat and len(fields) == 1:
            return [getattr(obj, fields[0], None) for obj in self._result_cache]

        return [
            tuple(getattr(obj, field, None) for field in fields)
            for obj in self._result_cache
        ]

    def distinct(self, *fields):
        """Return distinct results (basic implementation).

        Note: Full distinct with fields requires more complex logic.
        This implementation returns unique objects by id.
        """
        seen = set()
        rslt = []
        for obj in self._result_cache:
            obj_id = id(obj)
            if obj_id not in seen:
                seen.add(obj_id)
                rslt.append(obj)
        return self.__class__(
            self.model,
            rslt,
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

    def none(self):
        """Return empty queryset."""
        return self.__class__(
            self.model,
            [],
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

