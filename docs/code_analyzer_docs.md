# Module: code_analyzer.py

Code analyzer module for parsing Python source files using AST.

## Imports

```python
import ast
import json
from pathlib import Path
from typing import Dict
from typing import List
from typing import Any
from typing import Optional
```

## Classes

## Class: `CodeAnalyzer`

Analyzes Python source code and extracts structural information.

This class uses Python's Abstract Syntax Tree (AST) to parse source files
and extract functions, classes, imports, and docstrings.

### Methods

#### `__init__(self)`

Initialize the CodeAnalyzer.

#### `analyze_file(self, file_path: str)`

Analyze a single Python file and extract its structure.

Args:
    file_path: Path to the Python file to analyze
    
Returns:
    Dictionary containing extracted information:
    - functions: List of function definitions
    - classes: List of class definitions
    - imports: List of import statements
    - docstrings: Module-level docstring
    - errors: Any errors encountered during parsing
    
Example:
    >>> analyzer = CodeAnalyzer()
    >>> result = analyzer.analyze_file('example.py')
    >>> print(result['functions'])

#### `analyze_directory(self, dir_path: str, recursive: bool)`

Analyze all Python files in a directory.

Args:
    dir_path: Path to the directory to analyze
    recursive: Whether to search subdirectories recursively
    
Returns:
    Dictionary mapping file paths to their analysis results

#### `_parse_source(self, source_code: str, file_path: str)`

Parse Python source code using AST.

Args:
    source_code: The Python source code as a string
    file_path: Path to the file (for error reporting)
    
Returns:
    Dictionary containing parsed information

#### `_extract_imports(self, tree: ast.AST)`

Extract import statements from AST.

Args:
    tree: The AST tree to analyze
    
Returns:
    List of import information dictionaries

#### `_extract_functions(self, tree: ast.AST)`

Extract function definitions from AST.

Args:
    tree: The AST tree to analyze
    
Returns:
    List of function information dictionaries

#### `_extract_classes(self, tree: ast.AST)`

Extract class definitions from AST.

Args:
    tree: The AST tree to analyze
    
Returns:
    List of class information dictionaries

#### `_extract_methods(self, class_node: ast.ClassDef)`

Extract method definitions from a class node.

Args:
    class_node: The class AST node
    
Returns:
    List of method information dictionaries

#### `_extract_arguments(self, func_node: ast.FunctionDef | ast.AsyncFunctionDef)`

Extract function/method arguments.

Args:
    func_node: The function AST node
    
Returns:
    List of argument information dictionaries

#### `_get_decorator_name(self, decorator: ast.expr)`

Get the name of a decorator.

Args:
    decorator: The decorator AST node
    
Returns:
    String representation of the decorator

#### `_get_base_name(self, base: ast.expr)`

Get the name of a base class.

Args:
    base: The base class AST node
    
Returns:
    String representation of the base class

#### `_get_return_annotation(self, func_node: ast.FunctionDef | ast.AsyncFunctionDef)`

Get the return type annotation of a function.

Args:
    func_node: The function AST node
    
Returns:
    String representation of the return annotation, or None

#### `_is_method(self, func_node: ast.FunctionDef, tree: ast.AST)`

Check if a function is a method (inside a class).

Args:
    func_node: The function AST node
    tree: The full AST tree
    
Returns:
    True if the function is a method, False otherwise

#### `_error_result(self, error_message: str)`

Create an error result dictionary.

Args:
    error_message: The error message
    
Returns:
    Dictionary with error information

#### `to_json(self, result: Dict[str, Any], indent: int)`

Convert analysis result to JSON string.

Args:
    result: The analysis result dictionary
    indent: Number of spaces for indentation
    
Returns:
    JSON string representation

#### `get_project_stats(self, dir_results: Dict[str, Any])`

Calculate global statistics for a project.

Args:
    dir_results: The result from analyze_directory
    
Returns:
    Dictionary with global counts

#### `save_to_file(self, result: Dict[str, Any], output_path: str)`

Save analysis result to a JSON file.

Args:
    result: The analysis result dictionary
    output_path: Path where to save the JSON file

