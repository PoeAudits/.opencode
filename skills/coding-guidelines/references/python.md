# Python Coding Guidelines

Python-specific coding standards for writing clean, type-safe, and idiomatic Python. Consult this reference before writing any Python code. These rules supplement the general coding principles in the parent skill.

---

## Architecture & Design Patterns

- **Protocol vs ABC:** Always use `Protocol` for structural subtyping instead of `ABC` inheritance.
- **Functional vs Class-based:** Prefer functional style with pure functions unless multiple instances of the same object type are needed — then use classes.
- **Data-centric design:** Structure functions around data structures — functions receive and return the same data structure (mutated) or return a copied/transformed version.
- **Mutability:** Prefer mutable data structures; avoid `frozen=True` on dataclasses unless immutability is explicitly required.

## Type System

- **Explicit return types:** Annotate return types on all functions.
- **Comprehensive type annotations:** Annotate all function parameters, return values, and non-trivial variables.
- **Modern syntax:** Use `str | None` instead of `Optional[str]`. Use built-in collections (`list`, `dict`, `set`, `tuple`) over imported typing equivalents.
- **Private members:** Use single underscore prefix (`_private`) for private functions and variables.
- **Constants:** Use `UPPER_SNAKE_CASE` at module level for constants.

## Code Style

- **String formatting:** Use f-strings exclusively; avoid `%` formatting and `.format()` unless required for lazy evaluation (e.g., logging).
- **String quotes:** Use double quotes for strings (ruff default).
- **Line length:** 100 characters.
- **Import organization:** Standard library, third-party, local imports (alphabetically sorted within groups).
- **Variable naming:** Keep variable names consistent for easier grepping. Use descriptive names for exports.
- **Early returns:** Prefer early returns over nested conditionals.
- **Comprehensions:** Use list/dict/set comprehensions for single-level operations only; break nested comprehensions into explicit loops.
- **Match statements:** Use `match/case` when there are more than two options; use `if/elif/else` for simple binary or ternary conditions.
- **Walrus operator:** Avoid `:=` for clarity unless it significantly improves readability.
- **Spacing:** Proper spacing around operators and after commas. Add blank lines after class definitions and dataclass decorators.

## Error Handling

- Avoid bare `except:` — be specific with exception types.
- Use custom exception classes for domain-specific errors.
- Prefer early returns to reduce nesting in error paths.

## Context Managers

Use `with` statements for resource management (files, connections, locks).
Write custom context managers for resources that need setup/teardown.

```python
# Good
with open("file.txt") as f:
    content = f.read()

# Good - custom context manager
@contextmanager
def database_connection():
    conn = create_connection()
    try:
        yield conn
    finally:
        conn.close()
```

## Generators

Use generators for large datasets to avoid loading everything into memory.
Materialize to lists only when the full collection is needed.

```python
# Good - generator for large data
def process_large_file(path: Path) -> Iterator[dict]:
    with open(path) as f:
        for line in f:
            yield parse_line(line)
```

## Decorators

- Leverage decorators when they provide clear value.
- Keep custom decorators small and focused.
- Prefer simple functions over complex decorator chains.

## Module Exports

Define explicit `__all__` in modules to control public API.

```python
__all__ = ["UserService", "create_user", "UserConfig"]
```

## Docstrings

- Keep docstrings minimal or omit entirely.
- If used, keep to a single line describing the purpose.
- Avoid verbose parameter/return documentation — let type hints speak for themselves.

## Data Validation

- Use dataclasses for simple internal data structures.
- Use Pydantic for complex data structures or external data validation (APIs, config files, user input).

```python
# Simple internal data - use dataclass
@dataclass
class Point:
    x: float
    y: float

# Complex external data - use Pydantic
class UserConfig(BaseModel):
    name: str
    email: EmailStr
    settings: dict[str, Any]
```

## CLI Tools

Use `argparse` for command-line interfaces.

## Async

- Use `asyncio` as the async library.
- Prefer sync code unless async provides clear benefits (I/O bound operations, concurrent requests).

## Logging

- Use the standard `logging` module.
- Configure different colors for different log levels.
- Timestamp format includes date and time to the minute (no seconds/milliseconds).
- Format: `"%(asctime)s - %(levelname)s - %(message)s"` with `datefmt="%Y-%m-%d %H:%M"`.

## Testing

- **Framework:** Use `pytest`.
- **Organization:** Mirror source directory structure in tests.
- **Naming:** Use `test_*.py` for test files.
- **Structure:** Use multiple focused test files rather than one large test file.
- **Async tests:** Use `pytest-asyncio` when testing async code.

## Tooling & Formatting

- **Linter/Formatter:** Use ruff. Check all code with `uv run ruff check` and `uv run ruff format`.
- **Package manager:** Use `uv`.
- **Virtual environments:** Use `uv venv` to create virtual environments. Use default `.venv` directory name.

## Dependency Management

- Use `uv add` and `uv add --dev` to update dependencies — NOT manual `pyproject.toml` edits.
- Avoid adding new packages unless necessary.
- Vet new dependencies carefully (check source, maintenance, security).
- Keep dependencies up to date (check for major version updates regularly).

## Security

- Never commit or log secrets, API keys, or credentials.
- Use `.env` files with `dotenv.load_dotenv()`.
- Never hardcode API keys (e.g., `os.environ["ANTHROPIC_API_KEY"] = "sk-..."`).

## HTTP Client

- Use `requests` for synchronous HTTP requests.
- Use `httpx` if async HTTP is needed.

## Path Handling

- Use `pathlib.Path` instead of string paths.
- Avoid `os.path` functions; prefer `Path` methods.

## Script Entrypoints

Use the `if __name__ == "__main__":` pattern for script entrypoints.

```python
def main() -> None:
    # Script logic here
    pass

if __name__ == "__main__":
    main()
```

## File Structure

- Use `tmp/` folder for temporary files (gitignored).
- Follow Python conventions for file names (`snake_case`).
- Keep `__init__.py` files up to date within a directory if the files in the directory are edited.
- Group related functions together in files; separate unrelated code into different files.
- No hard max file length, but prioritize logical grouping over file size.
