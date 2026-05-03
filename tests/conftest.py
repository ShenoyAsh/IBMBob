"""Shared pytest fixtures and configuration."""

import pytest
from pathlib import Path

@pytest.fixture
def sample_data():
    """Fixture providing sample test data."""
    return {
        "test_key": "test_value",
        "number": 42
    }

@pytest.fixture
def temp_dir(tmp_path):
    """Fixture providing a temporary directory."""
    return tmp_path
