# Installation Guide

## Quick Install

### Option 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/dev-workflow-accelerator.git
cd dev-workflow-accelerator

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Option 2: Install from PyPI (When Published)

```bash
pip install dev-workflow-accelerator
```

### Option 3: Install from requirements.txt

```bash
# Clone the repository
git clone https://github.com/yourusername/dev-workflow-accelerator.git
cd dev-workflow-accelerator

# Install dependencies (optional - only for development)
pip install -r requirements.txt

# Run directly without installation
python -m src.main --help
```

## Verify Installation

After installation, verify it works:

```bash
# Check if the command is available
devflow --help

# Or run via Python module
python -m src.main --help
```

Expected output:
```
usage: main.py [-h] {analyze,document,test,all} ...

Developer Workflow Accelerator - Analyze, document, and test Python code
...
```

## Requirements

- **Python**: 3.10 or higher
- **Dependencies**: None! Uses Python standard library only
- **Optional**: pytest (for running generated tests)

## Development Setup

For contributing or development:

```bash
# Clone the repository
git clone https://github.com/yourusername/dev-workflow-accelerator.git
cd dev-workflow-accelerator

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run type checking
mypy src/

# Format code
black src/ tests/
```

## Troubleshooting

### Command not found: devflow

If `devflow` command is not found after installation:

1. Make sure pip's script directory is in your PATH
2. Use the alternative: `python -m src.main` instead

### Import errors

If you get import errors:

1. Make sure you're in the project root directory
2. Install in editable mode: `pip install -e .`
3. Or add the project to PYTHONPATH: `export PYTHONPATH="${PYTHONPATH}:$(pwd)"`

### Permission errors on Windows

Run your terminal as Administrator or use:
```bash
pip install --user -e .
```

## Uninstall

```bash
pip uninstall dev-workflow-accelerator
```

## Next Steps

After installation, check out:
- [README.md](README.md) - Project overview and usage
- [examples/](examples/) - Sample code and demonstrations
- [AGENTS.md](AGENTS.md) - Development guidelines