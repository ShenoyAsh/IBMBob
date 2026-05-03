# Sample Calculator Example

This directory contains a sample Python module to demonstrate the Developer Workflow Accelerator's capabilities.

## Before: Original Code

The `sample_calculator.py` file contains a simple Calculator class with minimal documentation:

```python
class Calculator:
    """Basic calculator with arithmetic operations."""
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    # ... more methods
```

## After: Running the Tool

Run the complete workflow:

```bash
python -m src.main all examples/sample_calculator.py
```

### Generated Outputs:

1. **Analysis Result** (`analysis_result.json`)
   - Extracted 1 class (Calculator)
   - Extracted 3 functions (calculate_average, find_max, find_min)
   - Identified all methods and their signatures

2. **Documentation** (`docs/sample_calculator_docs.md`)
   - Complete module documentation
   - Class and method descriptions
   - Function signatures with type hints
   - Organized in Markdown format

3. **Unit Tests** (`tests/test_sample_calculator.py`)
   - Test class for Calculator
   - Happy path tests for each method
   - Edge case test placeholders
   - Pytest fixtures

## Demonstration

### Step 1: Analyze

```bash
python -m src.main analyze examples/sample_calculator.py
```

Output:
```
Analysis complete!
  Classes: 1
  Functions: 3
  Imports: 0
Results saved to: analysis_result.json
```

### Step 2: Generate Documentation

```bash
python -m src.main document examples/sample_calculator.py
```

Output:
```
[OK] README.md generated
[OK] sample_calculator_docs.md generated
Documentation saved to: docs/
```

### Step 3: Generate Tests

```bash
python -m src.main test examples/sample_calculator.py
```

Output:
```
[OK] test_sample_calculator.py generated
Tests saved to: tests/
Run tests with: pytest tests/test_sample_calculator.py -v
```

## Key Improvements

### Documentation Enhancement
- **Before**: Minimal docstrings
- **After**: Complete Markdown documentation with:
  - Module overview
  - Class descriptions
  - Method signatures
  - Function documentation

### Test Coverage
- **Before**: No tests
- **After**: Comprehensive test suite with:
  - Initialization tests
  - Happy path tests for all methods
  - Edge case test placeholders
  - Pytest fixtures for easy testing

### Code Understanding
- **Before**: Manual code review needed
- **After**: Structured JSON analysis with:
  - All classes and methods
  - Function signatures
  - Type annotations
  - Import dependencies

## Try It Yourself

1. Modify `sample_calculator.py` to add new methods
2. Run `python -m src.main all examples/sample_calculator.py`
3. Check the generated documentation and tests
4. See how the tool adapts to your changes!

## Benefits Demonstrated

✅ **Time Savings**: Automated documentation and test generation
✅ **Consistency**: Standardized documentation format
✅ **Coverage**: Tests for all public methods
✅ **Understanding**: Quick overview of code structure
✅ **Maintainability**: Easy to keep docs and tests in sync