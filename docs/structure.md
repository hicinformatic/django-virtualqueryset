## Project Structure

Django VirtualQuerySet follows a standard Python package structure with source code in `src/`.

### General Structure

```
django-virtualqueryset/
├── src/
│   └── virtualqueryset/        # Main package directory
│       ├── __init__.py         # Package exports (QuerySets, Managers)
│       ├── models.py           # VirtualModel and ReadOnlyVirtualModel base classes
│       ├── managers.py         # Manager classes (VirtualManager, ConfigQuerySetManager, etc.)
│       ├── apps.py             # Django app configuration
│       ├── admin.py            # Django admin configuration
│       └── queryset/           # QuerySet implementations
│           ├── __init__.py     # QuerySet exports
│           ├── base.py         # InMemoryQuerySet base class
│           ├── config.py       # ConfigQuerySet (from Django settings)
│           ├── api.py          # APIQuerySet (from external APIs)
│           ├── json_qs.py      # JSONQuerySet (from JSON files)
│           └── cached.py       # CachedQuerySet (with caching)
├── tests/                      # Test suite
│   ├── settings.py             # Django test settings
│   └── ...
├── docs/                       # Documentation
│   └── ...
├── manage.py                   # Django management script
├── service.py                  # Main service entry point (qualitybase)
├── pyproject.toml              # Project configuration
└── README.md                   # Project README
```

### Module Organization Principles

- **Single Responsibility**: Each module should have a clear, single purpose
- **Separation of Concerns**: Keep different concerns in separate modules
- **Clear Exports**: Use `__init__.py` to define public API
- **Logical Grouping**: Organize related functionality together
- **Source Layout**: All source code in `src/` directory

### QuerySet Organization

The `queryset/` directory contains QuerySet implementations:

- **`base.py`**: Defines `InMemoryQuerySet` base class for in-memory data
- **`config.py`**: `ConfigQuerySet` loads data from Django settings
- **`api.py`**: `APIQuerySet` loads data from external APIs
- **`json_qs.py`**: `JSONQuerySet` loads data from JSON files
- **`cached.py`**: `CachedQuerySet` adds caching to any QuerySet

### Manager Organization

The `managers.py` module provides manager classes:

- **`VirtualManager`**: Base manager for virtual models
- **`ConfigQuerySetManager`**: Manager that loads data from Django settings
- **`APIQuerySetManager`**: Manager that loads data from external APIs
- **`JSONQuerySetManager`**: Manager that loads data from JSON files
- **`CachedQuerySetManager`**: Manager with caching support

### Model Organization

The `models.py` module provides base model classes:

- **`VirtualModel`**: Base class for virtual models (no database table)
- **`ReadOnlyVirtualModel`**: Explicitly read-only virtual model

### Package Exports

The public API is defined in `src/virtualqueryset/__init__.py`:

- **QuerySets**: `InMemoryQuerySet`, `ConfigQuerySet`, `APIQuerySet`, `JSONQuerySet`, `CachedQuerySet`
- **Managers**: `VirtualManager`, `ConfigQuerySetManager`, `APIQuerySetManager`, `JSONQuerySetManager`, `CachedQuerySetManager`
- **Models**: Import from `virtualqueryset.models` (not at module level due to Django initialization)
