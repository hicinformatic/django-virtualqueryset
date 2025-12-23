# AI Assistant Contract — Django VirtualQuerySet

**This document is the single source of truth for all AI-generated work in this repository.**  
All instructions in this file **override default AI behavior**.

Any AI assistant working on this project **must strictly follow this document**.

If a request conflicts with this document, **this document always wins**.

---

## Rule Priority

Rules in this document have the following priority order:

1. **ABSOLUTE RULES** — must always be followed, no exception
2. **REQUIRED RULES** — mandatory unless explicitly stated otherwise
3. **RECOMMENDED PRACTICES** — should be followed unless there is a clear reason not to
4. **INFORMATIONAL SECTIONS** — context and reference only

---

## ABSOLUTE RULES

These rules must always be followed.

- Follow this `AI.md` file exactly
- Do not invent new services, commands, abstractions, patterns, or architectures
- Do not refactor, redesign, or optimize unless explicitly requested
- Do not manipulate `sys.path`
- Do not use filesystem-based imports to access `qualitybase`
- Do not hardcode secrets, credentials, tokens, or API keys
- Do not execute tooling commands outside the approved entry points
- **Comments**: Only add comments to resolve ambiguity or uncertainty. Do not comment obvious code.
- **Dependencies**: Add dependencies only when absolutely necessary. Prefer standard library always.
- If a request violates this document:
  - Stop
  - Explain the conflict briefly
  - Ask for clarification

---

## REQUIRED RULES

### Language and Communication

- **Language**: English only
  - Code
  - Comments
  - Docstrings
  - Logs
  - Error messages
  - Documentation
- Be concise, technical, and explicit
- Avoid unnecessary explanations unless requested

### Code Simplicity and Minimalism

- **Write the simplest possible code**: Always choose the simplest solution that works
- **Minimal dependencies**: Add dependencies only when absolutely necessary. Prefer standard library. Only add when essential functionality cannot be reasonably implemented otherwise
- **Minimal comments**: Comments only to resolve ambiguity or uncertainty. Do not comment obvious code or reiterate what the code already states clearly
- **Good factorization**: Factorize code when it improves clarity and reduces duplication, but only if it doesn't add unnecessary complexity or abstraction

---

## Project Overview (INFORMATIONAL)

**Django VirtualQuerySet** is a Django library for creating QuerySet-like objects that are not backed by a database. It enables you to use Django's ORM patterns and admin interface with data from external sources.

### Core Functionality

1. **Virtual Models**: Create Django models without database tables
2. **QuerySet-like interface**: Use Django QuerySet methods with in-memory data
3. **Multiple data sources**: Load data from Django settings, external APIs, JSON files, or in-memory data
4. **Django admin integration**: Display non-database data in Django admin
5. **Caching support**: Add caching to any data source

### Available QuerySets

- `InMemoryQuerySet`: Base QuerySet for in-memory data
- `ConfigQuerySet`: Loads data from Django settings
- `APIQuerySet`: Loads data from external APIs
- `JSONQuerySet`: Loads data from JSON files
- `CachedQuerySet`: Adds caching to any QuerySet

### Available Managers

- `VirtualManager`: Base manager for virtual models
- `ConfigQuerySetManager`: Manager for Django settings data
- `APIQuerySetManager`: Manager for external API data
- `JSONQuerySetManager`: Manager for JSON file data
- `CachedQuerySetManager`: Manager with caching support

### Base Models

- `VirtualModel`: Base class for virtual models (no database table)
- `ReadOnlyVirtualModel`: Explicitly read-only virtual model

---

## Architecture (REQUIRED)

- QuerySet-based architecture for in-memory data
- Managers provide interface between models and QuerySets
- Models inherit from `VirtualModel` or `ReadOnlyVirtualModel`
- All source code in `src/` directory
- Source layout: `src/virtualqueryset/`

---

## Project Structure (INFORMATIONAL)

```
django-virtualqueryset/
├── src/virtualqueryset/    # Main package
│   ├── queryset/           # QuerySet implementations
│   ├── models.py           # VirtualModel base classes
│   ├── managers.py         # Manager classes
│   └── apps.py             # Django app configuration
├── tests/                  # Test suite
├── docs/                   # Documentation
├── manage.py               # Django management script
├── service.py              # Main service entry point (qualitybase)
└── pyproject.toml          # Project configuration
```

### Key Directories

- `src/virtualqueryset/queryset/`: QuerySet implementations
- `src/virtualqueryset/models.py`: Base model classes
- `src/virtualqueryset/managers.py`: Manager classes
- `tests/`: All tests using pytest

---

## Command Execution (ABSOLUTE)

- **Always use**: `./service.py dev <command>` or `python service.py dev <command>`
- **Always use**: `./service.py quality <command>` or `python service.py quality <command>`
- **Always use**: `./service.py django <command>` or `python service.py django <command>`
- Never execute commands directly without going through these entry points

---

## Code Standards (REQUIRED)

### Typing and Documentation

- All public functions and methods **must** have complete type hints
- Use **Google-style docstrings** for:
  - Public classes
  - Public methods
  - Public functions
- Document raised exceptions in docstrings where relevant

### Testing

- Use **pytest** exclusively
- All tests must live in the `tests/` directory
- New features and bug fixes require corresponding tests

### Linting and Formatting

- Follow **PEP 8**
- Use configured tools:
  - `ruff`
  - `mypy`
- Use the configured formatter:
  - `ruff format`

---

## Code Quality Principles (REQUIRED)

- **Simplicity first**: Write the simplest possible solution. Avoid complexity unless clearly necessary.
- **Minimal dependencies**: Minimize dependencies to the absolute minimum. Only add when essential functionality cannot be reasonably implemented otherwise. Always prefer standard library.
- **No over-engineering**: Do not add abstractions, patterns, or layers unless they solve a real problem or are clearly needed.
- **Comments**: Comments are minimal and only when they resolve ambiguity or uncertainty. Do not comment what the code already states clearly. Do not add comments that reiterate obvious logic.
- **Separation of concerns**: One responsibility per module
- **Good factorization**: Factorize code when it improves clarity and reduces duplication, but only if it doesn't add unnecessary complexity

---

## Module Organization (REQUIRED)

- Single Responsibility Principle
- Logical grouping of related functionality
- Clear public API via `__init__.py`
- Avoid circular dependencies
- Source code in `src/` directory

---

## Qualitybase Integration (ABSOLUTE)

- `qualitybase` is an installed package (used via service.py)
- Always use standard Python imports from `qualitybase.services` when needed
- No path manipulation: Never manipulate `sys.path` or use file paths to import qualitybase modules
- Direct imports only: Use `from qualitybase.services import ...` or `import qualitybase.services ...`
- Standard library imports: Use `importlib.import_module()` from the standard library if needed for dynamic imports
- Works everywhere: Since qualitybase is installed in the virtual environment, imports work consistently across all projects

---

## QuerySet Development (REQUIRED)

### Creating QuerySets

QuerySets must inherit from `InMemoryQuerySet` or another QuerySet class:

```python
from virtualqueryset.queryset.base import InMemoryQuerySet

class MyQuerySet(InMemoryQuerySet):
    def __init__(self, model=None, data=None, **kwargs):
        # Load data from source
        data = self.load_data()
        super().__init__(model=model, data=data, **kwargs)
    
    def load_data(self):
        # Implement data loading logic
        return []
```

### Required Methods

- QuerySets should implement data loading logic
- Support Django QuerySet methods (filter, exclude, order_by, etc.)
- Support lazy evaluation where possible

---

## Manager Development (REQUIRED)

### Creating Managers

Managers should inherit from `VirtualManager` or a specialized manager:

```python
from virtualqueryset.managers import VirtualManager
from virtualqueryset.queryset.base import InMemoryQuerySet

class MyManager(VirtualManager):
    queryset_class = InMemoryQuerySet
    
    def get_data(self):
        # Return list of model instances or dictionaries
        return []
```

### Required Methods

- Override `get_data()` to provide data source
- Set `queryset_class` to specify which QuerySet to use

---

## Model Development (REQUIRED)

### Creating Virtual Models

Virtual models must inherit from `VirtualModel` or `ReadOnlyVirtualModel`:

```python
from virtualqueryset.models import VirtualModel
from virtualqueryset.managers import ConfigQuerySetManager

class ConfigSetting(VirtualModel):
    key = models.CharField(max_length=255)
    value = models.TextField()
    
    objects = ConfigQuerySetManager('MY_SETTINGS')
    
    class Meta:
        managed = False
    
    def __str__(self):
        return self.key
```

### Required Meta Options

- `managed = False`: All virtual models must have this
- `abstract = True`: Base virtual models should be abstract

### Save and Delete

- By default, `save()` and `delete()` raise `NotImplementedError`
- Override if custom persistence logic is needed

---

## Environment Variables (REQUIRED)

- `ENVFILE_PATH`
  - Path to `.env` file to load automatically
  - Relative to project root if not absolute
- `ENSURE_VIRTUALENV`
  - Set to `1` to automatically activate `.venv` if it exists

---

## Error Handling (REQUIRED)

- Always handle errors gracefully
- Use appropriate exception types
- Provide clear, actionable error messages
- Do not swallow exceptions silently
- Document exceptions in docstrings where relevant
- Handle API failures with proper error handling when appropriate

---

## Configuration and Secrets (ABSOLUTE)

- Never hardcode:
  - API keys
  - Credentials
  - Tokens
  - Secrets
- Use environment variables or Django settings
- Clearly document required configuration

---

## Versioning (REQUIRED)

- Follow **Semantic Versioning (SemVer)**
- Update versions appropriately
- Clearly document breaking changes

---

## CLI System (INFORMATIONAL)

Django VirtualQuerySet uses qualitybase's service system:

- Services accessed via `./service.py <service> <command>`
- Available services: `dev`, `quality`, `django`, `publish`

---

## Anti-Hallucination Clause (ABSOLUTE)

If a requested change is:
- Not supported by this document
- Not clearly aligned with the existing codebase
- Requiring assumptions or invention

You must:
1. Stop
2. Explain what is unclear or conflicting
3. Ask for clarification

Do not guess. Do not invent.

---

## Quick Compliance Checklist

Before producing output, ensure:

- [ ] All rules in `AI.md` are respected
- [ ] No forbidden behavior is present
- [ ] Code is simple, minimal, and explicit (simplest possible solution)
- [ ] Dependencies are minimal (prefer standard library)
- [ ] Comments only resolve ambiguity (no obvious comments)
- [ ] Code is well-factorized when it improves clarity (without adding complexity)
- [ ] Imports follow Qualitybase rules
- [ ] Public APIs are typed and documented
- [ ] QuerySets inherit from InMemoryQuerySet correctly
- [ ] Managers inherit from VirtualManager correctly
- [ ] Models inherit from VirtualModel correctly
- [ ] Models have `managed = False` in Meta
- [ ] No secrets or credentials are hardcoded
- [ ] Tests are included when required
- [ ] Error handling is graceful

---

## Additional Resources (INFORMATIONAL)

- `purpose.md`: Detailed project purpose and goals
- `structure.md`: Detailed project structure and module organization
- `development.md`: Development guidelines and best practices
- `README.md`: General project information
