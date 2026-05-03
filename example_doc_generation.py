"""Example usage of the DocGenerator module."""

from src.analyzer import CodeAnalyzer
from src.doc_generator import DocGenerator


def main():
    """Demonstrate DocGenerator functionality."""
    # Step 1: Analyze the code
    print("Step 1: Analyzing code...")
    analyzer = CodeAnalyzer()
    analysis_result = analyzer.analyze_file("src/analyzer/code_analyzer.py")
    
    if analysis_result.get("errors"):
        print(f"Error: {analysis_result['errors']}")
        return
    
    # Step 2: Generate documentation
    print("Step 2: Generating documentation...")
    doc_gen = DocGenerator()
    
    # Generate README
    readme_content = doc_gen.generate_readme(analysis_result, "CodeAnalyzer Module")
    doc_gen.save_documentation(readme_content, "README.md")
    print("  [OK] README.md generated")
    
    # Generate module documentation
    module_docs = doc_gen.generate_module_docs(analysis_result)
    doc_gen.save_documentation(module_docs, "code_analyzer_docs.md")
    print("  [OK] Module documentation generated")
    
    # Generate class documentation
    if analysis_result.get("classes"):
        for cls in analysis_result["classes"]:
            class_docs = doc_gen.generate_class_docs(cls)
            filename = f"{cls['name']}_class.md"
            doc_gen.save_documentation(class_docs, filename)
            print(f"  [OK] {filename} generated")
    
    # Generate function documentation
    if analysis_result.get("functions"):
        for func in analysis_result["functions"]:
            func_docs = doc_gen.generate_function_docs(func)
            filename = f"{func['name']}_function.md"
            doc_gen.save_documentation(func_docs, filename)
            print(f"  [OK] {filename} generated")
    
    print("\nAll documentation generated in 'docs/' directory!")
    print("\nPreview of README.md:")
    print("=" * 60)
    print(readme_content[:500] + "...")


if __name__ == "__main__":
    main()

# Made with Bob
