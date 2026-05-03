"""Code analyzer module for parsing Python source files using AST."""

import ast
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class CodeAnalyzer:
    """Analyzes Python source code and extracts structural information.
    
    This class uses Python's Abstract Syntax Tree (AST) to parse source files
    and extract functions, classes, imports, and docstrings.
    """
    
    def __init__(self):
        """Initialize the CodeAnalyzer."""
        self.results: Dict[str, Any] = {}
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single Python file and extract its structure.
        
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
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return self._error_result(f"File not found: {file_path}")
            
            if not path.suffix == '.py':
                return self._error_result(f"Not a Python file: {file_path}")
            
            # Check file size (limit to 10MB)
            file_size = path.stat().st_size
            if file_size > 10 * 1024 * 1024:
                return self._error_result(f"File too large: {file_size / 1024 / 1024:.1f}MB (max 10MB)")
            
            with open(path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            return self._parse_source(source_code, str(path))
            
        except Exception as e:
            return self._error_result(f"Error analyzing file: {str(e)}")
    
    def analyze_directory(self, dir_path: str, recursive: bool = True) -> Dict[str, Any]:
        """Analyze all Python files in a directory.
        
        Args:
            dir_path: Path to the directory to analyze
            recursive: Whether to search subdirectories recursively
            
        Returns:
            Dictionary mapping file paths to their analysis results
        """
        try:
            path = Path(dir_path)
            
            if not path.exists():
                return self._error_result(f"Directory not found: {dir_path}")
            
            if not path.is_dir():
                return self._error_result(f"Not a directory: {dir_path}")
            
            pattern = "**/*.py" if recursive else "*.py"
            python_files = list(path.glob(pattern))
            
            results = {}
            for py_file in python_files:
                results[str(py_file)] = self.analyze_file(str(py_file))
            
            return {
                "directory": str(path),
                "files_analyzed": len(results),
                "results": results
            }
            
        except Exception as e:
            return self._error_result(f"Error analyzing directory: {str(e)}")
    
    def _parse_source(self, source_code: str, file_path: str) -> Dict[str, Any]:
        """Parse Python source code using AST.
        
        Args:
            source_code: The Python source code as a string
            file_path: Path to the file (for error reporting)
            
        Returns:
            Dictionary containing parsed information
        """
        try:
            tree = ast.parse(source_code)
            
            result = {
                "file": file_path,
                "module_docstring": ast.get_docstring(tree),
                "imports": self._extract_imports(tree),
                "functions": self._extract_functions(tree),
                "classes": self._extract_classes(tree),
                "errors": None
            }
            
            return result
            
        except SyntaxError as e:
            return self._error_result(f"Syntax error in {file_path}: {str(e)}")
        except Exception as e:
            return self._error_result(f"Parse error in {file_path}: {str(e)}")
    
    def _extract_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import statements from AST.
        
        Args:
            tree: The AST tree to analyze
            
        Returns:
            List of import information dictionaries
        """
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append({
                        "type": "from_import",
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno
                    })
        
        return imports
    
    def _extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function definitions from AST.
        
        Args:
            tree: The AST tree to analyze
            
        Returns:
            List of function information dictionaries
        """
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip methods (functions inside classes)
                if self._is_method(node, tree):
                    continue
                
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "args": self._extract_arguments(node),
                    "decorators": [self._get_decorator_name(d) for d in node.decorator_list],
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                    "returns": self._get_return_annotation(node)
                })
        
        return functions
    
    def _extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions from AST.
        
        Args:
            tree: The AST tree to analyze
            
        Returns:
            List of class information dictionaries
        """
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "bases": [self._get_base_name(base) for base in node.bases],
                    "methods": self._extract_methods(node),
                    "decorators": [self._get_decorator_name(d) for d in node.decorator_list]
                })
        
        return classes
    
    def _extract_methods(self, class_node: ast.ClassDef) -> List[Dict[str, Any]]:
        """Extract method definitions from a class node.
        
        Args:
            class_node: The class AST node
            
        Returns:
            List of method information dictionaries
        """
        methods = []
        
        for node in class_node.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append({
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "args": self._extract_arguments(node),
                    "decorators": [self._get_decorator_name(d) for d in node.decorator_list],
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                    "is_static": any(self._get_decorator_name(d) == "staticmethod" for d in node.decorator_list),
                    "is_class_method": any(self._get_decorator_name(d) == "classmethod" for d in node.decorator_list),
                    "returns": self._get_return_annotation(node)
                })
        
        return methods
    
    def _extract_arguments(self, func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> List[Dict[str, Any]]:
        """Extract function/method arguments.
        
        Args:
            func_node: The function AST node
            
        Returns:
            List of argument information dictionaries
        """
        args = []
        
        for arg in func_node.args.args:
            args.append({
                "name": arg.arg,
                "annotation": ast.unparse(arg.annotation) if arg.annotation else None
            })
        
        return args
    
    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Get the name of a decorator.
        
        Args:
            decorator: The decorator AST node
            
        Returns:
            String representation of the decorator
        """
        try:
            return ast.unparse(decorator)
        except Exception:
            return str(decorator)
    
    def _get_base_name(self, base: ast.expr) -> str:
        """Get the name of a base class.
        
        Args:
            base: The base class AST node
            
        Returns:
            String representation of the base class
        """
        try:
            return ast.unparse(base)
        except Exception:
            return str(base)
    
    def _get_return_annotation(self, func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> Optional[str]:
        """Get the return type annotation of a function.
        
        Args:
            func_node: The function AST node
            
        Returns:
            String representation of the return annotation, or None
        """
        if func_node.returns:
            try:
                return ast.unparse(func_node.returns)
            except Exception:
                return str(func_node.returns)
        return None
    
    def _is_method(self, func_node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if a function is a method (inside a class).
        
        Args:
            func_node: The function AST node
            tree: The full AST tree
            
        Returns:
            True if the function is a method, False otherwise
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if func_node in node.body:
                    return True
        return False
    
    def _error_result(self, error_message: str) -> Dict[str, Any]:
        """Create an error result dictionary.
        
        Args:
            error_message: The error message
            
        Returns:
            Dictionary with error information
        """
        return {
            "file": None,
            "module_docstring": None,
            "imports": [],
            "functions": [],
            "classes": [],
            "errors": error_message
        }
    
    def to_json(self, result: Dict[str, Any], indent: int = 2) -> str:
        """Convert analysis result to JSON string.
        
        Args:
            result: The analysis result dictionary
            indent: Number of spaces for indentation
            
        Returns:
            JSON string representation
        """
        return json.dumps(result, indent=indent)
    
    def get_project_stats(self, dir_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate global statistics for a project.
        
        Args:
            dir_results: The result from analyze_directory
            
        Returns:
            Dictionary with global counts
        """
        stats = {
            "total_files": dir_results.get("files_analyzed", 0),
            "total_classes": 0,
            "total_functions": 0,
            "total_methods": 0,
            "total_imports": 0
        }
        
        for file_result in dir_results.get("results", {}).values():
            if file_result.get("errors"):
                continue
            
            stats["total_classes"] += len(file_result.get("classes", []))
            stats["total_functions"] += len(file_result.get("functions", []))
            stats["total_imports"] += len(file_result.get("imports", []))
            
            for cls in file_result.get("classes", []):
                stats["total_methods"] += len(cls.get("methods", []))
                
        return stats

    def save_to_file(self, result: Dict[str, Any], output_path: str) -> None:
        """Save analysis result to a JSON file.
        
        Args:
            result: The analysis result dictionary
            output_path: Path where to save the JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)

# Made with Bob
