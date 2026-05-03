# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Overview
Developer Workflow Accelerator - A Python CLI tool for codebase analysis, documentation generation, and test creation.

## Build/Test Commands
```bash
# Run example usage
python example_usage.py

# Run single test (when tests are created)
pytest tests/test_code_analyzer.py::test_analyze_file -v

# Run all tests
pytest tests/ -v

# Type checking
mypy src/
```

## Code Style Guidelines

### Imports
- Order: stdlib → third-party → local modules
- Use absolute imports from `src/`
- Example: `from src.analyzer import CodeAnalyzer`

### Formatting
- Use type hints for all function parameters and return values
- Union types: Use `Type1 | Type2` syntax (Python 3.10+)
- Line length: 88 characters (Black default)

### Docstrings
- Google style format required
- Include Args, Returns, and Example sections
- Module-level docstring at top of each file

### Naming Conventions
- Classes: PascalCase (e.g., `CodeAnalyzer`)
- Functions/methods: snake_case (e.g., `analyze_file`)
- Private methods: prefix with `_` (e.g., `_parse_source`)
- Constants: UPPER_SNAKE_CASE

### Error Handling
- Use try-except blocks for file operations and parsing
- Return error dictionaries with `errors` field instead of raising exceptions
- Use `_error_result()` helper method for consistent error formatting

## Project-Specific Patterns

### AST Parsing
- All parsing uses Python's built-in `ast` module
- Use `ast.walk()` for traversing the tree
- Use `ast.get_docstring()` for extracting docstrings
- Use `ast.unparse()` for converting AST nodes back to strings

### Result Structure
All analysis methods return dictionaries with this structure:
```python
{
    "file": str,
    "module_docstring": str | None,
    "imports": List[Dict],
    "functions": List[Dict],
    "classes": List[Dict],
    "errors": str | None
}
```

### Method Extraction
- Use `_is_method()` to distinguish module-level functions from class methods
- Methods are extracted separately within `_extract_classes()`
- Check for `@staticmethod` and `@classmethod` decorators

## Testing Requirements
- Use pytest framework
- Test files in `tests/` directory
- Create fixtures for sample Python code
- Test both success and error cases
- Mock file system operations when appropriate