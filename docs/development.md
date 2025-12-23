## Development Guidelines

### General Rules

- Always execute project tooling through `./service.py <service> <command>` or `python service.py <service> <command>`.
- Default to English for all code artifacts (comments, docstrings, logging, error strings, documentation snippets, etc.) regardless of the language used in discussions.
- Keep comments minimal and only when they clarify non-obvious logic.
- Avoid reiterating what the code already states clearly.
- Add comments only when they resolve likely ambiguity or uncertainty.

### Simplicity and Dependencies

- **Keep functions simple**: Always write the simplest possible functions. Avoid unnecessary complexity unless it's clearly evident or necessary.
- **Minimize dependencies**: Limit dependencies to the absolute minimum. Only add new dependencies when they provide essential functionality that cannot be reasonably implemented otherwise.
- **Prefer standard library**: Use Python standard library whenever possible before adding external dependencies.
- **Avoid over-engineering**: Don't add abstractions, patterns, or layers unless they solve a real problem or are clearly needed.

### Code Quality

- **Testing**: Use pytest for all tests. Place tests in `tests/` directory.
- **Type Hints**: All public functions and methods must have complete type hints.
- **Docstrings**: Use Google-style docstrings for all public classes, methods, and functions.
- **Linting**: Follow PEP 8 and use the configured linters (ruff, mypy, etc.).
- **Formatting**: Use the configured formatter (ruff format, etc.).

### Module Organization

- Keep related functionality grouped together in logical modules
- Maintain clear separation of concerns between modules
- Use `__init__.py` to define clean public APIs
- Avoid circular dependencies
- Source code in `src/` directory

### Qualitybase Integration

- **qualitybase is an installed package**: Always use standard Python imports from `qualitybase`
- **No path manipulation**: Never manipulate `sys.path` or use file paths to import qualitybase modules
- **Direct imports only**: Use `from qualitybase.services import ...` or `import qualitybase.services ...`
- **Standard library imports**: Use `importlib.import_module()` from the standard library if needed for dynamic imports
- **Works everywhere**: Since qualitybase is installed in the virtual environment, imports work consistently across all projects

### QuerySet Development

- **QuerySet inheritance**: All QuerySets must inherit from `InMemoryQuerySet` or another QuerySet class
- **Required methods**: QuerySets should implement data loading and filtering logic
- **Lazy evaluation**: QuerySets should support lazy evaluation where possible
- **Django compatibility**: QuerySets must be compatible with Django's QuerySet interface

### Manager Development

- **Manager inheritance**: Managers should inherit from `VirtualManager` or a specialized manager
- **get_data() method**: Override `get_data()` to provide data source
- **queryset_class**: Set `queryset_class` to specify which QuerySet to use
- **Model compatibility**: Managers must work with Django models

### Model Development

- **Model inheritance**: Virtual models must inherit from `VirtualModel` or `ReadOnlyVirtualModel`
- **Meta.managed = False**: All virtual models must have `managed = False` in Meta
- **Meta.abstract = True**: Base virtual models should be abstract
- **save() and delete()**: Override if custom persistence logic is needed

### Error Handling

- Always handle errors gracefully
- Provide clear, actionable error messages
- Use appropriate exception types
- Document exceptions in docstrings
- Handle API failures with proper error handling when appropriate

### Configuration and Secrets

- Never hardcode API keys, credentials, or sensitive information
- Use environment variables or Django settings for configuration
- Provide clear documentation on required configuration
- Use Django settings for configuration data when appropriate

### Versioning

- Follow semantic versioning (SemVer)
- Update version numbers appropriately for changes
- Document breaking changes clearly
