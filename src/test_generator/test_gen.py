"""Test generator module for creating pytest unit tests from code analysis."""

import re
from typing import Dict, List, Any
from pathlib import Path


class TestGenerator:
    """Generates pytest unit tests from CodeAnalyzer output.
    
    This class creates test files with happy path tests, edge case tests,
    and fixtures based on the analyzed code structure.
    """
    
    def __init__(self):
        """Initialize the TestGenerator."""
        self.output_dir = Path("tests")
        self.indent = "    "
    
    def generate_test_file(self, analysis_data: Dict[str, Any], module_name: str = "module") -> str:
        """Generate a complete test file for a module.
        
        Args:
            analysis_data: Dictionary containing code analysis results
            module_name: Name of the module being tested
            
        Returns:
            String containing the complete test file content
            
        Example:
            >>> generator = TestGenerator()
            >>> test_code = generator.generate_test_file(analysis_data, "calculator")
        """
        # Validate input
        if not analysis_data:
            raise ValueError("analysis_data cannot be empty")
        
        if analysis_data.get("errors"):
            raise ValueError(f"Cannot generate tests from failed analysis: {analysis_data['errors']}")
        
        if not isinstance(module_name, str) or not module_name.strip():
            raise ValueError("module_name must be a non-empty string")
        
        sections = []
        
        # Import statements
        sections.append('"""Tests for the {} module."""\n'.format(module_name))
        sections.append("import pytest")
        
        # Import the module being tested
        imports_to_add = []
        if analysis_data.get("classes"):
            imports_to_add.extend([cls["name"] for cls in analysis_data["classes"]])
        if analysis_data.get("functions"):
            imports_to_add.extend([func["name"] for func in analysis_data["functions"]])
            
        if imports_to_add:
            # Determine package path (e.g. 'src.analyzer' or 'examples')
            file_path = analysis_data.get("file", "")
            package = ""
            if file_path:
                parts = Path(file_path).parts
                for part in parts[:-1]:
                    if part != ".":
                        package = part
                        break
            
            import_from = f"{package}.{module_name}" if package else module_name
            sections.append(f"from {import_from} import {', '.join(imports_to_add)}")
        
        sections.append("\n")
        
        # Generate fixtures
        fixtures = self._generate_fixtures(analysis_data)
        if fixtures:
            sections.append(fixtures)
            sections.append("\n")
        
        # Generate tests for classes
        if analysis_data.get("classes"):
            for cls in analysis_data["classes"]:
                class_tests = self.generate_class_tests(cls)
                sections.append(class_tests)
                sections.append("\n")
        
        # Generate tests for functions
        if analysis_data.get("functions"):
            for func in analysis_data["functions"]:
                func_tests = self.generate_function_tests(func)
                sections.append(func_tests)
                sections.append("\n")
        
        return "\n".join(sections)
    
    def generate_class_tests(self, class_data: Dict[str, Any]) -> str:
        """Generate test class for a given class.
        
        Args:
            class_data: Dictionary containing class information
            
        Returns:
            String containing test class code
        """
        # Validate input
        if not class_data or not isinstance(class_data, dict):
            raise ValueError("class_data must be a non-empty dictionary")
        
        if "name" not in class_data:
            raise ValueError("class_data must contain 'name' field")
        
        sections = []
        class_name = class_data["name"]
        
        # Test class header
        sections.append(f"class Test{class_name}:")
        sections.append(f'{self.indent}"""Tests for {class_name} class."""\n')
        
        # Test initialization
        sections.append(f"{self.indent}def test_initialization(self):")
        sections.append(f'{self.indent * 2}"""Test {class_name} can be initialized."""')
        
        # Check for __init__ arguments
        init_method = next((m for m in class_data.get("methods", []) if m["name"] == "__init__"), None)
        init_args = ""
        if init_method:
            args = [a for a in init_method.get("args", []) if a["name"] != "self"]
            if args:
                init_args = self._generate_sample_args(args)
                sections.append(f"{self.indent * 2}# TODO: Provide required init arguments")
        
        sections.append(f"{self.indent * 2}obj = {class_name}({init_args})")
        sections.append(f"{self.indent * 2}assert obj is not None")
        sections.append(f"{self.indent * 2}assert isinstance(obj, {class_name})\n")
        
        # Generate tests for each method
        for method in class_data.get("methods", []):
            if method["name"].startswith("_") and method["name"] != "__init__":
                continue  # Skip private methods except __init__
            
            if method["name"] == "__init__":
                continue  # Already tested above
            
            method_tests = self._generate_method_tests(method, class_name, class_data)
            sections.append(method_tests)
        
        return "\n".join(sections)
    
    def generate_function_tests(self, function_data: Dict[str, Any]) -> str:
        """Generate tests for a standalone function.
        
        Args:
            function_data: Dictionary containing function information
            
        Returns:
            String containing test functions
        """
        # Validate input
        if not function_data or not isinstance(function_data, dict):
            raise ValueError("function_data must be a non-empty dictionary")
        
        if "name" not in function_data:
            raise ValueError("function_data must contain 'name' field")
        
        sections = []
        func_name = self._sanitize_identifier(function_data["name"])
        
        # Happy path test
        sections.append(f"def test_{func_name}_happy_path():")
        sections.append(f'{self.indent}"""Test {func_name} with valid inputs."""')
        sections.append(f"{self.indent}# TODO: Implement test with valid inputs")
        sections.append(f"{self.indent}pass\n")
        
        # Edge case test
        sections.append(f"def test_{func_name}_edge_case():")
        sections.append(f'{self.indent}"""Test {func_name} with edge case inputs."""')
        sections.append(f"{self.indent}# TODO: Implement edge case test")
        sections.append(f"{self.indent}pass\n")
        
        # Error handling test
        sections.append(f"def test_{func_name}_error_handling():")
        sections.append(f'{self.indent}"""Test {func_name} handles errors correctly."""')
        
        # Smart edge case detection
        if "numbers" in str(function_data.get("args")) or "list" in str(function_data.get("args")):
            sections.append(f"{self.indent}with pytest.raises(ValueError):")
            sections.append(f"{self.indent * 2}{func_name}([])")
        else:
            sections.append(f"{self.indent}# TODO: Implement error handling test")
            sections.append(f"{self.indent}pass\n")
        
        return "\n".join(sections)
    
    def _generate_method_tests(self, method_data: Dict[str, Any], class_name: str, class_data: Dict[str, Any]) -> str:
        """Generate tests for a class method.
        
        Args:
            method_data: Dictionary containing method information
            class_name: Name of the class containing the method
            class_data: Full class dictionary for init analysis
            
        Returns:
            String containing method test code
        """
        sections = []
        method_name = method_data["name"]
        
        # Check for __init__ arguments to use in all tests
        init_method = next((m for m in class_data.get("methods", []) if m["name"] == "__init__"), None)
        init_args = ""
        if init_method:
            args = [a for a in init_method.get("args", []) if a["name"] != "self"]
            if args:
                init_args = self._generate_sample_args(args)

        # Happy path test
        sections.append(f"{self.indent}def test_{method_name}_happy_path(self):")
        sections.append(f'{self.indent * 2}"""Test {method_name} with valid inputs."""')
        sections.append(f"{self.indent * 2}obj = {class_name}({init_args})")
        
        # Generate sample call based on arguments
        args = method_data.get("args", [])
        if args and args[0]["name"] != "self":
            arg_names = [arg["name"] for arg in args if arg["name"] != "self"]
            sample_args = self._generate_sample_args(args)
            sections.append(f"{self.indent * 2}# TODO: Replace with actual test values")
            sections.append(f"{self.indent * 2}result = obj.{method_name}({sample_args})")
        else:
            sections.append(f"{self.indent * 2}result = obj.{method_name}()")
        
        sections.append(f"{self.indent * 2}assert result is not None")
        sections.append("")
        
        # Edge case test
        sections.append(f"{self.indent}def test_{method_name}_edge_case(self):")
        sections.append(f'{self.indent * 2}"""Test {method_name} with edge case inputs."""')
        sections.append(f"{self.indent * 2}obj = {class_name}({init_args})")
        
        # Smart detection for file operations or division
        if any(word in method_name.lower() for word in ["load", "save", "write", "read"]):
            sections.append(f"{self.indent * 2}with pytest.raises(Exception):")
            sections.append(f"{self.indent * 3}obj.{method_name}('non_existent_file')")
        elif "divide" in method_name.lower():
            sections.append(f"{self.indent * 2}with pytest.raises(ValueError):")
            sections.append(f"{self.indent * 3}obj.{method_name}(10, 0)")
        else:
            sections.append(f"{self.indent * 2}# TODO: Implement edge case test")
            sections.append(f"{self.indent * 2}pass")
        sections.append("")
        
        return "\n".join(sections)
    
    def _sanitize_identifier(self, name: str) -> str:
        """Sanitize a name to be a valid Python identifier.
        
        Args:
            name: The name to sanitize
            
        Returns:
            Valid Python identifier
        """
        # Replace invalid characters with underscore
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        
        # Ensure it doesn't start with a digit
        if sanitized and sanitized[0].isdigit():
            sanitized = f"_{sanitized}"
        
        # Handle empty or reserved keywords
        if not sanitized or sanitized in ('class', 'def', 'return', 'if', 'else', 'for', 'while'):
            sanitized = f"test_{sanitized}"
        
        return sanitized
    
    def _generate_fixtures(self, analysis_data: Dict[str, Any]) -> str:
        """Generate pytest fixtures for the test file.
        
        Args:
            analysis_data: Dictionary containing code analysis results
            
        Returns:
            String containing fixture definitions
        """
        sections = []
        
        # Generate fixture for each class
        if analysis_data.get("classes"):
            for cls in analysis_data["classes"]:
                class_name = cls["name"]
                fixture_name = class_name.lower() + "_instance"
                
                # Check for __init__ arguments
                init_method = next((m for m in cls.get("methods", []) if m["name"] == "__init__"), None)
                init_args = ""
                if init_method:
                    args = [a for a in init_method.get("args", []) if a["name"] != "self"]
                    if args:
                        init_args = self._generate_sample_args(args)

                sections.append("@pytest.fixture")
                sections.append(f"def {fixture_name}():")
                sections.append(f'{self.indent}"""Fixture that provides a {class_name} instance."""')
                sections.append(f"{self.indent}return {class_name}({init_args})")
                sections.append("")
        
        return "\n".join(sections) if sections else ""
    
    def _generate_sample_args(self, args: List[Dict[str, Any]]) -> str:
        """Generate sample argument values for test calls.
        
        Args:
            args: List of argument dictionaries
            
        Returns:
            String containing sample argument values
        """
        sample_values = []
        
        for arg in args:
            if arg["name"] == "self":
                continue
            
            annotation = arg.get("annotation", "")
            
            # Generate sample based on type annotation
            if "str" in annotation.lower():
                sample_values.append(f'"{arg["name"]}_value"')
            elif "int" in annotation.lower():
                sample_values.append("42")
            elif "float" in annotation.lower():
                sample_values.append("3.14")
            elif "bool" in annotation.lower():
                sample_values.append("True")
            elif "list" in annotation.lower():
                sample_values.append("[]")
            elif "dict" in annotation.lower():
                sample_values.append("{}")
            else:
                sample_values.append("None")
        
        return ", ".join(sample_values)
    
    def generate_conftest(self, analysis_data: Dict[str, Any]) -> str:
        """Generate conftest.py file with shared fixtures.
        
        Args:
            analysis_data: Dictionary containing code analysis results
            
        Returns:
            String containing conftest.py content
        """
        sections = []
        
        sections.append('"""Shared pytest fixtures and configuration."""\n')
        sections.append("import pytest")
        sections.append("from pathlib import Path\n")
        
        # Sample data fixture
        sections.append("@pytest.fixture")
        sections.append("def sample_data():")
        sections.append(f'{self.indent}"""Fixture providing sample test data."""')
        sections.append(f"{self.indent}return {{")
        sections.append(f'{self.indent * 2}"test_key": "test_value",')
        sections.append(f'{self.indent * 2}"number": 42')
        sections.append(f"{self.indent}}}\n")
        
        # Temp directory fixture
        sections.append("@pytest.fixture")
        sections.append("def temp_dir(tmp_path):")
        sections.append(f'{self.indent}"""Fixture providing a temporary directory."""')
        sections.append(f"{self.indent}return tmp_path\n")
        
        return "\n".join(sections)
    
    def save_test_file(self, content: str, filename: str, output_dir: str | None = None) -> None:
        """Save generated test file.
        
        Args:
            content: The test file content
            filename: Name of the test file
            output_dir: Optional output directory (defaults to self.output_dir)
        """
        # Validate input
        if not content or not isinstance(content, str):
            raise ValueError("content must be a non-empty string")
        
        if not filename or not isinstance(filename, str):
            raise ValueError("filename must be a non-empty string")
        
        if output_dir:
            path = Path(output_dir)
        else:
            path = self.output_dir
        
        # Ensure filename starts with test_
        if not filename.startswith("test_"):
            filename = f"test_{filename}"
        
        # Ensure .py extension
        if not filename.endswith(".py"):
            filename = f"{filename}.py"
        
        output_file = path / filename
        
        try:
            path.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except OSError as e:
            raise IOError(f"Failed to save test file to {output_file}: {str(e)}")

# Made with Bob
