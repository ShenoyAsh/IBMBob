"""Main CLI entry point for Developer Workflow Accelerator."""

import argparse
import sys
from pathlib import Path

from src.analyzer import CodeAnalyzer
from src.doc_generator import DocGenerator
from src.test_generator import TestGenerator


def analyze_command(filepath: str) -> None:
    """Run code analysis on the specified file.
    
    Args:
        filepath: Path to the Python file to analyze
    """
    print(f"Analyzing: {filepath}")
    
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_file(filepath)
    
    if result.get("errors"):
        print(f"Error: {result['errors']}")
        sys.exit(1)
    
    # Save analysis result
    output_file = "analysis_result.json"
    analyzer.save_to_file(result, output_file)
    
    print(f"\nAnalysis complete!")
    print(f"  Classes: {len(result.get('classes', []))}")
    print(f"  Functions: {len(result.get('functions', []))}")
    print(f"  Imports: {len(result.get('imports', []))}")
    print(f"\nResults saved to: {output_file}")


def document_command(filepath: str) -> None:
    """Generate documentation for the specified file.
    
    Args:
        filepath: Path to the Python file to document
    """
    print(f"Generating documentation for: {filepath}")
    
    try:
        # Analyze the file first
        analyzer = CodeAnalyzer()
        result = analyzer.analyze_file(filepath)
        
        if result.get("errors"):
            print(f"Error: {result['errors']}")
            sys.exit(1)
        
        # Generate documentation
        doc_gen = DocGenerator()
        module_name = Path(filepath).stem
        
        # Check if files exist and warn
        readme_path = Path("docs/README.md")
        if readme_path.exists():
            print("  [WARNING] docs/README.md already exists, will be overwritten")
        
        # Generate README
        readme = doc_gen.generate_readme(result, module_name)
        doc_gen.save_documentation(readme, "README.md")
        print("  [OK] README.md generated")
        
        # Generate module docs
        module_docs = doc_gen.generate_module_docs(result)
        doc_gen.save_documentation(module_docs, f"{module_name}_docs.md")
        print(f"  [OK] {module_name}_docs.md generated")
        
        print(f"\nDocumentation saved to: docs/")
    except ValueError as e:
        print(f"Validation Error: {str(e)}")
        sys.exit(1)
    except IOError as e:
        print(f"File Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        sys.exit(1)


def test_command(filepath: str) -> None:
    """Generate tests for the specified file.
    
    Args:
        filepath: Path to the Python file to generate tests for
    """
    print(f"Generating tests for: {filepath}")
    
    try:
        # Analyze the file first
        analyzer = CodeAnalyzer()
        result = analyzer.analyze_file(filepath)
        
        if result.get("errors"):
            print(f"Error: {result['errors']}")
            sys.exit(1)
        
        # Generate tests
        test_gen = TestGenerator()
        module_name = Path(filepath).stem
        
        # Check if test file exists and warn
        test_path = Path(f"tests/test_{module_name}.py")
        if test_path.exists():
            print(f"  [WARNING] tests/test_{module_name}.py already exists, will be overwritten")
        
        # Generate test file
        test_content = test_gen.generate_test_file(result, module_name)
        test_gen.save_test_file(test_content, f"test_{module_name}.py")
        print(f"  [OK] test_{module_name}.py generated")
        
        # Generate conftest if it doesn't exist
        conftest_path = Path("tests/conftest.py")
        if not conftest_path.exists():
            conftest_content = test_gen.generate_conftest(result)
            test_gen.save_test_file(conftest_content, "conftest.py")
            print("  [OK] conftest.py generated")
        
        print(f"\nTests saved to: tests/")
        print(f"\nRun tests with: pytest tests/test_{module_name}.py -v")
    except ValueError as e:
        print(f"Validation Error: {str(e)}")
        sys.exit(1)
    except IOError as e:
        print(f"File Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        sys.exit(1)


def all_command(filepath: str) -> None:
    """Run all operations (analyze, document, test) on the specified file.
    
    Args:
        filepath: Path to the Python file to process
    """
    print(f"Running all operations on: {filepath}\n")
    
    print("=" * 60)
    print("STEP 1: ANALYSIS")
    print("=" * 60)
    analyze_command(filepath)
    
    print("\n" + "=" * 60)
    print("STEP 2: DOCUMENTATION")
    print("=" * 60)
    document_command(filepath)
    
    print("\n" + "=" * 60)
    print("STEP 3: TEST GENERATION")
    print("=" * 60)
    test_command(filepath)
    
    print("\n" + "=" * 60)
    print("ALL OPERATIONS COMPLETE!")
    print("=" * 60)


def stats_command(dirpath: str) -> None:
    """Show global statistics for a directory.
    
    Args:
        dirpath: Path to the directory to analyze
    """
    print(f"Calculating stats for: {dirpath}")
    
    analyzer = CodeAnalyzer()
    dir_results = analyzer.analyze_directory(dirpath)
    
    if dir_results.get("errors"):
        print(f"Error: {dir_results['errors']}")
        sys.exit(1)
        
    stats = analyzer.get_project_stats(dir_results)
    
    print("\n" + "=" * 40)
    print("PROJECT OVERVIEW")
    print("=" * 40)
    print(f"Total Files:   {stats['total_files']}")
    print(f"Total Classes: {stats['total_classes']}")
    print(f"Total Funcs:   {stats['total_functions']}")
    print(f"Total Methods: {stats['total_methods']}")
    print(f"Total Imports: {stats['total_imports']}")
    print("=" * 40)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Developer Workflow Accelerator - Analyze, document, and test Python code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main analyze src/analyzer/code_analyzer.py
  python -m src.main document src/analyzer/code_analyzer.py
  python -m src.main test src/analyzer/code_analyzer.py
  python -m src.main all src/analyzer/code_analyzer.py
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze Python code structure")
    analyze_parser.add_argument("filepath", help="Path to Python file to analyze")
    
    # Document command
    doc_parser = subparsers.add_parser("document", help="Generate documentation")
    doc_parser.add_argument("filepath", help="Path to Python file to document")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Generate unit tests")
    test_parser.add_argument("filepath", help="Path to Python file to generate tests for")
    
    # All command
    all_parser = subparsers.add_parser("all", help="Run all operations")
    all_parser.add_argument("filepath", help="Path to Python file to process")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show project statistics")
    stats_parser.add_argument("dirpath", nargs="?", default=".", help="Directory to analyze (default: current)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Validate file exists (only for commands that need a specific file)
    if args.command in ["analyze", "document", "test", "all"]:
        try:
            filepath = Path(args.filepath)
            if not filepath.exists():
                print(f"Error: File not found: {args.filepath}")
                print(f"Please check the file path and try again.")
                sys.exit(1)
            
            if not filepath.suffix == ".py":
                print(f"Error: Not a Python file: {args.filepath}")
                print(f"This tool only works with Python (.py) files.")
                sys.exit(1)
        except Exception as e:
            print(f"Error validating file path: {str(e)}")
            sys.exit(1)
    elif args.command == "stats":
        if not Path(args.dirpath).exists():
            print(f"Error: Directory not found: {args.dirpath}")
            sys.exit(1)
    
    # Execute command
    try:
        if args.command == "analyze":
            analyze_command(args.filepath)
        elif args.command == "document":
            document_command(args.filepath)
        elif args.command == "test":
            test_command(args.filepath)
        elif args.command == "all":
            all_command(args.filepath)
        elif args.command == "stats":
            stats_command(args.dirpath)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
