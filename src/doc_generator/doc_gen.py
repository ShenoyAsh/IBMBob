"""Documentation generator module for creating Markdown documentation from code analysis."""

from typing import Dict, List, Any
from pathlib import Path


class DocGenerator:
    """Generates Markdown documentation from CodeAnalyzer output.
    
    This class takes structured data from CodeAnalyzer and generates
    comprehensive Markdown documentation including README files,
    function documentation, and module-level documentation.
    """
    
    def __init__(self):
        """Initialize the DocGenerator."""
        self.output_dir = Path("docs")
    
    def generate_readme(self, analysis_data: Dict[str, Any], project_name: str = "Project") -> str:
        """Generate a README.md file from analysis data.
        
        Args:
            analysis_data: Dictionary containing code analysis results
            project_name: Name of the project
            
        Returns:
            Markdown string for README.md
            
        Example:
            >>> generator = DocGenerator()
            >>> readme = generator.generate_readme(analysis_data, "MyProject")
        """
        # Validate input
        if not analysis_data:
            raise ValueError("analysis_data cannot be empty")
        
        if analysis_data.get("errors"):
            raise ValueError(f"Cannot generate documentation from failed analysis: {analysis_data['errors']}")
        
        if not isinstance(project_name, str) or not project_name.strip():
            raise ValueError("project_name must be a non-empty string")
        
        sections = []
        
        # Header
        sections.append(f"# {project_name}\n")
        
        # Module description
        if analysis_data.get("module_docstring"):
            sections.append(f"{analysis_data['module_docstring']}\n")
        
        # Table of contents
        sections.append("## Table of Contents\n")
        sections.append("- [Overview](#overview)")
        sections.append("- [Classes](#classes)")
        sections.append("- [Functions](#functions)")
        sections.append("- [Installation](#installation)")
        sections.append("- [Usage](#usage)\n")
        
        # Overview section
        sections.append("## Overview\n")
        sections.append(f"This module contains {len(analysis_data.get('classes', []))} classes "
                       f"and {len(analysis_data.get('functions', []))} functions.\n")
        
        # Classes section
        if analysis_data.get("classes"):
            sections.append("## Classes\n")
            for cls in analysis_data["classes"]:
                sections.append(f"### {cls['name']}\n")
                if cls.get("docstring"):
                    sections.append(f"{cls['docstring']}\n")
                sections.append(f"**Methods:** {len(cls.get('methods', []))}\n")
        
        # Functions section
        if analysis_data.get("functions"):
            sections.append("## Functions\n")
            for func in analysis_data["functions"]:
                sections.append(f"### {func['name']}\n")
                if func.get("docstring"):
                    sections.append(f"{func['docstring']}\n")
        
        # Installation section
        sections.append("## Installation\n")
        sections.append("```bash")
        sections.append("pip install -r requirements.txt")
        sections.append("```\n")
        
        # Usage section
        sections.append("## Usage\n")
        sections.append("```python")
        if analysis_data.get("classes"):
            first_class = analysis_data["classes"][0]["name"]
            sections.append(f"from module import {first_class}\n")
            sections.append(f"obj = {first_class}()")
        sections.append("```\n")
        
        return "\n".join(sections)
    
    def generate_function_docs(self, function_data: Dict[str, Any]) -> str:
        """Generate Google-style docstring documentation for a function.
        
        Args:
            function_data: Dictionary containing function information
            
        Returns:
            Markdown string with function documentation
        """
        # Validate input
        if not function_data or not isinstance(function_data, dict):
            raise ValueError("function_data must be a non-empty dictionary")
        
        if "name" not in function_data:
            raise ValueError("function_data must contain 'name' field")
        
        sections = []
        
        # Function signature
        args_str = self._format_arguments(function_data.get("args", []))
        return_type = function_data.get("returns", "None")
        
        sections.append(f"### `{function_data['name']}({args_str})`\n")
        
        # Docstring
        if function_data.get("docstring"):
            sections.append(f"{function_data['docstring']}\n")
        
        # Arguments
        if function_data.get("args"):
            sections.append("**Arguments:**\n")
            for arg in function_data["args"]:
                arg_name = arg["name"]
                arg_type = arg.get("annotation", "Any")
                sections.append(f"- `{arg_name}` ({arg_type}): Description needed")
        
        # Returns
        sections.append(f"\n**Returns:** `{return_type}`\n")
        
        # Decorators
        if function_data.get("decorators"):
            sections.append("**Decorators:**")
            for decorator in function_data["decorators"]:
                sections.append(f"- `@{decorator}`")
            sections.append("")
        
        return "\n".join(sections)
    
    def generate_class_docs(self, class_data: Dict[str, Any]) -> str:
        """Generate documentation for a class.
        
        Args:
            class_data: Dictionary containing class information
            
        Returns:
            Markdown string with class documentation
        """
        # Validate input
        if not class_data or not isinstance(class_data, dict):
            raise ValueError("class_data must be a non-empty dictionary")
        
        if "name" not in class_data:
            raise ValueError("class_data must contain 'name' field")
        
        sections = []
        
        # Class header
        bases = ", ".join(class_data.get("bases", []))
        if bases:
            sections.append(f"## Class: `{class_data['name']}({bases})`\n")
        else:
            sections.append(f"## Class: `{class_data['name']}`\n")
        
        # Class docstring
        if class_data.get("docstring"):
            sections.append(f"{class_data['docstring']}\n")
        
        # Methods
        if class_data.get("methods"):
            sections.append("### Methods\n")
            for method in class_data["methods"]:
                method_docs = self._format_method(method)
                sections.append(method_docs)
        
        return "\n".join(sections)
    
    def generate_module_docs(self, analysis_data: Dict[str, Any]) -> str:
        """Generate complete module-level documentation.
        
        Args:
            analysis_data: Dictionary containing complete code analysis
            
        Returns:
            Markdown string with full module documentation
        """
        # Validate input
        if not analysis_data:
            raise ValueError("analysis_data cannot be empty")
        
        if analysis_data.get("errors"):
            raise ValueError(f"Cannot generate documentation from failed analysis: {analysis_data['errors']}")
        
        sections = []
        
        # Module header
        file_name = Path(analysis_data.get("file", "module")).name
        sections.append(f"# Module: {file_name}\n")
        
        # Module docstring
        if analysis_data.get("module_docstring"):
            sections.append(f"{analysis_data['module_docstring']}\n")
        
        # Imports
        if analysis_data.get("imports"):
            sections.append("## Imports\n")
            sections.append("```python")
            for imp in analysis_data["imports"][:10]:  # Show first 10 imports
                if imp["type"] == "import":
                    sections.append(f"import {imp['module']}")
                else:
                    sections.append(f"from {imp['module']} import {imp['name']}")
            sections.append("```\n")
        
        # Classes
        if analysis_data.get("classes"):
            sections.append("## Classes\n")
            for cls in analysis_data["classes"]:
                class_docs = self.generate_class_docs(cls)
                sections.append(class_docs)
                sections.append("")
        
        # Functions
        if analysis_data.get("functions"):
            sections.append("## Functions\n")
            for func in analysis_data["functions"]:
                func_docs = self.generate_function_docs(func)
                sections.append(func_docs)
                sections.append("")
        
        return "\n".join(sections)
    
    def save_documentation(self, content: str, filename: str, output_dir: str | None = None) -> None:
        """Save generated documentation to a file.
        
        Args:
            content: The documentation content to save
            filename: Name of the output file
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
        
        output_file = path / filename
        
        try:
            path.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except OSError as e:
            raise IOError(f"Failed to save documentation to {output_file}: {str(e)}")
    
    def _format_arguments(self, args: List[Dict[str, Any]]) -> str:
        """Format function arguments for display.
        
        Args:
            args: List of argument dictionaries
            
        Returns:
            Formatted argument string
        """
        if not args:
            return ""
        
        formatted = []
        for arg in args:
            if arg.get("annotation"):
                formatted.append(f"{arg['name']}: {arg['annotation']}")
            else:
                formatted.append(arg['name'])
        
        return ", ".join(formatted)
    
    def _format_method(self, method_data: Dict[str, Any]) -> str:
        """Format a method for documentation.
        
        Args:
            method_data: Dictionary containing method information
            
        Returns:
            Formatted method documentation string
        """
        args_str = self._format_arguments(method_data.get("args", []))
        
        # Method signature
        result = f"#### `{method_data['name']}({args_str})`\n"
        
        # Docstring
        if method_data.get("docstring"):
            result += f"\n{method_data['docstring']}\n"
        
        # Method type indicators
        indicators = []
        if method_data.get("is_static"):
            indicators.append("Static method")
        if method_data.get("is_class_method"):
            indicators.append("Class method")
        if method_data.get("is_async"):
            indicators.append("Async method")
        
        if indicators:
            result += f"\n*{', '.join(indicators)}*\n"
        
        return result

# Made with Bob
