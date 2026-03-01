# AI Assistant Contract — Django Virtual QuerySet

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
- Do not use filesystem-based imports to access `qualitybase` or `virtualqueryset`
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

**Django Virtual QuerySet** is a Django library for creating QuerySet-like objects that are not backed by a database.

### Core Functionality

1. **Virtual Models** (`models.py`)
   - Base `VirtualModel` class for models without database tables
   - Support for external APIs, in-memory data, configuration

2. **Virtual Manager** (`managers.py`)
   - `VirtualManager` class for QuerySet-like operations
   - Filtering, ordering, and data retrieval

3. **QuerySet Utilities** (`queryset/`)
   - Filtering operations (`filter.py`)
   - Ordering operations (`order.py`)
   - Data management (`data.py`)

---

## Architecture (REQUIRED)

- Manager-based architecture for QuerySet-like operations
- Virtual models inherit from `VirtualModel` with `managed = False`
- QuerySet utilities provide filtering, ordering, and data management
- Compatible with Django ORM patterns and admin interface

---

## Project Structure (INFORMATIONAL)

```
django-virtualqueryset/
├── src/virtualqueryset/      # Main package
│   ├── models.py            # VirtualModel base class
│   ├── managers.py          # VirtualManager class
│   └── queryset/            # QuerySet utilities
│       ├── data.py          # Data management
│       ├── filter.py        # Filtering operations
│       └── order.py         # Ordering operations
├── tests/                   # Test suite
├── docs/                    # Documentation
├── service.py               # Main service entry point
└── pyproject.toml           # Project configuration
```

### Key Directories

- `src/virtualqueryset/models.py`: `VirtualModel` base class
- `src/virtualqueryset/managers.py`: `VirtualManager` for QuerySet operations
- `src/virtualqueryset/queryset/`: QuerySet utilities for filtering and ordering
- `tests/`: All tests using pytest-django

---

## Command Execution (ABSOLUTE)

- **Always use**: `./service.py dev <command>` or `python dev.py <command>`
- **Always use**: `./service.py quality <command>` or `python quality.py <command>`
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

- Use **pytest** with **pytest-django** exclusively
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
- Follow Django app structure conventions

---

## Virtual QuerySet Integration (ABSOLUTE)

- `virtualqueryset` is an installed package
- Always use standard Python imports:
  - `from virtualqueryset.models import VirtualModel`
  - `from virtualqueryset.managers import VirtualManager`
- Never manipulate import paths
- Never use file-based or relative imports to access `virtualqueryset`
- For dynamic imports, use:
  - `importlib.import_module()` from the standard library

---

## Qualitybase Integration (ABSOLUTE)

- `qualitybase` is an installed package (dependency)
- Always use standard Python imports from `qualitybase.services`
- No path manipulation: Never manipulate `sys.path` or use file paths to import qualitybase modules
- Direct imports only: Use `from qualitybase.services import ...` or `import qualitybase.services ...`
- Standard library imports: Use `importlib.import_module()` from the standard library if needed for dynamic imports
- Works everywhere: Since qualitybase is installed in the virtual environment, imports work consistently across all projects

---

## Virtual Model Architecture (REQUIRED)

### Creating Virtual Models

Virtual models must inherit from `VirtualModel`:

```python
from virtualqueryset.models import VirtualModel
from virtualqueryset.managers import VirtualManager

class MyVirtualModel(VirtualModel):
    objects = VirtualManager()
    
    class Meta:
        managed = False
```

### Managers

- Use `VirtualManager` for QuerySet-like operations
- Managers handle filtering, ordering, and data retrieval
- Ensure compatibility with Django QuerySet patterns

### QuerySet Operations

- Implement filtering through `queryset/filter.py`
- Implement ordering through `queryset/order.py`
- Manage data through `queryset/data.py`

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
- [ ] Imports follow Virtual QuerySet and Qualitybase rules
- [ ] Public APIs are typed and documented
- [ ] Virtual models inherit from VirtualModel correctly
- [ ] Managers use VirtualManager appropriately
- [ ] Tests are included when required
- [ ] No secrets or credentials are exposed

---

## Additional Resources (INFORMATIONAL)

- `purpose.md`: Detailed project purpose and goals
- `structure.md`: Detailed project structure and module organization
- `development.md`: Development guidelines and best practices
- `README.md`: General project information
