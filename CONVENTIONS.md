# Python Coding Conventions

## 1. Project Structure

### File Organization
- **Root Directory**: Reserved exclusively for project configuration files.
- **Source Directory**: Application code resides in `./resume_writer/` directory.
- **Test Directory**: All tests in top-level `./tests` directory only.
- **File Size**: Individual source files must not exceed **1000 lines**. When approaching this limit:
  - Extract functionality into new modules
  - Maintain logical organization during splits
  - Create new libraries as necessary

### File Lifecycle
- **Deletion**: Do not empty files; delete them entirely.
- **Variables**: All assigned variables must be used. Remove unused variables immediately.

## 2. Imports and Dependencies

### Import Placement
- Imports must **always** appear at the top of the file, **never** inline.
- Third-party imports should be moved into type-checking blocks where appropriate (see TC002).

### Preferred Libraries
Use the following libraries for specific domains:

| Domain | Library |
|--------|---------|
| CLI Parsing | `click` |
| File Operations | `pathlib` |
| Unit Testing | `pytest` |
| HTTP Requests | `httpx` (unless a specific library is provided) |
| LLM Connectivity | `litellm` |
| LLM Functions (extended) | `langchain` |

### Project-Specific Library Notes
- **LLM Processing**: This project uses `langchain` and related libraries for LLM processing
- **Web Search**: Uses `serpapi.GoogleSearch` with `SERPER_API_KEY` environment variable
- **Wikipedia**: Uses `langchain_community.retrievers.WikipediaRetriever`

### Deprecated Imports
- Replace `typing.List`, `typing.Dict`, etc., with built-in generics (`list`, `dict`).
- Use `X | Y` instead of `Union[X, Y]` (UP007).
- Use `X | None` instead of `Optional[X]` (UP045).

## 3. Code Style and Formatting

### String Quoting
- Use **double quotes** for all strings.

### Whitespace
- Blank lines must be truly blank—no trailing spaces or tabs.

### Output Standards
- **Text Output**: All questions and answers must be formatted in Markdown.
- **Prohibited**: Never use emojis in task output, CLI responses, API responses, or log messages. Use plain text (e.g., "completed", "high", "cancelled").

## 4. Functions and Type Safety

### Function Design
- **Single Purpose**: Functions must be short and serve a single purpose. Refactor long functions into smaller units.
- **Testability**: Functions must be easily mocked. Avoid complexity and inner/nested functions.
- **Arguments**: Use named arguments when calling functions whenever possible.
- **Boolean Arguments**: Do not use boolean-typed positional arguments (use keyword-only).
- **Defensive Coding**: Arguments to functions should check for valid inputs using `assert`. Returned values from called functions should check for validity using `assert`.

### Type Hints (Mandatory)
- **Always** use type hints for all arguments and return values.
- **Critical**: Correct type hints are essential.
- **`Any` Restrictions**: Use `Any` only for arguments that truly accept any type or when required by third-party interfaces. Never use `Any` to avoid proper typing—prefer specific types, `Union`, `object`, or generic alternatives.

## 5. Documentation

### Docstring Requirements
Every function must have a docstring serving as its specification. Structure:

```python
"""Description starting on first line with no line break.

Args:
    arg_name (type): Description of purpose.

Returns:
    type: Description of return value.

Raises:
    ExceptionType: When and why raised (optional).

Notes:
    1. Numbered step-by-step description of function internals.
    2. Exclude logging statements from numbered steps.
    3. Mention any network, disk, or database access.

"""
```

**Critical Rules**:
- Start on the first line: `"""Description starts immediately`
- Include blank line after last section
- Include `Args:` and `Returns:` sections always
- Include `Raises:` when applicable
- Include `Notes:` section with numbered steps describing function internals
- The Notes section should mention any network, disk, or database access
- Extract important logic descriptions into inline code comments, not the Notes section

### Class Documentation
- Document class purpose
- List members with their types

### HTML
- Prefer templates; avoid embedding HTML in Python code.

## 6. Error Handling and Logging

### Exception Patterns
- **Try/Except Structure**: Do not `return` from within a `try` block. Use the `else` clause for returns.
- **Logging**: Always log errors (`log.error` or `log.exception`) before raising exceptions.
- **FastAPI**: General exceptions on routes will be handled by FastAPI automatically.
- **Chaining**: Use `raise ... from err` or `raise ... from None` (B904).

### Logging Configuration
Every source file must initialize logging at the header:

```python
import logging

log = logging.getLogger(__name__)
```

### Logging Messages
- **Function Entry**: `log.debug` at function start with message `"{function_name} starting"`
- **Function Exit**: `log.debug` before return with message `"{function_name} returning"`
- **Formatting**: Never use f-strings or `%s` formatting directly in log calls.

  **Correct**:
  ```python
  _msg = f"{component_name} completed processing"
  log.info(_msg)
  ```

  **Incorrect**:
  ```python
  log.info(f"{component_name} completed processing")
  log.info("%s completed processing", component_name)
  ```

- **Exceptions**: Use `log.exception` when logging from an exception handler (includes traceback automatically).

### Output Stream (Critical)
**All logging output must go to `stderr`, never `stdout`.**

```python
# Correct
handler = logging.StreamHandler(sys.stderr)

# Incorrect
handler = logging.StreamHandler(sys.stdout)
```

**Rationale**: Separates diagnostic data (stderr) from program output (stdout), enabling proper redirection and Unix conventions.

## 7. Testing Standards

### Test Structure
- **Framework**: `pytest`
- **Style**: Write tests as functions, not classes.
- **Location**:
  - Place all tests in top-level `./tests` directory only
  - Mirror the source code structure within `./tests`
  - **Never** create tests inside source directories (e.g., no `./resume_writer/tests/`)
- **Logging**: Run unit tests with logging level set to DEBUG.
- **TDD**: Unit tests should be written before the code, and they should fail if the code is incorrect.

### Coverage Requirements
- **Mandatory**: 100% test coverage including branch coverage.
- **Command**: `pytest --cov=<module> --cov-branch --cov-report=term-missing --mypy`
- **Priority**: Write tests before code (TDD). Tests must fail if code is incorrect.
- **Scope**: All code paths, branches, defensive code, error handling, and edge cases must be tested. No exceptions.

**Note**: This codebase currently has variable test coverage (some modules at 0%). See AGENTS.md for project-specific testing guidance during the cleanup phase.

### File Naming
- Each `*.py` file should have a corresponding test file.
- **Unique Names**: All test files must have unique filenames across the entire test suite, even in separate paths.
- **Exceptions**: When source filenames collide (e.g., `user.py` → `test_user_route.py`), maintain a mappings file to track these exceptions and update it immediately when new mappings are created.

## 8. LLM Integration

### LLM Calls
- All calls to an LLM **must** use a `PydanticOutputParser` object
- All messages formatted for the LLM **must** include the `format_instructions` parameter
- All messages received from the LLM **must** use `langchain_core.utils.json.parse_json_markdown`
- The API key for LLM calls is in the environment variable `LLM_API_KEY`

## 9. Specific Frameworks and Deprecations

### FastAPI
- **Dependency Injection**: Always use `Annotated` with `Depends` to avoid FAST002 errors.

  ```python
  from typing import Annotated
  from fastapi import Depends

  async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
      return commons
  ```

### Deprecated Patterns (Avoid)
| Deprecated | Replacement |
|------------|-------------|
| `typing.List`, `typing.Dict` | `list`, `dict` |
| `datetime.datetime.utcnow()` | `datetime.datetime.now(datetime.UTC)` (timezone-aware) |
| `TemplateResponse(name, {"request": request})` | `TemplateResponse(request, name)` (Request is first parameter) |
| Pydantic class-based `config` | `ConfigDict` |

## 10. Git and Configuration Management

### Git Practices
- **Respect `.gitignore`**: Never force-add ignored files.
  - Do not use `git add -f` or `--force`
  - Keep directories like `_agent/`, `.venv/`, `__pycache__/`, etc., out of the repository

### Configuration Files
- **Do not create** configuration files in the workspace.
- A properly configured config file exists in the home directory.
- Ask first before creating or modifying any config files to prevent configuration drift.

## 11. Security
- **Secrets**: Never hardcode secret keys or defaults in code. Always retrieve secrets from external sources (environment variables, secret managers).
- **API Keys**: `SERPER_API_KEY` and `LLM_API_KEY` must be passed as environment variables

## 12. Quality Assurance (Ruff)

### McCabe Complexity
- Maximum cyclomatic complexity: **5**
- Refactor functions exceeding this threshold.

**Note**: This codebase currently has several functions exceeding complexity 5 (some at 6-9). These are grandfathered as legacy code. All new code must meet complexity 5. See AGENTS.md for guidance.

### Enabled Linting Rules
The following rules are enforced via `pyproject.toml`:

**Annotations & Typing**
- ANN001: Missing type annotation for function arguments
- ANN003: Missing type annotation for `**kwargs`
- ANN201: Missing return type annotation on public functions
- ANN401: Disallow use of `typing.Any` type
- TC002: Move third-party import into type-checking block
- TC006: Unquoted type expression in `cast()`
- UP007: Use `X | Y` for Union types
- UP035: Deprecated typing imports (e.g., `typing.List`)
- UP045: Use `X | None` for Optional types

**Code Quality**
- A002: Argument shadows Python built-in (e.g., `id`, `list`)
- ARG001: Unused function argument
- ARG002: Unused method argument
- B904: Raise without from clause
- BLE001: Do not catch blind `Exception`
- C: McCabe complexity check
- COM812: Missing trailing comma
- F401: Unused imports
- F541: F-string without placeholders
- F841: Unused local variable
- PIE790: Unnecessary `pass` statement
- PLR0913: Too many arguments in function definition
- PLR2004: Magic value used in comparison
- RET505: Superfluous else/return
- RUF006: Store reference to return value of `asyncio.create_task`
- SIM110: Use `any()`/`all()` instead of equivalent loop

**Documentation**
- D417: Missing argument description in docstring

**FastAPI**
- FAST (all): FastAPI-specific errors, including FAST002 for non-Annotated Depends

**Datetime**
- DTZ007: Naive datetime constructed using `datetime.strptime()` without %z

**Imports**
- I001: Import sorting (isort)

**Boolean Handling**
- FBT001: Boolean-typed positional argument in function definition
- FBT003: Boolean positional value in function call

### Running Checks

```bash
# Ruff
uv run ruff check
uv run ruff check --fix
uv run ruff check resume_writer/

# MyPy
uv run mypy resume_writer/

# Tests with coverage
uv run pytest tests/ --cov=resume_writer --cov-branch --cov-report=term-missing
```

### No `noqa` Policy
- **Prohibited**: `noqa` comments are not valid workarounds.
- All code must pass ruff checks without suppressions.
- **Remediation**: Fix underlying issues or refactor code to comply with rules.

## 13. Project-Specific Notes

### Agent Guidance
For project-specific guidance on handling existing technical debt, coverage exceptions, complexity grandfathering, and agent interaction patterns, see `AGENTS.md`.

### Type Checking Configuration
Third-party libraries without type stubs are configured in `pyproject.toml` under `[[tool.mypy.overrides]]`. Install available stub packages (e.g., `types-pytz`, `types-dateparser`) and add ignore patterns for libraries without stubs.

**Current stub configuration**:
```toml
[[tool.mypy.overrides]]
module = [
    "nltk",
    "nltk.*",
    "docx",
    "docx.*",
]
ignore_missing_imports = true
```

### Dependency Management
Use `uv` for all dependency operations:

```bash
# Add production dependency
uv add <package>

# Add development dependency
uv add --dev <package>

# Run commands
uv run pytest tests/
uv run ruff check resume_writer/
uv run mypy resume_writer/
```
