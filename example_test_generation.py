"""Example usage of the TestGenerator module."""

from src.analyzer import CodeAnalyzer
from src.test_generator import TestGenerator


def main():
    """Demonstrate TestGenerator functionality."""
    # Step 1: Analyze the code
    print("Step 1: Analyzing code...")
    analyzer = CodeAnalyzer()
    analysis_result = analyzer.analyze_file("src/analyzer/code_analyzer.py")
    
    if analysis_result.get("errors"):
        print(f"Error: {analysis_result['errors']}")
        return
    
    # Step 2: Generate tests
    print("Step 2: Generating tests...")
    test_gen = TestGenerator()
    
    # Generate test file
    test_content = test_gen.generate_test_file(analysis_result, "analyzer.code_analyzer")
    test_gen.save_test_file(test_content, "test_code_analyzer.py")
    print("  [OK] test_code_analyzer.py generated")
    
    # Generate conftest.py
    conftest_content = test_gen.generate_conftest(analysis_result)
    test_gen.save_test_file(conftest_content, "conftest.py")
    print("  [OK] conftest.py generated")
    
    print("\nAll test files generated in 'tests/' directory!")
    print("\nPreview of test_code_analyzer.py:")
    print("=" * 60)
    print(test_content[:800] + "...")
    
    print("\n\nTo run the tests:")
    print("  pytest tests/test_code_analyzer.py -v")


if __name__ == "__main__":
    main()

# Made with Bob
