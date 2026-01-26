## Project Structure

Django Virtual QuerySet follows a standard Django app structure with clear separation between models, managers, and QuerySet utilities.

### General Structure

```
django-virtualqueryset/
├── src/
│   └── virtualqueryset/      # Main package directory
│       ├── __init__.py       # Package exports
│       ├── apps.py           # App configuration
│       ├── models.py         # VirtualModel base class
│       ├── managers.py       # VirtualManager class
│       └── queryset/         # QuerySet utilities
│           ├── __init__.py   # QuerySet exports
│           ├── data.py       # Data management
│           ├── filter.py     # Filtering operations
│           └── order.py     # Ordering operations
├── tests/                    # Test suite
│   └── ...
├── docs/                     # Documentation
│   └── ...
├── service.py                # Main service entry point
├── pyproject.toml            # Project configuration
└── README.md                 # Project documentation
```

### Module Organization Principles

- **Single Responsibility**: Each module should have a clear, single purpose
- **Separation of Concerns**: Keep models, managers, and QuerySet utilities separate
- **Django Conventions**: Follow Django's app structure conventions
- **Clear Exports**: Use `__init__.py` to define public API
- **Logical Grouping**: Organize related functionality together

### Core Components

The package contains:

- **`models.py`**: `VirtualModel` base class for virtual models
- **`managers.py`**: `VirtualManager` class for QuerySet-like operations
- **`queryset/`**: QuerySet utilities for filtering, ordering, and data management
  - **`data.py`**: Data retrieval and management
  - **`filter.py`**: Filtering operations
  - **`order.py`**: Ordering operations

### Package Exports

The public API is defined in `src/virtualqueryset/__init__.py`:
- `VirtualModel`: Base model class for virtual models
- `VirtualManager`: Manager class for virtual QuerySets
- QuerySet utilities for filtering and ordering
