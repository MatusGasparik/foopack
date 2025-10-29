"""Tests for foopack-extras package."""

import pytest


def test_import():
    """Test that foopack_extras can be imported."""
    import foopack_extras

    assert foopack_extras is not None


def test_hello_extras_function():
    """Test hello_extras function exists and returns correct value."""
    from foopack_extras import hello_extras

    result = hello_extras()
    assert result == "hello from foopack-core + extras"
    assert isinstance(result, str)


def test_core_dependency():
    """Test that foopack_core dependency is available."""
    import foopack_core

    assert foopack_core is not None
    # Verify we can call core's hello function
    assert foopack_core.hello() == "hello from foopack-core"


def test_dependencies_pandas():
    """Test that pandas dependency is available."""
    import pandas as pd

    assert pd is not None
    # Basic pandas functionality test
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    assert len(df) == 3
    assert list(df.columns) == ["a", "b"]


def test_inherits_core_dependencies():
    """Test that core dependencies (numpy, xarray) are also available."""
    import numpy as np
    import xarray as xr

    assert np is not None
    assert xr is not None
