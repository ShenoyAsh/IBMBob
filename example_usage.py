"""Example usage of the CodeAnalyzer module."""

from src.analyzer import CodeAnalyzer


def main():
    """Demonstrate CodeAnalyzer functionality."""
    # Initialize the analyzer
    analyzer = CodeAnalyzer()
    
    # Analyze the code_analyzer.py file itself
    print("Analyzing code_analyzer.py...")
    result = analyzer.analyze_file("src/analyzer/code_analyzer.py")
    
    # Display results
    if result.get("errors"):
        print(f"Error: {result['errors']}")
    else:
        print(f"\nFile: {result['file']}")
        print(f"Module docstring: {result['module_docstring'][:50]}..." if result['module_docstring'] else "No module docstring")
        print(f"\nImports found: {len(result['imports'])}")
        print(f"Functions found: {len(result['functions'])}")
        print(f"Classes found: {len(result['classes'])}")
        
        # Show class details
        if result['classes']:
            print("\nClasses:")
            for cls in result['classes']:
                print(f"  - {cls['name']} (line {cls['line']})")
                print(f"    Methods: {len(cls['methods'])}")
                for method in cls['methods'][:3]:  # Show first 3 methods
                    print(f"      - {method['name']}()")
        
        # Save to JSON file
        analyzer.save_to_file(result, "analysis_result.json")
        print("\nResults saved to analysis_result.json")


if __name__ == "__main__":
    main()

# Made with Bob
