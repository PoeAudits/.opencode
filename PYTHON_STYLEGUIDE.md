Core Review Areas
Code Quality & Readability: Ensure code follows "write for readability" principle - imagine someone ramping up 3-9 months from now
Python Patterns: Check for proper Python patterns, especially as it relates to context managers and exceptions
Security: Prevent secret exposure and ensure proper authentication patterns

Python & Code Style
Type Safety: Explicit return types on functions, comprehensive type annotations
Modern Python: Use str | None instead of Optional[str], built-in collections over imported types
Import Organization: Standard library, third-party, local imports (alphabetically sorted within groups)
Variable Naming: Keep variable names consistent for easier grepping, use descriptive names for exports
Error Handling: Avoid bare except:, be specific with exception types
Code Patterns: Prefer early returns over nested conditionals

Formatting:
Add blank lines after class definitions and dataclass decorators
Use double quotes for strings (ruff default)
Line length of 100 characters
Proper spacing around operators and after commas
Check all code with uv run ruff check and uv run ruff format

Dependency Management:
Use the uv package manager
Avoid adding new packages unless necessary
Vet new dependencies carefully (check source, maintenance, security)
Use uv add and uv add --dev to update dependencies, NOT manual pyproject.toml edits
Keep dependencies up to date (check for major version updates regularly)

Security & Authentication
Secret Management:
Never commit or log secrets, API keys, or credentials
Use .env files with dotenv.load_dotenv()
Never use os.environ["ANTHROPIC_API_KEY"] = "sk-..."

File Structure:
Use tmp/ folder for temporary files (gitignored)
Follow python best practices for file names
Keep the __init__.py file up to date within a directory if the files in the directory are edited.
